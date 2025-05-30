import random
import string
from typing import List, Tuple


class Guesser:  
    def __init__(self, word_length: int, population_size: int = 100):
        self.word_length = word_length
        self.population_size = population_size
        self.population = []
        self.current_generation = 0
        self.alphabet = string.ascii_lowercase
        self.crossover_rate = 0.8
        self.mutation_rate = 0.1
        
        # Initialize population
        self.initialize_population()
    
    # CHROMOSOME ENCODING: Value encoding (character-based)
    def initialize_population(self):
        """Create initial random population using string-based encoding"""
        self.population = []
        for _ in range(self.population_size):
            # Each chromosome is a string of lowercase letters
            individual = ''.join(random.choice(self.alphabet) for _ in range(self.word_length))
            self.population.append(individual)
        self.current_generation = 0
    
    # Provide initial guess to GameMaster
    def provide_initial_guess_word(self) -> str:
        return random.choice(self.population)
    
    def evaluate_population(self, game_master) -> List[Tuple[str, int]]:
        evaluated_population = []
        for individual in self.population:
            cost = game_master.return_cost_to_guesser(individual)
            evaluated_population.append((individual, cost))
        return evaluated_population
    
    # PARENT SELECTION: Roulette Wheel Selection
    def roulette_wheel_selection(self, evaluated_population: List[Tuple[str, int]]) -> str:

        # Convert cost to fitness (lower cost = higher fitness)
        max_cost = max(cost for _, cost in evaluated_population) if evaluated_population else 1
        fitness_scores = [(individual, max_cost - cost + 1) for individual, cost in evaluated_population]
        
        total_fitness = sum(fitness for _, fitness in fitness_scores)
        if total_fitness == 0:
            return random.choice([individual for individual, _ in fitness_scores])
        
        # Spin the roulette wheel
        wheel_position = random.uniform(0, total_fitness)
        current_position = 0
        
        for individual, fitness in fitness_scores:
            current_position += fitness
            if current_position >= wheel_position:
                return individual
        
        return fitness_scores[-1][0]  # Fallback
    
    def select_parents(self, evaluated_population: List[Tuple[str, int]]) -> Tuple[str, str]:
        parent1 = self.roulette_wheel_selection(evaluated_population)
        parent2 = self.roulette_wheel_selection(evaluated_population)
        return parent1, parent2
    
    # CROSSOVER TECHNIQUE: Order Crossover
    def order_crossover(self, parent1: str, parent2: str) -> Tuple[str, str]:
        if len(parent1) <= 1:
            return parent1, parent2
        
        length = len(parent1)
        
        # Select two random crossover points
        point1 = random.randint(0, length - 1)
        point2 = random.randint(0, length - 1)
        
        # Ensure point1 <= point2
        if point1 > point2:
            point1, point2 = point2, point1
        
        # Create offspring
        offspring1 = [''] * length
        offspring2 = [''] * length
        
        # Copy substring from parents
        offspring1[point1:point2 + 1] = list(parent1[point1:point2 + 1])
        offspring2[point1:point2 + 1] = list(parent2[point1:point2 + 1])
        
        # Fill remaining positions maintaining order
        self._fill_remaining_positions(offspring1, parent2, point1, point2)
        self._fill_remaining_positions(offspring2, parent1, point1, point2)
        
        return ''.join(offspring1), ''.join(offspring2)
    
    def _fill_remaining_positions(self, offspring: List[str], parent: str, point1: int, point2: int):
        """Helper method for order crossover"""
        length = len(offspring)
        parent_chars = list(parent)
        
        # Start filling from position after crossover segment
        fill_pos = (point2 + 1) % length
        parent_pos = (point2 + 1) % length
        
        # Fill all empty positions
        for _ in range(length - (point2 - point1 + 1)):  # Number of positions to fill
            # Find next empty position in offspring
            while offspring[fill_pos] != '':
                fill_pos = (fill_pos + 1) % length
            
            # Take next character from parent (wrapping around)
            offspring[fill_pos] = parent_chars[parent_pos]
            parent_pos = (parent_pos + 1) % length
            fill_pos = (fill_pos + 1) % length
    
    def perform_crossover(self, parent1: str, parent2: str) -> Tuple[str, str]:
        if random.random() < self.crossover_rate:
            return self.order_crossover(parent1, parent2)
        else:
            return parent1, parent2
    
    # MUTATION TECHNIQUE: Bit Flipping Mutation
    def bit_flipping_mutation(self, individual: str) -> str:
        mutated = list(individual)
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = random.choice(self.alphabet)
        return ''.join(mutated)
    
    def perform_mutation(self, individual: str) -> str:
        return self.bit_flipping_mutation(individual)
    
    def choose_best_offspring(self, evaluated_population: List[Tuple[str, int]]) -> str:
        best_individual, _ = min(evaluated_population, key=lambda x: x[1])
        return best_individual
    
    def perform_ga_to_generate_new_word(self, game_master) -> str:
        self.current_generation += 1
        
        # Evaluate current population
        evaluated_population = self.evaluate_population(game_master)
        
        # Create new population
        new_population = []
        
        # Keep best individual (elitism)
        best_individual = self.choose_best_offspring(evaluated_population)
        new_population.append(best_individual)
        
        # Generate rest of population
        while len(new_population) < self.population_size:
            # 1. Select parents
            parent1, parent2 = self.select_parents(evaluated_population)
            
            # 2. Perform crossover
            offspring1, offspring2 = self.perform_crossover(parent1, parent2)
            
            # 3. Perform mutation
            offspring1 = self.perform_mutation(offspring1)
            offspring2 = self.perform_mutation(offspring2)
            
            new_population.extend([offspring1, offspring2])
        
        # Update population
        self.population = new_population[:self.population_size]
        
        # 4. Choose best offspring
        new_evaluated_population = self.evaluate_population(game_master)
        return self.choose_best_offspring(new_evaluated_population)
    
    # Provide optimized guess word to GameMaster
    def provide_optimized_guess_to_gamemaster(self, game_master) -> Tuple[str, int]:
        best_guess = self.perform_ga_to_generate_new_word(game_master)
        cost = game_master.return_cost_to_guesser(best_guess)
        return best_guess, cost
    
    def get_current_generation(self) -> int:
        return self.current_generation