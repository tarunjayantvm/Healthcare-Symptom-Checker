import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "poolside/laguna-m.1:free")


def get_llm_response(user_prompt: str, temperature: float = 0.7) -> str:
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY is not configured. Please add it to your .env file."

    payload = {
        "model": LLM_MODEL,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a healthcare symptom assistant. Answer using clear, general guidance, "
                    "identify likely conditions from the user input, and recommend whether they should "
                    "seek medical attention. Do not provide a diagnosis, and always include a disclaimer "
                    "that you are not a doctor."
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    }

    try:
        response = requests.post(LLM_BASE_URL, json=payload, headers=headers, timeout=25)
        response.raise_for_status()
        data = response.json()
        message = data.get("choices", [{}])[0].get("message", {}).get("content")
        return message or "No answer received from the language model."
    except requests.exceptions.RequestException as exc:
        return f"Error calling LLM: {exc}"


def infer_conditions(symptoms: list[str], duration: str, severity: str, history: list[str]) -> str:
    if not symptoms:
        return "No symptoms selected."

    suggestions = []
    symptom_text = ", ".join(symptoms)

    if any(term in symptoms for term in ["Chest pain", "Shortness of breath", "Dizziness"]):
        suggestions.append("cardiac or respiratory concerns, especially if the pain is new or severe")
    if any(term in symptoms for term in ["Fever", "Cough", "Sore throat"]):
        suggestions.append("respiratory infection such as a cold, flu, or bronchitis")
    if any(term in symptoms for term in ["Headache", "Nausea", "Light sensitivity"]):
        suggestions.append("a migraine or tension-related headache")
    if any(term in symptoms for term in ["Abdominal pain", "Nausea", "Diarrhea"]):
        suggestions.append("digestive upset, gastritis, or food-related irritation")
    if any(term in symptoms for term in ["Fatigue", "Weight change", "Cold intolerance"]):
        suggestions.append("a metabolic or thyroid-related issue")
    if any(term in symptoms for term in ["Joint pain", "Muscle ache"]):
        suggestions.append("a musculoskeletal strain or inflammation")

    if not suggestions:
        suggestions.append("general health and wellness issues that may benefit from rest, hydration, and evaluation")

    recommendation = "If your symptoms are worsening, persistent, or new, please seek medical attention promptly. "
    if severity in ["High", "Severe"] or duration in ["More than 7 days", "Sudden onset"]:
        recommendation = "Because your symptoms are serious or long-lasting, seek medical attention as soon as possible. "

    if "Heart disease" in history or "Diabetes" in history or "Asthma" in history:
        recommendation += "Your medical history suggests you should check with a healthcare provider sooner rather than later. "

    return (
        f"Based on the symptoms ({symptom_text}), possible areas to explore include: "
        f"{'; '.join(dict.fromkeys(suggestions))}. {recommendation}"
    )


def build_prompt(symptoms: list[str], duration: str, severity: str, history: list[str], extra: str) -> str:
    return (
        "A user has reported the following symptoms and medical history:\n"
        f"Symptoms: {', '.join(symptoms) if symptoms else 'None'}\n"
        f"Duration: {duration}\n"
        f"Severity: {severity}\n"
        f"Medical history: {', '.join(history) if history else 'None'}\n"
        f"Additional details: {extra or 'None'}\n\n"
        "Please provide: 1) likely conditions or health areas to consider, 2) whether the person should seek medical attention, "
        "and 3) general wellness advice. Use supportive language and include a disclaimer that this is not medical advice."
    )


def main() -> None:
    st.set_page_config(page_title="Healthcare Symptom Checker", page_icon="🩺", layout="wide")
    st.title("Healthcare Symptom Checker")
    st.write(
        "Use this tool to describe symptoms and medical history. It can suggest possible conditions and "
        "recommend whether to seek medical care, but it does not replace a healthcare professional."
    )

    with st.expander("How to use this app"):
        st.write(
            "1. Select symptoms and describe your condition honestly.\n"
            "2. Review the possible conditions and recommendation.\n"
            "3. Use the chat section for general health questions.\n"
            "4. Always seek medical care if symptoms are severe or concerning."
        )

    with st.form(key="symptom_form"):
        col1, col2 = st.columns(2)
        with col1:
            age_group = st.selectbox("Age group", ["Under 18", "18-35", "36-55", "56-75", "Over 75"])
            gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Non-binary", "Other"])
            symptoms = st.multiselect(
                "Symptoms",
                [
                    "Fever",
                    "Cough",
                    "Shortness of breath",
                    "Chest pain",
                    "Headache",
                    "Nausea",
                    "Abdominal pain",
                    "Fatigue",
                    "Dizziness",
                    "Sore throat",
                    "Joint pain",
                    "Muscle ache",
                    "Anxiety",
                ],
            )
            duration = st.selectbox(
                "How long have you had symptoms?",
                ["Less than 24 hours", "1-3 days", "4-7 days", "More than 7 days", "Sudden onset"],
            )
            severity = st.selectbox("Severity", ["Mild", "Moderate", "High", "Severe"])

        with col2:
            history = st.multiselect(
                "Medical history or chronic conditions",
                [
                    "Heart disease",
                    "Diabetes",
                    "High blood pressure",
                    "Asthma",
                    "Allergies",
                    "Previous surgery",
                    "None of the above",
                ],
            )
            lifestyle = st.multiselect(
                "Lifestyle factors",
                [
                    "Smoker",
                    "Regular exercise",
                    "High stress",
                    "Poor sleep",
                    "Balanced diet",
                    "Frequent travel",
                ],
            )
            extra_details = st.text_area(
                "Additional details (optional)",
                help="Add anything else that may be relevant, such as when symptoms started or what makes them better/worse.",
                height=140,
            )

        submit = st.form_submit_button("Analyze symptoms")

    if submit:
        st.subheader("Symptom assessment")
        local_summary = infer_conditions(symptoms, duration, severity, history)
        st.info(local_summary)

        if symptoms:
            prompt = build_prompt(symptoms, duration, severity, history, extra_details)
            with st.spinner("Contacting the medical assistant model..."):
                llm_answer = get_llm_response(prompt)
            st.write("### AI-assisted guidance")
            st.write(llm_answer)
        else:
            st.warning("Please select at least one symptom to receive an AI-assisted guidance summary.")

    st.markdown("---")
    st.header("General health & wellness chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form(key="chat_form"):
        question = st.text_area("Ask a health-related question", height=120)
        chat_submit = st.form_submit_button("Send question")

    if chat_submit and question.strip():
        prompt = (
            "A user is asking a general health or wellness question. Answer politely with general guidance, "
            "avoid medical diagnoses, and remind the user to consult a healthcare provider if needed.\n\n"
            f"Question: {question.strip()}"
        )
        with st.spinner("Generating response..."):
            answer = get_llm_response(prompt)
        st.session_state.chat_history.append((question.strip(), answer))

    for user_text, assistant_text in st.session_state.chat_history:
        st.chat_message("user", avatar="👤").write(user_text)
        st.chat_message("assistant", avatar="🩺").write(assistant_text)

    st.markdown(
        "<small>Disclaimer: This app provides general informational guidance only. It is not a substitute "
        "for professional medical advice, diagnosis, or treatment.</small>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
