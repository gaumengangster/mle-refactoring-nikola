from imports import *
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Import your custom functions
from data_cleaning import clean_data
from feature_engineering import engineer_features

import os
import skops.io as sio

if __name__ == "__main__":
    main()
    
def main():
    # Load raw data
    df = pd.read_csv("data/King_County_House_prices_dataset.csv")

    pipeline = Pipeline(steps=[
        ("cleaning", FunctionTransformer(clean_data)),
        ("feature_engineering", FunctionTransformer(engineer_features))
    ])
    
    print("🔹 Running preprocessing pipeline...")
    df_processed = pipeline.fit_transform(df)
    print(f"✅ Data processed. Shape: {X_processed.shape}")
    
    # Define columns to drop (data leakage or not useful)
    drop_lst = ['price', 'sqft_price', 'date', 'delta_lat', 'delta_long']

    # Select all feature columns except the ones above
    all_features = [x for x in df_processed.columns if x not in drop_lst]
    
    # X contains all descriptive variables defined above
    X = df_processed[all_features]
    # we define y (our dependent variable): we take the price
    y = df_processed.price
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # we can look at how much data is in each dataset
    print("X_train (features for the model to learn from): ", X_train.shape)
    print("y_train (labels for the model to learn from): ", y_train.shape)
    print("X_test (features to test the model's accuracy against): ", X_test.shape)
    print("y_test (labels to test the model's accuracy with): ", y_test.shape)
    
    # We determine the model, there must be 2 round brackets behind the model name!
    model_lin_reg = LinearRegression()
    
    # We determine which variables we pass to the model
    variables = ['grade',]
    
    # Training of the model
    model_lin_reg.fit(X_train[variables], y_train)
    
    # We look at how well our model performs on the test data
    print('adj. R^2:', round(1-(1-model_lin_reg.score(X_test[variables], y_test))*(X_test.shape[0]- 1)/(X_test.shape[0]-len(variables)-1), 2))
    
    # We determine the model, there must be 2 round brackets behind the model name!
    model_lin_reg = LinearRegression()
    
    # We determine which variables we pass to the model
    variables = ['grade','last_known_change']
    
    # we train the model
    model_lin_reg.fit(X_train[variables], y_train)
    
    # We look at how well our model performs on the test data
    print('adj. R^2:', round(1-(1-model_lin_reg.score(X_test[variables], y_test))*(X_test.shape[0]- 1)/(X_test.shape[0]-len(variables)-1), 2))
    
    # We want to create only polynomial variables of second order (^2)
    poly = PolynomialFeatures(2)
    
    # create a copy of the Train and Test data
    X_train_poly = X_train.copy()
    X_test_poly = X_test.copy()

    # drop the id column
    X_train_poly = X_train_poly.drop(columns=['id'])
    X_test_poly = X_test_poly.drop(columns=['id'])
    
    # We create new variables by calling poly
    X_train_sq = poly.fit_transform(X_train_poly)

    # We have to do the same for our test data, of course
    X_test_sq = poly.transform(X_test_poly)

    # We determine the model, there must be 2 round brackets behind the model name!
    model_lin_reg = LinearRegression()

    # We also train the model with squared variables
    model_lin_reg.fit(X_train_sq, y_train)

    # We look at how well our model performs on the test data
    print('adjusted R^2:', round(1-(1-model_lin_reg.score(X_test_sq, y_test))*(X_test_sq.shape[0]- 1)/(X_test_sq.shape[0]-X_test_sq.shape[1]-1), 2))

    # Error analysis
    # In order to better analyse the errors of our model, we create a new dataframe with the
    # columns "price" (the real price), as well as the latitudes and longitudes
    y_predictions = model_lin_reg.predict(X_test_sq)
    df_error = pd.DataFrame(y_test)
    df_error['latitude'] = X_test['lat']
    df_error['longitude'] = X_test['long']
    df_error['id'] = X_test['id']
    df_error.head(2)

    # To add the predicted price as a column as well, we must first reset the index
    df_error.reset_index(inplace=True, drop=True)
    df_error.head(2)

    # Now we can also add the predicted price as a column and calculate the difference
    df_error['price_prediction'] = y_predictions.round(2)
    df_error['price_difference'] = (df_error['price_prediction'] - df_error['price']).round(2)
    df_error['price_difference_procent'] = ((df_error['price_difference']/df_error['price'])*100).round(2)
    df_error.head(2)

    df_error[df_error['price_difference_procent']==df_error['price_difference_procent'].max()]

    X_test[X_test['id']==9272202260]


    # Create the directory if it doesn't exist
    os.makedirs("model", exist_ok=True)

    with open('model/model.bin', 'wb') as f_out:
        sio.dump(elastic, f_out)