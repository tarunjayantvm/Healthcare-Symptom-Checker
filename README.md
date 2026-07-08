# 🩺 Healthcare Symptom Checker

An AI-powered **Healthcare Symptom Checker** built with **Streamlit** and an **OpenRouter-compatible LLM**. The application collects user symptoms and medical history, asks intelligent follow-up questions, suggests possible health conditions, recommends appropriate medical attention, and provides general wellness guidance. It is designed for **informational purposes only** and is **not a substitute for professional medical advice or diagnosis**.

---

## ✨ Features

- 🤒 Symptom assessment with duration and severity tracking
- 📝 Medical history collection
- 🤖 AI-powered follow-up questions for better symptom evaluation
- 🩺 Possible condition identification based on reported symptoms
- 🚑 Guidance on whether medical attention may be needed
- 💬 Interactive health and wellness chat
- ⚡ Powered by OpenRouter-compatible Large Language Models
- 🎨 Clean and responsive Streamlit interface

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **OpenRouter API**
- **Large Language Models (LLMs)**
- **python-dotenv**

---

## 📂 Project Structure

```text
.
├── app.py
├── requirements.txt
├── .env.example
├── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/healthcare-symptom-checker.git
cd healthcare-symptom-checker
```

Create and activate a virtual environment (recommended):

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1/chat/completions
LLM_MODEL=poolside/laguna-m.1:free
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser.

---

---

## 🌟 Future Enhancements

- 🧠 More advanced symptom reasoning
- 🎙️ Voice-based symptom reporting
- 📄 Downloadable health summaries (PDF)
- 📊 Symptom history tracking
- 👨‍⚕️ Doctor and hospital recommendations
- 🌐 Multi-language support
- 📱 Mobile-friendly interface

---

⭐ If you found this project helpful, consider giving it a **Star** on GitHub!
