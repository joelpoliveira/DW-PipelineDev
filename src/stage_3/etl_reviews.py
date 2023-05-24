import sys
import csv
import pandas as pd
from tqdm import tqdm
from util.etl_modeling import *


class DateDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("date", source_filter)
        self._header = ("date_key","date_full_description", "year",
                        "month", "written_month", "day",
                        "written_day_of_week", "season", 
                        "day_of_week", "week_number_in_year", 
                        "is_weekend", "is_month_end")
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

            processed_row=(   
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
            self.save_processed_row(processed_row)



class VehicleDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("vehicle", source_filter)
        self._header = ("vehicle_key", "year",
                        "mileage", "make", 
                        "model", "fuel",
                        "cylinders", 
                        "engine", "transmission")
        
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
            processed_row=(
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
            self.save_processed_row(processed_row)



class ReviewDimension(AbstractDimension):
    def __init__(self, source_filter):
        super().__init__("review", source_filter)
        self._header = ("review_key", "username", 
                        "title", "review")
        self.filter_description_index = 10
        self.filter_title_index = 11
        self.filter_reviewer_index = 12
    
    def process_row(self, row):
        description_index = self.source_filter.get_columns()[self.filter_description_index]
        title_index = self.source_filter.get_columns()[self.filter_title_index]
        reviewer_index = self.source_filter.get_columns()[self.filter_reviewer_index]

        description = row[description_index]
        title = row[title_index]
        reviewer = row[reviewer_index]
        
        description_hash = get_hash(description)
        title_hash = get_hash(title)

        review_key = self.lookup_table.get_surrogate_key(str(
            (description_hash, title_hash, reviewer)
        ))
        if not self.lookup_table.surrogate_key_already_existed:
            processed_row=(
                review_key,
                reviewer,
                title,
                description
            )
            self.save_processed_row(processed_row)


class CarRatingFacts(AbstractFactTable):
    def __init__(self, source_filter, **kwargs):
        super().__init__("car_rating", source_filter)

        self.date_lookup_table = kwargs["date_lut"]
        self.vehicle_lookup_table = kwargs["vehicle_lut"]
        self.review_lookup_table = kwargs["review_lut"]

        self._header = ("date_key", "vehicle_key", "review_key", "rating")

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
        rating_index = self.source_filter.get_columns()[9]
        description_index = self.source_filter.get_columns()[10]
        title_index = self.source_filter.get_columns()[11]
        reviewer_index = self.source_filter.get_columns()[12]

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
        date = str(pd.Timestamp(row[date_index]))
        rating = row[rating_index] 
        description = row[description_index]
        title = row[title_index]
        reviewer = row[reviewer_index]

        description_hash = get_hash(description)
        title_hash = get_hash(title)

        date_key = self.date_lookup_table.get_surrogate_key(date)
        vehicle_key = self.vehicle_lookup_table.get_surrogate_key(str(
            (year, mileage, make, model, fuel, cylinders, engine, transmission)
        ))
        review_key = self.review_lookup_table.get_surrogate_key(str(
            (description_hash, title_hash, reviewer)
        ))

        processed_row=(date_key, vehicle_key, review_key, rating)
        self.save_processed_row(processed_row)


if __name__ == "__main__":
    source_path = sys.argv[1]

    source_filter = SourceColumnsFilter([
            "Year",
            None, 
            "Company", 
            "Model", 
            None, 
            None, 
            None,
            None,
            "Date",
            "Rating",
            "Review",
            "Title",
            "Reviewer"
        ])
    source_filter.set_filename(source_path)
    
    dateDim = DateDimension(source_filter)
    vehicleDim = VehicleDimension(source_filter)
    reviewDim = ReviewDimension(source_filter)
    ratingFacts = CarRatingFacts(
        source_filter,
        date_lut=dateDim.lookup_table,
        vehicle_lut = vehicleDim.lookup_table,
        review_lut = reviewDim.lookup_table    
    )

    print("Beginning ETL process...")
    dateDim.begin_process()
    vehicleDim.begin_process()
    reviewDim.begin_process()
    ratingFacts.begin_process()

    with open(source_path, "r", encoding="utf-8") as f:
        flen = sum(1 for _ in csv.reader(
            open(source_path, "r", encoding="utf-8"), 
            delimiter=",")
        )
        f.readline()

        file_reader = csv.reader(f, delimiter=",") 
        for r in tqdm(file_reader, total=flen):    
            dateDim.process_row(r)
            vehicleDim.process_row(r)
            reviewDim.process_row(r)
            ratingFacts.process_row(r)

    print("Saving files...")
    ratingFacts.end_process()
    reviewDim.end_process()
    vehicleDim.end_process()
    dateDim.end_process()

    print("ETL process finished!")