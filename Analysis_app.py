import numpy as np
import pickle
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
import folium
from streamlit_folium import folium_static
import networkx as nx
import seaborn as sns

#import the dataset
with open('data.pkl', 'rb') as f:
    df = pickle.load(f)

def conflict_events_by_country(data):
    # Group the data by country and count the number of events
    country_counts = data['COUNTRY'].value_counts()

    # Create a bar chart to visualize the counts
    plt.figure(figsize=(16, 12))
    country_counts.plot(kind='bar')
    plt.xlabel('Country')
    plt.ylabel('Number of Conflict Events')
    plt.title('Count of Conflict Events by Country')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.title("Conflict events by country")
    st.write("This chart shows conflict events by country.")

    # Display the bar chart in Streamlit
    st.pyplot(plt)

# Count of Conflict Events by Year
def count_of_Conflict_Events_by_Year(df):
    # Group the data by year and count the number of events
    year_counts = df['YEAR'].value_counts().sort_index()

    # Create a line chart to visualize the counts
    plt.figure(figsize=(10, 6))
    year_counts.plot(kind='line', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Number of Conflict Events')
    plt.title('Count of Conflict Events by Year')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.write('Count of Conflict Events by Year')
    # Display the line chart in Streamlit
    st.pyplot(plt)

# Distribution of Conflict Event Types
def distribution_of_conflict_event_types(df):
    # Calculate the frequency of each event type
    event_type_counts = df['EVENT_TYPE'].value_counts()

    # Create a pie chart to visualize the distribution
    plt.figure(figsize=(8, 8))
    event_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Distribution of Conflict Event Types')
    plt.tight_layout()

    st.write('Distribution of Conflict Event Types')
    # Display the pie chart in Streamlit
    st.pyplot(plt)

def summary_statistics_of_fatalities(df):
    # Calculate summary statistics of fatalities
    fatalities_stats = df['FATALITIES'].describe()

    # Display the summary statistics
    st.subheader('Summary Statistics of Fatalities')
    st.write(fatalities_stats)

def fatalities_per_year(df):
    # Group the data by year and calculate the total fatalities
    fatalities_per_year = df.groupby('YEAR')['FATALITIES'].sum()

    # Create a bar chart to visualize fatalities per year
    plt.figure(figsize=(8, 6))
    fatalities_per_year.plot(kind='bar')
    plt.xlabel('Year')
    plt.ylabel('Total Fatalities')
    plt.title('Fatalities per Year')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar chart in Streamlit
    st.subheader('Fatalities per Year')
    st.pyplot(plt)


def distribution_of_conflict_events_by_location(data):
    # Group the data by location and count the number of events
    location_counts = data['COUNTRY'].value_counts().reset_index()
    location_counts.columns = ['COUNTRY', 'Count']

    # Fetch the world countries GeoJSON data
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    response = requests.get(f'{url}/world-countries.json')
    world_geojson = response.json()

    # Create a choropleth map
    m = folium.Map(location=[0, 0], zoom_start=3.3)
    folium.Choropleth(
        geo_data=world_geojson,
        name='Choropleth',
        data=location_counts,
        columns=['COUNTRY', 'Count'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Conflict Events',
        highlight=True
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Display the choropleth map in Streamlit
    folium_static(m)

def relationships_between_actors(data):
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges between actors
    G.add_edges_from(data[['ACTOR1', 'ACTOR2']].values)

    # Calculate node positions using the Kamada-Kawai layout
    pos = nx.kamada_kawai_layout(G)

    # Draw the network graph
    plt.figure(figsize=(16, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray', arrows=True)
    plt.title('Relationships Between Actors')
    plt.tight_layout()

    # Display the network graph in Streamlit
    st.subheader('relationships_between_actors')
    st.pyplot(plt)

def correlation_analysis(data):
    # Select the relevant columns for correlation analysis
    selected_columns = ['EVENT_TYPE', 'FATALITIES', 'GEO_PRECISION']

    # Subset the data with the selected columns
    subset_data = data[selected_columns]

    # Calculate the correlation matrix
    correlation_matrix = subset_data.corr()

    # Create a heatmap to visualize the correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Analysis')
    plt.tight_layout()

    # Display the heatmap in Streamlit
    st.pyplot(plt)

# Set up sidebar options
sidebar_options = ['Homepage','Descriptive Analysis', 'Temporal Analysis', 'Geospatial Analysis', 'Actor Analysis', 'Event Type Analysis', 'Casualty Analysis']

# Set the page title
st.title('African Conflicts Dashboard')
st.write("This dashboard provides an overview of global conflicts from 1997 to 2017.")

# Add a sidebar to select the analysis type
selected_analysis = st.sidebar.selectbox('Select Analysis', sidebar_options)


# Perform analysis based on the selected option
if selected_analysis == 'Homepage':
    st.write("Use the sidebar to navigate to different pages.")
    st.write("The Dashboard is still going through updates you can however look at the code on my github,(https://github.com/mbuguajnr23/ACLED) I'd love the feedback")
    distribution_of_conflict_events_by_location(df)

elif selected_analysis == 'Descriptive Analysis':
    # Add code for descriptive analysis
    st.header('Descriptive Analysis')

    conflict_events_by_country(df)
    count_of_Conflict_Events_by_Year(df)
    distribution_of_conflict_event_types(df)
    summary_statistics_of_fatalities(df)
    fatalities_per_year(df)
    relationships_between_actors(df)
    

elif selected_analysis == 'Temporal Analysis':
    # Add code for temporal analysis
    st.header('Temporal Analysis')
    # Perform the analysis
    correlation_analysis(df)
    # ...

elif selected_analysis == 'Geospatial Analysis':
    # Add code for geospatial analysis
    st.header('Geospatial Analysis')
    # ...

elif selected_analysis == 'Actor Analysis':
    # Add code for actor analysis
    st.header('Actor Analysis')
    # ...

elif selected_analysis == 'Event Type Analysis':
    # Add code for event type analysis
    st.header('Event Type Analysis')
    # ...

elif selected_analysis == 'Casualty Analysis':
    # Add code for casualty analysis
    st.header('Casualty Analysis')
    # ...

# visualizations to the dashboard
# Conflict events by country

# # Run the Streamlit app
# if __name__ == '__main__':
#     main()
