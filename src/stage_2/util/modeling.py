import numpy as np
from tqdm import tqdm
from hashlib import md5
EMPTY_VALUE = "Unknown"

def get_car_foreign_keys(
    df,
    car_dim,
    year_label=None,
    mileage_label=None, 
    make_label=None,
    model_label=None,
    fuel_label=None,
    cylinders_label=None,
    engine_label=None,
    transmission_label=None
):
    keys=[]
    for row in tqdm(df.index):
        year = df.loc[row, year_label] if year_label!=None else EMPTY_VALUE
        mileage = df.loc[row, mileage_label] if mileage_label!=None else EMPTY_VALUE
        make = df.loc[row, make_label] if make_label!=None else EMPTY_VALUE
        model = df.loc[row, model_label] if model_label!=None else EMPTY_VALUE
        fuel = df.loc[row, fuel_label] if fuel_label!=None else EMPTY_VALUE
        cyl = df.loc[row, cylinders_label] if cylinders_label!=None else EMPTY_VALUE
        eng = df.loc[row, engine_label] if engine_label!=None else EMPTY_VALUE
        trans = df.loc[row, transmission_label] if transmission_label!=None else EMPTY_VALUE

        temp_df = car_dim[ car_dim.vehicle_year == year ]
        temp_df = temp_df[ temp_df.vehicle_model == model ]
        temp_df = temp_df[ temp_df.vehicle_make == make ]
        temp_df = temp_df[ temp_df.vehicle_mileage == mileage ]
        temp_df = temp_df[ temp_df.vehicle_number_cylinders==cyl ]
        temp_df = temp_df[ temp_df.vehicle_engine==eng ]

        keys.append(
            temp_df[
                (temp_df.vehicle_transmission==trans) &
                (temp_df.vehicle_fuel==fuel)
            ].index[0]
        )
    return keys



def get_date_foreign_key(
    df,
    date_dim,
    date_label=None
):
    keys=[]
    for row in tqdm(df.index):
        date = df.loc[row, date_label] if date_label!=None else EMPTY_VALUE
        
        keys.append(    
            date_dim[ 
                (date_dim.date_full_description==date)
            ].index[0]
        )
    return keys



def get_review_foreign_key(
    df,
    review_dim,
    description_label=None,
    username_label=None,
    title_label=None
):
    keys=[]
    for row in tqdm(df.index):
        item = df.loc[row]
        
        descript = item[description_label] if description_label!= None else EMPTY_VALUE
        user = item[username_label] if username_label!= None else EMPTY_VALUE
        title = item[title_label] if username_label!=None else EMPTY_VALUE
        
        temp_df = review_dim[
            review_dim.review_hash==int(md5(descript.encode()).hexdigest(), 16)
        ]
        temp_df = temp_df[
            temp_df.review_title==title
        ]
        temp_df = temp_df[
            temp_df.review_username==user
        ]
        keys.append(
            temp_df[ 
                (temp_df.review_description==descript)
            ].index[0]
        )
    return keys




def get_loc_foreign_key(
    df,
    loc_dim,
    lat_label=None,
    long_label=None,
    state_label=None
):
    keys=[]
    for row in tqdm(df.index):
        item = df.loc[row]
        
        lat = item[lat_label] if lat_label!= None else EMPTY_VALUE
        long = item[long_label] if long_label!= None else EMPTY_VALUE
        state = item[state_label] if state_label!=None else EMPTY_VALUE
        
        temp_df = loc_dim[(loc_dim.location_state == state)]
        keys.append(
            temp_df[
                #(loc_dim.location_state == df.loc[row, state_label]) &
                (temp_df.location_lat==lat) &
                (temp_df.location_long==long)
            ].index[0]
        )
    return keys



def get_fuel_prices(
    df,
    fuel_prices,
    date_label,
    fuel_label,
):
    prices = []
    for row in tqdm(df.index):
        item = df.loc[row]
        price = fuel_prices[
            (fuel_prices["Start Date"]<=item[date_label]) &
            (fuel_prices["Stop Date"]>item[date_label])
        ]
        try:
            if item[fuel_label]=="gas":
                prices.append(
                    price["Gasoline Price"].item()
                )
            elif item[fuel_label]=="diesel":
                prices.append(
                    price["Diesel Price"].item()
                )
            else:
                prices.append(0)
        except:
            prices.append(EMPTY_VALUE)
    return prices



def get_sales_fact_table(
    df,
    price_label, 
    price_of_fuel, 
    car_keys, 
    date_sold_keys, 
    date_post_keys, 
    location_keys
):
    facts = pd.DataFrame(columns =["vehicle_key", "date_sold_key", "location_key", "fuel_price", "sales_price", "date_posted_key"])
    
    facts["vehicle_key"] = car_keys
    facts["location_key"] = location_keys
    facts["date_sold_key"] = date_sold_keys
    facts["sales_price"] = df[price_label].tolist()
    facts["fuel_price"] = price_of_fuel
    facts["date_posted_key"] = date_post_keys
    
    return facts


def get_review_fact_table(
    df,
    rating_label,  
    car_keys, 
    date_keys, 
    review_keys
):
    facts = pd.DataFrame(columns =["vehicle_key", "date_key", "review_key", "review_rating"])
    
    facts["vehicle_key"] = car_keys
    facts["date_key"] = date_keys
    facts["review_rating"] = df[rating_label].tolist()
    facts["review_key"] = review_keys
    
    return facts





"""

Same operations with numpy searching instead of pandas


Numpy has a lot less overhead


"""


def get_loc_foreign_key_np(
    df,
    loc_dim,
    lat_label=None,
    long_label=None,
    state_label=None
):
    keys=[]
    index = df.index
    cols = [
        df.columns.get_loc(c) if c!=None else EMPTY_VALUE for c in [
            lat_label, long_label, state_label
        ]
    ]
    df = df.to_numpy()
    loc_dim = loc_dim.to_numpy()
    for row in tqdm(range(df.shape[0])):
        item = df[row]
        
        lat = item[cols[0]] if cols[0] != EMPTY_VALUE else EMPTY_VALUE
        long = item[cols[1]]  if cols[1] != EMPTY_VALUE else EMPTY_VALUE
        state = item[cols[2]]  if cols[2] != EMPTY_VALUE else EMPTY_VALUE
        
        temp_df = loc_dim[(loc_dim[:, 0] == state)]
        keys.append(
            index[
                np.where(
                    (temp_df[:, 1]==lat) &
                    (temp_df[:, 2]==long)
                )[0]
            ].item()
        )
    return keys


def get_date_foreign_key_np(
    df,
    date_dim,
    date_label=None
):
    keys=[]
    index = df.index
    cols = [
        df.columns.get_loc(c) if c!=None else EMPTY_VALUE for c in [
            date_label
        ]
    ]
    df = df.to_numpy()
    date_dim = date_dim.to_numpy()
    
    for row in tqdm(range(df.shape[0])):
        date = df[row, cols[0]] if cols[0] != EMPTY_VALUE else EMPTY_VALUE
        
        keys.append(    
            index[
                np.where(
                    date_dim[:,0]==date
                )[0]
            ]
        )
    return keys


def get_car_foreign_keys_np(
    df,
    car_dim,
    year_label=None,
    mileage_label=None, 
    make_label=None,
    model_label=None,
    fuel_label=None,
    cylinders_label=None,
    engine_label=None,
    transmission_label=None
):
    keys=[]
    
    for _, item in tqdm(df.iterrows()):
        year = item[year_label] if year_label!=None else EMPTY_VALUE
        mileage = item[mileage_label] if mileage_label!=None else EMPTY_VALUE
        make = item[make_label] if make_label!=None else EMPTY_VALUE
        model = item[model_label]  if model_label!=None else EMPTY_VALUE
        fuel = item[fuel_label] if fuel_label!=None else EMPTY_VALUE
        cyl = item[cylinders_label] if cylinders_label!=None else EMPTY_VALUE
        eng = item[engine_label] if engine_label!=None else EMPTY_VALUE
        trans = item[transmission_label] if transmission_label!=None else EMPTY_VALUE
            
        
        
        year_cond = car_dim.vehicle_year.to_numpy()==year
        temp_df = car_dim[year_cond]
        model_cond = temp_df.vehicle_model.to_numpy()==model
        temp_df = temp_df[model_cond]
        make_cond = temp_df.vehicle_make.to_numpy()==make
        temp_df = temp_df[make_cond]
        fuel_cond = temp_df.vehicle_fuel_type.to_numpy()==fuel
        temp_df = temp_df[fuel_cond]
        mileage_cond = temp_df.vehicle_mileage.to_numpy()==mileage
        temp_df = temp_df[mileage_cond]
        cyl_cond = temp_df.vehicle_number_cylinders.to_numpy()==cyl
        temp_df = temp_df[cyl_cond]
        eng_cond = temp_df.vehicle_engine.to_numpy()==eng
        temp_df = temp_df[eng_cond]

        keys.append(
            #car_dim[cond].index[0]
            temp_df[temp_df.vehicle_transmission==trans].index[0]
        )

    return keys


def get_review_foreign_key_np(
    df,
    review_dim,
    description_label=None,
    username_label=None,
    title_label=None
):
    keys=[]
    
    
    for _, item in tqdm(df.iterrows()):        
        descript = item[description_label] if description_label!= None else EMPTY_VALUE
        user = item[username_label] if username_label!= None else EMPTY_VALUE
        title = item[title_label] if username_label!=None else EMPTY_VALUE
        
        hash_cond = review_dim.review_hash.to_numpy()==int(md5(descript.encode()).hexdigest(), 16)
        temp_df = review_dim[hash_cond]
        
        user_cond = temp_df.review_username.to_numpy()==user
        temp_df = temp_df[user_cond]
        
        title_cond = temp_df.review_title.to_numpy()==title
        temp_df = temp_df[title_cond]
        keys.append(
            temp_df[ 
                (temp_df.review_description==descript) 
            ].index[0]
        )
    return keys