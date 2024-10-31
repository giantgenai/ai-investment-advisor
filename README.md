# AI Investment App
![GitHub stars](https://img.shields.io/github/stars/giantgenai/ai-investment-advisor?style=social)
![Forks](https://img.shields.io/github/forks/giantgenai/ai-investment-advisor?style=social)
![Issues](https://img.shields.io/github/issues/giantgenai/ai-investment-advisor)
![Last Commit](https://img.shields.io/github/last-commit/giantgenai/ai-investment-advisor)
![Repo Size](https://img.shields.io/github/repo-size/giantgenai/ai-investment-advisor)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![Build](https://img.shields.io/badge/build-passing-brightgreen)


Welcome to AI Investment App! 🚀 

This application leverages large language models to analyze recent news summaries on companies and generate investment recommendations. By entering an industry name, the AI identifies the top three companies within that sector and evaluates their latest news to determine the most promising investment opportunity.



## Table of Contents
<!-- - [Overview](#overview) -->
- [Features](#features)
- [Installation](#installation)
- [Examples](#examples)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

<!-- ## Overview
The AI Image Classifier app enables users to upload an image and receive a classification from various categories like 'Dog', 'Cat', 'Car', etc. This is useful for quickly categorizing large datasets of images. -->

## Features
- **News Scraping:** The application scrapes financial news from sources like CNBC and Yahoo Finance. It uses python libraries `requests` and `BeautifulSoup` to fetch and parse web content. The scraped articles are saved locally with metadata like title, source, and timestamp.
- **Investment Recommendation:** The app uses a language model to analyze news summaries and recommend investments. The companies news are scraped and summarized by `Crawl4ai`'s `LLMExtractionStrategy` with options of using `OpenAI's GPT models` or `Ollama's LLaMA 3` model, which is compatible with OpenAI's API format but runs locally.
- **Local LLM Integration:** The app is configured to use `Ollama's LLaMA models locally`, leveraging their OpenAI-compatible API. This setup involves running a local server and using a placeholder API key ('ollama'), which is required but not used for authentication.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/giantgenai/ai-investment-advisor.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
   ```bash
   cd app
   python investment_app.py

