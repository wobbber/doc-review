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

def review_document(content: str, checks: list) -> pd.DataFrame:
    results = []
    chunks = split_into_chunks(content, max_tokens=3000)

    for i, chunk in enumerate(chunks):
        for check in checks:
            prompt = f"Review this chunk of the document against the following check: {check}\n\nChunk {i + 1}:\n{chunk}"
            try:
                # Specify the model: 'gpt-4o' or 'gpt-4o-mini'
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  # Change to 'gpt-4o-mini' if desired
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
