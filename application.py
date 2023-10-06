import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.sidebar.title("WHATSAPP CHAT ANALYZER")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)


    user_list= df['user_name'].unique().tolist()
    user_list.sort()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.insert(0,'Overall')


    selected_user = st.sidebar.selectbox('Show Anlysis wrt',user_list)
    if st.sidebar.button('Show Anlysis'):

        col1,col2,col3,col4 = st.columns(4)

        num_messages, num_words, media_count,links_count = helper.fetch_stats(selected_user,df)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Total Media')
            st.title(media_count)
            
        with col4:
            st.header('Total Links')
            st.title(links_count)

        #Word Cloud
        st.header('Most used words')
        wc= helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(wc,cmap='BuGn')
        st.pyplot(fig.figure)

        #Busiest Users
            
        if selected_user=='Overall':
            st.header('Busiest User')
            col1,col2 = st.columns(2)
            messages_per_user,message_per=helper.most_busiest_person(df)

            with col1:
                fig,ax= plt.subplots()
                bar = sns.barplot(x=messages_per_user.index,y=messages_per_user.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig.figure)

            with col2:
                st.dataframe(message_per)

        #Most Common Words

        st.title("Most Common Words")
        col1,col2 = st.columns(2)
        with col1:
            most_common_words = helper.most_common_words(selected_user,df)
            st.dataframe(most_common_words)
        with col2:
            fig,ax = plt.subplots()
            ax.barh(most_common_words[0],most_common_words[1],color='green')
            plt.grid()
            st.pyplot(fig)

        # Most commmon emoji
        st.title('Most Common Emoji')
        most_common_emoji = helper.most_common_emoji(selected_user,df)

        st.dataframe(most_common_emoji)

        #Monthly timeline

        st.title('Monthly Timeline')
        monthly_timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(monthly_timeline['year_month'],monthly_timeline['messages'],color="green")
        plt.xticks(rotation='vertical')
        plt.grid()
        st.pyplot(fig)
        #Day timeline

        st.title('Day Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        dates = daily_timeline['date'].unique()
        ax.plot(daily_timeline['date'],daily_timeline['messages'],color="green")
        plt.xticks(rotation='vertical')
        plt.xlabel('Days')
        plt.ylabel('Messages_count')
        st.pyplot(fig)  

     # activity map
    st.title('Activity Map')

    col1,col2 = st.columns(2)
    with col1:
        #busiest month
        st.title('Busiest Month')
        busiest_month = helper.busiest_month(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(busiest_month['index'],busiest_month['month_name'],color="cyan")
        plt.xlabel('Messages_count')
        plt.ylabel('Months')
        st.pyplot(fig)
    with col2:
        st.title('Busiest Day')
        busiest_day = helper.busiest_day(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(busiest_day['index'],busiest_day['day_name'],color="cyan")
        plt.xlabel('Messages_count')
        plt.ylabel('Days')
        st.pyplot(fig)


