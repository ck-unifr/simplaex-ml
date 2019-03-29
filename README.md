# simplaex-ml

Simplaex ML Coding Task

 Problem Description
Assume, we have historical data about how many megabytes were downloaded from the Internet by some person, split by hour. For each row of data we have two values: hour of day (integer, 0 to 23; we don’t care about the exact day when that happened) and volume in megabytes (float, 0 to 1000):


HoD, Volume

0, 512.4

5, 114

15, 28

0, 12

17, 324



Let’s also assume that this person was paying by traffic volume and the tariffs differ depending on the hour of the day, as follows:


Time range, Price in cents per megabyte

0:00 to 9:00, 5

9:00 to 18:00, 11

18:00 to 0:00, 19


Tasks
Write a class InternetData: 


1. The initialization method should take as an input two pandas dataframes: 

one with the historical data -  If the historical data is not passed it should be generated randomly for a year, i.e., 365 * 24 rows, with two columns — hour of day and some random volume of data. 

another with tariffs - If the tariffs dataframe is not passed, the one from the description should be used. You can define the format of the tariffs dataframe by yourself.


2. Create a method add_cost(how: String) that will return a historical dataframe with an additional column “cost” that will show how much money was spent for every hour in the historical data. 

There are multiple ways to do it in pandas, some very slow, some pretty fast. Come up with several solutions, include them all.

The add_cost should choose the method based on the value of its ‘how’ parameter.


3. Create a method compare_approaches() that compares the performance of all of your solutions and returns the results in a dictionary {“method_name”: time}
