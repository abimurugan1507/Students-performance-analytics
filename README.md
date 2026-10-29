# 🎓 Student Performance Analytics Dashboard

## 📌 Project Overview

# Student Performance Analytics Dashboard

🚀 **[View Live Dashboard](https://students-performance-analytics-gqngskqvmylgjvyekmdame.streamlit.app/)**

An interactive student performance analysis project built using Python, Pandas, and Streamlit.

The **Student Performance Analytics Dashboard** is a data analytics project developed using Python and Streamlit. It analyzes student academic performance, study habits, and other factors to identify patterns that may be associated with students' final grades.

The dashboard presents key performance indicators, interactive charts, correlation analysis, and automatically generated insights in a user-friendly interface.

## 🎯 Project Objectives

- Analyze students' academic performance.
- Compare first, second, and final-period grades.
- Explore the relationship between study time and final grades.
- Examine student absences and performance patterns.
- Visualize important data insights through an interactive dashboard.

## 🛠️ Tools & Technologies

- **Python** – Data analysis and application logic
- **Pandas** – Data cleaning and manipulation
- **Streamlit** – Interactive dashboard development
- **Matplotlib / Seaborn** – Data visualization
- **CSV** – Dataset storage
- **VS Code** – Development environment

## 📊 Dashboard Features

- Key Performance Indicator (KPI) cards
- Grade category distribution
- G1, G2, and G3 grade comparison
- Correlation heatmap
- Study-time analysis
- Absence analysis
- Interactive sidebar filters
- Student data search and table
- CSV download option
- Automatically generated insights

## 🔍 Key Findings

- The average final grade (G3) is approximately **10.42 out of 20**.
- G2 has a strong positive correlation with G3 (approximately **0.905**).
- G1 also shows a strong positive correlation with G3 (approximately **0.801**).
- Study time has a weak positive correlation with G3 (approximately **0.098**).
- Approximately **47.09%** of students scored 10 or below in G3.

*Note: Correlation indicates an association, not necessarily a cause-and-effect relationship.*

## 📁 Project Structure

```text
studentanlyst/
├── app.py
├── analyze_data.py
├── student_data.csv
└── README.md
```

## ⚙️ How to Run the Project

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Install the required libraries

Open the terminal in the project folder and run:

```bash
pip install streamlit pandas matplotlib seaborn
```

### 3. Run the dashboard

```bash
python -m streamlit run app.py
```

### 4. Open the dashboard

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to explore the dashboard.

## 💡 Skills Demonstrated

- Exploratory Data Analysis (EDA)
- Data visualization
- Data interpretation
- Python programming
- Interactive dashboard development
- Basic statistical and correlation analysis

## 🚀 Future Improvements

- Add more advanced statistical analysis.
- Improve dashboard filtering and visualizations.
- Deploy the dashboard online.
- Explore machine learning models to predict student performance.

## 👩‍💻 Author

**Abi Murugan**  
B.Sc. Computer Science Graduate  
Aspiring Data Analyst
