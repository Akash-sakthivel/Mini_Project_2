# Bird Species Observation Analysis in Forest and Grassland Ecosystem

## Project Overview
The Bird Species Observation Analysis project is designed to explore and analyze bird species' diversity, distribution, and habitat preferences in forest and grassland ecosystems. Using Python, PostgreSQL and Streamlit, this project provides insights into how environmental conditions influence bird populations.

### Objectives
- To clean, preprocess, and structure bird species observational data.
- To analyze species distribution, behavioral trends, and environmental impacts.
- To develop an interactive Streamlit dashboard or Power BI visualization for exploration.
- To provide data-driven insights for biodiversity conservation and habitat management.

## Technologies Used
- **Programming Language**: Python
- **Database**: PostgreSQL
- **Web Application Framework**: Streamlit
- **Data Visualization**: Matplotlib, Plotly
- **Data Processing**: Pandas, NumPy

## Setup Instructions

### Prerequisites
- Python 3.0 installed on your machine.
- PostgreSQL database setup for structured data storage (optional for Power BI).
- Jupyter Notebook (optional for data exploration).

### Installation
1. **Install Required Packages**:
   ```bash
   pip install streamlit pandas sqlalchemy matplotlib numpy plotly seaborn 
   ```
2. **Database Configuration**:
   - Create a database in PostgreSQL.
   - Update the database connection details in the `Forest_Birds_Dataset.ipynb` file.
   - Update the database connection details in the `Grassland_Birds_Dataset.ipynb` file.

3. **Run the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```
   
## Project Structure
```
Bird-Species-Analysis/
│── app.py                          # Main Streamlit application
│── Forest_Birds_Dataset.ipynb      # EDA and species analysis script and Database connection settings
│── Grassland_Birds_Dataset.ipynb   # EDA and species analysis script and Database connection settings
└── README.md                       # Project documentation
```

## Dataset Description
The dataset consists of multiple Excel sheets, each representing a different administrative unit with bird species observations.

### Key Columns
- **Location Information**: Admin_Unit_Code, Site_Name, Plot_Name, Location_Type (Forest/Grassland)
- **Time-Based Data**: Year, Date, Start_Time, End_Time, Visit
- **Species Data**: Common_Name, Scientific_Name, Sex, AOU_Code
- **Environmental Conditions**: Temperature, Humidity, Sky, Wind, Disturbance
- **Observation Details**: ID_Method, Distance, Flyover_Observed, Activity Type
- **Conservation Status**: PIF_Watchlist_Status, Regional_Stewardship_Status

### Sheets Overview
Each Excel sheet corresponds to a specific park or conservation area, such as:
- **ANTI** – Antietam National Battlefield
- **CATO** – Catoctin Mountain Park
- **CHOH** – Chesapeake and Ohio Canal National Historical Park

## Data Analysis

### Data Cleaning & Preprocessing
- Handling missing values and standardizing observation formats.
- Consolidating multiple sheets into a structured dataset.
- Filtering out incomplete or inconsistent records.

### Exploratory Data Analysis (EDA)
1. **Temporal Analysis**:
   - Analyze bird activity based on Year, Month, and Season.
   - Identify peak observation periods.

2. **Spatial Analysis**:
   - Compare forest vs. grassland bird diversity.
   - Identify high-density biodiversity locations.

3. **Species Behavior & Habitat Analysis**:
   - Determine the most observed species and their preferred habitat.
   - Analyze activity patterns based on ID_Method and Distance.

4. **Environmental Influence**:
   - Study correlations between Temperature, Humidity, and bird observations.
   - Assess the impact of disturbances (Disturbance column).

### Data Visualization & Dashboard

## Interactive Streamlit Dashboard
- Home Page: Overview of bird species observations.
- Species Distribution: Species distribution across Forest Dataset, Grassland Dataset and compare both.
- Biodiversity Insights: 7 different insights are provided for better understanding of the Data.

## Example Visualizations
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plot-Level Analysis (Observations by Plot_Name)
plot_analysis = forest_df.groupby("Plot_Name")["Common_Name"].nunique().reset_index()
plot_analysis = plot_analysis.sort_values(by="Common_Name", ascending=False).head(10)  # Top 10 plots

# Visualization: Observations per Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=plot_analysis, x="Plot_Name", y="Common_Name", palette="mako")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Plot Name")
plt.ylabel("Unique Species Count")
plt.title("Top 10 Plots with Highest Species Diversity")
plt.show()
```

## User Interface
The Streamlit application features an intuitive user interface with:
- **Bird Species Search**: Find species based on name, habitat, or activity.
- **Seasonal Trends**: View how observations change over time.
- **Interactive Filters**: Sort data by environmental conditions, observer, or location.

### Challenges and Solutions

## Challenges
-  Handling missing and inconsistent data across multiple sheets.
- Ensuring accurate geographic mapping without precise latitude/longitude data.
- Balancing data size for efficient dashboard performance.

## Solutions
- Implemented data imputation techniques for missing values.
- Used administrative unit codes to approximate geographic locations.
- Optimized SQL queries and caching to improve dashboard speed.

## Future Enhancements
- Integrate Machine Learning for species prediction based on environmental factors.
- Add Geospatial Analysis using QGIS or Google Maps API.
- Enhance Power BI Visualizations for deeper insights.

## Conclusion
The **Bird Species Observation Analysis** project provides valuable insights into bird diversity, habitat preferences, and environmental influences. Through data cleaning, analysis, and visualization, this project helps identify conservation priorities and biodiversity trends. The interactive Streamlit dashboard and Power BI visualizations enhance data exploration, making it easier for stakeholders to derive actionable insights. Future enhancements, such as machine learning and geospatial integration, can further improve species predictions and habitat conservation planning.

## References
- [Streamlit Documentation](https://docs.streamlit.io/)
