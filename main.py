from game_master import GameMaster
from guesser import Guesser


def display_header(target_word: str) -> None:
    print(f"\nWord to be guessed: {target_word}")
    print("-" * 40)
    print("Generation | Best Guess | Cost Value")
    print("-" * 40)


def display_generation_result(generation: int, best_guess: str, cost_value: int) -> None:
    print(f"{generation:10d} | {best_guess:10s} | {cost_value:10d}")


def get_target_word() -> str:
    while True:
        word = input("Enter the word to be guessed: ").strip()
        if word and word.isalpha():
            return word.lower()
        print("Please enter a valid word containing only letters.")


def main():    
    print("Welcome to Pinoy-Henry's Pinoy Henyo!")
    print("=" * 50)
    
    # Get target word from user
    target_word = get_target_word()
    
    # Initialize Game Master and Guesser
    game_master = GameMaster(target_word)
    guesser = Guesser(game_master.get_word_length())
    
    # Initialize population
    guesser.initialize_population()
    
    # Display header
    display_header(target_word)
    
    # STOPPING TECHNIQUE: maximum generation
    max_generations = 100
    found_solution = False
    
    # Evolution loop
    for generation in range(1, max_generations + 1):
        # Evolve one generation
        best_guess, cost_value = guesser.evolve_generation(game_master)
        
        # Display results
        display_generation_result(generation, best_guess, cost_value)
        
        # Check if word is guessed correctly
        if game_master.is_correct(best_guess):
            print("-" * 50)
            print(f"SUCCESS! Word guessed correctly in generation {generation}!")
            print(f"Final answer: {best_guess}")
            found_solution = True
            break
    
    if not found_solution:
        print("-" * 50)
        print(f"Maximum generations ({max_generations}) reached.")
        print(f"Best guess: {best_guess} (Cost: {cost_value})")
    
    print("=" * 50)


if __name__ == "__main__":
    main()