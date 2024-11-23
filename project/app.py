import streamlit as st
from documents import load_documents
from generate_review import review_document
import os


def update_checks():
    if checks_string == "":
        st.info(f"{0} Check Detected")
        return

    number_of_lines = checks_string.count("\n")
    st.info(f"{number_of_lines + 1} Check Detected")


checks_string = st.text_area(
    "Enter Checks Line By Line", value="This is a sample default value"
)
update_checks()

checks = checks_string.splitlines()

prompt_base = st.text_area(
    "Enter Prompt for facilitating Checks",
    "Review this chunk of the document against the following check: ",
)

llm_agent = st.selectbox(
    "Your LLM Client: ",
    ("OpenAI", "Gemini", "Claude"),
)

api_key = st.text_input("Enter API Key (Leave Blank For Default)")

if api_key == "":
    if llm_agent == "OpenAI":
        # api_key = os.environ.get("OPENAI_API")
        api_key = st.secrets["api"]["OPENAI_API"]
        model_details = st.selectbox(
            "Your LLM Model: ",
            ("gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"),
        )

    elif llm_agent == "Gemini":
        # api_key = os.environ.get("GEMINI_API")
        api_key = st.secrets["api"]["GEMINI_API"]
        model_details = st.selectbox(
            "Your LLM Model: ",
            ("gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"),
        )

temp = st.slider("Temperature For Model", min_value=0.1, max_value=1.5, step=0.1)
max_tokens = st.slider("Max Tokens", min_value=100, max_value=500, step=10)

st.title("AI-Powered CTD Document Review")
st.write("Upload your CTD Document, and let AI review it using the pre-loaded checks.")
uploaded_files = st.file_uploader(
    "Upload Documents (PDF only)", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    st.success("Document successfully uploaded!")

if st.button("Review Document"):
    if uploaded_files:
        st.spinner("Processing your document...")
        combined_content = ""
        for uploaded_file in uploaded_files:
            doc_content = load_documents(uploaded_file) + "\n\n"

        review_results = review_document(
            content=doc_content,
            checks=checks,
            prompt_base=prompt_base,
            api_key=api_key,
            llm_agent=llm_agent,
            temp=temp,
            max_tokens=max_tokens,
            model_details=model_details
        )

        st.success("Document review completed!")
        st.dataframe(review_results)

        st.download_button(
            label="Download Review Report",
            data=review_results.to_csv(index=False),
            file_name="document_review_report.csv",
            mime="text/csv",
        )

    else:
        st.error("Please upload a document to proceed.")
