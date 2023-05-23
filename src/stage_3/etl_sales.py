import os
import sys
import json
import pandas as pd
from tqdm import tqdm
from geopy import Nominatim
from abc import abstractclassmethod

class SourceColumnsFilter:
    def __init__(self, col_names):
        self.col_names = col_names
        self.file_name = None

    def set_filename(self, file_name):
        self.file_name = file_name
        self.create_column_positions()

    def create_column_positions(self):
        self.columns = []
        with open(self.file_name, "r") as f:
            header = f.readline().strip().split(",")

            for col_name in self.col_names:
                if col_name == None:
                    self.columns.append(None)
                else:
                    for j, header_col in enumerate(header):
                        if col_name == header_col:
                            self.columns.append(j)
                            break
    
    def get_columns(self):
        return self.columns



class LookupTable:
    def __init__(self, dim_name):
        self.dim_name = dim_name
        self.file_name = f"lut_{self.dim_name}.json"
        self.load()

    def load(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                self.lookup_table = json.load(f)
                try:
                    self.next_surrogate_key = max(self.lookup_table.values()) + 1
                except ValueError:
                    self.next_surrogate_key = 1
        else:
            self.lookup_table = {}
            self.next_surrogate_key = 1

    def get_surrogate_key(self, natural_key):
        #natural key migth be a large tuple or just a string
        if natural_key in self.lookup_table:
            self.surrogate_key_already_existed = True
            return self.lookup_table[natural_key]
        else:
            self.lookup_table[natural_key] = self.next_surrogate_key
            self.next_surrogate_key += 1
            self.surrogate_key_already_existed = False
            return self.lookup_table[natural_key]
        
    def save(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.lookup_table, f, sort_keys=True)



class AbstractDimension:
    def __init__(self, dim_name, source_filter):
        self.dim_name = dim_name
        self.source_filter = source_filter
        self.file_name = f"dim_{self.dim_name}.csv"
        self.file = open(self.file_name, "a", encoding="utf-8")
        self.lookup_table = LookupTable(self.dim_name)
        self._header=None

    def end_process(self):
        if self._header!=None:
            self.file.close()
            self.lookup_table.save()
    
    @abstractclassmethod
    def process_row(self, row):
        pass
        #natural_key = self.get_natural_key(row)
        #surrogate_key = self.lookup_table.get_surrogate_key(natural_key)
        #self.write_row(surrogate_key, row)
        
    def save_processed_row(self, processed_row):
        if self._header!=None:
            processed_row +="\n"
            self.file.write(processed_row)
            


class DateDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("date", source_filter)
        self._header = ("date_full_description", "date_year",
                        "date_month", "date_written_month", "date_day",
                        "date_written_day_of_week", "date_season", 
                        "date_day_of_week", "date_week_number_in_year", 
                        "day_is_weekend", "day_is_month_end")
        self.filter_date_index = 8

    def get_season(self, date):
        day = date.day_of_year
        spring = range(80, 172)
        summer = range(172, 264)
        fall = range(264, 355)

        if day in spring:
            return 'spring'
        elif day in summer:
            return 'summer'
        elif day in fall:
            return 'fall'
        else:
            return 'winter'

    def process_row(self, row):
        date_index = self.source_filter.get_columns()[self.filter_date_index]
        
        date_full_description = row.split(",")[date_index]
        date_full_description = pd.Timestamp(
            date_full_description, 
        )
        
        time_key = self.lookup_table.get_surrogate_key(str(date_full_description))

        if not self.lookup_table.surrogate_key_already_existed:
            date_year = date_full_description.year
            date_month = date_full_description.month
            date_day = date_full_description.day
            date_is_weekend = date_full_description.isoweekday()!=1
            date_written_month = date_full_description.month_name().lower()
            date_week_number_in_year = date_full_description.weekofyear
            date_month_is_month_end = date_full_description.is_month_end
            date_day_of_week = date_full_description.weekday()
            date_written_day_of_week = date_full_description.day_name().lower()
            date_season = self.get_season(date_full_description)

            processed_row=",".join(list(map(str,
                (   
                    time_key,
                    date_full_description,
                    date_year,
                    date_month,
                    date_written_month,
                    date_day,
                    date_written_day_of_week,
                    date_season,
                    date_day_of_week,
                    date_week_number_in_year,
                    date_is_weekend,
                    date_month_is_month_end
                )
            )))

            self.save_processed_row(processed_row)

        
    


class LocationDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("location", source_filter)
        self._header = ("location_state", "location_latitude", "location_longitude")

        self.filter_lat_index = 9
        self.filter_long_index = 10
        self.filter_state_index = 11
        self.geolocator = Nominatim(user_agent="http")


    def _get_location(self, lat, long):
        location = self.geolocator.reverse((lat, long))
        return location
    
    def get_county(self, lat, long):
        location = self._get_location(lat, long)
        if location == None:
            return "Unknown"
        else:
            if "county" in location.raw["address"]:
                return location.raw["address"]["county"]
            else:
                return "Unknown"
        
    def process_row(self, row):
        lat_idx = self.source_filter.get_columns()[self.filter_lat_index]
        long_idx = self.source_filter.get_columns()[self.filter_long_index]
        state_idx = self.source_filter.get_columns()[self.filter_state_index]

        row = row.split(",")
        lat = row[lat_idx]
        long = row[long_idx]
        state = row[state_idx]

        loc_key = self.lookup_table.get_surrogate_key((state, lat, long))
        if not self.lookup_table.surrogate_key_already_existed:
            #county = self.get_county(lat, long)

            processed_row=",".join(list(map(str,
                (
                    loc_key,
                    state,
                    #county,
                    lat,
                    long
                )
            )))
            self.save_processed_row(processed_row)

class VehicleDimension(AbstractDimension):
    def __init__(self):
        super().__init__("vehicle")
        self._header = ()


class CarSalesFacts:
    def __init__(self):
        pass




def get_source_filter(idx):
    if idx=="1":
        return SourceColumnsFilter([
            "model_year",
            "mileage", 
            "make", 
            "model", 
            "fuel", 
            None, 
            None,
            None,
            "purchase_date",
            "lat",
            "long",
            "state"
        ])
    if idx=="2":
        return SourceColumnsFilter([
            "Year",
            "Mileage",
            "Make", 
            "Model", 
            "fuel", 
            "NumCylinders", 
            "Engine",
            None,
            "datesold",
            "lat",
            "long",
            "state"
        ])
    if idx=="3":
        return SourceColumnsFilter([
            "year", 
            "odometer",
            "manufacturer",
            "model",
            "fuel", 
            "cylinders",
            None,
            "transmission",
            "posting_date",
            "lat",
            "long",
            "state"
        ])
    else:
        print("Invalid source index")
        exit(1)


if __name__=="__main__":
    source_path, source_index = sys.argv[1:]

    # Source 1 - tn_mvr.csv
    source_filter=get_source_filter(source_index)
    source_filter.set_filename(source_path)

    #print(source_filter.get_columns())
    dateDim = DateDimension(source_filter)
    locationDim = LocationDimension(source_filter)

    print("Beginning ETL process...")
    with open(source_path, "r", encoding="utf-8") as f:
        flen = sum(1 for _ in open(source_path, "r"))
        
        f.readline()
        for r in tqdm(f, total=flen):
            r = r.strip()
            #dateDim.process_row(r)
            locationDim.process_row(r)
    print("Saving files...")
    dateDim.end_process()
    print("ETL process finished!")