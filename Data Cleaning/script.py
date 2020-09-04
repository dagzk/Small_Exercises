import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import codecademylib3_seaborn

# inspect states0.csv and check tidiness
state0 = pd.read_csv("states0.csv")
print(state0)

# combine all csv files sharing similar name
import glob
states = glob.glob("states*.csv")

# run each file with csv extension into a DataFrame and concatenate all DataFrames together
df_list = []
for filename in states:
  dataframe = pd.read_csv(filename)
  df_list.append(dataframe)
# combined DataFrame is us_census
us_census = pd.concat(df_list)

# check length
len(us_census)
print(us_census)

# display a summary of the table
print(us_census.info())
# display the column names
print(us_census.columns)
# display data types of each column
print(us_census.dtypes)
# Some are objects instead of int/float
# display first five rows
print(us_census.head())

# Remove $ sign from Income
# Remove character entries and convert to numerical
us_census.Income = us_census['Income'].replace('[\$]', '', regex=True)

us_census.Income = pd.to_numeric(us_census.Income)

# Separate Gender Population
# Create name_split column
name_split = us_census['name_split'] = us_census.GenderPop.str.split("_")
print(us_census)

# Create the 'Men' column
us_census['Men'] = us_census.name_split.str.get(0)

# Create the 'Women' column
us_census['Women'] = us_census.name_split.str.get(1)

# print first five rows
print(us_census.head())

# Remove character entries for Men and convert to numerical
us_census.Men = us_census['Men'].replace('[M]', '', regex=True)

us_census.Men = pd.to_numeric(us_census.Men)

# Same for Women
us_census.Women = us_census['Women'].replace('[F,]', '', regex=True)

us_census.Women = pd.to_numeric(us_census.Women)

# Fill the NaNs for Women with Formula
us_census["Women"] = us_census['Women'].fillna(us_census["TotalPop"]-us_census["Men"])
print(us_census)

# Print State with Women
print(us_census[['State','Women']])

# check for duplicates and drop them
duplicates = us_census.State.duplicated()
print(duplicates)
print(duplicates.value_counts())
# 9 duplicates found, drop them and save as new census
census = us_census.drop_duplicates(subset = ['State'])
# Check if correct
duplicates2 = census.State.duplicated()
print(duplicates2)
print(duplicates2.value_counts())
print(census)

# Scatter plot with Women VS Income
plt.scatter(census["Women"], census["Income"])
plt.show()

# display the column names
print(census.columns)

# Take the wanted columns into new census
new_census = census[['State','TotalPop','Hispanic','White','Income','Men','Women']]
print(new_census)

# Edit races (just Hispanic & White), take % off and make them numeric
new_census.Hispanic = new_census['Hispanic'].replace('[%]', '', regex=True)

new_census.Hispanic = pd.to_numeric(new_census.Hispanic)

new_census.White = new_census['White'].replace('[%]', '', regex=True)

new_census.White = pd.to_numeric(new_census.White)

print(new_census)

# Print other scatter plots

plt.scatter(new_census["White"], new_census["Income"])
plt.show()
plt.scatter(new_census["Hispanic"], new_census["Income"])
plt.show()