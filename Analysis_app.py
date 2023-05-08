import numpy as np
import pickle
import pandas as pd
import streamlit as st


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


# def events_per_country(data):
#     events_per_country = data.groupby("country").size()
#     fig, ax = plt.subplots()
#     ax.bar(events_per_country.index, events_per_country.values)
#     ax.set_xlabel("Country")
#     ax.set_ylabel("Number of Events")
#     ax.set_title("Number of events per country")
#     ax.set_xticklabels(events_per_country.index, rotation=90)
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



# set the option for Streamlit to not show the global use warning
st.set_option('deprecation.showPyplotGlobalUse', False)

# create the event type chart and display it on Streamlit
fig1 = wordcloud_chart(df)
st.pyplot(fig1)


# # create the events per country chart and display it on Streamlit
# fig2 = events_per_country_chart(df)
# st.pyplot(fig2)

# # create the country fatality chart and display it on Streamlit
# fig3 = country_fatality_chart(df)
# st.pyplot(fig3)

# # create the sub-event type chart and display it on Streamlit
# fig4 = sub_event_type_chart(df)
# st.pyplot(fig4)

# # create the source scale chart and display it on streamlit
# fig5 = source_scale_chart(df)
# st.pyplot(fig5)

# fig6 = events_per_country(df)
# st.pyplot(fig6)

# fig7 = event_type_per_country_chart(df)
# st.pyplot(fig7)

# fig8 = event_type_per_country_pie(df)
# st.pyplot(fig8)
