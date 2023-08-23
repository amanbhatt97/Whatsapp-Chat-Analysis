""" This script takes the text file of whatsapp messages,
preprocess it and returns a dataframe from it. """

#----- Dependencies ----#

# for regular expression
import re  

# for reading and preprocessing
import pandas as pd  

# datetime 
from datetime import *


def fetch_date(data):

    # pattern that represents date
    date_pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AP]M'

    # datetime of message
    datetimes = re.findall(date_pattern, data)

    # convert timestamps to 24 hur format
    dates = []
    for timestamp in datetimes:
        # Parse the original timestamp
        original_datetime = datetime.strptime(timestamp, '%m/%d/%y, %I:%M:%S %p')
        
        # Convert to 24-hour format
        new_datetime = original_datetime.strftime('%m/%d/%y, %H:%M')
        
        dates.append(new_datetime)

    return dates


def fetch_message(data):
    # pattern that represents date
    message_pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AP]M\]'

    # messages after removing dates
    messages = re.split(message_pattern, data)[1:]
    messages

    return messages


def preprocess(data):

    # creating dates
    dates = fetch_date(data)

    # creating messages
    messages = fetch_message(data)

    # creating dataframe of dates and messages
    df = pd.DataFrame({'user_message': messages, 'date': dates})

    # convert date column to datetime column
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M')

    """ seperating user name from messages """
    users = []
    messages = []

    # loop over messages
    for message in df['user_message']:
        # splitting on the patterm
        entry = re.split('([\w\W]+?):\s', message)
         
        users.append(entry[1])
        messages.append(" ".join(entry[2:]))

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # remove security code messages
    df = df[~df['message'].str.startswith("‎‎Your security code")]

    # remove '[' at the end of each message
    df['message'] = df['message'].str.rstrip('[')

    # remove messages containing phone number change
    df = df[~df['message'].str.contains("changed their phone number")]

    # removing white space from username
    df['user'] = df['user'].str.strip()

    # removing white space from messages
    df['message'] = df['message'].str.strip()

    # Remove '\n' from the 'message' column
    df['message'] = df['message'].str.replace('\n', '')

    # Replace message containing 'omitted' with '<media_omitted>'
    df.loc[df['message'].str.contains('omitted'), 'message'] = '<media_omitted>'


    """ datetime features """
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    return df


