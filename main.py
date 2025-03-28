import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# OpenAI API setup with DeepSeek model
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Function to fetch website content
def fetch_website_content(url):
    """Fetches and returns the website's full text content."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=" ")  # Extracts only text
            return text.strip()
        else:
            return f"Error: Unable to fetch content (Status Code: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

# Function to summarize text using DeepSeek
def summarize_text(text):
    """Summarizes content using DeepSeek AI."""
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You are a professional news summarizer."},
            {"role": "user", "content": f"Summarize this article:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# Function to translate text to Hindi using DeepSeek
def translate_to_hindi(text):
    """Translates text into Hindi using DeepSeek AI."""
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": f"Translate this English text into Hindi:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🌐 AI Website Extractor, Summarizer & Translator")

# Input URL
url = st.text_input("🔗 Enter Website URL:")

if st.button("🚀 Fetch, Summarize & Translate"):
    if url:
        with st.spinner("Fetching content..."):
            content = fetch_website_content(url)

        if content.startswith("Error"):
            st.error(content)
        else:
            st.subheader("📜 Extracted Content")
            st.write(content[:2000])  # Show a preview (limit to 2000 chars)

            with st.spinner("Summarizing content..."):
                summary = summarize_text(content)
            
            st.subheader("📌 Summarized Content")
            st.write(summary)

            with st.spinner("Translating to Hindi..."):
                hindi_translation = translate_to_hindi(summary)
            
            st.subheader("📝 Translated Summary (Hindi)")
            st.write(hindi_translation)
    else:
        st.error("Please enter a valid URL.")
