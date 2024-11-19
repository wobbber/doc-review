import streamlit as st
from documents import load_documents, load_checks
from generate_review import review_document

st.spinner("Loading pre-defined checks from input PDFs...")
checks = load_checks()
st.success("Checks loaded successfully!")

st.title("AI-Powered CTD Document Review")
st.write("Upload your CTD Document, and let AI review it using the pre-loaded checks.")
uploaded_files = st.file_uploader("Upload Documents (PDF only)", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    st.success("Document successfully uploaded!")

if st.button("Review Document"):
    if uploaded_files:
        st.spinner("Processing your document...")
        combined_content = ""
        for uploaded_file in uploaded_files:
            doc_content = load_documents(uploaded_file) + "\n\n"

        review_results = review_document(content=doc_content, checks=checks)

        st.success("Document review completed!")
        st.dataframe(review_results)

        st.download_button(
            label="Download Review Report",
            data=review_results.to_csv(index=False),
            file_name="document_review_report.csv",
            mime="text/csv"
        )
    
    else:
        st.error("Please upload a document to proceed.")