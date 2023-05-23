import os
import sys
import csv
import json
import pandas as pd
from tqdm import tqdm
from abc import abstractclassmethod

TABLES_DIR = "./tables/"
LOOKUP_DIR = "./lookup/"

def mileage_to_miles_band(mileage):
    """
    Function that converts the mileage to a mileage band 
    """
    if mileage=="Unknown": return mileage

    mileage=int(mileage.split(".")[0])
    if mileage < 26000: return "[0, 26000)"
    if mileage < 60500: return "[26000, 60500)"
    if mileage < 98500: return "[60500, 98500)"
    if mileage < 143400: return "[98500, 143400)"
    if mileage < 209000: return "[143400, 209000)"
    return "[209000, ?)"


class SourceColumnsFilter:
    """
    This class receives the column names of the source file. 
    A list is generated with the respective indexes of the columns in that file.
    The incoming column names guarantee the order of the indexes in the list, which is:
        - model_year
        - mileage
        - make
        - model
        - fuel
        - cylinders
        - engine
        - transmission
        - purchase_date
        - latitude
        - longitude
        - state
    If a column is not present in the source file, the value in the list must be None.
    """
    def __init__(self, col_names):
        self.col_names = col_names
        self.file_name = None

    def set_filename(self, file_name):
        """
        Sets the file name of the source file and creates the list of indexes.
        """
        self.file_name = file_name
        self.create_column_positions()

    def create_column_positions(self):
        """
        Creates the list of indexes.
        """
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
        assert len(self.col_names)==len(self.columns), "Columns names do not match source header!"
    
    def get_columns(self):
        return self.columns



class LookupTable:
    """
    
    """
    def __init__(self, dim_name):
        self.dim_name = dim_name
        self.file_name = LOOKUP_DIR + f"lut_{self.dim_name}.json"
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
        self.file_name = TABLES_DIR + f"dim_{self.dim_name}.csv"
        self.file = None
        self.lookup_table = LookupTable(self.dim_name)
        self._header=None

    def begin_process(self):
        if self._header!=None:
            save_header_row_in_dimension_file = False

            if not os.path.isfile(self.file_name):
                save_header_row_in_dimension_file = True
            
            self.file = open(self.file_name, "a", encoding="utf-8")

            if save_header_row_in_dimension_file:
                self.file.write(",".join(self._header)+"\n")
        

    def end_process(self):
        if self._header!=None:
            self.file.close()
            self.lookup_table.save()
    
    @abstractclassmethod
    def process_row(self, row):
        pass
        
    def save_processed_row(self, processed_row):
        if self._header!=None:
            processed_row +="\n"
            self.file.write(processed_row)
            


class DateDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("date", source_filter)
        self._header = ("date_key","date_full_description", "date_year",
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
        
        date_full_description = row[date_index]
        try:
            date_full_description = pd.Timestamp(
                date_full_description[:10], 
            )
        except Exception as e:
            print(date_full_description)
            print(date_full_description[:10])
            exit(-1)
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
        self._header = ("location_key", "location_state", 
                        "location_latitude", "location_longitude")

        self.filter_lat_index = 9
        self.filter_long_index = 10
        self.filter_state_index = 11
        
    def process_row(self, row):
        lat_idx = self.source_filter.get_columns()[self.filter_lat_index]
        long_idx = self.source_filter.get_columns()[self.filter_long_index]
        state_idx = self.source_filter.get_columns()[self.filter_state_index]

        lat = row[lat_idx]
        long = row[long_idx]
        state = row[state_idx]

        loc_key = self.lookup_table.get_surrogate_key(str((state, lat, long)))
        if not self.lookup_table.surrogate_key_already_existed:
            processed_row=",".join(list(map(str,
                (
                    loc_key,
                    state,
                    lat,
                    long
                )
            )))
            self.save_processed_row(processed_row)


class VehicleDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("vehicle", source_filter)
        self._header = ("vehicle_key", "vehicle_year",
                        "vehicle_number_of_cylinders", 
                        "vehicle_mileage", "vehicle_make", 
                        "vehicle_model", "vehicle_engine",
                        "vehicle_fuel_type", "vehicle_transmission_type")
        
        self.filter_year_index = 0
        self.filter_mileage_index = 1
        self.filter_make_index = 2
        self.filter_model_index = 3
        self.filter_fuel_index = 4
        self.filter_cylinders_index = 5
        self.filter_engine_index = 6
        self.filter_transmission_index = 7
    
    def process_row(self, row):
        year_index = self.source_filter.get_columns()[self.filter_year_index]
        mileage_index = self.source_filter.get_columns()[self.filter_mileage_index]
        make_index = self.source_filter.get_columns()[self.filter_make_index]
        model_index = self.source_filter.get_columns()[self.filter_model_index]
        fuel_index = self.source_filter.get_columns()[self.filter_fuel_index]
        cylinders_index = self.source_filter.get_columns()[self.filter_cylinders_index]
        engine_index = self.source_filter.get_columns()[self.filter_engine_index]
        transmission_index = self.source_filter.get_columns()[self.filter_transmission_index]

        year = row[year_index] if year_index!=None else "Unknown"
        mileage = mileage_to_miles_band(
            row[mileage_index] if mileage_index!=None else "Unknown"
        )
        make = row[make_index] if make_index!=None else "Unknown"
        model = row[model_index] if model_index!=None else "Unknown"
        fuel = row[fuel_index] if fuel_index!=None else "Unknown"
        cylinders = row[cylinders_index] if cylinders_index!=None else "Unknown"
        engine = row[engine_index] if engine_index!=None else "Unknown"
        transmission = row[transmission_index] if transmission_index!=None else "Unknown"

        vehicle_key = self.lookup_table.get_surrogate_key(str(
            (year, mileage, make, model, fuel, cylinders, engine, transmission)
        ))
        if not self.lookup_table.surrogate_key_already_existed:
            processed_row=",".join(list(map(str,
                (
                    vehicle_key,
                    year,
                    mileage,
                    make,
                    model,
                    fuel,
                    cylinders,
                    engine,
                    transmission
                )
            )))
            self.save_processed_row(processed_row)


class CarSalesFacts:
    def __init__(self,
                 source_filter,
                 date_lookup_table,
                 location_lookup_table,
                 vehicle_lookup_table):
        self.fact_name = "car_sales"
        self.file_name = TABLES_DIR + f"fact_{self.fact_name}.csv"
        self.file = None#open(self.file_name, "a", encoding="utf-8")
        
        self.source_filter = source_filter
        self.date_lookup_table = date_lookup_table
        self.location_lookup_table = location_lookup_table
        self.vehicle_lookup_table = vehicle_lookup_table

        self._header = ("date_key",
                       "location_key",
                       "vehicle_key",
                       "sale_price",
                       "fuel_price")
        
        with open("./source/fuel_prices.json", "r") as f:
            self.fuel_prices = json.load(f)
    
    def get_fuel_price_at_date(self, fuel, date):
        if fuel=="electric" or fuel=="eletric":
            return "0"

        try:
            prices = self.fuel_prices[date]
            
            if fuel=="gas":
                return str(prices["Gasoline Price"])
            elif fuel=="diesel":
                return str(prices["Diesel Price"])
            else:
                print("Invalid fuel type")
                exit(-2)
        except KeyError:
            return "0"
        
    def begin_process(self):
        save_header_row_in_file = False

        if not os.path.isfile(self.file_name):
            save_header_row_in_file = True
        
        self.file = open(self.file_name, "a", encoding="utf-8")

        if save_header_row_in_file:
            self.file.write(",".join(self._header)+"\n")

    def end_process(self):
        """
        Closes the facts file.
        """
        if self.file is not None:
            self.file.close()
            self.file = None

    def process_row(self, row):
        year_index = self.source_filter.get_columns()[0]
        mileage_index = self.source_filter.get_columns()[1]
        make_index = self.source_filter.get_columns()[2]
        model_index = self.source_filter.get_columns()[3]
        fuel_index = self.source_filter.get_columns()[4]
        cylinders_index = self.source_filter.get_columns()[5]
        engine_index = self.source_filter.get_columns()[6]
        transmission_index = self.source_filter.get_columns()[7]
        date_index = self.source_filter.get_columns()[8]
        lat_index = self.source_filter.get_columns()[9]
        long_index = self.source_filter.get_columns()[10]
        state_index = self.source_filter.get_columns()[11]
        price_index = self.source_filter.get_columns()[12]

        year = row[year_index] if year_index!=None else "Unknown"
        mileage = mileage_to_miles_band(
            row[mileage_index] if mileage_index!=None else "Unknown"
        )
        make = row[make_index] if make_index!=None else "Unknown"
        model = row[model_index] if model_index!=None else "Unknown"
        fuel = row[fuel_index] if fuel_index!=None else "Unknown"
        cylinders = row[cylinders_index] if cylinders_index!=None else "Unknown"
        engine = row[engine_index] if engine_index!=None else "Unknown"
        transmission = row[transmission_index] if transmission_index!=None else "Unknown"
        date = str(pd.Timestamp(row[date_index][:10]))
        lat = row[lat_index] 
        long = row[long_index]
        state = row[state_index]
        price = row[price_index]

        vehicle_natural_key = self.vehicle_lookup_table.get_surrogate_key(str(
            (year, mileage, make, model, fuel, cylinders, engine, transmission)
        ))
        date_natural_key = self.date_lookup_table.get_surrogate_key(date)
        location_natural_key = self.location_lookup_table.get_surrogate_key(
            str((state, lat, long))
        )

        processed_row = ",".join(list(map(str,
            (
                date_natural_key,
                location_natural_key,
                vehicle_natural_key,
                price,
                self.get_fuel_price_at_date(fuel, date)
            )
        )))
        self.save_processed_row(processed_row)

    def save_processed_row(self, processed_row):
        """
        Saves the processed row to the dimension file.
        """
        if self.file is not None:
            processed_row +="\n"
            self.file.write(processed_row)

def get_source_filter(idx):
    # Source 1 - tn_mvr.csv
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
            "state",
            "price"
        ])
    # Source 2 - used_car_sales.csv
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
            "state",
            "pricesold"
        ])
    # Source 3 - vehicles.csv
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
            "state",
            "price"
        ])
    else:
        print("Invalid source index")
        exit(1)


if __name__=="__main__":
    source_path, source_index = sys.argv[1:]

    # Source 1 - tn_mvr.csv
    source_filter=get_source_filter(source_index)
    source_filter.set_filename(source_path)

    dateDim = DateDimension(source_filter)
    locationDim = LocationDimension(source_filter)
    vehicleDim = VehicleDimension(source_filter)
    salesFacts = CarSalesFacts(
        source_filter,
        dateDim.lookup_table,
        locationDim.lookup_table,
        vehicleDim.lookup_table    
    )
    
    print("Beginning ETL process...")
    dateDim.begin_process()
    locationDim.begin_process()
    vehicleDim.begin_process()
    salesFacts.begin_process()

    with open(source_path, "r", encoding="utf-8") as f:
        flen = sum(1 for _ in open(source_path, "r", encoding="utf-8"))
        f.readline()

        file_reader = csv.reader(f, delimiter=",") 
        for r in tqdm(file_reader, total=flen):
            dateDim.process_row(r)
            locationDim.process_row(r)
            vehicleDim.process_row(r)
            salesFacts.process_row(r)
    
    print("Saving files...")
    salesFacts.end_process()
    vehicleDim.end_process()
    locationDim.end_process()
    dateDim.end_process()
    print("ETL process finished!")