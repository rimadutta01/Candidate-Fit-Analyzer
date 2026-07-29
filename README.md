# Candidate Fit Analyzer

An AI-powered resume screening and candidate-job matching application built with **Streamlit** and **Azure OpenAI**. The system analyses resumes, compares them with job descriptions, computes candidate-job similarity, and provides detailed insights to assist recruiters in making informed hiring decisions.

---

## Features

- Upload resumes in PDF format
- Extract resume text automatically
- AI-powered resume analysis using Azure OpenAI
- Match resumes against job descriptions
- Generate similarity scores
- Identify candidate strengths and weaknesses
- Display missing skills
- Interactive Streamlit interface

---

## Tech Stack

- Python
- Streamlit
- Azure OpenAI
- LangChain
- PDFPlumber
- Scikit-learn
- Pandas
- NumPy

---

## Project Structure

```
JOB_MATCHING/
│
├── .streamlit/
│   └── config.toml
│
├── prompts/
│   └── analysis_prompt.py
│
├── utils/
│   ├── azure_llm.py
│   ├── embedding_matcher.py
│   └── resume_parser.py
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/rimadutta01/Candidate-Fit-Analyzer.git
```

Navigate into the project

```bash
cd Candidate-Fit-Analyzer
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
AZURE_OPENAI_API_KEY=YOUR_API_KEY

AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com/

AZURE_OPENAI_DEPLOYMENT=gpt-4o

AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Future Enhancements

- Multiple resume comparison
- Resume ranking
- Dashboard analytics
- Candidate recommendations
- ATS score prediction
- Interview question generation

---

## Author

**Rima Dutta**

M.Sc. Data Science

CHRIST (Deemed to be University)

---

## License

This project is developed for educational and research purposes.