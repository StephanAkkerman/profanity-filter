import logging
from importlib import resources

import pyarrow.parquet as pq

from constants import SUPPORTED_LANGUAGES


class ProfanityFilter:
    def __init__(self, lang_code: str):
        if lang_code not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language code: {lang_code}")

        self.lang_code = lang_code
        self.bad_words: set[str] = set()

        # Dynamically locate the parquet file inside the installed package
        try:
            # Looks inside src/data/profanity.parquet
            self.parquet_path = resources.files("data").joinpath("profanity.parquet")
        except Exception as e:
            logging.error(f"Could not locate bundled data package: {e}")
            self.parquet_path = None

        self._load_list()

    def _load_list(self) -> None:
        if not self.parquet_path or not self.parquet_path.is_file():
            logging.warning("⚠️ Parquet file not found. Filter will be open.")
            return

        try:
            table = pq.read_table(
                self.parquet_path,
                columns=["word"],
                filters=[("lang", "==", self.lang_code)],
            )
            raw_words = table.column("word").to_pylist()
            self.bad_words = {str(w).lower() for w in raw_words if w}
        except Exception as e:
            logging.warning(f"⚠️ Error loading blocklist for '{self.lang_code}': {e}")

    def is_clean(self, word: str) -> bool:
        """Returns True if the word is NOT in the profanity blocklist."""
        if not self.bad_words:
            return True
        return word.lower() not in self.bad_words
