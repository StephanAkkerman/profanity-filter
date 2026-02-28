import tempfile
import unittest
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

# Import directly from the installed package
from multilingual_profanity import ProfanityFilter


class TestProfanityFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary Parquet file with dummy profanity data
        before any tests run.
        """
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_parquet_path = Path(cls.temp_dir.name) / "test_profanity.parquet"

        # Create dummy data: English and Dutch bad words
        data = {
            "lang": ["en", "en", "nl", "nl"],
            "word": ["badword", "uglyword", "kanker", "hoer"],
        }

        table = pa.Table.from_pydict(data)
        pq.write_table(table, cls.test_parquet_path)

    @classmethod
    def tearDownClass(cls):
        """Cleans up the temporary directory after all tests finish."""
        cls.temp_dir.cleanup()

    def test_default_initialization(self):
        """
        Test that it loads the actual bundled package data without crashing.
        (Requires the real profanity.parquet to be built in data/ first).
        """
        try:
            # We don't pass parquet_path here to trigger importlib.resources
            pf = ProfanityFilter("en")
            self.assertTrue(isinstance(pf.bad_words, set))
        except Exception as e:
            self.fail(f"Default initialization failed to load bundled data: {e}")

    def test_unsupported_language_raises_error(self):
        """Test that initializing with a bad language code raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ProfanityFilter("zz", parquet_path=self.test_parquet_path)

        self.assertIn("Unsupported language code: zz", str(context.exception))

    def test_missing_parquet_file_fails_open(self):
        """Test that a missing Parquet file doesn't crash, but allows all words (fail-open)."""
        pf = ProfanityFilter("en", parquet_path="does_not_exist.parquet")

        self.assertEqual(len(pf.bad_words), 0)
        self.assertTrue(pf.is_clean("badword"))  # Should be clean because list is empty

    def test_successful_loading_and_filtering(self):
        """Test that words are correctly flagged as clean or blocked using the dummy file."""
        pf = ProfanityFilter("en", parquet_path=self.test_parquet_path)

        # Exact matches
        self.assertFalse(pf.is_clean("badword"))
        self.assertFalse(pf.is_clean("uglyword"))

        # Case-insensitive checking
        self.assertFalse(pf.is_clean("BADWORD"))
        self.assertFalse(pf.is_clean("BadWord"))

        # Clean words
        self.assertTrue(pf.is_clean("hello"))
        self.assertTrue(pf.is_clean("world"))

    def test_predicate_pushdown_isolation(self):
        """
        Test that loading 'en' ONLY loads 'en' words,
        proving our pyarrow filters are working correctly.
        """
        pf_en = ProfanityFilter("en", parquet_path=self.test_parquet_path)
        pf_nl = ProfanityFilter("nl", parquet_path=self.test_parquet_path)

        # 'kanker' is a Dutch bad word. Blocked in NL, clean in EN.
        self.assertFalse(pf_nl.is_clean("kanker"))
        self.assertTrue(pf_en.is_clean("kanker"))

        # 'badword' is an English bad word. Blocked in EN, clean in NL.
        self.assertFalse(pf_en.is_clean("badword"))
        self.assertTrue(pf_nl.is_clean("badword"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
