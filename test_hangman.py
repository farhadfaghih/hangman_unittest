import unittest
import hangman


class TestBank(unittest.TestCase):
    def setUp(self) -> None:
        self.word_bank = hangman.Bank()

    def test_pick_topic(self):
        self.word_bank.pick_topic()
        self.assertIn(self.word_bank.current_topic, self.word_bank.topics)

    def test_get_word(self):
        self.word_bank.get_word()
        if self.word_bank.response:
            if self.word_bank.response.status_code == 200:
                self.assertIs(self.word_bank.api_response_status, True)
                self.assertIsInstance(self.word_bank.current_word, str)
            else:
                self.assertIs(self.word_bank.api_response_status, False)
        else:
            self.assertIs(self.word_bank.api_response_status, False)

    def test_pick_word(self):
        self.word_bank.pick_topic()
        self.word_bank.pick_word()
        self.assertIn(self.word_bank.current_word, self.word_bank.topics[self.word_bank.current_topic])

    def test_display_maker(self):
        self.word_bank.display_maker()
        self.assertEqual(len(self.word_bank.current_word), len(self.word_bank.current_word_display))
        self.assertEqual((len(self.word_bank.current_word) * "_"), "".join(self.word_bank.current_word_display))

    def test_check_solve(self):
        self.word_bank.current_word_display = ["_", "_", "c"]
        self.word_bank.check_solve()
        self.assertIs(self.word_bank.not_solved, True)
        self.word_bank.current_word_display = ["a", "b", "c"]
        self.word_bank.check_solve()
        self.assertIs(self.word_bank.not_solved, False)


class TestPlayer(unittest.TestCase):
    pass


class TestProcess(unittest.TestCase):
    def setUp(self) -> None:
        self.word_bank = hangman.Bank()
        self.word_bank.current_word = "dog"
        self.word_bank.current_word_display = ["_", "_", "_"]
        self.word_bank.letters_already_guessed = ["a", "b", "c"]
        self.word_bank.letters_guessed_counter = 3
        self.player1 = hangman.Player()
        self.player1.lives = 5
        self.game = hangman.Processes()

    def test_validate_user_input(self):
        self.player1.answer = "y"
        self.assertIs(self.game.validate_user_input(self.player1), True)
        self.assertIs(self.player1.guess_validation_incomplete, False)
        self.player1.answer = "ab"
        self.assertIs(self.game.validate_user_input(self.player1), None)
        self.player1.answer = "1"
        self.assertIs(self.game.validate_user_input(self.player1), None)
        self.player1.answer = " "
        self.assertIs(self.game.validate_user_input(self.player1), None)
        self.player1.answer = ""
        self.assertIs(self.game.validate_user_input(self.player1), None)
        self.player1.answer = "."
        self.assertIs(self.game.validate_user_input(self.player1), None)

    def test_check_answer_update_lives(self):
        self.player1.answer = "a"
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player1), "repeated")
        self.assertEqual(self.player1.lives, 5)
        self.player1.answer = "k"
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player1), "False")
        self.assertEqual(self.player1.lives, 4)
        self.assertEqual(self.word_bank.letters_already_guessed, ["a", "b", "c", "k"])
        self.player1.answer = "o"
        self.assertEqual(self.game.check_answer_update_lives(self.word_bank, self.player1), "True")
        self.assertEqual(self.player1.lives, 4)
        self.assertEqual(self.word_bank.current_word_display, ["_", "o", "_"])
        self.assertEqual(self.word_bank.letters_guessed_counter, 4)
        self.assertEqual(self.word_bank.letters_already_guessed, ["a", "b", "c", "k", "o"])


if __name__ == "__main__":
    unittest.main()
