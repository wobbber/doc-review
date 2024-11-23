import streamlit as st
from dotenv import load_dotenv
import time
# import math as m
import pandas as pd
import openai
import google.generativeai as genai

load_dotenv()
# api_key = st.secrets["api"]["GROQ_API_KEY"]
# api_key = os.environ.get('OPENAI_API')
# client = Groq(api_key=api_key)


def split_into_chunks(text: str, max_tokens: int = 30000) -> list:
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


def review_document(
    content: str,
    checks: list,
    prompt_base: str,
    api_key: str,
    llm_agent: str,
    temp: float,
    max_tokens: int,
    model_details: str
) -> pd.DataFrame:
    start_time = time.time()
    results = []
    chunks = split_into_chunks(content, max_tokens=3000)

    if llm_agent == "OpenAI":
        openai.api_key = api_key
    elif llm_agent == "Gemini":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_details)
        generationConfig = {"temperature": temp}
        # generationConfig = {"temperature":temp,"maxOutputTokens":max_tokens}

    else:
        raise Exception("Anubhav Have No Access to any other LLM_Agent")

    checks = ["\n".join(checks)]

    for i, chunk in enumerate(chunks):
        for check in checks:
            prompt = f"{prompt_base} {check}\n\nChunk {i + 1}:\n{chunk}"
            try:
                if llm_agent == "OpenAI":
                    response = openai.ChatCompletion.create(
                        model=model_details,
                        messages=[
                            {"role": "system", "content": "Need to perform Checklist"},
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=max_tokens,
                        temperature=temp,
                    )
                    ai_response = response["choices"][0]["message"]["content"]

                elif llm_agent == "Gemini":
                    response = model.generate_content(
                        prompt, generation_config=generationConfig
                    )
                    ai_response = response.text

                results.append(
                    {
                        "Check": check,
                        "Chunk": i + 1,
                        "Feedback": ai_response,
                        "Action Required": (
                            "Yes"
                            if "missing" in ai_response.lower()
                            or "incorrect" in ai_response.lower()
                            else "No"
                        ),
                    }
                )

            except Exception as e:
                results.append(
                    {
                        "Check": check,
                        "Chunk": i + 1,
                        "Feedback": f"Error: {str(e)}",
                        "Action Required": "Unknown",
                    }
                )
    st.write(f'Time Taken = {round(time.time() - start_time,2)} secs')
    return pd.DataFrame(results)
