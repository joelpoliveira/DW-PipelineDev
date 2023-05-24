import os
import csv
import json
from hashlib import md5
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

def get_hash(string):
        return md5(string.encode()).hexdigest()

class SourceColumnsFilter:
    """
    This class receives the column names of the source file. 
    A list is generated with the respective indexes of the columns in that file.
    The incoming column names guarantee the order of the indexes in the list, which is:

    ( A )--> ETL Sales:
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

    ( B )--> ETL Reviews:
        - model_year
        - mileage
        - make
        - model
        - fuel
        - cylinders
        - engine
        - transmission
        - publication_date
        - rating
        - review
        - title

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
            self.file_writer = csv.writer(self.file, delimiter=",", lineterminator="\n")

            if save_header_row_in_dimension_file:
                self.file_writer.writerow(self._header)
        

    def end_process(self):
        if self._header!=None:
            self.file.close()
            self.file = None
            self.file_writer = None
            self.lookup_table.save()
    
    @abstractclassmethod
    def process_row(self, row):
        pass
        
    def save_processed_row(self, processed_row):
        if self._header!=None:
            self.file_writer.writerow(processed_row)


class AbstractFactTable:
    def __init__(self, fact_name, source_filter):
        self.fact_name = fact_name
        self.file_name = TABLES_DIR + f"fact_{self.fact_name}.csv"
        self.file = None
        self.file_writer = None
        
        self.source_filter = source_filter
        self._header = None

    def begin_process(self):
        save_header_row_in_file = False

        if not os.path.isfile(self.file_name):
            save_header_row_in_file = True
        
        self.file = open(self.file_name, "a", encoding="utf-8")
        self.file_writer = csv.writer(self.file, delimiter=",", lineterminator="\n") 

        if save_header_row_in_file:
            self.file_writer.writerow(self._header)

    def end_process(self):
        """
        Closes the facts file.
        """
        if self.file is not None:
            self.file.close()
            self.file = None

    @abstractclassmethod
    def process_row(self, row):
        pass

    def save_processed_row(self, processed_row):
        """
        Saves the processed row to the dimension file.
        """
        if self.file is not None:
            self.file_writer.writerow(processed_row)