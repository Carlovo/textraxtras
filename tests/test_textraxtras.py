import json
import os

from textraxtras import hello
from unittest import TestCase


class TestSmoke(TestCase):
    def test_sanity(self):
        self.assertTrue(True)

    def test_integration(self):
        self.assertEqual("Hello from textraxtras!", hello())


def load_json_file(filepath: str):
    with open(filepath) as json_file:
        return json.load(json_file)


def load_json_files(path: str) -> list:
    filenames = next(os.walk(path))[2]
    return [load_json_file(f"{path}/{filename}") for filename in sorted(filenames)]


class TestQualityTestData(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fixture_pairs = (
            it
            for it in zip(
                load_json_files("tests/fixtures/expected_text"),
                load_json_files("tests/fixtures/detect_document_text"),
            )
        )

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
