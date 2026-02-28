import logging
from importlib import resources
from pathlib import Path

import pyarrow.parquet as pq

from .constants import SUPPORTED_LANGUAGES


class ProfanityFilter:
    def __init__(self, lang_code: str, parquet_path: str | Path | None = None):
        if lang_code not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language code: {lang_code}. "
                f"Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
            )

        self.lang_code = lang_code
        self.bad_words: set[str] = set()

        # ✨ Dependency Injection for testing
        if parquet_path:
            self.parquet_path = Path(parquet_path)
        else:
            try:
                # Use standard library to find the bundled data in the package
                # Python 3.9+ standard
                trav = resources.files("multilingual_profanity.data").joinpath(
                    "profanity.parquet"
                )

                # Resources might be inside a zip/wheel, so we need to handle it properly
                # For basic pyarrow loading, converting it to a string path usually works if unzipped,
                # but we'll store it as a Path-like object or string.
                # In editable mode, trav is just a pathlib.Path wrapper.
                self.parquet_path = trav
            except Exception as e:
                logging.error(f"Could not locate bundled data package: {e}")
                self.parquet_path = None

        self._load_list()

    def _load_list(self) -> None:
        if self.parquet_path is None:
            logging.warning("⚠️ Parquet file path is None. Filter will be open.")
            return

        # Standardize check (works for both pathlib.Path and importlib Traversable)
        if not getattr(self.parquet_path, "is_file", lambda: False)():
            logging.warning(
                f"⚠️ Parquet file not found at {self.parquet_path}. Filter will be open."
            )
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
        if not self.bad_words:
            return True
        return word.lower() not in self.bad_words
