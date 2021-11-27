import pandas as pd
import numpy as np
import pymysql

from datetime import datetime, timedelta
import plotly.express as px

def get_db():
    db = pymysql.connect(host='35.76.154.105', port=3306, user='root', passwd='1234',
                         db='AI_result', charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM coin'
    cursor.execute(sql)
    result = cursor.fetchall()
    test = pd.DataFrame(result)
    return test

def pre_data():
    test = get_db()
    test['date'] = pd.to_datetime(test['date'])
    test['week'] = test['date'].dt.weekday

    indexNames = test[(test['week'] == 5) | (test['week'] == 6)].index
    test.drop(indexNames, inplace=True)
    
    test['s'] = - test['s']
    test['s'] = round(test['s'], 3)

    test['num_1'] = test.groupby('coin')['num'].diff()
    test['num_3'] = test.groupby('coin')['num'].diff(3)
    test['num_5'] = test.groupby('coin')['num'].diff(5)
    test['s_1'] = test.groupby('coin')['s'].diff()
    test['s_3'] = test.groupby('coin')['s'].diff(3)
    test['s_5'] = test.groupby('coin')['s'].diff(5)

    test.rename(columns = {'num':'게시물 수', 's':'감정분석 평균'}, inplace=True)

    week = datetime.now() - timedelta(days=7)
    week = week.strftime('%Y-%m-%d')

    data = test.loc[test.date == week]
    data.reset_index(drop=True, inplace=True)
    return data

def get_plot_1d():
    data = pre_data()
    fig = px.scatter(data, x='num_1', y='s_1',
                 color='감정분석 평균', hover_name='coin', size='게시물 수',
                 color_continuous_scale=px.colors.diverging.RdYlGn,
                 labels={'num_1':'1일 전 게시물 수와 비교',
                         's_1':'1일 전 감정분석과 비교'})
    return fig

#get_plot_1d()

#get_plot_1d().write_html('plot_1d.html')

def get_plot_3d():
    data = pre_data()
    fig = px.scatter(data, x='num_3', y='s_3',
                 color='감정분석 평균', hover_name='coin', size='게시물 수',
                 color_continuous_scale=px.colors.diverging.RdYlGn,
                 labels={'num_3':'3일 전 게시물 수와 비교',
                         's_3':'3일 전 감정분석과 비교'})
    return fig

#get_plot_3d()

#get_plot_3d().write_html('plot_3d.html')

def get_plot_5d():
    data = pre_data()
    fig = px.scatter(data, x='num_5', y='s_5',
                 color='감정분석 평균', hover_name='coin', size='게시물 수',
                 color_continuous_scale=px.colors.diverging.RdYlGn,
                 labels={'num_5':'5일 전 게시물 수와 비교',
                         's_5':'5일 전 감정분석과 비교'})
    return fig

#get_plot_5d()

#get_plot_5d().write_html('plot_5d.html')