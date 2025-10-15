from imports import *

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Loading of the dataset via pandas
    kc_data = df.copy()

    # We look at the first 5 lines of our data set.
    # We want to make sure that the data has been read in correctly.
    print(kc_data.head())

    print(kc_data.shape)

    print(kc_data.info())

    print(kc_data.nunique())

    print(kc_data.describe().round(2))

    # Output of the line in which the condition "bedrooms = 33" is present.
    print(kc_data.query('bedrooms == 33'))

    # We will drop this row
    kc_data.drop(15856, axis=0, inplace=True)

    # We replace "?" with Nan
    kc_data['sqft_basement'] = kc_data['sqft_basement'].replace('?', np.nan)
    # And we change the dtype of the column "sqft_basement" to float
    kc_data['sqft_basement'] = kc_data['sqft_basement'].astype(float)

    # We are calculating the "sqft_basement" by substracting sqft_above of sqft_living
    kc_data.eval('sqft_basement = sqft_living - sqft_above', inplace=True)

    #missing values
    # Summation of the missing values and calculation of the missing values as a percentage
    missing_values = pd.DataFrame(kc_data.isnull().sum(),columns=['count'])
    missing_values['percentage'] = (missing_values['count']/kc_data.shape[0]*100).round(2)
    missing_values.query('count != 0')

    # We display how often the different values of the variable occur.
    kc_data['view'].value_counts()

    # We replace Nan values in "view" with the most frequent expression (0)
    kc_data['view'] = kc_data['view'].fillna(0)

    # We display how often the different values of the variable occur.
    kc_data.waterfront.value_counts()

    # We replace Nan values in "waterfront" with the most frequent expression (0)
    kc_data.waterfront = kc_data.waterfront.fillna(0)

    # We again look at the missing data
    missing_values = pd.DataFrame(kc_data.isnull().sum(),columns=['count'])
    missing_values['percentage'] = missing_values['count']/kc_data.shape[0]*100
    missing_values.query('count != 0')



    # We will create an empty list in which we will store values
    last_known_change = []

    # For each row in our data frame, we look at what is in the column "yr_renovated".
    for idx, yr_re in kc_data.yr_renovated.items():
        # if "yr_renovated" is 0 or contains no value, we store the year of construction of the house in our empty listes ab
        if str(yr_re) == 'nan' or yr_re == 0.0:
            last_known_change.append(kc_data.yr_built[idx])
        # if there is a value other than 0 in the column "yr_renovated", we transfer this value into our new list
        else:
            last_known_change.append(int(yr_re))

    # We create a new column and take over the values of our previously created list
    kc_data['last_known_change'] = last_known_change

    # We delete the "yr_renovated" and "yr_built" columns
    kc_data.drop("yr_renovated", axis=1, inplace=True)
    kc_data.drop("yr_built", axis=1, inplace=True)
    
    return kc_data