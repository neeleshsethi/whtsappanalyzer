import streamlit as st
import  preprocessor,matplotlib,seaborn as sns
import helper

import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("whtspp analyzer")
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetch uniqie users
    user_list = df['user'].unique().tolist()
    #user_list.remove('group notification'
    if 'group notification' in user_list:
       user_list.remove('group notification')
    if 'Meta AI' in user_list:
       user_list.remove('Meta AI')
    if '🇮🇳 T20 World Champions 🇮🇳' in user_list:
       user_list.remove('🇮🇳 T20 World Champions 🇮🇳')
    if 'D16 Core Group' in user_list:
       user_list.remove('D16 Core Group')
    if 'NP - JAI SHRI RAM' in user_list:
       user_list.remove('NP - JAI SHRI RAM')

    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("SHow analysis with respect to ",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages , words ,num_media_messages, num_links =  helper.fetch_stats(selected_user,df)
        st.title('Top Stats')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Vedio Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)


        # Monthly TImeline
        st.title("Monthly timeline")

        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

         # Daily TImeline
        st.title("Daily timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity map')
        col1, col2 = st.columns(2)
        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Weekly activity map')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        # finding the busiest users in group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                 ax.bar(x.index, x.values, color='red')
                 plt.xticks(rotation='vertical')
                 st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        df_wc = helper.create_word_cloud(selected_user, df)
        fig, axis = plt.subplots()
        axis.imshow(df_wc)
        st.pyplot(fig)



        #most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)
   # Emoji analysis

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)









