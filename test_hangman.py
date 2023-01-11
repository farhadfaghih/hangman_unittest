import unittest
import requests

import hangman


class TestBank(unittest.TestCase):
    def setUp(self):
        self.word_bank = hangman.Bank()
        self.word_bank.pick_topic()
        self.word_bank.pick_word()
        self.word_bank.display_maker()

    def test_pick_topic(self):
        self.assertIn(self.word_bank.current_topic, self.word_bank.topics)

    def test_get_word(self):
        with GetWordContextManager() as word_bank:
            if word_bank.response:
                if word_bank.response.status_code == 200:
                    self.assertIs(word_bank.api_response_status, True)
                else:
                    self.assertIs(word_bank.api_response_status, False)
            else:
                self.assertIs(word_bank.api_response_status, False)

    def test_pick_word(self):
        self.assertIn(self.word_bank.current_word, self.word_bank.topics[self.word_bank.current_topic])

    def test_display_maker(self):
        self.assertEqual(len(self.word_bank.current_word), len(self.word_bank.current_word_display))
        self.assertEqual((len(self.word_bank.current_word) * "_"), "".join(self.word_bank.current_word_display))

    def test_check_solve(self):
        with CurrentWordDisplayContextManager(["_", "_", "c"]) as word_bank:
            self.assertIs(word_bank.not_solved, True)
            del word_bank
        with CurrentWordDisplayContextManager(["a", "b", "c"]) as word_bank:
            self.assertIs(word_bank.not_solved, False)
            del word_bank


class CurrentWordDisplayContextManager:
    def __init__(self, word):
        self.word = word
        self.word_bank = hangman.Bank()

    def __enter__(self):
        self.word_bank.current_word_display = self.word
        self.word_bank.check_solve()
        return self.word_bank

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.word_bank


class GetWordContextManager:
    def __init__(self):
        self.word_bank = None

    def __enter__(self):
        self.word_bank = hangman.Bank()
        self.word_bank.get_word()
        return self.word_bank

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.word_bank


class TestPlayer(unittest.TestCase):
    pass


class TestProcess(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
