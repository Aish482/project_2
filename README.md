# Traffic Violations Insight System

## Project Overview
This project builds a complete data analytics system for traffic violations data, including data cleaning, exploratory data analysis (EDA), and an interactive Streamlit dashboard.

## Skills Covered
- Python Programming
- SQL (SQLite)
- Data Cleaning and Pre-processing
- Streamlit
- Visualization (Matplotlib/Seaborn/Plotly)

## Domain
Transportation

## Objectives
1. **Data Cleaning & Preprocessing**: Clean and standardize the raw dataset.
2. **Exploratory Data Analysis (EDA)**: Analyze patterns and insights.
3. **Streamlit Visualization Dashboard**: Interactive dashboard for exploration.

## Setup Instructions
1. Create and activate a virtual environment:  
   `python -m venv .venv`  
   `.venv\Scripts\Activate.ps1` (PowerShell) or `.venv\Scripts\activate` (cmd)
2. Install dependencies: `pip install -r requirements.txt`
3. Run data cleaning: `python data_cleaning.py` (This may take time due to large dataset)
4. (Optional) Run EDA: `python eda.py`
5. Launch dashboard: `streamlit run app.py`

## Files
- `app.py`: Streamlit dashboard.
- `data_cleaning.py`: Cleans and loads data into SQLite database.
- `eda.py`: Performs EDA and generates plots.
- `requirements.txt`: Python dependencies.
- `pyproject.toml`: Project configuration and tool settings.
- `traffic_violations.db`: SQLite database (created after cleaning).
- `.gitignore`: Excludes large/generated files from Git.

## Business Use Cases
- Improve road safety
- Identify hotspots
- Allocate patrol vehicles
- Detect repeat offenders
- Inform policy decisions

## Recommendations
- For production, consider using a more robust database like PostgreSQL.
- Optimize queries for better performance on large datasets.
- Add more advanced ML models for prediction if needed.