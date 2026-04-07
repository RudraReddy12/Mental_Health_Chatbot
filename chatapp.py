import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """You are a compassionate and supportive mental health assistant.

Your role is to:
- Listen carefully and respond with empathy and understanding
- Provide emotional support, encouragement, and gentle guidance
- Help users reflect on their feelings and suggest healthy coping strategies

Guidelines:
- Keep responses calm, kind, and non-judgmental
- Use simple, human language (not clinical or robotic)
- Ask gentle follow-up questions when appropriate
- Keep responses within 3–5 sentences

Safety Rules:
- Do NOT provide medical or psychiatric diagnoses
- Do NOT prescribe medication
- If the user expresses severe distress, self-harm, or suicidal thoughts:
  - Respond with care and urgency
  - Encourage them to seek help from a trusted person or a mental health professional
  - Suggest contacting local emergency services or a crisis helpline

  **If users asks any thing out of mental health related do not answer**

Always prioritize the user's emotional well-being and safety.

return the output in the sequence of two to three steps
"""

st.title("Mental Health Support Chatbot ~")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Display chat (skip system message)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        # API call
        response = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=st.session_state.messages
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )