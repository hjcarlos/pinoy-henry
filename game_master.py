class GameMaster:  
    def __init__(self):
        self.target_word = ""
        self.word_length = 0
    
    # Provide the word to be guessed
    def get_word_from_user(self):
        while True:
            word = input("Enter the word to be guessed: ").strip().lower()
            if word and word.isalpha():
                self.target_word = word
                self.word_length = len(word)
                print(f"Target word set: {self.target_word}")
                break
            else:
                print("Please enter a valid word containing only letters.")
    
    # Compute the cost value
    def compute_cost_value(self, guess_word: str) -> int:
        if len(guess_word) != self.word_length:
            return self.word_length
        
        cost = 0
        for i in range(self.word_length):
            if guess_word[i] != self.target_word[i]:
                cost += 1
        
        return cost
    
    # Return the cost value
    def return_cost_to_guesser(self, guess_word: str) -> int:
        return self.compute_cost_value(guess_word)
    
    # Confirm correct answer
    def confirm_correct_answer(self, guess_word: str) -> bool:
        return guess_word == self.target_word
    
    def get_target_word(self) -> str:
        return self.target_word
    
    def get_word_length(self) -> int:
        return self.word_length