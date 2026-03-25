# answer_generator.py
import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_answer(question, context_docs, chat_history=[]):

    # Build context text + collect sources
    context_text = ""
    sources = []

    for doc in context_docs:
        context_text += doc["text"] + "\n\n"
        if doc["source"] not in sources:
            sources.append(doc["source"])

    system_prompt = f"""You are Dobby, a helpful and loyal AI study assistant.
Answer questions based on the context below. Be friendly and clear.
If the answer is not in the context, say "Dobby does not know this, Master."

Context from documents:
{context_text}"""

    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content, sources