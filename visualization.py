from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def sentiment_plot(df):
    sentiment_objects = [TextBlob(statuses_text) for statuses_text in df['statuses_text']]
    # creating the polarity for each tweet
    sentiment_objects[0].polarity, sentiment_objects[0]
    # Create list of polarity valuesx and tweet text
    sentiment_values = [[statuses_text.sentiment.polarity, str(statuses_text)] for statuses_text in sentiment_objects]
    # create data frame with the polarity values
    df_polarity = pd.DataFrame(sentiment_values, columns=["polarity", "statuses_text"])
    # creating a categorical variable if polarity is less than 0 then sentiment is negative, if  polarity== 0 then
    # sentiment is neutral and else sentiment is positive
    conditions = [
        (df['polarity'] < 0),
        (df['polarity'] > 0),
        (df['polarity'] == 0)
    ]
    # create a list of the values we want to assign for each condition
    values = ['negative', 'positive', 'neutral']

    # create a new column and use np.select to assign values to it using our lists as arguments
    df['sentiment'] = np.select(conditions, values)
    df.drop(columns=['polarity'], inplace=True)
    location_plot = df.groupby('sentiment').tweets_location.value_counts().unstack(0).plot.barh()
    plt.title("Class weight intervals")
    plt.ylabel("Number of Occurrences")

    plt.show()

