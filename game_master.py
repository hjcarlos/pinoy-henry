class GameMaster:   
    def __init__(self, target_word: str):
        self.target_word = target_word.lower()
        self.word_length = len(self.target_word)
    
    def calculate_cost(self, guess: str) -> int:
        if len(guess) != len(self.target_word):
            return len(self.target_word)
        
        cost = 0
        for i in range(len(self.target_word)):
            if guess[i] != self.target_word[i]:
                cost += 1
        return cost
    
    def is_correct(self, guess: str) -> bool:
        return guess.lower() == self.target_word
    
    def get_target_word(self) -> str:
        return self.target_word
    
    def get_word_length(self) -> int:
        return self.word_length