# HuggingFace Daily Paper Newsletter Multilingual

<div align="center">
  <a href="https://internlm.org/">
    <img src="https://internlm.org/assets/logo-a0611363.svg" alt="InternLM" height="80"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/">
    <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="HuggingFace" height="80"/>
  </a>
</div>

<p align="center">
  <em>Translating HuggingFace Daily Papers with InternLM</em>
</p>

<div align="center">

[English](README.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md)

</div>

---

This project automatically downloads and processes HuggingFace daily paper data and translates it into multiple languages using the InternLM large language model. The project runs automatically every day to ensure timely retrieval and translation of the latest papers.

## Model Used

- **Translation Model**: [InternLM-3](https://internlm.org/)
  - Developer: Shanghai AI Laboratory
  - Version: internlm3-latest
  - Features:
    - Powerful multilingual translation capabilities
    - Accurate understanding and translation of academic texts
    - Real-time translation via API

## Features

- Automatic download of HuggingFace daily paper data
- Support for downloading historical data from specific dates
- Use of Beijing time as default timezone
- Complete activity logging
- JSON format paper metadata storage
- Translation of English papers to multiple languages using InternLM-3:
  - Japanese
  - Korean
  - Spanish
  - French
- Automated workflow:
  - Daily automatic download of latest papers
  - Automatic multilingual translation
  - Automatic repository updates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hf-daily-paper-newsletter-multilingual.git
cd hf-daily-paper-newsletter-multilingual
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Manual Execution

#### Download Today's Papers

```bash
python download_papers.py
```

#### Download Papers from a Specific Date

```bash
python download_papers.py --date 2024-03-20
```

#### Translate Papers

First obtain an InternLM API key, then run:

```bash
python translate_papers.py --date 2024-03-20 --api_key your_api_key_here
```

### Automatic Execution

The project is configured with two GitHub Actions workflows:

1. `daily-paper-download.yml`: Automatically downloads latest papers at 9:00 AM Beijing time
2. `daily-paper-translate.yml`: Automatic translation after download

To enable automatic translation, you need to set `INTERNLM_API_KEY` in the repository's Secrets.

## Data Storage

- Original English paper data is stored in the `Paper_metadata_download` directory
- Translated papers are stored in the `Translated_papers` directory, organized by language code:
  - ja/: Japanese translations
  - ko/: Korean translations
  - es/: Spanish translations
  - fr/: French translations
- All files are saved in JSON format with names in `YYYY-MM-DD.json` format

## Return Status

- Success: exit code 0
- Error: exit code 1
- No data: exit code 0 (with warning in log)

## Acknowledgments

- [InternLM](https://internlm.org/) - For providing powerful translation capabilities
- [HuggingFace](https://huggingface.co/) - For providing daily paper data
