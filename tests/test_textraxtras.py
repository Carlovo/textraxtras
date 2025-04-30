import json
import os
from typing import Any
from unittest import TestCase

from textraxtras import get_unique_words


class TestSmoke(TestCase):
    def test_sanity(self):
        self.assertTrue(True)


def load_json_file(filepath: str) -> Any:
    with open(filepath) as json_file:
        return json.load(json_file)


def load_json_files(path: str) -> list:
    filenames = next(os.walk(path))[2]
    return [load_json_file(f"{path}/{filename}") for filename in sorted(filenames)]


def words_in_sentences(sentences: list[str]) -> set[str]:
    return set(word for line in sentences for word in line.split(" "))


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
                expected_words = words_in_sentences(expected_lines)

                detected_words = {
                    block["Text"]
                    for block in detected_text["Blocks"]
                    if block["BlockType"] == "WORD"
                }

                self.assertSetEqual(expected_words, detected_words)

    def test_get_unique_words(self):
        for expected_lines, detected_text in self._fixture_pairs:
            with self.subTest(
                expected_lines=expected_lines, detected_text=detected_text
            ):
                expected_words = words_in_sentences(expected_lines)

                detected_words = get_unique_words(detected_text)

                self.assertSetEqual(expected_words, detected_words)
