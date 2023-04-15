from tqdm import tqdm
from hashlib import md5


def get_car_foreign_keys(
    df,
    car_dim,
    year_label=None,
    mileage_label=None, 
    make_label=None,
    model_label=None,
    fuel_label=None,
):
    keys=[]
    for row in tqdm(df.index):
        try:
            year = df.loc[row, year_label] if year_label!=None else "Unknown"
            mileage = df.loc[row, mileage_label] if mileage_label!=None else "Unknown"
            make = df.loc[row, make_label] if make_label!=None else "Unknown"
            model = df.loc[row, model_label] if model_label!=None else "Unknown"
            fuel = df.loc[row, fuel_label] if fuel_label!=None else "Unknown"
            
            temp_df = car_dim[(car_dim.vehicle_year == year)]
            temp_df = temp_df[(temp_df.vehicle_make == make)]
            temp_df = temp_df[(temp_df.vehicle_model == model)]
            temp_df = temp_df[(temp_df.vehicle_mileage == mileage)]

            keys.append(
                temp_df[(temp_df.vehicle_fuel_type==fuel)].index[0]
            )
        except:
            print(row)
            break
    return keys



def get_date_foreign_key(
    df,
    date_dim,
    date_label=None
):
    keys=[]
    for row in tqdm(df.index):
        date = df.loc[row, date_label] if date_label!=None else "Unknown"
        
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
        descript = df.loc[row, description_label] if description_label!= None else "Unknown"
        user = df.loc[row, username_label] if username_label!= None else "Unknown"
        title = df.loc[row, title_label] if username_label!=None else "Unknown"
        
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