#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import pandas as pd


# write data to csv
def statistics(user_id):
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    with open('data.csv', 'a', newline="") as fil:
        wr = csv.writer(fil, delimiter=';')
        wr.writerow([data, user_id])


# create a report
def analysis():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    df = pd.read_csv('data.csv', delimiter=';', encoding='utf8')
    df_today = df[df['data'] == today]
    number_of_users = len(df['id'].unique())
    number_of_requests = len(df.index)
    number_of_users_today = len(df_today['id'].unique())
    number_of_requests_today = len(df_today.index)


   # number_of_days = len(df['data'].unique())

    message_to_user = 'Number of requests today: ' + '%s' % number_of_requests_today + '\n' \
                      +  'Total number of requests: '+ '%s' % number_of_requests + '\n' \
                      + 'Number of users today: ' + '%s' %number_of_users_today + '\n' \
                      + 'Total number of users: ' + '%s' %number_of_users



    return message_to_user

