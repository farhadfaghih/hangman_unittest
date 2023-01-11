from random import choice
import re
import requests
import json


class Bank:
    colours = ['red', 'blue']
    animals = ['dog', 'cat']
    topic_names = ['Colours', 'Animals']
    topics = {'Colours': colours, 'Animals': animals}
    api = 'https://api.api-ninjas.com/v1/randomword'
    api_key = 'FRkfTIwrgLLk+4TIMd+NMA==m6isKOfXzCLPgdGz'

    def __init__(self):
        self.current_topic = ''
        self.current_word = ''
        self.current_word_display = []
        self.letters_guessed_counter = 0
        self.not_solved = True
        self.letters_already_guessed = []
        self.response = None

    def get_word(self) -> None:
        try:
            self.response = requests.get(f"{self.api}", headers={'X-Api-Key': f"{self.api_key}"}, params={type: 'noun'})
            if self.response.status_code == 200:
                word = json.loads(self.response.text)
                self.current_word = word['word'].lower()
        except requests.exceptions.ConnectionError:
            self.current_topic = choice(self.topic_names)
            self.current_word = choice(self.topics[self.current_topic])
        for i in range(len(self.current_word)):
            self.current_word_display.append('_')

    def check_solve(self) -> None:
        self.not_solved = "_" in self.current_word_display


class Player:
    def __init__(self):
        self.lives = 0
        self.answer = ''
        self.guess_validation_incomplete = True

    def guess(self, guess_input: str) -> None:
        self.answer = guess_input.lower()


class Processes:
    def __init__(self):
        pass

    @staticmethod
    def validate_user_input(player: Player):
        expression = re.match('(?i)[a-z]', player.answer)
        if expression is None or len(player.answer) > 1:
            return None
        else:
            player.guess_validation_incomplete = False
            return True

    @staticmethod
    def check_answer_update_lives(bank: Bank, player: Player) -> str:
        if player.answer in bank.letters_already_guessed:
            return '\nLetter already guessed.'

        elif player.answer not in bank.current_word:
            player.lives -= 1
            bank.letters_already_guessed.append(player.answer)
            return '\nNope!'

        else:
            for i in range(len(bank.current_word)):
                if player.answer == bank.current_word[i]:
                    bank.current_word_display[i] = player.answer
                    bank.letters_guessed_counter += 1
                    bank.letters_already_guessed.append(player.answer)
            return '\nNice!'


class Main:
    while True:
        word_bank = Bank()
        player1 = Player()
        game = Processes()
        word_bank.get_word()
        print(f'Topic: {word_bank.current_topic}' if word_bank.current_topic else "Topic: random word from API")
        print(f'Word is {len(word_bank.current_word)} letters long.')
        print(word_bank.current_word_display)
        player1.lives = len(word_bank.current_word) * 3
        while word_bank.not_solved and player1.lives > 0:
            while player1.guess_validation_incomplete:
                player1.guess(input('Guess a letter: '))
                if game.validate_user_input(player1) is None:
                    print('\nPlease guess a single alphabet')
            print(game.check_answer_update_lives(word_bank, player1))
            print('Lives remaining: {}'.format(player1.lives))
            print(word_bank.current_word_display)
            player1.guess_validation_incomplete = True
            word_bank.check_solve()

        if word_bank.not_solved:
            print('\nYou lose')
            print('Word was {}'.format(word_bank.current_word))
        else:
            print('\nYou win!')
        replay = input('Press any key to play again, x to quit: ')
        print('\n')
        if replay.upper() == 'X':
            break


if __name__ == "__main__":
    play = Main()
