# AI-Powered CTD Document Review

This project enables automated review of CTD (Common Technical Document) PDFs using AI. It checks uploaded documents against predefined criteria and generates actionable feedback.

---

## Features

- **Automated PDF Text Extraction**: Extracts content from uploaded PDFs for analysis.
- **Predefined Checklists**: Loads checks from `checklist.pdf` and `ctd questions.pdf`.
- **Chunk-Based AI Review**: Splits document content into manageable chunks for efficient AI processing.
- **Actionable Feedback**: Highlights areas requiring correction based on predefined checks.
- **Streamlit Interface**: Intuitive UI for document uploads and review results.
- **Downloadable Reports**: Generates a CSV file of the review results.

---

## Requirements

To run this project, ensure the following dependencies are installed (as specified in `requirements.txt`):

- `streamlit`
- `pymupdf`
- `pandas`
- `groq`
- `python-dotenv`

---

## Setup Instructions

- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

- Add your GROQ API Key:
  Create a `.env` file in the root directory.
  Add the following line:
  ```
  GROQ_API_KEY=your_groq_api_key
  ```

- Ensure the pre-defined checklists(`checklist.pdf` and `ctd questions.pdf` or any named file) are in the root directory.

---

## Running the Application

- Launch the application with Streamlit:
  ```
  streamlit run .\project\app.py
  ```

- Open the link provided by Streamlit in your browser to access the app.

---

## Usage Instructions

- Upload Documents:
  - Upload one or more PDF files for review.

- Run the Review:
  - Click the Review Document button to start the analysis.

- View Results:
  - The app will display the review results in a table format.

- Download Report:
  - Download the review report as a CSV file using the Download Review Report button.

---

## Project Structure

- `app.py`: Streamlit app that provides the user interface.
- `documents.py`: Contains functions for PDF text extraction and loading predefined checks.
- `generate_review.py`: Handles document review logic using the GROQ API.
- `requirements.txt`: Lists project dependencies.

---

## Notes

- Ensure your `.env` file contains a valid GROQ_API_KEY for accessing the GROQ API.
- Place `checklist.pdf` and `ctd questions.pdf` or any named file in the root directory before running the application.
- The app processes only `.pdf` files.