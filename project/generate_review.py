import streamlit as st
import openai
import pandas as pd

# Load API key from Streamlit secrets
api_key = st.secrets["api"]["OPENAI_API_KEY"]
openai.api_key = api_key

def split_into_chunks(text: str, max_tokens: int = 3000) -> list:
    lines = text.splitlines()
    chunks = []
    current_chunk = []

    for line in lines:
        if sum(len(l) for l in current_chunk) + len(line) > max_tokens:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
        else:
            current_chunk.append(line)
    
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    return chunks

async def review_document(content: str, checks: list) -> pd.DataFrame:
    results = []
    chunks = split_into_chunks(content, max_tokens=3000)

    for i, chunk in enumerate(chunks):
        for check in checks:
            prompt = f"Review this chunk of the document against the following check: {check}\n\nChunk {i + 1}:\n{chunk}"
            try:
                # Use the new `acreate` method
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",  # Use "gpt-4" or "gpt-3.5-turbo" depending on your access
                    messages=[{"role": "user", "content": prompt}]
                )

                ai_response = response["choices"][0]["message"]["content"]
                results.append({
                    "Check": check,
                    "Chunk": i + 1,
                    "Feedback": ai_response,
                    "Action Required": "Yes" if "missing" in ai_response.lower() or "incorrect" in ai_response.lower() else "No",
                })
            
            except Exception as e:
                results.append({
                    "Check": check,
                    "Chunk": i + 1,
                    "Feedback": f"Error: {str(e)}",
                    "Action Required": "Unknown",
                })
    
    return pd.DataFrame(results)

# Streamlit UI for uploading and reviewing documents
st.title("Document Review with GPT-4")
st.write("Upload a document and provide checks for review.")

# File uploader
uploaded_file = st.file_uploader("Upload your document (text file only)", type="txt")

# Input for checks
checks_input = st.text_area("Enter checks (one per line)")

if uploaded_file and checks_input:
    # Process the uploaded file and checks
    document_content = uploaded_file.read().decode("utf-8")
    checks = checks_input.splitlines()

    st.write("Processing the document...")
    results = st.experimental_singleton(review_document(document_content, checks))

    st.write("Review Results:")
    st.dataframe(results)
