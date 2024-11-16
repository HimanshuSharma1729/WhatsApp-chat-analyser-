import re
import pandas as pd

def preprocess(data):
    # Updated pattern to match the date-time format in your WhatsApp data
    pattern = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s'

    messages = re.split(pattern, data)[1:]  # Split the data based on the pattern
    dates = re.findall(pattern, data)       # Extract dates using the pattern

    # Create DataFrame with user messages and corresponding dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    #print(df['message_date'])
    # Convert 'message_date' to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
   # print(df['message_date'])
    # Rename 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists to store users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)  # Split based on 'username: message'
        if entry[1:]:  # If there is a user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # If it's a system notification (no username)
            users.append('group_notification')
            messages.append(entry[0])
    print(len(users))
    print(df['user_message'])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional time-based features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Generate time periods for each message
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period

    return df
