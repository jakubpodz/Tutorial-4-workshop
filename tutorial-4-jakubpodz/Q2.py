"""These questions use data from the Fama and French data library on stock market returns:
 http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/index.html
 Note that these questions are designed to test your understanding of the material covered on the course to date.
 We will learn faster and more efficient ways of doing some of these tasks in future lectures.

a.	Load the data from the ‘ff_monthly.csv’ file into a variable 'monthly_returns',
    use the first column as an index (this contains the year and month of the data as a string)
b.	Create a new column ‘Mkt’ as ‘Mkt-RF’ + ‘RF’
c.	Create two new columns in the loaded DataFrame, ‘Month’ and ‘Year’ to contain the year and month
    of the dataset extracted from the index column.
d.	Create a new DataFrame 'summary_stats' with columns ‘Mean’ and ‘Standard Deviation’ and the full set of years from (b) above as an index.
e.	Write a function which accepts (r_m,s_m) the monthy mean and standard deviation of a return series and
    returns a tuple (r_a,s_a), the annualised mean and standard deviation.
    Use the formulae: r_a = (1+r_m)**12 -1, and s_a = s_m * 12**0.5.
f.	Loop through each year in the data, and calculate the annualised mean and standard deviation of the new ‘Mkt’ column,
    storing each in the newly created DataFrame.
    Note that the values in the input file are % returns, and need to be divided by 100 to return decimals
    (i.e the value for August 2022 represents a return of -3.78%).
g.	Print the DataFrame and output it to a csv file 'summary_stats.csv'.

    Harder...

h.	The ‘Great Moderation’ (GM) period is often defined as the period between the January 2004 and June 2007 (inclusive).
    Using a list comprehensions, build a dictionary with keys (‘GM’,’PreGM’,’PostGM’) and set each value set to be a list
    of months in the index which are counted in each period (for the list use the syntax [i for i in collection if condition])
i.	Construct a series 'GMS' containing the (monthly) standard deviation of returns in each period.
    Print the series, and output the series to ‘Moderation.csv’.

j.	Was monthly US stock market volatility lower in the GM period than before / after?
"""

import pandas as pd

monthly_returns = pd.read_csv('ff_monthly.csv', index_col=0)

monthly_returns['Mkt'] = monthly_returns['Mkt-RF'] + monthly_returns['RF']

monthly_returns.index = monthly_returns.index.astype(str)
monthly_returns['Year'] = monthly_returns.index.str[:4]
monthly_returns['Month'] = monthly_returns.index.str[4:]

summary_stats = pd.DataFrame()
summary_stats['Mean'] = monthly_returns.groupby('Year')['Mkt'].mean()
summary_stats['Standard Deviation'] = monthly_returns.groupby('Year')['Mkt'].std()

def annualised_mean (r_m,s_m):
    r_a = (1+r_m)**12 -1
    s_a = s_m * 12**0.5
    return r_a,s_a

summary_stats['Annualised Mean'] = 0.0
summary_stats['Annualised Standard Deviation'] = 0.0

for year in summary_stats.index:
    ann_mean1, ann_std1 = annualised_mean(summary_stats.loc[year, 'Mean'], summary_stats.loc[year, 'Standard Deviation'])
    ann_mean = ann_mean1/100
    ann_std = ann_std1/100
    summary_stats.loc[year, 'Annualised Mean'] = ann_mean
    summary_stats.loc[year, 'Annualised Standard Deviation'] = ann_std

# Display the summary statistics
print(summary_stats)

summary_stats.to_csv('summary_stats.csv')

gm_start = '200401'
gm_end = '200706'

periods = {
    'GM':[i for i in monthly_returns.index if gm_start <= i <= gm_end ]
    ,'PreGM':[i for i in monthly_returns.index if i < gm_start]
    ,'PostGM':[i for i in monthly_returns.index if i > gm_end]
}

print(periods)

GMS = pd.Series(periods['GM']) 

GMS = pd.Series({
    'GM': monthly_returns.loc[periods['GM'], 'Mkt'].std(),
    'PreGM': monthly_returns.loc[periods['PreGM'], 'Mkt'].std(),
    'PostGM': monthly_returns.loc[periods['PostGM'], 'Mkt'].std()
})

# Print the series
print(GMS)

# Output the series to 'Moderation.csv'
GMS.to_csv('Moderation.csv', header=['Standard Deviation'])

print("\nComparison of Monthly US Stock Market Volatility:")
print(f"Volatility during GM period: {GMS['GM']:.6f}")
print(f"Volatility before GM period: {GMS['PreGM']:.6f}")
print(f"Volatility after GM period: {GMS['PostGM']:.6f}")

is_lower = (GMS['GM'] < GMS['PreGM']) and (GMS['GM'] < GMS['PostGM'])
if is_lower:
    print("Monthly US stock market volatility was lower during the GM period than before and after.")
else:
    print("Monthly US stock market volatility was not lower during the GM period than before and after.")


"""

Comparison of Monthly US Stock Market Volatility:
Volatility during GM period: 2.222642
Volatility before GM period: 5.543343
Volatility after GM period: 4.731873
Monthly US stock market volatility was lower during the GM period than before and after.

"""

