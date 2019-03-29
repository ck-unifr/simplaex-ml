# Simplaex ML coding task.
# The description can be found in README.md
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
            dictTarData['time-range'] = ['0-9', '9-18', '18-0']
            dictTarData['price'] = [5, 11, 19]
            tarData = pd.DataFrame(dictTarData, columns=['time-range', 'price'])

        self.hisData = histData
        self.tarData = tarData


    def add_cost(self, how = None):
        '''
        Create a method add_cost(how: String) that will return a historical dataframe with an additional column “cost”
        that will show how much money was spent for every hour in the historical data.

        There are multiple ways to do it in pandas, some very slow, some pretty fast. Come up with several solutions, include them all.

        The add_cost should choose the method based on the value of its ‘how’ parameter.

        :param how: a string
        :return: a dataframe
        '''

        def f(x, tarData):
            '''
            get correct price of each row of the historical data
            :param x: the 'hod' of historical data frame
            :param tarData: the tariffs dataframe
            :return: the correct price
            '''
            for index, row in tarData.iterrows():
                time_range = row['time-range'].split('-')
                if int(x) >= int(time_range[0]) and int(x) <= int(time_range[1]):
                    return row['price']
            return 0

        if how is None or how == '0':
            self.hisData['cost-per-mega'] = self.hisData['hod'].apply(f, args=[self.tarData])
            self.hisData['cost'] = self.hisData['cost-per-mega']*self.hisData['volume']
            self.hisData.drop(columns=['cost-per-mega'], inplace=True)
        elif how == '1':
            listCost = [0 for i in range(0, len(self.hisData.index))]
            for indexHis, rowHis in self.hisData.iterrows():
                hod = rowHis['hod']
                volume = rowHis['volume']
                for indexTar, rowTar in self.tarData.iterrows():
                    time_range = rowTar['time-range'].split('-')
                    if int(hod) >= int(time_range[0]) and int(hod) <= int(time_range[1]):
                        listCost[indexHis] = (rowTar['price']*volume)
                        break

            self.hisData['cost'] = pd.Series(listCost, index=self.hisData.index)

        return self.hisData




def compare_approaches():
    '''
    Create a method compare_approaches() that compares the performance of all of your solutions and returns the results in a dictionary {“method_name”: time}
    '''

    dict_hist = {'hod': [0, 5, 15, 0, 17],
                 'volume': [512.4, 114, 28, 12, 324]
                 }
    df_hist = pd.DataFrame(dict_hist, columns=['hod', 'volume'])
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

    print(dict_runtime)




if __name__ == '__main__':
    compare_approaches()