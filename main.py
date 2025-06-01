import matplotlib.pyplot as plt
from game_master import GameMaster
from guesser import Guesser


def display_ga_techniques():
    print("Pinoy Henyo Game using Genetic Algorithm")
    print("=" * 50)
    print("GA TECHNIQUES:")
    print("- Chromosome Encoding: String-based encoding")
    print("- Parent Selection: Roulette Wheel Selection")
    print("- Crossover Technique: Order Crossover")
    print("- Mutation Technique: Bit Flipping Mutation")
    print("- Stopping Criterion: Maximum Generation (100)")
    print("=" * 50)


def display_results_header(target_word: str):
    print(f"\nWord to be guessed: {target_word}")
    print("-" * 40)
    print("Generation | Best Guess | Cost Value")
    print("-" * 40)


def display_generation_result(generation: int, best_guess: str, cost_value: int):
    print(f"{generation:10d} | {best_guess:10s} | {cost_value:10d}")


def plot_cost_function_graph(generations: list, costs: list, target_word: str):
    plt.figure(figsize=(10, 6))
    plt.plot(generations, costs, 'b-', linewidth=2, marker='o', markersize=4)
    plt.title(f'Cost Function Minimization Over Generations\nTarget Word: "{target_word}"')
    plt.xlabel('Generation (N)')
    plt.ylabel('Cost Value')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, max(generations) + 5)
    plt.ylim(0, max(costs) + 1)
    
    # Add annotation for final cost
    plt.annotate(f'Final Cost: {costs[-1]}', 
                xy=(generations[-1], costs[-1]), 
                xytext=(generations[-1], costs[-1] + 1),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, color='red')
    
    plt.tight_layout()
    plt.show()


def main(): 
    # Display GA techniques
    display_ga_techniques()
    
    # INITIALIZATION
    # GameMaster: User provides the word to be guessed
    game_master = GameMaster()
    game_master.get_word_from_user()
    
    # Initialize Guesser
    guesser = Guesser(game_master.get_word_length())
    
    # Display results header
    display_results_header(game_master.get_target_word())
    
    # GAME PROPER
    # Guesser: Provide initial guess to GameMaster
    initial_guess, initial_cost = guesser.provide_optimized_guess_to_gamemaster(game_master)
    display_generation_result(0, initial_guess, initial_cost)
    initial_cost = game_master.return_cost_to_guesser(initial_guess)
    display_generation_result(0, initial_guess, initial_cost)
    
    # Tracking for visualization
    generations = [0]
    costs = [initial_cost]
    
    # STOPPING TECHNIQUE: Maximum Generation (100)
    max_generations = 1000
    solution_found = False
    
    # Evolution loop
    for generation in range(1, max_generations + 1):
        # Guesser: Perform GA to generate new word and provide to GameMaster
        best_guess, cost_value = guesser.provide_optimized_guess_to_gamemaster(game_master)
        
        # Track for visualization
        generations.append(generation)
        costs.append(cost_value)
        
        # Display generation result
        display_generation_result(generation, best_guess, cost_value)
        
        # GameMaster: Confirm if correct answer
        if game_master.confirm_correct_answer(best_guess):
            print("-" * 40)
            print(f"SUCCESS! Word guessed correctly in generation {generation}!")
            print(f"Final answer: {best_guess}")
            print(f"Final cost: {cost_value}")
            solution_found = True
            break
    
    # Final results
    if not solution_found:
        print("-" * 40)
        print(f"Maximum generations ({max_generations}) reached.")
        print(f"Best guess: {best_guess}")
        print(f"Final cost: {cost_value}")
    
    print("=" * 50)
    
    # Display cost function graph
    print("Generating cost function graph...")
    plot_cost_function_graph(generations, costs, game_master.get_target_word())


if __name__ == "__main__":
    main()