"""
Author : Mohlatlego Nakeng
         Raymond Chiruka
         
Task : This function performs the bot detection on twitter scripted data.         
"""


import re
import pandas as pd
import numpy as np


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


def massage_creator(df):
    # remove twitter handles (@user)
    # This has been commented out since the dataset being used here has the human/bot category
    # convert twitter dates to datetypes
    # del df["Unnamed: 0"]  # removing index column
    df['statuses_user_created_at'] = pd.to_datetime(df['statuses_user_created_at']).dt.date
    df['statuses_created_at'] = pd.to_datetime(df['statuses_created_at']).dt.date
    # calculate the number of days the profile has been in use
    df['profile_in_use'] = df['statuses_created_at'] - df['statuses_user_created_at']
    df['profile_in_use'] = pd.to_numeric(df['profile_in_use'].dt.days, downcast='integer')
    df['messages_per_day'] = df['statuses_user_statuses_count'] / df['profile_in_use']
    # create variable in human or bot
    df['message_creator'] = df['messages_per_day'].apply(lambda x: 'Bot' if x > 72 else 'Human')
    return df
