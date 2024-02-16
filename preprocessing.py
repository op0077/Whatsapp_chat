import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[pa][m]\s-\s'
    msg = re.split(pattern, data)[1:]
    # using [1:] bcz without it an empty string is coming in msg list
    dates = re.findall(pattern, data)
    dataframe = pd.DataFrame({'user_message': msg, 'message_date': dates})
    # creating  dataframe for data
    dataframe['message_date'] = pd.to_datetime(dataframe['message_date'], format='%d/%m/%y, %I:%M %p - ')
    user = []
    msgs = []

    for msg1 in dataframe['user_message']:
        entry = re.split('([\w\W]+?):\s', msg1)
        if entry[1:]:  # user_name
            user.append(entry[1])
            msgs.append(entry[2])
        else:
            user.append('kargo_notification')
            msgs.append(entry[0])

    dataframe['user'] = user
    dataframe['msg'] = msgs

    dataframe.drop(columns=['user_message'], inplace=True)
    dataframe['year'] = dataframe['message_date'].dt.year
    dataframe['o_date'] = dataframe['message_date'].dt.date
    dataframe['month_num'] = dataframe['message_date'].dt.month
    dataframe['month'] = dataframe['message_date'].dt.month_name()
    dataframe['day'] = dataframe['message_date'].dt.day
    dataframe['day_name'] = dataframe['message_date'].dt.day_name()
    dataframe['hour'] = dataframe['message_date'].dt.hour
    dataframe['minute'] = dataframe['message_date'].dt.minute
    period = []
    for hour in dataframe[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+ "-" + str('00'))
        elif hour == 0:
            period.append(str('00')+ "-" + str(hour + 1))
        else:
            period.append(str(hour)+ "-" + str(hour + 1))
    dataframe['period'] = period
    return dataframe
