#Uni quiz solution but using pandas (COMP9021 do not use pandas for their python lectures)

# Uses National Data on the relative frequency of first names in the
# population of U.S. births, stored in a directory "names", in files
# named "yobxxxx.txt with xxxx (the year of birth)
# ranging from 1880 to 2020.
# The "names" directory is a subdirectory if the working directory.
# Prompts the user for a male first name, and finds out the years
# when this name was most popular in terms of ranking amongst male names.
# Displays an error message if the name is not recorded for any year.
# Otherwise, displays the ranking, and the years in decreasing
# order of frequency, computed, for a given year, as the count of
# the name for the year divided by the sum of the counts of all
# male names for the year.
# Years are displayed at most 5 per line, separated by a single space,
# with 4 leading spaces before the first year on each line.
#
# You CANNOT use pandas for this quiz; if you do, your submission
# will not be assessed.

import pandas as pd
from pathlib import Path

path = Path('names')
gender = Path('gender')
male_subdir = gender / 'male_subdir' #gender = path = / 'gender'
female_subdir = gender / 'female_subdir'

targeted_first_name = input('Enter a male first name: ')

#male/female names be seperated into two different files
for filename in path.glob('*.txt'):
    #in original code 
    #with open(fname) as file:
    #   csv_file = csv.reader(file)
    #   first_name, gender, count = 0,0,0
    df = pd.read_csv(filename, header = None, names = ['first_name', 'gender', 'count'])
    male_df = df[df['gender'] == 'M']
    female_df = df[df['gender'] == 'F']

    #reference: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
    male_df.to_csv(male_subdir / filename.name, index = False)
    female_df.to_csv(female_subdir / filename.name, index = False)

rank = float('inf')
best_years =[]
frequency = []

for filename in sorted(male_subdir.glob('*.txt')):
    year = int(filename.name[3:7])
    df = pd.read_csv(filename)

    num_male = df.shape[0]
    recorded_count = df[df['firstname'] == targeted_first_name]['count'].sum()
    tally = df['count'].sum() #sum of males

    if num_male < rank:
        rank = num_male
        best_years = [year]
        frequency = [recorded_count / tally] 
    elif num_male == rank:
        rank +=1
        best_years.append(year)
    
    frequency.append(recorded_count / tally)

#main
if best_years:
    print("   ", end="")
    # enumerate() in python, (index, sequence)
    for i, years in enumerate(best_years, start = 1):
        print(f'{year}', end = " " if (i % 5) != 0 and i != len(best_years) else "\n    ")

    print(f'\nBy decreasing order of frequency, {targeted_first_name} was most popular in the following years: {best_years}') 
    print(f'Its rank was {rank}.')

else:
    print(f'{targeted_first_name} is not a male first name in my records.')
