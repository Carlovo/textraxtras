import json

from textraxtras import hello
from unittest import TestCase


class TestSmoke(TestCase):
    def test_sanity(self):
        self.assertTrue(True)

    def test_integration(self):
        self.assertEqual("Hello from textraxtras!", hello())


class TestQualityTestData(TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_pairs = []

        for it in range(1, 8):
            with open(f"tests/fixtures/lines{it}.json") as json_file:
                expected_lines = json.load(json_file)
            with open(f"tests/fixtures/detect_document_text{it}.json") as json_file:
                detected_text = json.load(json_file)
            fixture_pairs.append((expected_lines, detected_text))

        cls._fixture_pairs = tuple(fixture_pairs)

    def test_all_words_present(self):
        for expected_lines, detected_text in self._fixture_pairs:
            with self.subTest(
                expected_lines=expected_lines, detected_text=detected_text
            ):
                expected_word_string = " ".join(expected_lines)
                expected_words = set(expected_word_string.split(" "))

                detected_words = {
                    block["Text"]
                    for block in detected_text["Blocks"]
                    if block["BlockType"] == "WORD"
                }

                self.assertSetEqual(expected_words, detected_words)
