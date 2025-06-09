# 🌴 AI RESUME ANALYZER PRO USING AI AND NLP 🌴  
*A Tool for Resume Analysis, Predictions and Recommendations*

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen) 
![Language](https://img.shields.io/badge/Python-3.9.12-yellow) 
![Code Size](https://img.shields.io/github/repo-size/deepakpadhi986/AI-Resume-Analyzer)

---

💖 **Built by** [Abhiram Rangoon](https://github.com/abhiram-1729)    

🚀 *This project was undertaken as a demonstration of my skills, knowledge, and potential in the field of Computer Science*

## 📌 Scope

i. ✅ Can be used to extract all resume data into a **structured tabular format** and export as **CSV**, enabling organizations to use the data for **analytics**.

ii. 🧠 Provides **recommendations**, **predictions**, and an **overall score** to help users **improve their resumes** and iteratively test them on the tool.

iii. 📈 Can help **increase traffic** to the tool through an engaging **user section** and feedback loop.

iv. 🎓 Useful for **colleges and universities** to gain insights into student resumes **before placements**.

v. 📊 Enables **analytics** to track the **roles most commonly targeted** by users.

vi. 🔁 Supports continuous **tool improvement** based on **user feedback**.


## 🍻 Tech Stack

- **Frontend:**  Streamlit / React.js / HTML-CSS (optional based on implementation)
- **Backend:**  Python (Flask / FastAPI), NLP Libraries (spaCy, NLTK), Transformers
- **Database:**  MySQL
- **Modules:**  Resume Parsing, Keyword Extraction, Recommendation Engine, Admin Dashboard, Analytics, Feedback System

---

## 🤦‍♂️ Features

### 👤 Client:

- Fetching **location** and miscellaneous data
- Using **parsing techniques** to extract:
  - Basic Info
  - Skills
  - Keywords
- Using **logical algorithms** to recommend:
  - Skills that can be added
  - Predicted job role
  - Courses and certificates
  - Resume tips and ideas
  - Overall resume score
  - Interview & resume tip videos

---

### 🛠️ Admin:

- View all applicant data in a **tabular format**
- **Download** user data as a **CSV file**
- Access and manage uploaded resumes in the **Uploaded Resume** folder
- View user **feedback and ratings**
- Visualize data using **Pie Charts** for:
  - Ratings
  - Predicted fields / roles
  - Experience levels
  - Resume scores
  - User count
  - City / State / Country distribution

---

## 💬 Feedback System

- Simple **form filling**
- **Rating** can be given in the form of emoji
- Displays an **overall ratings pie chart**
- Shows **comment history** from past users

## 😅 Requirements

Make sure you have the following installed to ensure a smooth setup:

- 🐍 **Python (v3.9.12)**  
  [Download Python 3.9.12](https://www.python.org/downloads/release/python-3912/)

- 🛢️ **MySQL**  
  [Download MySQL](https://www.mysql.com/downloads/)

- 🖊️ **Visual Studio Code** (Preferred Code Editor)  
  [Download VS Code](https://code.visualstudio.com/Download)

- 🛠️ **Visual Studio Build Tools for C++** (Required for some dependencies)  
  [Download Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)

## 👀 Setup & Installation

To run this project, follow the steps below: 😨

---


```bash
git clone https://github.com/deepakpadhi986/AI-Resume-Analyzer.git

---

### 🧪 2. Create and Activate Virtual Environment (Recommended)
Open terminal or command prompt, navigate to the project folder:

cd AI-Resume-Analyzer
python -m venv venvapp
venvapp\Scripts\activate

---

### 📦 3. Install Required Packages
cd App
pip install -r requirements.txt
python -m spacy download en_core_web_sm

---

### 🗃️ 4. Set Up Database
Create a MySQL database named cv.
Update your credentials in:
AI-Resume-Analyzer/App/App.py
At line 95, replace with your MySQL user credentials:
connection = pymysql.connect(host='localhost', user='abhi', password='abhi123', db='cv')

---

### 🔁 5. Replace File in Dependency
venvapp/Lib/site-packages/pyresparser
Replace the existing resume_parser.py with the custom resume_parser.py provided inside the pyresparser folder of the project.

---

### 🎉 6. Run the App
Make sure your virtual environment is activated and you're inside the App directory.
streamlit run App.py

---
