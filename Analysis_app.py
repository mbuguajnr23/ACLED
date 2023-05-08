import numpy as np
import pickle
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
import folium
from streamlit_folium import folium_static


with open('data.pkl', 'rb') as f:
    df = pickle.load(f)


def wordcloud_chart(data):
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.pyplot as plt
    text = " ".join(df['NOTES'].dropna()) 
    # Concatenate all the text data from your dataset into a single string
    wordcloud = WordCloud(width=800, height=800,
                      background_color= 'white',
                      stopwords= set(STOPWORDS),
                      min_font_size= 10)
    wordcloud.generate(text)
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
def events_per_year(data):
    # create a new column for the year
    data['YEAR'] = data['EVENT_DATE'].dt.year
    # group the data by year and count the number of events in each year
    attacks_by_year = data.groupby('YEAR').size()
    # create a line plot of the frequency of attacks over time
    fig, ax = plt.subplots()
    ax.plot(attacks_by_year.index, attacks_by_year.values)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Attacks')
    ax.set_title('Frequency of Attacks in Africa, 1997-2017')


def fatalities_by_country(data):
    # Create a pivot table to get the number of fatalities by country and year
    fatalities_by_country = data.pivot_table(index='COUNTRY', columns='YEAR', values='FATALITIES', aggfunc='sum')

    # Get the top 20 countries with the most fatalities
    top_countries = fatalities_by_country.sum(axis=1).nlargest(20)

    # Filter the pivot table to only include top countries
    fatalities_by_country = fatalities_by_country.loc[top_countries.index]

    # Create a scatter plot to show the intensity of conflicts
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(fatalities_by_country.mean(axis=1),  # X-axis: average number of fatalities
               fatalities_by_country.std(axis=1),   # Y-axis: standard deviation of fatalities
               s=fatalities_by_country.sum(axis=1) * 0.5,  # Size of bubble: total number of fatalities
               alpha=0.5)  # Transparency of bubbles
    ax.set_xlabel('Average number of fatalities')
    ax.set_ylabel('Standard deviation of fatalities')
    ax.set_title('Intensity of conflicts by country')
    

def conflict_type_count(data):
    conflict_counts = df['EVENT_TYPE'].value_counts()

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(conflict_counts.index, conflict_counts.values)

    # Set plot labels and title
    ax.set_xlabel('Conflict Type')
    ax.set_ylabel('Number of Conflicts')
    ax.set_title('Types of Conflicts')
    plt.xticks(rotation=90)



def events_per_country(data):
    events_per_country = data.groupby("COUNTRY").size()
    fig, ax = plt.subplots()
    ax.bar(events_per_country.index, events_per_country.values)
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of Events")
    ax.set_title("Number of events per country")
    ax.set_xticklabels(events_per_country.index, rotation=90)
    return fig


def chloropleth_mapping(data):
    conflicts_by_country = data.groupby('COUNTRY').size().reset_index(name='counts')
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    response = requests.get(f'{url}/world-countries.json')
    world_geojson = response.json()

    m = folium.Map(location=[30, 0], zoom_start=2)
    folium.GeoJson(
        world_geojson,
        name='World conflicts',
        tooltip=folium.features.GeoJsonTooltip(fields=['name'], labels=False),
        style_function=lambda x: {'fillColor': 'red', 'color': 'black', 'weight': 2, 'fillOpacity': 0.5}
    ).add_to(m)

    m = folium.Map(location=[0, 0], zoom_start=2)
    folium.Choropleth(
        geo_data=world_geojson,
        name='choropleth',
        data=conflicts_by_country,
        columns=['COUNTRY', 'counts'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Conflicts',
    ).add_to(m)
    folium.LayerControl().add_to(m)
    
    folium_static(m)


# set the option for Streamlit to not show the global use warning
st.set_option('deprecation.showPyplotGlobalUse', False)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# define the sidebar
st.sidebar.title("Global Conflicts Dashboard")
page = st.sidebar.selectbox("Select a page", ["Homepage", "Choropleth Map", "Wordcloud Chart", 
                                              "Events per Year", "Fatalities by Country",
                                              "Sub-event Type Count", "Events per Country"])

# create the homepage
if page == "Homepage":
    st.title("Global Conflicts Dashboard")
    st.write("This dashboard provides an overview of global conflicts from 2010 to 2020.")
    st.write("Use the sidebar to navigate to different pages.")

# create the choropleth map page
elif page == "Choropleth Map":
    st.title("Fatalities by Country")
    fig = chloropleth_mapping(df)
    st.plotly_chart(fig)

# create the wordcloud chart page
elif page == "Wordcloud Chart":
    st.title("Wordcloud of Conflict Events")
    fig = wordcloud_chart(df)
    st.pyplot(fig)

# create the events per year page
elif page == "Events per Year":
    st.title("Events per Year")
    fig = events_per_year(df)
    st.plotly_chart(fig)

# create the fatalities by country page
elif page == "Fatalities by Country":
    st.title("Total Fatalities by Country")
    fig = fatalities_by_country(df)
    st.plotly_chart(fig)

# create the sub-event type count page
elif page == "Sub-event Type Count":
    st.title("Sub-event Types")

# def event_type_chart(data):
#     event_type_counts = data['EVENT_TYPE'].value_counts()
#     fig, ax = plt.subplots()
#     ax.pie(event_type_counts.values,
#            labels=event_type_counts.index, autopct='%1.1f%%')
#     ax.set_title("Event Type Distribution")
#     return fig


# def events_per_country_chart(data):
#     events_per_country = data.groupby("year").size()
#     fig, ax = plt.subplots()
#     ax.bar(events_per_country.index, events_per_country.values)
#     ax.set_xlabel("year")
#     ax.set_ylabel("Number of events")
#     ax.set_title("Number of events per country")
#     return fig


# def country_fatality_chart(data):
#     country_fatality = data.groupby("country")["fatalities"].sum()
#     fig, ax = plt.subplots()
#     ax.pie(country_fatality.values,
#            labels=country_fatality.index)
#     ax.set_title("Percentage of Fatalities in Each Country")
#     return fig


# def source_scale_chart(data):
#     source_scale_events = data.groupby("source_scale").size()
#     fig, ax = plt.subplots()
#     ax.pie(source_scale_events.values,
#            labels=source_scale_events.index)
#     ax.set_title("Number of Events per Source Scale")
#     return fig


# def sub_event_type_chart(data):
#     sub_event_type_events = data.groupby("sub_event_type").size()
#     fig, ax = plt.subplots()
#     ax.barh(sub_event_type_events.index, sub_event_type_events.values)
#     ax.set_xlabel("Number of Events")
#     ax.set_ylabel("Sub-Event-Type")
#     ax.set_title("Total Analysis of Sub-Event-Type")
#     return fig

# def event_type_per_country_chart(data):
#     event_type_per_country = data.groupby(["country", "event_type"]).size()
#     event_type_per_country = event_type_per_country.reset_index(name="counts")
#     event_type_per_country = event_type_per_country.pivot(
#         index='country', columns='event_type', values='counts')
#     event_type_per_country.plot(kind='bar', stacked=True)
#     plt.xlabel("Country")
#     plt.ylabel("Number of events")
#     plt.title("Event Type Distribution per Country")
#     return plt.gcf()


# def event_type_per_country_pie(data):
#     event_type_per_country = data.groupby(
#         ["country", "event_type"]).size().reset_index(name='counts')
#     countries = event_type_per_country['country'].unique()
#     for country in countries:
#         country_data = event_type_per_country[event_type_per_country['country'] == country]
#         fig, ax = plt.subplots()
#         ax.pie(country_data['counts'],
#                labels=country_data['event_type'], autopct='%1.1f%%')
#         ax.set_title(f"Event Type Distribution in {country}")
#         st.pyplot(fig)



# # create the source scale chart and display it on streamlit
# fig5 = source_scale_chart(df)
# st.pyplot(fig5)



# fig7 = event_type_per_country_chart(df)
# st.pyplot(fig7)

# fig8 = event_type_per_country_pie(df)
# st.pyplot(fig8)
