import emoji
from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]
        #1 Count messages
    num_messages=len(df['messages'])
        #2 Count total words 
    words=[]
    for message in df['messages']:
        if message !='<Media omitted>':
            words.extend(message.split())
    media=[]
    for message in df['messages']:
        if message =='<Media omitted>':
            media.extend(message)

    extract = URLExtract()
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), len(media),len(links)



def most_busiest_person(df):
    #1 Message count
    messages_per_user = df['user_name'].value_counts().head()
    #2  Message percent
    message_percent = round((df['user_name'].value_counts()/len(df['user_name']))*100,2)
    message_per = pd.DataFrame(messages_per_user)
    message_per.columns = ['message_count']
    message_per['message_percent'] = message_percent

    return messages_per_user,message_per

def create_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words=f.read()
    temp= df[df['messages']!='<Media omitted>']
    df1 = temp[temp['user_name']!='group_notification']

    words=[]
    for message in df1['messages']:
        x=message.lower().split()
        for i in x:
            if i not in stop_words:
                words.append(i)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df1['messages'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words=f.read()
    temp= df[df['messages']!='<Media omitted>']
    df1 = temp[temp['user_name']!='group_notification']

    words=[]
    for message in df1['messages']:
        x=message.lower().split()
        for i in x:
            if i not in stop_words:
                words.append(i)

    most_common = pd.DataFrame(Counter(words).most_common(20))
    return most_common


def most_common_words1(selected_user,df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def most_common_emoji(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]
    emojis=[]
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    df_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return df_emoji

def monthly_timeline(selected_user,df):
    
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]

    timeline = df.groupby(['year','month_name']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(str(timeline['year'][i])+'-'+str(timeline['month_name'][i]))
    timeline['year_month'] = time
    timeline = timeline[['year_month','messages']]

    return timeline
        

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]

    timeline = df.groupby(['date']).count()['messages'].reset_index()
    return timeline

def busiest_month(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]

    month= df['month_name'].value_counts().reset_index()
    return month


def busiest_day(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user_name']==selected_user]

    day= df['day_name'].value_counts().reset_index()
    return day
