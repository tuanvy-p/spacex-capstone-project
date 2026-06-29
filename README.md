# SpaceX Falcon 9 Landing Prediction

## Project Overview

This project analyzes SpaceX Falcon 9 launch data to predict whether the first stage will land successfully. The analysis includes data collection, data wrangling, exploratory data analysis, SQL analysis, interactive visual analytics, and predictive modeling.

## Main Objective

The main objective is to build a classification model that predicts the landing outcome of the Falcon 9 first stage based on launch-related features such as payload mass, orbit, launch site, booster version, and flight number.

## Project Components

1. Data Collection using SpaceX API
2. Data Collection using Web Scraping
3. Data Wrangling and Feature Engineering
4. Exploratory Data Analysis with Visualization
5. Exploratory Data Analysis with SQL
6. Interactive Visual Analytics with Folium Map
7. Interactive Dashboard with Plotly Dash
8. Predictive Analysis using Classification Models

## Machine Learning Models

The following classification models were compared:

- Logistic Regression
- Support Vector Machine
- Decision Tree Classifier
- K-Nearest Neighbors

## Key Tools and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Requests
- BeautifulSoup
- SQLite
- Folium
- Plotly Dash
- Scikit-learn

## Repository Structure

```text
spacex-capstone-project/
│
├── notebooks/
│   ├── 1_spacex_api_data_collection.ipynb
│   ├── 2_web_scraping.ipynb
│   ├── 3_data_wrangling.ipynb
│   ├── 4_eda_visualization.ipynb
│   ├── 5_eda_sql.ipynb
│   ├── 6_folium_map.ipynb
│   └── 7_predictive_analysis.ipynb
│
├── dash_app/
│   └── spacex_dash_app.py
│
├── data/
│   └── spacex_cleaned_data.csv
│
├── images/
│   └── visualization_results
│
└── Data Science Capstone Project Report.pdf
