import streamlit as st
import pandas as pd
from io import StringIO
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# title in sidebar
st.sidebar.title("Whatsapp Chat Analyser")


# file to upload for analysis
uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:

    # read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # convert into string
    data = bytes_data.decode("utf-8")

    # processed data
    df = preprocessor.preprocess(data)


    # --------- fetch unique user names -------- #

    # fetch unique user names to list
    user_list = df['user'].unique().tolist()

    # sort by name
    user_list.sort()

    # insert overall optiom
    user_list.insert(0,"Overall")

    # sidebar to select user
    selected_user = st.sidebar.selectbox("Show Analysis with", user_list)


    # ------------ display messages ------------ # 

    # fetching all messages
    all_messages = helper.fetch_messages(selected_user, df)

    # for selected user: 
    if selected_user != 'Overall':
        st.title(f"Messages by {selected_user}")

    # for overall:
    else:
        st.title('All Messages')
    
    # display messages
    st.dataframe(all_messages) 


    # ----------- displaying statistics ----------- #

    # total messages, words, media file shared, links shared
    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    # display title
    st.title("Top Statistics")

    # creating a layout with 4 columns
    col1, col2, col3, col4 = st.columns(4)

    # display total messages 
    with col1:
        st.header("Total Messages")
        st.title(num_messages)

    # display total words
    with col2:
        st.header("Total Words")
        st.title(words)

    # display number of media files shared
    with col3:
        st.header("Media Shared")
        st.title(num_media_messages)

    # display number of links shared
    with col4:
        st.header("Links Shared")
        st.title(num_links)


    # ------ finding the busiest users in the group ----- #

    # display most busy users for overall 
    if selected_user == 'Overall':

        # title 
        st.title('Most Busy Users')

        # top 5 busy users, percentage of messages by each user
        x, new_df = helper.most_busy_users(df)
        
        # creating figure and axes
        fig, ax = plt.subplots()

        # creating a layout with 2 columns 
        col1, col2 = st.columns(2)

        # creating plot 
        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # display percentage of messages by each user
        with col2:
            st.dataframe(new_df)


    # ------ creating wordcloud ----- #
    
    # title to display
    st.title("Wordcloud")

    # wordcloud words
    df_wc = helper.create_wordcloud(selected_user,df)

    # creating figure and axes 
    fig,ax = plt.subplots()

    # display wordcloud on axes
    ax.imshow(df_wc)

    # display wordcloud figure using streamlit
    st.pyplot(fig)


    # ------ most common words ----- #

    most_common_df = helper.most_common_words(selected_user,df)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

    st.title('Most commmon words')
    st.pyplot(fig)


    # monthly timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)


    # # emoji analysis
    # emoji_df = helper.emoji_helper(selected_user,df)
    # st.title("Emoji Analysis")

    # col1,col2 = st.columns(2)

    # with col1:
    #     st.dataframe(emoji_df)
    # with col2:
    #     fig,ax = plt.subplots()
    #     ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
    #     st.pyplot(fig)