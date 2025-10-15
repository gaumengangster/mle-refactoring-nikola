from imports import *

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    kc_data = df.copy()
    kc_data['sqft_price'] = (kc_data.price/(kc_data.sqft_living + kc_data.sqft_lot)).round(2)
    
    kc_data[kc_data['sqft_price']==kc_data['sqft_price'].max()]
    
    kc_data[kc_data['price']==kc_data['price'].max()]
    
    # Absolute difference of latitude between centre and property
    kc_data['delta_lat'] = np.absolute(47.62774- kc_data['lat'])
    # Absolute difference of longitude between centre and property
    kc_data['delta_long'] = np.absolute(-122.24194-kc_data['long'])
    # Distance between centre and property
    kc_data['center_distance']= ((kc_data['delta_long']* np.cos(np.radians(47.6219)))**2 + kc_data['delta_lat']**2)**(1/2)*2*np.pi*6378/360
    
    water_distance = []
    # For each row in our data frame we now calculate the distance to the seafront
    for idx, lat in kc_data.lat.items():
        ref_list = []
        for x,y in zip(list(water_list.long), list(water_list.lat)):
            ref_list.append(dist(kc_data.long[idx], kc_data.lat[idx],x,y).min())
        water_distance.append(min(ref_list))
        
    # wir erstellen eine neue Spalte und übernehmen die Werte unserer vorher erstellten Liste
    kc_data['water_distance'] = water_distance
    
    # we create a new column and take over the values of our previously created list
    print(kc_data.describe().round(2))
    
    return kc_data
    
# This function helps us to calculate the distance between the house overlooking the seafront and the other houses.
def dist(long, lat, ref_long, ref_lat):
    '''dist computes the distance in km to a reference location. Input: long and lat of 
    the location of interest and ref_long and ref_lat as the long and lat of the reference location'''
    delta_long = long - ref_long
    delta_lat = lat - ref_lat
    delta_long_corr = delta_long * np.cos(np.radians(ref_lat))
    return ((delta_long_corr)**2 +(delta_lat)**2)**(1/2)*2*np.pi*6378/360