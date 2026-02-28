# Multilingual Profanity Filter

<!-- Add a banner here like: https://github.com/StephanAkkerman/fintwit-bot/blob/main/img/logo/fintwit-banner.png -->

---
<!-- Adjust the link of the first and second badges to your own repo -->
<p align="center">
  <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/StephanAkkerman/profanity-filter/pyversions.yml?label=python%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13&logo=python&style=flat-square">
  <img src="https://img.shields.io/github/license/StephanAkkerman/profanity-filter.svg?color=brightgreen" alt="License">
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

## Introduction

This project provides a profanity filter that supports multiple languages. It is designed to be easy to use and integrate into various applications. The filter uses a comprehensive list of profane words for each supported language, allowing it to effectively identify and filter out inappropriate content.

It uses the [List of Dirty, Naughty, Obscene, and Otherwise Bad Words](https://github.com/LDNOOBWV2/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words_V2) as its primary source for profane words, which is a widely used repository of such words in multiple languages.

## Table of Contents 🗂

- [Supported Languages 🌐](#supported-languages-)
- [Installation](#installation)
- [Usage](#usage)
- [Citation](#citation)
- [Contributing](#contributing)
- [License](#license)

## Supported Languages 🌐

The profanity filter currently supports the same languages as the LDNOOBWV2 repository, you can find it [here](https://github.com/LDNOOBWV2/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words_V2?tab=readme-ov-file#languages-files-overview).


## Installation ⚙️
<!-- Adjust the link of the second command to your own repo -->

This package is available on PyPI, so you can install it using pip:

```bash
pip install multilingual-profanity
```

## Usage ⌨️

Here's a simple example of how to use the `ProfanityFilter` class:

```python
from multilingual_profanity import ProfanityFilter

pf = ProfanityFilter("nl")
print(pf.is_clean("fiets")) # Output: True
print(pf.is_clean("kanker")) # Output: False
```

## Citation ✍️
<!-- Be sure to adjust everything here so it matches your name and repo -->
If you use this project in your research, please cite as follows:

```bibtex
@misc{profanity_filter,
  author  = {Stephan Akkerman},
  title   = {Profanity Filter},
  year    = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/StephanAkkerman/profanity-filter}}
}
```

## Contributing 🛠
<!-- Be sure to adjust the repo name here for both the URL and GitHub link -->
Contributions are welcome! If you have a feature request, bug report, or proposal for code refactoring, please feel free to open an issue on GitHub. We appreciate your help in improving this project.\
![https://github.com/StephanAkkerman/profanity-filter/graphs/contributors](https://contributors-img.firebaseapp.com/image?repo=StephanAkkerman/profanity-filter)

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
