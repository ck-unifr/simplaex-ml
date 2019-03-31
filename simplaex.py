# Simplaex ML coding task.
# The description of the task can be found in README.md
#
# author: Kai chen
# date: Mar 2019
#

import pandas as pd
import random
import time


class InternetData:

    def __init__(self, histData=None, tarData=None):
        '''
        The initialization method should take as an input two pandas dataframes:

        one with the historical data -  If the historical data is not passed it should be generated randomly for a year,
        i.e., 365 * 24 rows, with two columns — hour of day and some random volume of data (float, 0 to 1000 megabytes).

        another with tariffs - If the tariffs dataframe is not passed, the one from the description should be used.
        You can define the format of the tariffs dataframe by yourself.

        :param histData: a pandas dataframe presents the historical data
        :param tarData: a pandas dataframe presents the tariffs data
        '''

        if histData is None:
            dictHistData = {'hod': [], 'volume': []}
            dictHistData['hod'] = [i_hour for i_day in range(0, 365) for i_hour in range(0, 24)]
            dictHistData['volume'] = [random.uniform(0, 1000) for i_day in range(0, 365) for i_hour in range(0, 24)]
            histData = pd.DataFrame(dictHistData, columns=['hod', 'volume'])

        if tarData is None:
            dictTarData = {'time-range': [], 'price': []}
            dictTarData['time-range'] = ['0:00 to 9:00', '9:00 to 18:00', '18:00 to 0:00']
            dictTarData['price'] = [5, 11, 19]
            tarData = pd.DataFrame(dictTarData, columns=['time-range', 'price'])

        self.hisData = histData
        self.tarData = tarData

    def getTime(self, str_time):
        '''
        Transfer the string format time to float format time
        for example, '5:30' -> 5.5
        :param str_time: time in the string format, e.g. 0:00,
        :return: time in float format
        '''
        arr_time = str_time.split(':')
        hour = int(arr_time[0])
        if arr_time[1][0] == '0':
            minute = int(arr_time[1][1])
        else:
            minute = int(arr_time[1])
        return hour+(minute*1.0/60)

    def getStartStopTime(self, str_time):
        '''
        Get the start and stop time in float from a string time in the format ('hour:minute')
        for example, '0:00 to 9:30' -> 0, 9.5
        '''
        arr_time = str_time.split(' ')
        start_time = self.getTime(arr_time[0])
        stop_time = self.getTime(arr_time[2])
        if stop_time < start_time: # because we may have 18:00 to 0:00
            stop_time = 24
        return start_time, stop_time

    def add_cost(self, how = None):
        '''
        Create a method add_cost(how: String) that will return a historical dataframe with an additional column “cost”
        that will show how much money was spent for every hour in the historical data.
        There are multiple ways to do it in pandas, some very slow, some pretty fast. Come up with several solutions, include them all.
        The add_cost should choose the method based on the value of its ‘how’ parameter.
        '''

        if how is None or how == '0':
            def getDictPrice(tarData):
                '''
                return a dictionary {hour:price} from the tariffs dataframe
                '''
                dictPrice = {i:0 for i in range(0, 25)}
                for index, row in tarData.iterrows():
                    start_time, stop_time = self.getStartStopTime(row['time-range'])
                    for i in range(int(start_time), round(stop_time)):
                        dictPrice[i] = row['price']
                return dictPrice
            dictPrice = getDictPrice(self.tarData)
            self.hisData['cost'] = self.hisData['hod'].apply(lambda x : dictPrice[int(x)]) * self.hisData['volume']
        elif how == '1':
            def getDictPrice(tarData):
                '''
                return a dictionary {hour:price} from the tariffs dataframe
                '''
                dictPrice = {i:0 for i in range(0, 25)}
                for index, row in tarData.iterrows():
                    start_time, stop_time = self.getStartStopTime(row['time-range'])
                    for i in range(int(start_time), round(stop_time)):
                        dictPrice[i] = row['price']
                return dictPrice
            dictPrice = getDictPrice(self.tarData)
            self.hisData['cost-per-mega'] = self.hisData['hod'].apply(lambda x : dictPrice[int(x)])
            self.hisData['cost'] = self.hisData['cost-per-mega']*self.hisData['volume']
            self.hisData.drop(['cost-per-mega'], axis=1, inplace=True)
        elif how == '2':
            def f(x, tarData):
                '''
                for each row of the historical dataframe, get the price of the hour
                '''
                for index, row in tarData.iterrows():
                    start_time, stop_time = self.getStartStopTime(row['time-range'])
                    if int(x) >= int(start_time) and int(x) < round(stop_time):
                        return row['price']
                return 0
            self.hisData['cost-per-mega'] = self.hisData['hod'].apply(f, args=[self.tarData])
            self.hisData['cost'] = self.hisData['cost-per-mega']*self.hisData['volume']
            self.hisData.drop(['cost-per-mega'], axis=1, inplace=True)
        elif how == '3':
            listCost = [0 for i in range(0, len(self.hisData.index))]
            for indexHis, rowHis in self.hisData.iterrows():
                hod = rowHis['hod']
                volume = rowHis['volume']
                for indexTar, rowTar in self.tarData.iterrows():
                    start_time, stop_time = self.getStartStopTime(rowTar['time-range'])
                    if int(hod) >= int(start_time) and int(hod) < round(stop_time):
                        listCost[indexHis] = (rowTar['price']*volume)
                        break
            self.hisData['cost'] = pd.Series(listCost, index=self.hisData.index)

        return self.hisData

def compare_approaches():
    '''
    Create a method compare_approaches() that compares the performance of all of your solutions and returns the results in a dictionary {“method_name”: time}
    '''
    #dict_hist = {'hod': [0, 5, 15, 0, 17],
    #             'volume': [512.4, 114, 28, 12, 324]
    #             }
    #df_hist = pd.DataFrame(dict_hist, columns=['hod', 'volume'])
    df_hist = None

    dict_runtime = {}

    start_time = time.time()
    internet1 = InternetData(histData=df_hist)
    internet1.add_cost(how='0')
    dict_runtime['0'] = time.time() - start_time
    #print(df_hist)

    start_time = time.time()
    internet2 = InternetData(histData=df_hist)
    internet2.add_cost(how='1')
    dict_runtime['1'] = time.time() - start_time
    #print(df_hist)

    start_time = time.time()
    internet3 = InternetData(histData=df_hist)
    internet3.add_cost(how='2')
    dict_runtime['2'] = time.time() - start_time
    # print(df_hist)

    start_time = time.time()
    internet4 = InternetData(histData=df_hist)
    internet4.add_cost(how='3')
    dict_runtime['3'] = time.time() - start_time
    # print(df_hist)

    print(dict_runtime)



if __name__ == '__main__':
    compare_approaches()

    #test the functions
    # dict_hist = {'hod': [0, 5, 15, 0, 17, 18, 23],
    #             'volume': [512.4, 114, 28, 12, 324, 100, 100]
    #             }
    # df_hist = pd.DataFrame(dict_hist, columns=['hod', 'volume'])
    # #df_hist = None
    #
    # dict_runtime = {}
    #
    # start_time = time.time()
    # internet1 = InternetData(histData=df_hist)
    # print(internet1.tarData)
    # internet1.add_cost(how='1')
    # dict_runtime['1'] = time.time() - start_time
    # print(df_hist)

