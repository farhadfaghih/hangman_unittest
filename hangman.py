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
        self.api_response_status = False

    def pick_topic(self) -> None:
        self.current_topic = choice(self.topic_names)

    def get_word(self) -> None:
        try:
            response = requests.get(f"{self.api}", headers={'X-Api-Key': f"{self.api_key}"}, params={type: 'noun'})
            if response.status_code == 200:
                word = json.loads(response.text)
                self.api_response_status = True
                self.current_word = word['word'].lower()
        except requests.exceptions.ConnectionError:
            pass

    def pick_word(self) -> None:
        self.current_word = choice(self.topics[self.current_topic])

    # this method is to access the current_word_display easier
    def display_maker(self) -> None:
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
        self.answer = guess_input


class Processes:
    def __init__(self):
        pass

    @staticmethod
    def validate_user_input(player: Player):
        expression = re.match('(?i)[a-z]', player.answer)
        player.answer = player.answer.lower()
        if expression is None or len(player.answer) > 1:
            return None
        else:
            player.guess_validation_incomplete = False
            return True

    @staticmethod
    def check_answer_update_lives(bank: Bank, player: Player) -> str:
        if player.answer in bank.letters_already_guessed:
            return "repeated"

        elif player.answer not in bank.current_word:
            player.lives -= 1
            bank.letters_already_guessed.append(player.answer)
            return "False"

        else:
            for i in range(len(bank.current_word)):
                if player.answer == bank.current_word[i]:
                    bank.current_word_display[i] = player.answer
                    bank.letters_guessed_counter += 1
                    bank.letters_already_guessed.append(player.answer)
            return "True"


class Main:
    def __init__(self):
        pass

    while True:
        word_bank = Bank()
        player1 = Player()
        game = Processes()
        word_bank.get_word()
        if not word_bank.api_response_status:
            word_bank.pick_topic()
            print(f'Topic: {word_bank.current_topic}')
            word_bank.pick_word()
        print(f'Word is {len(word_bank.current_word)} letters long.')
        word_bank.display_maker()
        print(word_bank.current_word_display)
        player1.lives = len(word_bank.current_word) * 3

        while word_bank.not_solved and player1.lives > 0:
            while player1.guess_validation_incomplete:
                player1.guess(input('Guess a letter: '))
                if game.validate_user_input(player1) is None:
                    print('\nPlease guess a single alphabet')
            info = game.check_answer_update_lives(word_bank, player1)
            if info == "repeated":
                print('\nLetter already guessed.')
            elif info == "False":
                print('\nNope!')
            elif info == "True":
                print('\nNice!')
            print('Lives remaining: {}'.format(player1.lives))
            print(word_bank.current_word_display)
            player1.guess_validation_incomplete = True
            word_bank.check_solve()

        if not word_bank.not_solved:
            print('\nYou win!')

        else:
            print('\nYou lose')
            print('Word was {}'.format(word_bank.current_word))

        replay = input('Press any key to play again, x to quit: ')
        print('\n')
        if replay.upper() == 'X':
            break


Play = Main()
del Play
