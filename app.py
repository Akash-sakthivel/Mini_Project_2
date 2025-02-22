import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


# Database connection
DATABASE_URI = "postgresql+psycopg2://postgres:190701@localhost:5432/Birds_Observations"
engine = create_engine(DATABASE_URI)

# Helper function to execute SQL queries
def execute_query(query, params=None):
    with engine.connect() as connection:
        return pd.read_sql(query, connection, params=params)

# Cache data loading for optimization
@st.cache_data
def load_data(dataset):
    query = f"SELECT * FROM {dataset.lower()}"
    return pd.read_sql(query, engine)

# UI Configuration
st.set_page_config(page_title="Bird Observation Dashboard", layout="wide")

# Main Page Title
st.title("🐦 Bird Species Observation Analysis")

# Sidebar Selection
st.sidebar.title("Filters")
dataset_choice = st.sidebar.radio("Choose Dataset", ["Forest", "Grassland", "Compare Both"])


if dataset_choice == "Compare Both":
    df_forest = load_data("Forest")
    df_grassland = load_data("Grassland")
    
    # Merge datasets for comparison
    df_forest["Ecosystem"] = "Forest"
    df_grassland["Ecosystem"] = "Grassland"
    df_combined = pd.concat([df_forest, df_grassland])

     # Histogram of Most Observed Bird Species
    st.subheader("Most Observed Bird Species")
    fig = px.histogram(df_combined, x="Common_Name", title="Most Observed Bird Species",
                       category_orders={"Common_Name": df_combined["Common_Name"].value_counts().index[:20]})
    st.plotly_chart(fig, use_container_width=True)

     # Temporal Heatmap
    st.subheader("Year-wise and Month-wise Observations")
    df_combined["Year"] = pd.to_datetime(df_combined["Date"]).dt.year
    df_combined["Month"] = pd.to_datetime(df_combined["Date"]).dt.month
    heatmap_data = df_combined.groupby(["Year", "Month"]).size().reset_index(name="Observations")
    fig_heatmap = px.density_heatmap(heatmap_data, x="Month", y="Year", z="Observations", title="Temporal Heatmap of Observations", color_continuous_scale="Viridis")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Environmental Factor Influence
    st.subheader("Environmental Factors vs Bird Activity")
    fig_env = px.scatter(df_combined, x="Temperature", y="Humidity", color="Common_Name", size_max=10, title="Influence of Temperature & Humidity on Bird Activity")
    st.plotly_chart(fig_env, use_container_width=True)
    
    # High-Activity Regions and Seasons
    st.subheader("High-Activity Regions and Seasons")
    activity_data = df_combined.groupby(["Location_Type", "Month"]).size().reset_index(name="Activity Count")
    fig_activity = px.bar(activity_data, x="Month", y="Activity Count", color="Location_Type", title="Seasonal Bird Activity by Region")
    st.plotly_chart(fig_activity, use_container_width=True)
    
    # Comparison Plots
    st.subheader("Comparison of Observations Between Forest and Grassland")
    fig_compare = px.histogram(df_combined, x="Ecosystem", y="Common_Name", histfunc="count", title="Bird Observations in Different Ecosystems", color="Ecosystem")
    st.plotly_chart(fig_compare, use_container_width=True)
    
    fig_temp = px.box(df_combined, x="Ecosystem", y="Temperature", title="Temperature Variation Between Ecosystems", color="Ecosystem")
    st.plotly_chart(fig_temp, use_container_width=True)
    
    fig_species = px.bar(df_combined.groupby(["Ecosystem", "Common_Name"]).size().reset_index(name="Count"), x="Ecosystem", y="Count", color="Common_Name", title="Species Distribution Across Ecosystems")
    st.plotly_chart(fig_species, use_container_width=True)
    
else:
    df = load_data(dataset_choice)
    
    # Filters
    selected_species = st.sidebar.multiselect("Select Bird Species", df["Common_Name"].unique())

    # Dropdown for Insights Selection
    st.sidebar.title("Choose Insights")
    insight_choice = st.sidebar.selectbox("Select Bird Species Insights", [
        "Temporal Analysis", "Spatial Analysis", "Species Analysis", "Environmental Conditions", 
        "Distance and Behavior", "Observer Trends", "Conservation Insights"
    ])

    
    # Apply Filters
    if selected_species:
        df = df[df["Common_Name"].isin(selected_species)]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Observations", len(df))
    col2.metric("Unique Species", df["Common_Name"].nunique())
    col3.metric("Avg Temperature", f"{df['Temperature'].mean():.2f}°C")
    col4.metric("Unique Locations", df["Plot_Name"].nunique())
    
    # Time-Series Plot
    st.subheader("Bird Sightings Over Time")
    time_series = df.groupby("Date")["Common_Name"].count().reset_index()
    fig = px.line(time_series, x="Date", y="Common_Name", title="Observations Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Observations by Site
    st.subheader("Observations Per Site")
    site_counts = df["Plot_Name"].value_counts().reset_index()
    site_counts.columns = ["Site Name", "Observations"]
    fig2 = px.bar(site_counts, x="Site Name", y="Observations", title="Observations Per Site", color="Observations")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Bird Diversity Pie Chart
    st.subheader("Bird Species Diversity")
    species_counts = df["Common_Name"].value_counts().reset_index()
    species_counts.columns = ["Species", "Count"]
    fig3 = px.pie(species_counts, names="Species", values="Count", title="Species Distribution")
    st.plotly_chart(fig3)

    # Display Insights based on Selection
    if insight_choice == "Temporal Analysis":
        st.subheader("Year-wise and Month-wise Observations")
        df["Year"] = pd.to_datetime(df["Date"]).dt.year
        df["Month"] = pd.to_datetime(df["Date"]).dt.month
        
        # Define seasons based on months
        def get_season(month):
            if month in [12, 1, 2]:
                return "Winter"
            elif month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            else:
                return "Autumn"
        
        df["Season"] = df["Month"].apply(get_season)
        
        # Count bird sightings per season
        seasonal_trends = df.groupby("Season")["Common_Name"].count()
        
        # Plot seasonal trends
        fig, ax = plt.subplots(figsize=(8, 5))
        seasonal_trends.plot(kind="bar", color=["blue", "green", "red", "orange"], ax=ax)
        ax.set_xlabel("Season")
        ax.set_ylabel("Number of Sightings")
        ax.set_title("Bird Sightings Across Different Seasons")
        st.pyplot(fig)

    elif insight_choice == "Spatial Analysis":
        st.subheader("Top 10 Plots with Highest Species Diversity")
        plot_analysis = df.groupby("Plot_Name")["Common_Name"].nunique().reset_index()
        plot_analysis = plot_analysis.sort_values(by="Common_Name", ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=plot_analysis, x="Plot_Name", y="Common_Name", palette="mako", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_xlabel("Plot Name")
        ax.set_ylabel("Unique Species Count")
        ax.set_title("Top 10 Plots with Highest Species Diversity")
        st.pyplot(fig)

    elif insight_choice == "Species Analysis":
        st.subheader("Most Common Identification Methods and Observation Intervals")
        id_method_counts = df["ID_Method"].value_counts().reset_index()
        id_method_counts.columns = ["ID_Method", "Count"]
        
        interval_length_counts = df["Interval_Length"].value_counts().reset_index()
        interval_length_counts.columns = ["Interval_Length", "Count"]
        
        # Visualization: ID Methods
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        sns.barplot(data=id_method_counts, x="ID_Method", y="Count", palette="viridis", ax=ax1)
        ax1.set_xlabel("ID Method")
        ax1.set_ylabel("Count")
        ax1.set_title("Most Common Identification Methods")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right")
        st.pyplot(fig1)
        
        # Visualization: Interval Lengths
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        sns.barplot(data=interval_length_counts, x="Interval_Length", y="Count", palette="magma", ax=ax2)
        ax2.set_xlabel("Interval Length")
        ax2.set_ylabel("Count")
        ax2.set_title("Most Common Observation Interval Lengths")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right")
        st.pyplot(fig2)
    
    elif insight_choice == "Environmental Conditions":
        st.subheader("Correlation Between Weather Conditions and Bird Observations")
        weather_cols = ["Temperature", "Humidity", "Distance"]
        existing_cols = [col for col in weather_cols if col in df.columns]
        df[existing_cols] = df[existing_cols].apply(pd.to_numeric, errors='coerce')
        
        # Compute correlation matrix
        weather_corr = df[existing_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(weather_corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Correlation Between Weather Conditions and Bird Observations")
        st.pyplot(fig)
        
        # Scatterplot: Temperature vs Bird Sightings
        bird_counts_temp = df.groupby("Temperature")["Common_Name"].nunique().reset_index()
        bird_counts_temp.columns = ["Temperature", "Bird_Count"]
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=bird_counts_temp, x="Temperature", y="Bird_Count", alpha=0.5, palette="viridis", ax=ax2)
        ax2.set_xlabel("Temperature (°C)")
        ax2.set_ylabel("Unique Bird Species Observed")
        ax2.set_title("Impact of Temperature on Bird Sightings")
        st.pyplot(fig2)
    
    elif insight_choice == "Distance and Behavior":
        st.subheader("Frequency of Flyover Observations")
        if "Flyover_Observed" in df.columns:
            flyover_counts = df["Flyover_Observed"].value_counts().reset_index()
            flyover_counts.columns = ["Flyover_Observed", "Count"]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=flyover_counts, x="Flyover_Observed", y="Count", palette="coolwarm", ax=ax)
            ax.set_xlabel("Flyover Observed")
            ax.set_ylabel("Number of Observations")
            ax.set_title("Frequency of Flyover Observations")
            st.pyplot(fig)
    
    elif insight_choice == "Observer Trends":
        st.subheader("Observer Bias in Bird Observations")
        observer_analysis = df.groupby("Observer")["Common_Name"].nunique().reset_index()
        observer_analysis.columns = ["Observer", "Unique_Species"]
        
        if not observer_analysis.empty:
            fig1, ax1 = plt.subplots(figsize=(12, 5))
            sns.barplot(data=observer_analysis, x="Observer", y="Unique_Species", palette="coolwarm", ax=ax1)
            ax1.set_xlabel("Observer")
            ax1.set_ylabel("Unique Bird Species Observed")
            ax1.set_title("Observer Bias in Bird Observations")
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
            st.pyplot(fig1)
        else:
            st.write("No data available for observer analysis.")
        
        st.subheader("Impact of Visit Patterns on Species Count")
        visit_analysis = df.groupby("Visit")["Common_Name"].nunique().reset_index()
        visit_analysis.columns = ["Visit", "Unique_Species"]
        
        if not visit_analysis.empty:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=visit_analysis, x="Visit", y="Unique_Species", marker="o", color="b", ax=ax2)
            ax2.set_xlabel("Visit Number")
            ax2.set_ylabel("Unique Bird Species Observed")
            ax2.set_title("Impact of Visit Patterns on Species Count")
            ax2.grid(True)
            st.pyplot(fig2)
        else:
            st.write("No data available for visit analysis.")
    
    elif insight_choice == "Conservation Insights":
        st.subheader("Watchlist Trends and Regional Stewardship Status")
        if "PIF_Watchlist_Status" in df.columns and "Regional_Stewardship_Status" in df.columns:
            watchlist_counts = df.groupby(["PIF_Watchlist_Status", "Regional_Stewardship_Status"])["Common_Name"].nunique().reset_index()
            watchlist_counts.columns = ["PIF_Watchlist_Status", "Regional_Stewardship_Status", "Unique_Species"]
            
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            sns.barplot(data=watchlist_counts, x="PIF_Watchlist_Status", y="Unique_Species", hue="Regional_Stewardship_Status", palette="magma", ax=ax1)
            ax1.set_xlabel("PIF Watchlist Status")
            ax1.set_ylabel("Unique Bird Species Observed")
            ax1.set_title("Watchlist Trends and Regional Stewardship Status")
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
            ax1.legend(title="Regional Stewardship Status")
            st.pyplot(fig1)
        else:
            st.write("PIF_Watchlist_Status or Regional_Stewardship_Status columns are missing.")
        
        st.subheader("Distribution of Species Based on AOU Code")
        if "AOU_Code" in df.columns:
            fig2, ax2 = plt.subplots(figsize=(12, 5))
            sns.histplot(df["AOU_Code"].dropna(), bins=30, kde=True, color="b", ax=ax2)
            ax2.set_xlabel("AOU Code")
            ax2.set_ylabel("Frequency of Species")
            ax2.set_title("Distribution of Species Based on AOU Code")
            ax2.grid(True)
            st.pyplot(fig2)
        else:
            st.write("AOU_Code column is missing.")
    
 
