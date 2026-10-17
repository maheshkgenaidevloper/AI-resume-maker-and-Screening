# AI-resume-maker-and-Screening
# 🤖 AI Resume Maker & Smart Resume Screening System

<p align="center">
  <strong>A Python-powered application to create professional resumes and screen candidates against job descriptions.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Domain-AI%20%7C%20NLP-purple" alt="AI and NLP"/>
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Project status"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License"/>
</p>

## 📌 Project Overview

The **AI Resume Maker & Smart Resume Screening System** is a Python-based web application designed to simplify resume creation and candidate screening.

The application allows users to generate downloadable PDF resumes, upload candidate resumes, extract relevant skills, compare resumes against job descriptions, calculate matching scores, rank candidates, and export screening reports.

It combines Python, Streamlit, text processing, skill extraction, and similarity scoring in a single interactive application.

## 🎯 Project Objectives

- Create professional resumes in PDF format.
- Extract readable text from PDF and DOCX resumes.
- Identify relevant skills in resumes and job descriptions.
- Calculate resume-to-job-description matching scores.
- Rank candidates based on configurable matching criteria.
- Identify matched and missing skills.
- Export screening results to CSV for further analysis.

## ✨ Key Features

### 📝 1. AI Resume Maker
- Enter personal and professional information.
- Add professional summary, skills, education, experience, and projects.
- Generate and download a resume in PDF format.
- Organize information into clearly structured sections.

### 🔍 2. Smart Resume Screening
- Upload multiple resumes in PDF or DOCX format.
- Extract text from supported document types.
- Detect predefined technical and professional skills.
- Compare resumes against a job description.
- Calculate a candidate matching score.
- Display matched and missing skills.

### 📊 3. Recruiter Dashboard
- View the number of screened candidates.
- Display average and highest matching scores.
- Rank candidates by matching score.
- Visualize candidate scores in a bar chart.
- Export screening results to a CSV file.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Regular Expressions | Text processing and skill detection |
| Python Collections and Math | Word-frequency similarity calculation |
| PyPDF | Extract text from PDF resumes |
| python-docx | Read DOCX resumes |
| ReportLab | Generate downloadable PDF resumes |
| CSV | Export screening reports |

**Note:** The current lightweight version uses Python's standard library for similarity scoring. It does not require Scikit-learn, SciPy, Pandas, an LLM API, or paid services to run the core features.

## 📂 Project Structure

```text
AI-Resume-Maker-and-Screening/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── sample_resumes/
    └── README.md
```

The `sample_resumes/` folder is optional. Avoid committing real resumes or personal information.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 or a compatible Python version.
- Visual Studio Code or another Python editor.
- Git for version control.
- A modern web browser.

### Step 1: Clone the repository

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/AI-Resume-Maker-and-Screening.git
```

Navigate into the project folder:

```bash
cd AI-Resume-Maker-and-Screening
```

If you have not uploaded the project yet, create the folder locally and open it in VS Code instead.

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, usually:

```text
http://localhost:8501
```

## 📦 Requirements

Create `requirements.txt` with the following contents:

```text
streamlit
pypdf
python-docx
reportlab
```

The application uses Python's built-in modules for CSV processing, regular expressions, mathematical calculations, and word-frequency counting.

## 🚀 How to Use

### Resume Maker

1. Open the **Resume Maker** tab.
2. Enter your name and email address.
3. Add your professional summary, skills, work experience, education, and projects.
4. Click **Generate Resume PDF**.
5. Download your resume.

### Resume Screening

1. Open the **Resume Screening** tab.
2. Paste the target job description.
3. Upload one or more candidate resumes in PDF or DOCX format.
4. Click **Screen Candidates**.
5. Review the matching scores, matched skills, and missing skills.
6. Download the screening report in CSV format.

### Recruiter Dashboard

1. Open the **Screening Results** tab.
2. Review candidate counts and matching-score statistics.
3. Compare candidates using the ranking table and bar chart.

## 🧠 Resume Matching Methodology

The application combines text similarity and skill coverage into a configurable score.

**Formula:**

```text
Final Score = (0.60 × Text Similarity)
            + (0.40 × Skill Coverage)
```

Both inputs are expressed as percentages.

- **Text similarity:** Word-frequency cosine similarity between the resume and job description.
- **Skill coverage:** Percentage of recognized job-description skills also detected in the resume.

For example, if text similarity is 70% and skill coverage is 80%:

```text
Final Score = (0.60 × 70) + (0.40 × 80)
            = 74%
```

The resulting score is a preliminary matching indicator, not a validated probability of hiring success.

## ⚠️ Limitations

- Skill detection relies on a predefined skills list.
- Word-frequency similarity does not understand the full semantic meaning of text.
- Scanned PDFs may require OCR before their contents can be extracted.
- Formatting and layout options are limited in the initial resume generator.
- The current version does not use a generative AI model to write resume content.
- A high matching score does not guarantee candidate suitability.

Use the application as a decision-support tool. Recruiters should review resumes manually and avoid automatic rejection based solely on the score.

## 🛠️ Troubleshooting

### 1. Streamlit command not found

Run:

```bash
python -m pip install streamlit
python -m streamlit run app.py
```

### 2. ModuleNotFoundError

Activate the project's virtual environment and install the requirements:

```powershell
venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 3. Application Control policy blocks a DLL

If an earlier version of the project produces an error involving `_moduleTNC`, SciPy, or Scikit-learn, check that your `app.py` no longer imports `sklearn` or `scipy` when using the lightweight implementation described here.

If Windows continues blocking a DLL, ask your system administrator to review the Application Control policy. Do not disable security protections to work around the issue.

### 4. No text extracted from a PDF

The uploaded PDF may be scanned or image-based. Use a text-based PDF or add an OCR component to support scanned documents.

### 5. Screening results are empty

Confirm that the job description is not empty, that the resume contains extractable text, and that the uploaded file is a supported PDF or DOCX document.

## 🔮 Future Enhancements

- Integrate an LLM API for AI-generated resume summaries and achievement statements.
- Add semantic embeddings for improved resume matching.
- Introduce a database to store candidate and job information.
- Add customizable resume templates.
- Implement OCR for scanned resumes.
- Add job-specific skill configuration and explainable screening results.
- Develop recruiter authentication and job-management features.
- Deploy the application using Streamlit Community Cloud or another hosting platform.

## 🔐 Privacy and Security

- Do not upload confidential resumes or personal information to a public repository.
- Avoid storing uploaded resumes unless necessary and explicitly disclosed.
- Obtain appropriate permission before processing candidate information.
- Keep API keys and secrets out of source code.
- Add authentication and access controls before deploying the application for real recruitment use.

## 💼 Portfolio Value

This project demonstrates practical experience with:

- Python application development.
- Streamlit web application development.
- Text extraction and preprocessing.
- NLP-inspired skill matching.
- Similarity scoring and ranking.
- PDF generation and CSV reporting.
- Debugging, dependency management, and GitHub project organization.

## 📄 License

This project is distributed under the MIT License. If you intend to use that license, add a `LICENSE` file containing the standard MIT License text and your copyright information.

---

⭐ If you find this project useful, consider starring the repository and sharing suggestions for improvements.
