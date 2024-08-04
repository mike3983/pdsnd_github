import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'all-project-files/chicago.csv',
              'new york city': 'all-project-files/new_york_city.csv',
              'washington': 'all-project-files/washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def user_filters():
    """
     Asks user to specify a city, month, and day to analyze.
     Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello!! Time to explore some bikeshare data!!')

    city = input('Which city data do you want to examine: Washington, Chicago, or New York City?').lower()
    while city not in ('washington', 'chicago', 'new york city'):
        city = input('The city you have entered is not recognized. Please enter: Washington, Chicago, or New York City: ').lower()
    
    month = input('Which month data would you like to see? We have data from January to June. If you would like to see all months, enter ALL: ').lower()
    while month not in MONTHS:
        month = input('This is not a valid month. Please enter a month from January to June: ').lower()
    
    day = input('Which day of the week would you like to view? If you would like to see all days, please enter ALL: ').lower()
    while day not in DAYS:    
        day = input('This is not a valid day. Please try again: ').lower()
    
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """    
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        month = MONTHS.index(month) + 1
    df = df.loc[df['month'] == month]
    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    
    print('\Calculating the Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('The most common month is: ' +  MONTHS[common_month].title())

    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is: ' + common_day_of_week)

    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: ' + str(common_start_hour))
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ' + common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: ' + common_end_station)
 
    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station: ' + str(frequent_combination.split("||")))
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ' + str(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ' + str(mean_travel_time))
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    type_of_user = df['User Type'].value_counts()
    print('The count of user types: \n' + str(type_of_user))
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        gender = df['Gender'].value_counts()
        print('The count of user gender is: \n' + str(gender))
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth is: {}\n'.format(earliest_birth))
        print('Most recent birth is: {}\n'.format(most_recent_birth))
        print('Most common birth is: {}\n'.format(most_common_birth))
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """
    Displays raw data on user request.
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five rows of raw data? Enter Yes or No.\n').lower()
        if view_raw_data != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next + 5])


def main():
    while True:
        city, month, day = user_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            view_raw_data = input('\nWould you like to view first five rows of raw data? Enter yes or no.\n').lower()
            if view_raw_data != 'yes':
                break
            raw_data(df)
            break
        restart = input('\nWould you like to restart? Enter Yes or No.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()

