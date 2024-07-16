
"""The dataset contains data for 344 penguins. 
There are 3 different species of penguins in this dataset, collected from 3 islands in the Palmer Archipelago, Antarctica.

Data were collected and made available by Dr. Kristen Gorman and the Palmer Station, Antarctica LTER,
a member of the Long Term Ecological Research Network. 
(Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data. 
R package version 0.1.0. https://allisonhorst.github.io/palmerpenguins/.doi:10.5281/zenodo.3960218.) 
Accessed via the Seaborn datasets package. 

1.	Create a Python script to do the following:
a.	Load the Penguins data set from ‘penguins.csv’ file in to a dataframe 'penguins'.
b.	Split the data by ‘species’ and ‘island’ (The syntax for combining criteria with a logical ‘and’ in pandas is:
     “my_df[(my_df[my_col]==y)&( penguins[my_2nd_col]==x)]” 
    where my_df is a DataFrame, my_col and my_2nd_col are valid columns names in my_df, and x and y are variables).
c.	Write each subset of data to a .csv file named 'species_island.csv' where species and island 
    denote the appropriate split of the data
d.	Display a summary of each subset of the data using .describe().
e.	Create a DataFrame 'body_mass', with index equal to the species, and columns equal to the isalnd and populate with
    the mean body mass (in grams) for each subset of penguins
f.	The command ‘df.max()’ gives the maximum value in a DataFrame. 
    Assign a tuple 'heaviest' equal to the (species, island) where the penguins are on average heaviest.
g. Output a sentence to indicate which subset of penguins are on average the heaviest.
"""

import pandas as pd

#1
#a.

penguins = pd.read_csv('penguins.csv')
print(penguins.tail())

species = penguins['species'].unique()
island = penguins['island'].unique()

body_mass = pd.DataFrame(index=species, columns=island)
heaviest = pd.DataFrame(index=species, columns=island)


for i in island:
    for s in species:
        subset = penguins[(penguins['island']=='Torgersen')&(penguins['species']=='Adelie')]
        if not subset.empty:

            filename = f"{s}_{i}.csv"
            subset.to_csv(filename, index=False)

            print(f"Summary for {s} on {i}:")
            print(subset.describe(), "\n")

            mean_body_mass = subset['body_mass_g'].mean()
            body_mass.at[s, i] = mean_body_mass

            mass_max = subset[body_mass].max
            heaviest.at[s, i] = mass_max


heaviest_tuple = body_mass.idxmax().max()
print(f"\nThe (species, island) where the penguins are on average heaviest: {heaviest_tuple}")




