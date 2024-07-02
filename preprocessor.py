import  pandas as pd
import re

def preprocess(data):
        pattern = r'\[(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AP]M)\]\s(.+?)(?=\s*\[\d{1,2}/\d{1,2}/\d{2}|\Z)'

    # Assuming the text is stored in a variable called 'text'
        matches = re.findall(pattern, data, re.DOTALL)

        df = pd.DataFrame(matches, columns=['Date', 'user_message'])

    # Convert 'Date' column to datetime
        df['message_date'] = pd.to_datetime(df['Date'], format='%m/%d/%y, %I:%M:%S %p')

    # Format the datetime to the desired string format
        df['message_date'] = df['message_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        users = []
        messages = []
        for message in df['user_message']:
             matchtemp = '([\W\w]+?:\s)'
             entry = re.split(matchtemp,message)
             if entry[1:]:
                    users.append(entry[1].rstrip(': '))
                    messages.append(entry[2])
             else:
                    users.append('group notification')
                    messages.append(entry[0])
        df['user'] = users
        df['message'] = messages
        df['date'] = pd.to_datetime(df['message_date'])
        df = df.drop(columns=['Date', 'user_message'])
        df.head()
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['month_num'] = df['date'].dt.month
        df['only_date'] = df['date'].dt.date
        df['day_name'] = df['date'].dt.day_name()
        period = []
        for hour in df[['day_name','hour']]['hour']:
            if hour == 23:
                period.append(str(hour)+ "-"+ str('00'))
            elif hour == 00:
                period.append(str(hour)+"-"+str(hour +1))
            else:
                period.append(str(hour)+"-"+ str(hour+1))
        df['period'] = period
        return df
