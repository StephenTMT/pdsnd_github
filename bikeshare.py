import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Enter "Exit" at any point to close the program')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("What city would you like to analyze, Chicago, New York City, or Wasington?\n")
        if city.lower().strip() in CITY_DATA:
            city = city.lower().strip()
            break
        elif city.lower().strip() == "exit":
            exit()
        else:
            print("Input does not match any option, please try again.")


    # get user input for month (all, january, february, ... , june)
    while True:
        filter = input("Would you like to filter the data by month, day, or not at all? Enter \"None\" if not at all\n")
        if filter.lower().strip() == "month":
            filter = "month"
            break
        elif filter.lower().strip() == "day":
            filter = "day"
            break
        elif filter.lower().strip() == "none":
            filter = "none"
            month = "all"
            day = "all"
            break
        elif filter.lower().strip() == "exit":
            exit()
        else:
            print("Input does not match any option, please try again.")

    if filter == "month":
    # get user input for month (all, january, february, ... , june)
        while True:
            month = input("Which month - January, February, March, April, May, or June?\n")
            month_lst = ["january", "february", "march", "april", "may", "june"]

            if month.lower().strip() in month_lst:
                month = month.lower().strip()
                month = month_lst.index(month) + 1
                day = "all"
                break
            elif month.lower().strip() == "exit":
                exit()
            else:
                print("Input does not match any option, please try again.")

    if filter == "day":
    # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
            day_list = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

            if day.lower().strip() in day_list:
                day = day.lower().strip()
                month = "all"
                break
            elif day.lower().strip() == "exit":
                exit()
            else:
                print("Input does not match any option, please try again.")

    print('-'*40)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    if month != "all":
        df = df[df["Start Time"].dt.month == month]

    if day != "all":
        df = df[df["Start Time"].dt.weekday_name == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_lst = ["January", "February", "March", "April", "May", "June"]
    top_month = df["Start Time"].dt.month.mode()[0]
    print("The most common month was", month_lst[top_month - 1])

    # display the most common day of week
    top_day = df["Start Time"].dt.weekday_name.mode()[0]
    print("The most common starting day of the week was", top_day)

    # display the most common start hour
    top_hour = df["Start Time"].dt.hour.mode()[0]
    print("The most common starting hour was", top_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df["Start Station"].mode()[0]
    print("The most common starting station was", top_start_station)

    # display most commonly used end station
    top_end_station = df["End Station"].mode()[0]
    print("The most common ending station was", top_end_station)

    # display most frequent combination of start station and end station trip
    top_combo = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print("The most common combiation of stations was", top_combo[0] + ' and ' + top_combo[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df["Trip Duration"].sum()
    print("The total trip duration was", total_time, "seconds")

    # display mean travel time
    total_time = df["Trip Duration"].mean()
    print("The total trip duration was", total_time, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_counts = df["User Type"].value_counts()
    print("There were", type_counts["Subscriber"], "subscribers and", type_counts["Customer"], "customers in this time period")

    # Display counts of gender
    if 'Gender' in df:
        type_counts = df["Gender"].value_counts()
        print("There were", type_counts["Male"], "men and", type_counts["Female"], "women users in this time period")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df["Birth Year"].min()
        latest_year = df["Birth Year"].max()
        most_common_year = df["Birth Year"].mode()

        print("The earliest birth year was", int(earliest_year))
        print("The most recent birth year was", int(latest_year))
        print("The most common birth year was", int(most_common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    current_row = 0

    # Display raw data to user until they request to stop
    while True:
        next_set = df[current_row:current_row+5]
        current_row = current_row + 5
        print(next_set)
        while True:
            check = input("Would like to see more data? Enter \"Yes\" if so, otherwise enter \"Stop\"\n")
            if check.lower().strip() == 'yes' or check.lower().strip() == 'stop':
                break
            else:
                print("Input does not match any option, please try again.")
        if check.lower().strip() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter \"Yes\" or \"No\".\n')
            if restart.lower().strip() == 'yes' or restart.lower().strip() == 'no':
                break
            else:
                print("Input does not match any option, please try again.")
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
	main()
