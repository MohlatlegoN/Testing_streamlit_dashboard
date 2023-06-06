"""
Author : Mohlatlego Nakeng
         Raymond Chiruka
Task : This is the appication script for a dashboard and visualizations.
"""
import base64
import streamlit as st
import pandas as pd
from Topics import topics_sa, topics_global
from bots_detection import massage_creator
from location_identifier import load_data
from wordcloud import WordCloud
import matplotlib as plt

st.set_option('deprecation.showfileUploaderEncoding', False)
showPyplotGlobalUse = False
st.title('Covid19za Consortium: COVID-19 SOCIAL MEDIA DATA MINING PROJECT')

st.sidebar.subheader("MIT808 group 6")
st.sidebar.image("data/up.jpg", use_column_width=True)


# FUNCTIONT TO EXPORT PROCESSED DATA
def get_table_download_link_csv(df):
    # csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    # b64 = base64.b64encode(csv.encode()).decode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
    return href


# Import raw data
st.sidebar.subheader("Upload raw data")
upload_data = st.sidebar.file_uploader(label="upoad csv or excelfile",
                                       type=['csv', 'xlsx'])
# Import labelling data
#st.sidebar.subheader("Upload data labelling")
global df
if upload_data is not None:
    try:
        df = pd.read_csv(upload_data)
    except Exception as e:
        print(e)
        df = pd.read_excel(upload_data)
else:
    st.write("Please import data-set (excel sheet or csv)")


# st.write(df)
def main():
    st.sidebar.header('Model and Visualization Selection')
    pick = ["Visualization", "location-classification", "Bots-detection"]
    function = st.sidebar.selectbox("Select funtion here", pick)

    if function == 'location-classification':
        st.subheader("Categorisation of South African and international social media data-set")
        st.write(
            "This function helps with the clustering of social media generated data according to tweets location. The "
            "aim is to monitor the "
            "South African social media discussion about the COVID-19 pandemic against the rest of the world")

        st.write(" (i) The function generates: Classification of South African and International  status text/tweets")
        # st.write(" (ii) We also monitor the sentiment of the on the texts")
        data = load_data(df)
        data1 = data["tweets_location"]
        st.write(data1.value_counts())
        st.bar_chart(data1.value_counts())
        st.write(data[["statuses_text", "tweets_location"]])

        # visualization
    # global df
    elif function == "Visualization":
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.subheader("This a visualization dashboard")
        st.write("We visualize the data-set using descriptive based on the processed data")
        pick = ["location-categorisation", "Bots-detection", "Topic-discussions"]
        vue = st.selectbox("Select funtion here", pick)
        dataset = load_data(df)
        if vue == "location-categorisation":
            st.write(dataset.groupby('sentiment').tweets_location.value_counts().unstack(0))
            dataset.groupby('sentiment').tweets_location.value_counts().unstack(0).plot.bar()
            st.pyplot()
            dataset.tweets_location.value_counts().plot.pie()
            plt.pyplot.title('South African and International texts categorisation')
            plt.pyplot.axis('off')
            st.pyplot()
        elif vue == "Bots-detection":
            st.write(dataset.groupby('sentiment').message_creator.value_counts().unstack(0))
            dataset.groupby('sentiment').message_creator.value_counts().unstack(0).plot.bar()
            st.pyplot()
            dataset.message_creator.value_counts().plot.pie()
            plt.pyplot.title('Bots detection plot (bot vs human categorisation)')
            st.pyplot()
        elif vue == "Topic-discussions":

            st.write("Lets see the topics discussed locally vs internationally")
            pick = ["Local tweets", "international tweets"]
            vue1 = st.selectbox("Select function here", pick)
            if vue1 == "Local tweets":
                wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110) \
                    .generate(topics_sa(dataset))
                plt.pyplot.figure(figsize=(10, 7))
                plt.pyplot.imshow(wordcloud, interpolation="bilinear")
                plt.pyplot.axis('off')
                plt.pyplot.title('TEXTS-SOUTH AFRICA')
                plt.pyplot.show()
                st.pyplot()
            elif vue1 == "international tweets":
                wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(topics_global
                                                                                                          (dataset))

                plt.pyplot.figure(figsize=(10, 7))
                plt.pyplot.imshow(wordcloud, interpolation="bilinear")
                plt.pyplot.axis('off')
                plt.pyplot.title('TEXTS-Global')
                plt.pyplot.show()
                st.pyplot()
        # st.write(plot1)

    elif function == "Bots-detection":
        st.subheader("Bot detection")
        st.write("Detecting  Bots and human stratas")
        massage_creator(df)
        df1 = df['message_creator']
        st.write(df1.value_counts())
        st.bar_chart(df1.value_counts())
        st.write(df[["statuses_text", "message_creator", "messages_per_day"]])
        #st.write(get_table_download_link_csv(df))


if __name__ == '__main__':
    main()
