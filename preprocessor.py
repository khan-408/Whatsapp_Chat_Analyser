import re
from datetime import datetime
import pandas as pd

def preprocessor(text):

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\u202fpm\s-\s'
    pattern1 = '\u202f'
    pattern3='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    match = re.search(pattern3, text)
    # match1 = re.search(pattern, text)


    if match:
        pattern = pattern3
        
    messages = re.split(pattern,text)[1:]
    date = re.findall(pattern,text)
    match1 = re.search(pattern1,date[1])
    if match1:
        dates=[]
        for i in date:
            dates.append(''.join(re.split(pattern1,i)))
        dates = [i.split('-')[0].strip() for i in dates]
        # Define the format of the input string
        input_format = "%d/%m/%y, %I:%M%p"
        dt_obj = []
        for i in dates:
            # Parse the input string to a datetime object
            dt_obj.append(datetime.strptime(i, input_format))

        # Convert to 24-hour format
        output_format = "%d/%m/%y, %H:%M"
        message_date = []
        for i in dt_obj:
            message_date.append(i.strftime(output_format)) 
    else: 
        date = [i.split('-')[0].strip() for i in date]
        message_date=date

    df = pd.DataFrame({'user_messages':messages,'message_date':message_date})
    pattern2='([\w\W]+?):\s'
    user_name = []
    messages = []

    for message in df['user_messages']:
        entry=re.split(pattern2,message)
        if entry[1:]:
            user_name.append(entry[1])
            messages.append(''.join(entry[2:]))

        else:
            user_name.append('group_notification')
            messages.append(entry[0])

    df['messages']=messages
    df['user_name']=user_name  
    df['messages'] = df['messages'].apply(lambda x: x.replace('\n','').strip())
    df = df[['user_name','messages','message_date']]

    df['message_date'] = pd.to_datetime(df['message_date'])

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month
    df['month_name'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute  
    df['date'] = df['message_date'].dt.date



    return df
