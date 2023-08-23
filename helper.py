""" This script is to create methods that will be helpful for analysis. """

# for extracting urls
from urllib.parse import urlparse

# for regular expression
import re

# for wordcloud
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


# ----- fetching messages for overall or individual users ----- #

def fetch_messages(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        df = df[['date', 'message']]

    else:
        df = df[['date', 'user', 'message']] 

    df = df.set_index('date')
    return df


# ----- fetching stats ----- #

def fetch_stats(selected_user, df):

    # for user selected, display messages for that user only
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. fetch number of messages
    num_messages = df.shape[0]

    # 2. fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. fetch number of media messages
    num_media_messages = df[df['message'] == '<media_omitted>'].shape[0]

    # 4. fetch number of links shared

    # regular expression pattern for extracting URLs
    url_pattern = re.compile(r'https?://\S+')

    # Extract URLs from the 'message' column
    links = []
    for message in df['message']:
        extracted_links = url_pattern.findall(message)
        links.extend(extracted_links)


    return num_messages,len(words),num_media_messages,len(links)



# ----- fetching most busy users ----- #

def most_busy_users(df):

    # top 5 busy users
    x = df['user'].value_counts().head()

    # percentage of messages by each user
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns = {'count': 'percent',
                   'user': 'name'})
    
    return x, df



# ----- creating wordcloud ----- #

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<media_omitted>']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


# ----- most common words ----- #
def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<media_omitted>']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI])

#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

#     return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap