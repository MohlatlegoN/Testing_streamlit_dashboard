# load libraries
# import streamlit as st
import re
import string
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from textblob import TextBlob

nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
stop_words = stopwords.words('english')
stemmer = PorterStemmer()


def load_data(df):
    # drop keep necessary features
    data = df.loc[:, ['statuses_text',
                      'statuses_lang',
                      'statuses_user_location',
                      'statuses_created_at',
                      'statuses_user_created_at',
                      'statuses_user_statuses_count']]

    # drop non english tweets
    # change status language to english or non english
    data['statuses_lang'].mask(data['statuses_lang'] == 'uk', 'en', inplace=True)
    data['statuses_lang'] = data['statuses_lang'].apply(lambda x: 'en' if x == 'en' else 'non_english')
    data = data[data['statuses_lang'] == 'en']

    # drop columns with more than 70% missing
    pct_null = data.isnull().sum() / len(data)
    missing_features = pct_null[pct_null > 0.70].index
    data.drop(missing_features, axis=1, inplace=True)

    # drop duplicated rows and columns
    data.drop_duplicates(keep=False, inplace=True)
    data.T.drop_duplicates().T

    # drop all examples with missing values
    data = data.dropna(axis=0, how='any')

    # remove punctuation in location
    data['statuses_user_location'] = data['statuses_user_location'].str.replace("[^a-zA-Z]", " ")

    # change status location to local or global

    def checkl(T):
        TSplit_space = [x.lower().strip() for x in T.split()]
        TSplit_comma = [x.lower().strip() for x in T.split(',')]
        TSplit = list(set().union(TSplit_space, TSplit_comma))

        if 'southafrica' in TSplit or 'mzansi' in TSplit or 'joburg' in TSplit or 'johannesburg' in TSplit or 'capetown' in TSplit or 'durban' in TSplit or 'westerncape' in TSplit or 'gauteng' in TSplit:
            T = 'local'
        else:
            T = 'global'

        return T

    # Appling the function on the dataframe column

    data['tweets_location'] = data['statuses_user_location'].dropna().apply(checkl)

    # convert twitter dates to datetypes
    data['statuses_user_created_at'] = pd.to_datetime(data['statuses_user_created_at']).dt.date
    data['statuses_created_at'] = pd.to_datetime(data['statuses_created_at']).dt.date
    # calculate the number of days the profile has been in use
    data['profile_in_use'] = data['statuses_created_at'] - data['statuses_user_created_at']
    data['profile_in_use'] = pd.to_numeric(data['profile_in_use'].dt.days, downcast='integer')
    data['messages_per_day'] = data['statuses_user_statuses_count'] / data['profile_in_use']
    # create variable in human or bot
    data['message_creator'] = data['messages_per_day'].apply(lambda x: 'Bot' if x > 72 else 'Human')

    def remove_pattern(input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)

        return input_txt

    def preprocess_tweet_text(tweet):
        tweet.lower()
        # Remove urls
        tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
        # Remove user @ references and '#' from tweet
        # tweet = tweet.str.replace("[^a-zA-Z#]", " ")
        # Remove punctuations
        tweet = tweet.translate(str.maketrans('', '', string.punctuation))
        # Remove stopwords
        tweet_tokens = word_tokenize(tweet)
        filtered_words = [w for w in tweet_tokens if not w in stop_words]
        # lower case all words
        ps = PorterStemmer()
        stemmed_words = [ps.stem(w) for w in filtered_words]
        lemmatizer = WordNetLemmatizer()
        lemma_words = [lemmatizer.lemmatize(w, pos='a') for w in stemmed_words]

        return " ".join(filtered_words)

    # remove twitter handles (@user)
    data['statuses_text'] = np.vectorize(remove_pattern)(data['statuses_text'], "@[\w]*")
    # remove special characters, numbers, punctuations
    data['statuses_text'] = data['statuses_text'].str.replace("[^a-zA-Z#]", " ")
    # preprocessing tweete and retweets
    data['statuses_text'] = data['statuses_text'].apply(preprocess_tweet_text)
    # make dataframe lowercase
    data = data.applymap(lambda s: s.lower() if type(s) == str else s)

    # create sentiment feature
    sentiment_objects = [TextBlob(statuses_text) for statuses_text in data['statuses_text']]
    # creating the polarity for each tweet
    sentiment_objects[0].polarity, sentiment_objects[0]
    # Create list of polarity valuesx and tweet text
    sentiment_values = [[statuses_text.sentiment.polarity, str(statuses_text)] for statuses_text in sentiment_objects]

    # create data frame with the polarity values
    data_polarity = pd.DataFrame(sentiment_values, columns=["polarity", "statuses_text"])
    data['polarity'] = data_polarity['polarity']
    # creating a categorical variable if polarity is less than 0 then sentiment is negative, if  polarity== 0 then
    # sentiment is neutral and else sentiment is positive
    conditions = [
        (data['polarity'] < 0),
        (data['polarity'] > 0),
        (data['polarity'] == 0)
    ]

    # create a list of the values we want to assign for each condition
    values = ['negative', 'positive', 'neutral']

    # create a new column and use np.select to assign values to it using our lists as arguments
    data['sentiment'] = np.select(conditions, values)

    # drop unnecesary variables
    data.drop(columns=['polarity',
                       'statuses_created_at',
                       'statuses_user_location',
                       'statuses_user_created_at',
                       'statuses_user_statuses_count',
                       'profile_in_use',
                       'messages_per_day'], inplace=True)
    # drop rows with sentiment 0
    data = data[data['sentiment'] != '0']
    return data

