# Developed by Abhiram Rangoon [Python Developer | Data Scientist | Data Analyst]
# Enhanced with innovative UI/UX design
import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon='✨',
    layout="wide",
    initial_sidebar_state="expanded"
)
###### Packages Used ######

import base64, random
import time, datetime
import pymysql
import os
import socket
import platform
import geocoder
import secrets
import io
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
import numpy as np
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import nltk
nltk.download('stopwords')

# Custom CSS for enhanced UI
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/styles.css")

###### Preprocessing functions ######

def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()      
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-link">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf" class="pdf-viewer"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.markdown("""
    <style>
        /* Make all h2, h3, h4 subheaders black */
        .css-15zrgzn h2, 
        .css-15zrgzn h3, 
        .css-15zrgzn h4, 
        .css-15zrgzn h5, 
        .css-15zrgzn h6 {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)
    st.markdown("""
    <style>
        h2, h3, h4, h5, h6 {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

    st.subheader("**Courses & Certifications Recommendations 🎓**")


    # Inject custom CSS for styling
    # Inject custom CSS for styling
    st.markdown("""
    <style>
        /* Make all text inside course container black */
        .course-container, 
        .course-container * {
            color: black !important;
            font-weight: 600 !important;
        }

        /* Course cards */
        .course-card {
            background-color: #f8f9fa !important;
            border-radius: 12px !important;
            padding: 15px 20px !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        .course-card:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
        }

        /* Links inside cards */
        .course-card a {
            color: black !important;
            text-decoration: none !important;
        }
        .course-card a:hover {
            color: #5f27cd !important;
        }

        /* Numbering in bold */
        .course-card b {
            margin-right: 10px !important;
            color: black !important;
        }

        /* Selectbox label */
        label[for="course_select"] {
            color: black !important;
            font-weight: 600 !important;
        }

        /* Selected option text in selectbox */
        div[role="combobox"] > div {
            color: black !important;
        }

        /* Dropdown options text */
        div[role="listbox"] div {
            color: black !important;
        }

        /* Placeholder and input text if any */
        input, select, textarea {
            color: black !important;
        }
        ::placeholder {
            color: black !important;
            opacity: 1 !important;
        }
    </style>
""", unsafe_allow_html=True)

    # Course rendering logic
    rec_course = []
#     st.markdown("""
#     <style>
#         /* Label text */
#         label[for="course_select"] {
#             color: black !important;
#             font-weight: 600;
#         }
#         /* Selected option text */
#         div[role="combobox"] > div {
#             color: black !important;
#         }
#         /* Dropdown options text */
#         div[role="listbox"] div {
#             color: black !important;
#         }
#     </style>
# """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        /* Selectbox label text */
        div[data-baseweb="select"] > div > label {
            color: black !important;
            font-weight: 600 !important;
        }
        label[for="course_select"] {
        color: black !important;
        font-weight: 600 !important;
    }
        /* Selected option text */
        div[data-baseweb="select"] > div > div > div {
            color: black !important;
        }

        /* Dropdown options */
        div[role="listbox"] div {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)
    no_of_reco = st.selectbox(
    'Select Number of Recommendations:',
    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    index=4,  # Default is 5
    key='course_select'
)
    random.shuffle(course_list)

    st.markdown("<div class='course-container'>", unsafe_allow_html=True)
    for i, (c_name, c_link) in enumerate(course_list[:no_of_reco], start=1):
        st.markdown(
            f"<div class='course-card'><b>{i}</b><a href='{c_link}' target='_blank'>{c_name}</a></div>",
            unsafe_allow_html=True
        )
        rec_course.append(c_name)
    st.markdown("</div>", unsafe_allow_html=True)

    return rec_course


###### Database Stuffs ######

connection = pymysql.connect(host='localhost', user='root', password='Abhiram1729@', db='cv')
cursor = connection.cursor()

def insert_data(sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country, act_name, act_mail, act_mob, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses, pdf_name):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, str(latlong), city, state, country, act_name, act_mail, act_mob, name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses, pdf_name)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def insertf_data(feed_name, feed_email, feed_score, comments, Timestamp):
    DBf_table_name = 'user_feedback'
    insertfeed_sql = "insert into " + DBf_table_name + """
    values (0,%s,%s,%s,%s,%s)"""
    rec_values = (feed_name, feed_email, feed_score, comments, Timestamp)
    cursor.execute(insertfeed_sql, rec_values)
    connection.commit()

###### Page Configuration ######



###### Custom UI Components ######

def gradient_text(text, color1, color2):
    return f"""
    <style>
    .header-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 1rem;
    }}

    .gradient-text {{
        font-size: clamp(2rem, 5vw, 4rem);
        font-weight: 800;
        background: linear-gradient(90deg, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
        animation: fadeIn 1s ease-in-out;
    }}

    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(-20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    @media (max-width: 768px) {{
        .gradient-text {{
            font-size: clamp(1.5rem, 6vw, 2.5rem);
        }}
    }}
    </style>
    <div class="header-container">
        <div class="gradient-text">{text}</div>
    </div>
    """

def animated_header():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated-header {
        animation: fadeIn 1.5s ease-out;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    <h1 class="animated-header">AI Resume Analyzer Pro</h1>
    """, unsafe_allow_html=True)

def create_card(title, content, icon):
    return f"""
    <style>
    .card {{
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        padding: 2rem;
        margin: 1rem auto;
        max-width: 300px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    .card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }}

    .card-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #764ba2;
    }}

    .card h3 {{
        font-size: 1.5rem;
        margin: 0.5rem 0;
        color: #333;
    }}

    .card p {{
        font-size: 1rem;
        color: #666;
        line-height: 1.5;
    }}

    @media (max-width: 768px) {{
        .card {{
            max-width: 90%;
            padding: 1.5rem;
        }}
    }}
    </style>

    <div class="card">
        <div class="card-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """


###### Main function run() ######

def run():
    # Custom CSS injection
    st.markdown("""
<style>
/* ===== Global App Background ===== */
.stApp {
    background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ===== Sidebar Styling ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}
[data-testid="stSidebar"] .css-1v0mbdj, .sidebar .sidebar-content {
    background: transparent !important;
    color: white !important;
}

/* ===== Button Styling ===== */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 12px 26px;
    font-weight: 600;
    border-radius: 30px;
    border: none;
    transition: 0.3s ease;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
}

/* ===== Input Fields ===== */
.stTextInput > div > div > input,
.stTextArea > div > textarea {
    border-radius: 12px;
    padding: 10px 14px;
    background: #ffffffee;
    box-shadow: inset 0 0 6px rgba(0,0,0,0.05);
    border: 1px solid #ddd;
}

/* ===== Cards ===== */
.card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: center;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.15);
}
.card-icon {
    font-size: 3rem;
    color: #667eea;
    margin-bottom: 1rem;
}

/* ===== Course Cards ===== */
.course-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    transition: 0.3s ease;
}
.course-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* ===== Download Link ===== */
.download-link {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white !important;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: bold;
    text-decoration: none;
    transition: background 0.3s ease;
}
.download-link:hover {
    background: linear-gradient(135deg, #5a6fe0, #6840a0);
    color: white;
}

/* ===== Progress Bar ===== */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #667eea, #764ba2);
}

/* ===== PDF Viewer ===== */
.pdf-viewer {
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

/* ===== Alerts ===== */
.stAlert {
    border-radius: 10px;
    background: #e3f2fd;
    color: #0d47a1;
    padding: 1rem;
}

/* ===== Custom Tabs & Misc ===== */
.st-b7 {
    background-color: transparent !important;
}
.st-at {
    background-color: #667eea !important;
}

/* ===== Mobile Responsive Cards ===== */
@media (max-width: 768px) {
    .card {
        padding: 20px;
    }
    .card h3 {
        font-size: 1.25rem;
    }
}
</style>
""", unsafe_allow_html=True)


    # App Header
    st.markdown(gradient_text("AI Resume Analyzer Pro", "#667eea", "#764ba2"), unsafe_allow_html=True)
    st.markdown("""
<div class="subtitle-container">
    <p class="subtitle-text">
        Your intelligent resume analysis tool powered by <strong>AI</strong>
    </p>
</div>

<style>
.subtitle-container {
    text-align: center;
    margin-top: -30px;
    margin-bottom: 40px;
}

.subtitle-text {
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: #444;
    background: linear-gradient(90deg, #764ba2, #667eea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
    letter-spacing: 0.3px;
    animation: fadeInUp 1s ease-out;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(15px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)


    # Sidebar Title and Footer with Enhanced Styling
    st.sidebar.markdown("""
<style>
/* Sidebar Background */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    padding-top: 2rem;
    font-family: 'Segoe UI', Tahoma, sans-serif;
}

/* Menu Title */
.sidebar-title {
    text-align: center;
    margin-bottom: 30px;
    animation: fadeIn 1.2s ease-in-out;
}

.sidebar-title h2 {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    margin: 0;
}

/* Footer Styling */
.sidebar-footer {
    text-align: center;
    margin-top: 60px;
    font-size: 0.9rem;
    animation: fadeInUp 1.2s ease-in-out;
}

.sidebar-footer h4 {
    font-weight: bold;
    font-size: 1.1rem;
    margin-bottom: 0;
    background: linear-gradient(to right, #ff5f6d, #ffc371);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-footer p {
    color: #cfcfcf;
    margin: 4px 0;
}

/* Animations */
@keyframes fadeIn {
    0% {opacity: 0; transform: translateY(-10px);}
    100% {opacity: 1; transform: translateY(0);}
}

@keyframes fadeInUp {
    0% {opacity: 0; transform: translateY(20px);}
    100% {opacity: 1; transform: translateY(0);}
}

/* Divider line */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    margin: 1.5rem 0;
}
</style>

<!-- Title Block -->
<div class="sidebar-title">
    <h2>🧭 Navigator</h2>
</div>
""", unsafe_allow_html=True)

# Menu Options
    activities = ["User", "Feedback", "About", "Admin"]
    choice = st.sidebar.selectbox("", activities, key='nav_select')

# Divider
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Footer Block
    st.sidebar.markdown("""
<div class="sidebar-footer">
    <p>Designed & developed by</p>
    <h4>Abhiram Rangoon</h4>
    <p>Python Developer | Data Scientist | UI/UX Designing | AI/ML Engineer </p>
</div>
""", unsafe_allow_html=True)


    ###### Creating Database and Table ######

    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
    cursor.execute(db_sql)

    # Create table user_data and user_feedback
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                    sec_token varchar(20) NOT NULL,
                    ip_add varchar(50) NULL,
                    host_name varchar(50) NULL,
                    dev_user varchar(50) NULL,
                    os_name_ver varchar(50) NULL,
                    latlong varchar(50) NULL,
                    city varchar(50) NULL,
                    state varchar(50) NULL,
                    country varchar(50) NULL,
                    act_name varchar(50) NOT NULL,
                    act_mail varchar(50) NOT NULL,
                    act_mob varchar(20) NOT NULL,
                    Name varchar(500) NOT NULL,
                    Email_ID VARCHAR(500) NOT NULL,
                    resume_score VARCHAR(8) NOT NULL,
                    Timestamp VARCHAR(50) NOT NULL,
                    Page_no VARCHAR(5) NOT NULL,
                    Predicted_Field BLOB NOT NULL,
                    User_level BLOB NOT NULL,
                    Actual_skills BLOB NOT NULL,
                    Recommended_skills BLOB NOT NULL,
                    Recommended_courses BLOB NOT NULL,
                    pdf_name varchar(50) NOT NULL,
                    PRIMARY KEY (ID)
                    );
                """
    cursor.execute(table_sql)

    DBf_table_name = 'user_feedback'
    tablef_sql = "CREATE TABLE IF NOT EXISTS " + DBf_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                        feed_name varchar(50) NOT NULL,
                        feed_email VARCHAR(50) NOT NULL,
                        feed_score VARCHAR(5) NOT NULL,
                        comments VARCHAR(100) NULL,
                        Timestamp VARCHAR(50) NOT NULL,
                        PRIMARY KEY (ID)
                    );
                """
    cursor.execute(tablef_sql)

    ###### CODE FOR CLIENT SIDE (USER) ######

    if choice == 'User':
        with st.container():
            st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 40px 30px;
        border-radius: 20px;
        color: #fff;
        box-shadow: 0 12px 30px rgba(0, 242, 254, 0.4);
        max-width: 800px;
        margin: 0 auto 40px auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .hero-section:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.6);
    }
    .hero-section h2 {
        font-size: 2.8rem;
        margin-bottom: 15px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-shadow: 0 3px 8px rgba(0,0,0,0.2);
    }
    .hero-section p {
        font-size: 1.25rem;
        line-height: 1.5;
        max-width: 600px;
        margin: 0 auto;
        color: #e0f7fa;
        text-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    /* Responsive */
    @media (max-width: 600px) {
        .hero-section h2 {
            font-size: 2rem;
        }
        .hero-section p {
            font-size: 1rem;
        }
    }
</style>

<div class="hero-section">
    <h2>Resume Analysis Portal</h2>
    <p>Upload your resume and receive intelligent recommendations to boost your career prospects.</p>
</div>
""", unsafe_allow_html=True)

            # How It Works
            st.markdown("""
            <div class="section">
                <h2 class="section-title">How It Works</h2>
                <div class="steps-container">
                    <div class="step-card">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h3>Upload Your Resume</h3>
                            <p>Simply upload your resume in PDF format. Our system supports all standard resume formats.</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h3>AI Analysis</h3>
                            <p>Our advanced algorithms parse your resume to extract key information and patterns.</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h3>Get Insights</h3>
                            <p>Receive detailed feedback on your resume's strengths and areas for improvement.</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">4</div>
                        <div class="step-content">
                            <h3>Career Boost</h3>
                            <p>Get personalized recommendations to enhance your skills and job prospects.</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">5</div>
                        <div class="step-content">
                            <h3>Resume Quality Analysis</h3>
                            <p>Get personalized recommendations to enhance your skills and job prospects.</p>
                        </div>
                    </div>
                    <div class="step-card">
                        <div class="step-number">6</div>
                        <div class="step-content">
                            <h3>Bonus Resources</h3>
                            <p>Get personalized recommendations to enhance your skills and job prospects.</p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

             # User Information Form
            with st.expander("Personal Information (Optional)", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    act_name = st.text_input("Full Name", placeholder="Enter you Name....", key='name')
                with col2:
                    act_mail = st.text_input("Email", placeholder="Enter your Email....", key='email')
                with col3:
                    act_mob = st.text_input("Phone", placeholder="Mobile No...", key='phone')
                # Collecting User Information
            st.markdown("""
            <style>
                .side-form {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 15px;
                }
                .form-label {
                    min-width: 80px;
                    font-weight: 600;
                    color: #2d3748;
                }
                .form-input {
                    flex-grow: 1;
                }
            </style>
            """, unsafe_allow_html=True)

            # Create your 3 main columns
            # col1, col2, col3 = st.columns(3)

            # with col1:
            #     st.markdown('<div class="side-form"><div class="form-label">Full Name*</div><div class="form-input">', unsafe_allow_html=True)
            #     act_name = st.text_input('', placeholder='Enter your full name', key='name')
            #     st.markdown('</div></div>', unsafe_allow_html=True)

            # with col2:
            #     st.markdown('<div class="side-form"><div class="form-label">Email*</div><div class="form-input">', unsafe_allow_html=True)
            #     act_mail = st.text_input('', placeholder='Enter your email', key='email')
            #     st.markdown('</div></div>', unsafe_allow_html=True)

            # with col3:
            #     st.markdown('<div class="side-form"><div class="form-label">Phone*</div><div class="form-input">', unsafe_allow_html=True)
            #     act_mob = st.text_input('', placeholder='Enter your phone', key='phone')
            #     st.markdown('</div></div>', unsafe_allow_html=True)

            # Collecting Miscellaneous Information
            sec_token = secrets.token_urlsafe(12)
            host_name = socket.gethostname()
            ip_add = socket.gethostbyname(host_name)
            dev_user = os.getlogin()
            os_name_ver = platform.system() + " " + platform.release()
            try:
                g = geocoder.ip('me')
                latlong = g.latlng
                geolocator = Nominatim(user_agent="http", timeout=10)  # Increased timeout
                location = geolocator.reverse(latlong, language='en', exactly_one=True)
                address = location.raw['address'] if location else {}
            except Exception as e:
                st.warning(f"Could not fetch location details: {str(e)}")
                address = {}
            cityy = address.get('city', 'Unknown')
            statee = address.get('state', 'Unknown')
            countryy = address.get('country', 'Unknown')  
            city = cityy
            state = statee
            country = countryy

            # Upload Resume Section
            st.markdown('''<h3 style="color: #2d3436; margin-top: 20px;">Upload Your Resume</h3>''', unsafe_allow_html=True)
            st.markdown('<p style="color: #636e72;">Supported format: PDF</p>', unsafe_allow_html=True)
            
            pdf_file = st.file_uploader("", type=["pdf"], key='resume_uploader')
            
            if pdf_file is not None:
                with st.spinner('Analyzing your resume...'):
                    time.sleep(2)
                    progress_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(percent_complete + 1)
                    progress_bar.empty()

                # Save uploaded file
                upload_dir = os.path.join(os.path.dirname(__file__), "Uploaded_Resumes")
                os.makedirs(upload_dir, exist_ok=True)
                save_image_path = os.path.join(upload_dir, pdf_file.name)
                pdf_name = pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                # Show PDF preview
                st.markdown('''<h3 style="color: #2d3436;">Resume Preview</h3>''', unsafe_allow_html=True)
                show_pdf(save_image_path)

                # Parse resume data
                resume_data = ResumeParser(save_image_path).get_extracted_data()
                if resume_data:
                    resume_text = pdf_reader(save_image_path)

                    # Resume Analysis Results
                    st.markdown("""
                    <div class="dashboard-section">
                        <h2 class="section-title">Resume Analysis Dashboard</h2>
                        <div class="dashboard-grid">
                    """, unsafe_allow_html=True)

                    # Basic Info Card
                    with st.expander("📌 Basic Information", expanded=True):
                        col1, col2 = st.columns(2)
                        try:
                            with col1:
                                st.markdown(f"**Name:** {resume_data['name']}")
                                st.markdown(f"**Email:** {resume_data['email']}")
                            with col2:
                                st.markdown(f"**Contact:** {resume_data['mobile_number']}")
                                st.markdown(f"**Degree:** {str(resume_data['degree'])}")
                            st.markdown(f"**Resume Pages:** {str(resume_data['no_of_pages'])}")
                        except:
                            pass

                    # Experience Level Prediction
                    cand_level = ''
                    if resume_data['no_of_pages'] < 1:                
                        cand_level = "NA"
                        st.markdown("""
                        <div class="analysis-card warning">
                            <h3>Experience Level: Fresher</h3>
                            <p>Your resume appears to be very brief. Consider adding more details about your education, projects, or any relevant experience.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif 'INTERNSHIP' in resume_text or 'INTERNSHIPS' in resume_text or 'Internship' in resume_text or 'Internships' in resume_text:
                        cand_level = "Intermediate"
                        st.markdown("""
                        <div class="analysis-card success">
                            <h3>Experience Level: Intermediate</h3>
                            <p>Your internship experience is valuable. Highlight specific projects and achievements during your internships.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif 'EXPERIENCE' in resume_text or 'WORK EXPERIENCE' in resume_text or 'Experience' in resume_text or 'Work Experience' in resume_text:
                        cand_level = "Experienced"
                        st.markdown("""
                        <div class="analysis-card primary">
                            <h3>Experience Level: Experienced</h3>
                            <p>Your professional experience is impressive. Quantify your achievements with metrics where possible.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        cand_level = "Fresher"
                        st.markdown("""
                        <div class="analysis-card warning">
                            <h3>Experience Level: Fresher</h3>
                            <p>Consider adding projects, coursework, or extracurricular activities to strengthen your resume.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Skills Analysis and Recommendation
                    st.markdown("""
    <div style="color: #111111; font-weight: 600; font-size: 1.7rem; margin-bottom: 6px;">
        Your Current Skills:
    </div>
""", unsafe_allow_html=True)

                    keywords = st_tags(
                        label='',  # Hides the default label
                        text='See recommendations below',
                        value=resume_data['skills'],
                        key='skills_tag'
                    )

                    # Skills Recommendation Engine
                    ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                    web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress','javascript', 'angular js', 'C#', 'Asp.net', 'flask']
                    android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                    ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                    uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
                    n_any = ['english','communication','writing', 'microsoft office', 'leadership','customer management', 'social media']

                    recommended_skills = []
                    reco_field = ''
                    rec_course = ''

                    for i in resume_data['skills']:
                        # Data Science Recommendation
                        if i.lower() in ds_keyword:
                            reco_field = 'Data Science'
                            st.markdown("""
                            <div class="analysis-card success">
                                <h3>Career Path Suggestion: Data Science</h3>
                                <p>Based on your skills, you might excel in Data Science roles. Here are some skills to enhance:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("🎯 Our analysis suggests you're looking for Data Science roles.")
                            recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                            recommended_keywords = st_tags(label='### Recommended Skills:',
                                                        text='Based on your current skills',
                                                        value=recommended_skills,
                                                        key='ds_skills')
                            # st.markdown('''<div class="card">
                            #                 <p>Adding these skills will boost your resume for Data Science positions.</p>
                            #             </div>''', unsafe_allow_html=True)
                            rec_course = course_recommender(ds_course)
                            break

                        # Web Development Recommendation
                        elif i.lower() in web_keyword:
                            reco_field = 'Web Development'
                            st.markdown("""
                            <div class="analysis-card success">
                                <h3>Career Path Suggestion: Web Development</h3>
                                <p>Based on your skills, you might excel in Web Development roles. Here are some skills to enhance:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("🎯 Our analysis suggests you're looking for Web Development roles.")
                            recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                            recommended_keywords = st_tags(label='### Recommended Skills:',
                                                        text='Based on your current skills',
                                                        value=recommended_skills,
                                                        key='web_skills')
                            # st.markdown('''<div class="card">
                            #                 <p>Adding these skills will boost your resume for Web Development positions.</p>
                            #             </div>''', unsafe_allow_html=True)
                            rec_course = course_recommender(web_course)
                            break

                        # Android Development Recommendation
                        elif i.lower() in android_keyword:
                            reco_field = 'Android Development'
                            st.markdown("""
                            <div class="analysis-card success">
                                <h3>Career Path Suggestion: Android Development</h3>
                                <p>Based on your skills, you might excel in Android Development roles. Here are some skills to enhance:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("🎯 Our analysis suggests you're looking for Android Development roles.")
                            recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                            recommended_keywords = st_tags(label='### Recommended Skills:',
                                                        text='Based on your current skills',
                                                        value=recommended_skills,
                                                        key='android_skills')
                            # st.markdown('''<div class="card">
                            #                 <p>Adding these skills will boost your resume for Android Development positions.</p>
                            #             </div>''', unsafe_allow_html=True)
                            rec_course = course_recommender(android_course)
                            break

                        # iOS Development Recommendation
                        elif i.lower() in ios_keyword:
                            reco_field = 'IOS Development'
                            st.markdown("""
                            <div class="analysis-card success">
                                <h3>Career Path Suggestion: iOS Development</h3>
                                <p>Based on your skills, you might excel in iOS Development roles. Here are some skills to enhance:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("🎯 Our analysis suggests you're looking for iOS Development roles.")
                            recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                            recommended_keywords = st_tags(label='### Recommended Skills:',
                                                        text='Based on your current skills',
                                                        value=recommended_skills,
                                                        key='ios_skills')
                            # st.markdown('''<div class="card">
                            #                 <p>Adding these skills will boost your resume for iOS Development positions.</p>
                            #             </div>''', unsafe_allow_html=True)
                            rec_course = course_recommender(ios_course)
                            break

                        # UI/UX Recommendation
                        elif i.lower() in uiux_keyword:
                            reco_field = 'UI-UX Development'
                            st.markdown("""
                            <div class="analysis-card success">
                                <h3>Career Path Suggestion: UI/UX Design</h3>
                                <p>Based on your skills, you might excel in UI/UX Design roles. Here are some skills to enhance:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("🎯 Our analysis suggests you're looking for UI/UX Design roles.")
                            recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                            recommended_keywords = st_tags(label='### Recommended Skills:',
                                                        text='Based on your current skills',
                                                        value=recommended_skills,
                                                        key='uiux_skills')
                            # st.markdown('''<div class="card">
                            #                 <p>Adding these skills will boost your resume for UI/UX Design positions.</p>
                            #             </div>''', unsafe_allow_html=True)
                            rec_course = course_recommender(uiux_course)
                            break

                        # No Specific Field
                        elif i.lower() in n_any:
                            reco_field = 'NA'
                            st.markdown("""
                            <div class="analysis-card warning">
                                <h3>Career Path Suggestion: General</h3>
                                <p>Currently we specialize in Data Science, Web, Mobile, and UI/UX Development. Your skills seem more general.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.warning("⚠️ Currently we specialize in Data Science, Web, Mobile, and UI/UX Development")
                            recommended_skills = ['No specific recommendations']
                            recommended_keywords = st_tags(label='### Recommended Skills:',
                                                        text='Currently no specific recommendations',
                                                        value=recommended_skills,
                                                        key='na_skills')
                            rec_course = "Sorry! Not Available for this Field"
                            break

                    # Resume Quality Analysis
                    st.markdown("""
                    <div class="quality-section">
                        <h2 class="section-title">Resume Quality Analysis</h2>
                        <div class="quality-grid">
                    """, unsafe_allow_html=True)

                    resume_score = 0
                    analysis_results = []

                    # Resume Sections Analysis
                    def check_section(section, keywords, points, message_positive, message_negative):
                        nonlocal resume_score
                        if any(keyword in resume_text for keyword in keywords):
                            resume_score += points
                            analysis_results.append(f"✅ {message_positive}")
                        else:
                            analysis_results.append(f"❌ {message_negative}")

                    check_section("Objective", ["Objective", "Summary"], 6,
                                "You have a clear Objective/Summary section",
                                "Consider adding an Objective/Summary to communicate your career goals")

                    check_section("Education", ["Education", "School", "College"], 12,
                                "Your Education section is well-presented",
                                "Your resume would benefit from adding Education details")

                    check_section("Experience", ["EXPERIENCE", "Experience", "WORK EXPERIENCE", "Work Experience"], 16,
                                "Your Experience section is comprehensive",
                                "Adding professional Experience would strengthen your resume")

                    check_section("Internships", ["INTERNSHIPS", "INTERNSHIP", "Internships", "Internship"], 6,
                                "Your Internship experience is valuable",
                                "Internship experience can help you stand out")

                    check_section("Skills", ["SKILLS", "SKILL", "Skills", "Skill"], 7,
                                "Your Skills section is well-organized",
                                "A dedicated Skills section helps recruiters quickly assess your abilities")

                    check_section("Hobbies", ["HOBBIES", "Hobbies"], 4,
                                "Your Hobbies add personality to your resume",
                                "Hobbies can show your personality and cultural fit")

                    check_section("Interests", ["INTERESTS", "Interests"], 5,
                                "Your Interests provide additional context",
                                "Interests can show your passion beyond work")

                    check_section("Achievements", ["ACHIEVEMENTS", "Achievements"], 13,
                                "Your Achievements demonstrate your capabilities",
                                "Achievements can differentiate you from other candidates")

                    check_section("Certifications", ["CERTIFICATIONS", "Certifications", "Certification"], 12,
                                "Your Certifications show specialized knowledge",
                                "Certifications can validate your skills")

                    check_section("Projects", ["PROJECTS", "PROJECT", "Projects", "Project"], 19,
                                "Your Projects showcase practical experience",
                                "Projects demonstrate your ability to apply knowledge")

                    # Display analysis results
                    with st.expander("🔍 Detailed Resume Analysis", expanded=True):
                        for result in analysis_results:
                            st.markdown(result)

                    # Resume Score Visualization
                    st.markdown(f"""
                    <div class="score-section">
                        <h2 class="section-title">Resume Score</h2>
                        <div class="score-container">
                            <div class="score-card">
                                <div class="score-circle">
                                    <div class="score-value">{resume_score}</div>
                                    <div class="score-label">out of 100</div>
                                </div>
                                <div class="score-description">
                    """, unsafe_allow_html=True)

                    # Score Progress Bar
                    my_bar = st.progress(0)
                    for percent_complete in range(resume_score):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1)

                    # Score Interpretation
                    if resume_score >= 80:
                        st.markdown("""
                        <div style="color: black;">
                            <h3>🌟 Excellent!</h3>
                            <p>Your resume is well-structured and comprehensive. It effectively showcases your qualifications and experience.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    elif resume_score >= 60:
                        st.markdown("""
                        <div style="color: black;">
                            <h3>👍 Good!</h3>
                            <p>Your resume has most key sections but could be improved with more details and better organization.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    elif resume_score >= 40:
                        st.markdown("""
                        <div style="color: black;">
                            <div style="font-size: 1.5rem; font-weight: bold;">🤔 Fair</div>
                            <p>Consider adding more sections and details to strengthen your resume and better highlight your qualifications.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.markdown("""
                        <div style="color: black;">
                            <h3>📝 Needs Work</h3>
                            <p>Your resume is missing several important sections. Focus on adding more content and structure.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    
                    st.markdown("""
                                </div>
                            </div>
                            <div class="score-info">
                💡 Note: This score evaluates the completeness of your resume content, not the quality of your experience.
            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Store data in database
                    ts = time.time()
                    cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    timestamp = str(cur_date+'_'+cur_time)

                    insert_data(str(sec_token), str(ip_add), (host_name), (dev_user), (os_name_ver), (latlong), (city), (state), (country), (act_name), (act_mail), (act_mob), resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course), pdf_name)

                    # Bonus Resources
                    with st.container():
                        st.markdown("""
                            <style>
                                .bonus-card {
                                    background-color: #ffffff;
                                    padding: 10px;
                                    border-radius: 15px;
                                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                                    margin-top: 2rem;
                                    margin-bottom: 2rem;
                                }

                                .bonus-header {
                                    text-align: center;
                                    font-size: 1.8rem;
                                    font-weight: 700;
                                    color: #3b3b3b;
                                    margin-bottom: 5px;
                                }

                                .video-title {
                                    font-size: 1.1rem;
                                    font-weight: 600;
                                    color: #374785;
                                    margin-bottom: 10px;
                                    text-align: center;
                                }
                            </style>
                            <div class="bonus-card">
                                <div class="bonus-header">🎁 Bonus Resources</div>
                            </div>
                        """, unsafe_allow_html=True)

                        # Create a new container inside the card visually
                        card_container = st.container()

                        with card_container:
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown('<div class="video-title">🖊️ Resume Writing Tips</div>', unsafe_allow_html=True)
                                resume_vid = random.choice(resume_videos)
                                st.video(resume_vid)

                            with col2:
                                st.markdown('<div class="video-title">💼 Interview Preparation Tips</div>', unsafe_allow_html=True)
                                interview_vid = random.choice(interview_videos)
                                st.video(interview_vid)

                        # st.snow()





                else:
                    st.error("Sorry, we couldn't process your resume. Please try with a different PDF file.")

    ###### CODE FOR FEEDBACK SIDE ######
    elif choice == 'Feedback':
        st.markdown("""
        <div class="hero-section" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="hero-content">
                <h1>We Value Your Feedback</h1>
                <p class="hero-subtitle">Help us improve by sharing your experience</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
    <style>
        /* Headings and labels */
        h3, h4, h5, label, .stTextInput label, .stTextArea label, .stSlider label, p {
            color: #000000 !important;
        }

        /* Placeholder text */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #000000 !important;
            opacity: 0.6 !important;
        }

        /* Actual input text color */
        .stTextInput input,
        .stTextArea textarea {
            color: #000000 !important;
        }

        /* Slider label color */
        .stSlider > div > div > div > div {
            color: #000000 !important;
        }

        /* Optional: background cleanup */
        .stTextInput,
        .stTextArea {
            background-color: transparent !important;
        }
    </style>
""", unsafe_allow_html=True)
        # Feedback Form
        with st.form("feedback_form", clear_on_submit=True):
            st.markdown("### Share Your Experience")
            
            col1, col2 = st.columns(2)
            with col1:
                feed_name = st.text_input("Name*", placeholder="Your name")
            with col2:
                feed_email = st.text_input("Email*", placeholder="Your email")
            st.markdown("""
    <style>
        /* Remove Streamlit default blue background */
        .main {
            background-color: #f8f9fa; /* Light neutral background */
        }

        /* Optional: Remove sidebar background */
        .css-1d391kg, .css-1vq4p4l {
            background-color: #ffffff !important;
        }

        /* Optional: Override primary color if it looks blue */
        :root {
            --primary-color: #4a4a4a;  /* Dark grey */
            --background-color: #f8f9fa;
            --secondary-background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)
            feed_score = st.radio(
    "How would you rate your experience?",
    [1, 2, 3, 4, 5],
    format_func=lambda x: {
        1: "😞 Terrible",
        2: "😕 Not Great",
        3: "😐 Average",
        4: "😊 Good",
        5: "😍 Excellent"
    }[x],
    horizontal=True
)
            comments = st.text_area("Comments/Suggestions", placeholder="Your feedback helps us improve...")
            
            ts = time.time()
            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            timestamp = str(cur_date+'_'+cur_time)
            
            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                if feed_name and feed_email:
                    insertf_data(feed_name, feed_email, feed_score, comments, timestamp)
                    st.success("🎉 Thank you for your feedback!")
                    st.balloons()
                else:
                    st.warning("Please fill in all required fields (Name and Email)")

        # Feedback Analytics
        st.markdown("---")
        st.markdown("### Feedback Analytics")
        
        try:
            # Fetch feedback data
            query = 'select * from user_feedback'        
            plotfeed_data = pd.read_sql(query, connection)

            if not plotfeed_data.empty:
                # Ratings Distribution
                st.subheader("User Ratings Distribution")
                fig = px.pie(plotfeed_data, names=plotfeed_data.feed_score.unique(), 
                            values=plotfeed_data.feed_score.value_counts(),
                            title="Distribution of User Ratings",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig, use_container_width=True)

                # Recent Comments
                st.subheader("Recent Feedback Comments")
                cursor.execute('select feed_name, comments from user_feedback order by Timestamp desc limit 5')
                recent_comments = cursor.fetchall()
                for i, (name, comment) in enumerate(recent_comments, 1):
                    st.markdown(f"""
                    <div class="card" style="margin-bottom: 10px;">
                        <p><b>{i}. {name}:</b> {comment}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No feedback data available yet.")
        except:
            st.info("No feedback data available yet.")

    ###### CODE FOR ABOUT PAGE ######
    elif choice == 'About':
        st.markdown("""
        <div style="background: #000000; 
                    padding: 20px; border-radius: 15px; color: white; margin-bottom: 30px;">
            <h2 style="color: white; text-align: center;">About AI Resume Analyzer Pro</h2>
            <p style="text-align: center; color: #cccccc;">Your intelligent resume analysis companion</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            <div style="background: #111111; padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
                <h3 style="color: #667eea;">What is AI Resume Analyzer?</h3>
                <p style="color: #cccccc;">An intelligent tool that parses information from your resume using natural language processing, 
                identifies key skills, clusters them into relevant sectors, and provides personalized recommendations 
                to improve your resume and job prospects.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: #111111; padding: 20px; border-radius: 15px; color: white;">
                <h3 style="color: #667eea;">How It Works</h3>
                <ol style="color: #cccccc;">
                    <li>Upload your resume in PDF format</li>
                    <li>Our AI analyzes the content and structure</li>
                    <li>Get instant feedback on your resume's strengths</li>
                    <li>Receive personalized improvement recommendations</li>
                    <li>Access curated learning resources</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #111111; padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
                <h3 style="color: #667eea;">Key Features</h3>
                <ul style="color: #cccccc;">
                    <li>🔍 Detailed resume analysis and scoring</li>
                    <li>🎯 Personalized career field prediction</li>
                    <li>💡 Skill gap analysis and recommendations</li>
                    <li>📚 Curated course and certification suggestions</li>
                    <li>📊 Interactive visual feedback</li>
                    <li>🔒 Secure and private processing</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: #111111; padding: 20px; border-radius: 15px; color: white;">
                <h3 style="color: #667eea;">Technologies Used</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">Python</span>
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">Streamlit</span>
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">NLP</span>
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">PyResParser</span>
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">Plotly</span>
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">MySQL</span>
                    <span style="background: #333333; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; color: white;">PDF Miner</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <h3 style="color: white;">About the Developer</h3>
            <div style="display: inline-block; text-align: left; max-width: 600px;">
                <div style="background: #111111; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); color: white;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="flex: 1;">
                            <h4 style="margin-bottom: 5px; color: #667eea;">Abhiram Rangoon</h4>
                            <p style="color: #cccccc; margin-top: 0;">Python Developer | Data Scientist | Data Analyst</p>
                        </div>
                    </div>
                    <p style="color: #cccccc;">With expertise in data science and software development, I created this tool to help job seekers optimize their resumes and stand out in today's competitive market.</p>
                    <div style="margin-top: 15px;">
                        <a href="https://www.linkedin.com/in/abhiramrangoon" target="_blank" style="margin-right: 10px; text-decoration: none; color: #0077b5;">LinkedIn</a>
                        <a href="https://github.com/abhiramrangoon" target="_blank" style="margin-right: 10px; text-decoration: none; color: #38a169;">GitHub</a>
                        <a href="mailto:abhiram@example.com" style="text-decoration: none; color: #d44638;">Email</a>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    ###### CODE FOR ADMIN SIDE (ADMIN) ######
    else:
        st.markdown("""
<style>
    /* Make the entire app background black */
    .reportview-container, 
    .main, 
    .block-container {
        background-color: #000000 !important;
        color: white !important;
    }

    /* Cards background and text */
    .card {
        background-color: #121212 !important;
        color: white !important;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
    }

    /* Override dataframes and tables */
    .stDataFrame, .stDataFrame > div, .stDataFrame > div > div {
        background-color: #121212 !important;
        color: white !important;
    }

    /* Override Plotly charts container background */
    .js-plotly-plot .plotly {
        background-color: #000000 !important;
    }

    /* Style scrollbars for dark background (optional) */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #121212;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #555;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

        # Admin Login
        with st.container():
            st.markdown("""
<style>
    .admin-login-label {
        color: #2d3748 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 5px !important;
    }
    .admin-login-input {
        margin-bottom: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# Admin login form with visible labels
            col1, col2 = st.columns(2)
            st.markdown("""
<style>
    .admin-login-label {
        color: black !important;
        font-weight: 600;
        margin-bottom: 5px;
        font-size: 16px;
    }
    /* Also make sure the input text is black */
    div.stTextInput > div > input {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)
            with col1:
                st.markdown('<div class="admin-login-label">Username</div>', unsafe_allow_html=True)
                ad_user = st.text_input(
                    "",  # Empty label since we're using our custom label above
                    placeholder="Enter admin username",
                    key="admin_user"
                )

            with col2:
                st.markdown('<div class="admin-login-label">Password</div>', unsafe_allow_html=True)
                ad_password = st.text_input(
                    "",  # Empty label since we're using our custom label above
                    placeholder="Enter admin password",
                    type="password",
                    key="admin_pass"
                )

            # Login button (centered below the inputs)
            _, center_col, _ = st.columns([1, 2, 1])
            with center_col:
                if st.button("Login", key="admin_login"):
                    if ad_user == "abhi" and ad_password == "abhi123":
                        st.session_state.admin_logged_in = True
                        st.success("Login successful!")
                        st.experimental_rerun()
                    else:
                        st.error("Invalid credentials")

                        if st.button("Login", key="admin_login"):
                            if ad_user == 'abhi' and ad_password == 'abhi123':
                                st.session_state.admin_logged_in = True
                                st.success("Login successful!")
                            else:
                                st.error("Invalid credentials")

        if st.session_state.get('admin_logged_in', False):
            # Fetch user data
            cursor.execute('''SELECT ID, ip_add, resume_score, convert(Predicted_Field using utf8), 
                            convert(User_level using utf8), city, state, country from user_data''')
            datanalys = cursor.fetchall()
            plot_data = pd.DataFrame(datanalys, columns=['Idt', 'IP_add', 'resume_score', 
                                                       'Predicted_Field', 'User_Level', 
                                                       'City', 'State', 'Country'])

            # Admin Dashboard Overview
            st.markdown("### Dashboard Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>Total Users</h3>
                    <h2 style="color: #667eea;">{plot_data.Idt.count()}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                avg_score = plot_data.resume_score.astype(float).mean()
                st.markdown(f"""
                <div class="card">
                    <h3>Average Resume Score</h3>
                    <h2 style="color: #667eea;">{avg_score:.1f}/100</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                common_field = plot_data.Predicted_Field.mode()[0]
                st.markdown(f"""
                <div class="card">
                    <h3>Most Common Field</h3>
                    <h2 style="color: #667eea;">{common_field}</h2>
                </div>
                """, unsafe_allow_html=True)

            # User Data Section
            st.markdown("### User Data")
            cursor.execute('''SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob, 
                            convert(Predicted_Field using utf8), Timestamp, Name, Email_ID, 
                            resume_score, Page_no, pdf_name, convert(User_level using utf8), 
                            convert(Actual_skills using utf8), convert(Recommended_skills using utf8), 
                            convert(Recommended_courses using utf8), city, state, country, 
                            latlong, os_name_ver, host_name, dev_user from user_data''')
            data = cursor.fetchall()
            
            df = pd.DataFrame(data, columns=['ID', 'Token', 'IP Address', 'Name', 'Mail', 'Mobile', 
                                           'Predicted Field', 'Timestamp', 'Predicted Name', 
                                           'Predicted Mail', 'Resume Score', 'Total Page', 'File Name', 
                                           'User Level', 'Actual Skills', 'Recommended Skills', 
                                           'Recommended Course', 'City', 'State', 'Country', 
                                           'Lat Long', 'Server OS', 'Server Name', 'Server User'])
            
            st.dataframe(df, height=500)
            st.markdown(get_csv_download_link(df, 'User_Data.csv', 'Download Full Report'), 
                        unsafe_allow_html=True)

            # Analytics Section
            st.markdown("### Analytics")
            
            # Field Distribution
            st.subheader("Field Distribution")
            field_counts = plot_data.Predicted_Field.value_counts()
            fig1 = px.pie(field_counts, values=field_counts.values, 
                         names=field_counts.index, 
                         title='Career Field Distribution',
                         color_discrete_sequence=px.colors.sequential.Aggrnyl)
            st.plotly_chart(fig1, use_container_width=True)

            # Experience Level Distribution
            st.subheader("Experience Level Distribution")
            level_counts = plot_data.User_Level.value_counts()
            fig2 = px.bar(level_counts, x=level_counts.index, y=level_counts.values,
                         title='User Experience Levels',
                         color=level_counts.values,
                         color_continuous_scale='Aggrnyl')
            st.plotly_chart(fig2, use_container_width=True)

            # Resume Score Distribution
            st.subheader("Resume Score Distribution")
            fig3 = px.histogram(plot_data, x='resume_score', nbins=20,
                               title='Distribution of Resume Scores',
                               color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig3, use_container_width=True)

            # Geographical Distribution
            st.subheader("Geographical Distribution")
            if not plot_data[['Country', 'State', 'City']].empty:
                country_counts = plot_data.Country.value_counts().reset_index()
                country_counts.columns = ['Country', 'Count']
                fig4 = px.choropleth(country_counts, locations='Country',
                                    locationmode='country names', color='Count',
                                    title='User Distribution by Country',
                                    color_continuous_scale='Aggrnyl')
                st.plotly_chart(fig4, use_container_width=True)

            # Feedback Data
            st.markdown("### User Feedback")
            cursor.execute('''SELECT * from user_feedback''')
            feedback_data = cursor.fetchall()
            
            if feedback_data:
                feedback_df = pd.DataFrame(feedback_data, columns=['ID', 'Name', 'Email', 
                                                                 'Feedback Score', 'Comments', 
                                                                 'Timestamp'])
                st.dataframe(feedback_df)
                
                # Feedback Analysis
                st.subheader("Feedback Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Feedback Ratings")
                    fig5 = px.pie(feedback_df, names=feedback_df['Feedback Score'].astype(str), 
                                 values=feedback_df['Feedback Score'].value_counts(),
                                 title='Feedback Score Distribution',
                                 color_discrete_sequence=px.colors.sequential.Aggrnyl)
                    st.plotly_chart(fig5, use_container_width=True)
                
                with col2:
                    st.markdown("#### Recent Comments")
                    recent_feedback = feedback_df.sort_values('Timestamp', ascending=False).head(5)
                    for _, row in recent_feedback.iterrows():
                        st.markdown(f"""
                        <div class="card" style="margin-bottom: 10px; padding: 10px;">
                            <p><b>{row['Name']} ({row['Feedback Score']}/5):</b> {row['Comments']}</p>
                            <small>{row['Timestamp']}</small>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No feedback data available yet.")

            if st.button("Logout", key="admin_logout"):
                st.session_state.admin_logged_in = False
                st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    run()