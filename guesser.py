# guesser 

import random
import string
from typing import List, Tuple
from game_master import GameMaster


class Guesser:
    def __init__(self, word_length: int, population_size: int = 100):
        self.word_length = word_length
        self.alphabet = string.ascii_lowercase
        
        self.population_size = population_size
        self.population = []
        
        self.crossover_rate = 0.8
        self.mutation_rate = 0.1

        self.generation = 0
        
        
    def initialize_population(self) -> None:
        
        # Create the first gen of random guess
        self.population = []
        for _ in range(self.population_size):
            individual = ''.join(random.choice(self.alphabet) for _ in range(self.word_length))
            self.population.append(individual)
        
        self.generation = 0
    
    
    def evaluate_population(self, game_master: GameMaster) -> List[Tuple[str, int]]:
        evaluated_pop = []
        for individual in self.population:
          
            cost = game_master.calculate_cost(individual)
            evaluated_pop.append((individual, cost))
        
        return evaluated_pop
    
    
    def roulette_wheel_selection(self, evaluated_pop: List[Tuple[str, int]]) -> str:
        # Select a guess parent base on fitness
        max_cost = max(cost for _, cost in evaluated_pop)
        fitness_scores = [(individual, max_cost - cost + 1) for individual, cost in evaluated_pop]
        
        total_fitness = sum(fitness for _, fitness in fitness_scores)
        if total_fitness == 0:
            
            # If all guesses have bad fitness score, pick a guess randomly
            return random.choice([individual for individual, _ in fitness_scores])
        
        # Spin the wheel to pick one guess
        wheel_position = random.uniform(0, total_fitness)
        current_position = 0
        
        
        for individual, fitness in fitness_scores:
            current_position += fitness
            if current_position >= wheel_position:
                return individual
        
        return fitness_scores[-1][0]
    
    
    
    # CROSSOVER TECHNIQUE: single-point crossover
    def single_point_crossover(self, parent1: str, parent2: str) -> Tuple[str, str]:
        # Combine two parent guesses
        if len(parent1) <= 1:
            return parent1, parent2
        
        crossover_point = random.randint(1, len(parent1) - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return offspring1, offspring2
    
    
    
    # MUTATION TECHNIQUE: bif-flipping mutation
    def bit_flipping_mutation(self, individual: str) -> str:
        # change some letters randomly when guessing
        mutated = list(individual)
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = random.choice(self.alphabet)
        return ''.join(mutated)
    
    
    # Find the best guess with lowest cost
    def get_best_individual(self, evaluated_pop: List[Tuple[str, int]]) -> Tuple[str, int]:
        return min(evaluated_pop, key=lambda x: x[1])
    
    def evolve_generation(self, game_master: GameMaster) -> Tuple[str, int]:
        self.generation += 1
        
        # Evaluate current guesses 
        evaluated_pop = self.evaluate_population(game_master)
        # Find the best guess atm
        best_individual, best_cost = self.get_best_individual(evaluated_pop)
        new_population = []
        
        # Keep the best guesses using elitism
        new_population.append(best_individual)


        # Generate guesses until it reached to 100
        while len(new_population) < self.population_size:
            
            # choose two parent guesses
            parent1 = self.roulette_wheel_selection(evaluated_pop)
            parent2 = self.roulette_wheel_selection(evaluated_pop)
            
            
            # combine to make children (new guesses)
            if random.random() < self.crossover_rate:
                offspring1, offspring2 = self.single_point_crossover(parent1, parent2)
            
            else:
                offspring1, offspring2 = parent1, parent2
            
            
            # Randomly mutate new guesses
            offspring1 = self.bit_flipping_mutation(offspring1)
            offspring2 = self.bit_flipping_mutation(offspring2)
            
            
            # add it to new generation
            new_population.extend([offspring1, offspring2])
            
          
        self.population = new_population[:self.population_size]
        
        # Return the best guess and itss cost
        return best_individual, best_cost
    
    
    # Return what generation we're on
    def get_current_generation(self) -> int:
        return self.generation