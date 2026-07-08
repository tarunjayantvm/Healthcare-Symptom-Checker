# Healthcare Symptom Checker

A Streamlit app to gather symptoms and medical history, identify possible conditions, and provide general health and wellness advice. This app is intended for informational purposes only and does not replace professional medical care.

## Features

- Symptom selection form with duration, severity, and medical history
- Local condition inference for fast guidance
- AI-assisted summary using OpenRouter LLM
- General health chat for non-diagnostic wellness questions
- GitHub-safe setup with `.env` ignored and `.env.example` provided

## Setup

1. Clone the repository or download the files.
2. Create a Python environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add your OpenRouter API key:

```bash
copy .env.example .env
```

5. Run the app:

```bash
streamlit run app.py
```

## Environment variables

Add these variables to `.env`:

```env
OPENROUTER_API_KEY=REPLACE_WITH_OPENROUTER_KEY
LLM_BASE_URL=https://openrouter.ai/api/v1/chat/completions
LLM_MODEL=poolside/laguna-m.1:free
```

## Notes

- This app is not a medical diagnosis tool.
- Always seek professional medical attention for serious or worsening symptoms.
- Do not commit your real `.env` file to GitHub.
