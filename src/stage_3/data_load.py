
import os
import pandas as pd
import psycopg2 as pg

os.environ["PGGSSENCMODE"] = "disable"

CONNECTION =  pg.connect(
    host="appserver-01.alunos.di.fc.ul.pt",
    database="ipai13", 
    user="ipai13", 
    password='ipai13'
)

TABLE_CREATE_QUERIES = {
    "date_dimension": """
CREATE TABLE date_dimension (
    date_key               NUMERIC(9, 0),
    date_full_description  TIMESTAMP NOT NULL,
    year                   NUMERIC(4, 0) NOT NULL,
    month                  NUMERIC(2, 0) NOT NULL,
    written_month          VARCHAR(9) NOT NULL,
    day                    NUMERIC(2, 0) NOT NULL,
    written_day_of_week    VARCHAR(9) NOT NULL,
    season                 VARCHAR(6) NOT NULL,
    day_of_week            NUMERIC(1, 0) NOT NULL,
    week_number_in_year    NUMERIC(2, 0) NOT NULL,
    is_weekend             BOOLEAN NOT NULL,
    is_month_end           BOOLEAN NOT NULL,
--
    PRIMARY KEY (date_key),
--
    CHECK (date_key>0),
    CHECK (year>0),
    CHECK (month BETWEEN 0 AND 12),
    CHECK (UPPER(written_month) in 
        ('JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
            'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER')
    ),
    CHECK (day BETWEEN 0 AND 31),
    CHECK (UPPER(written_day_of_week) in
        ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')
    ),
    CHECK (UPPER(season) in 
        ('SPRING', 'SUMMER', 'FALL', 'WINTER')
    ),
    CHECK (day_of_week BETWEEN 0 AND 6),
    CHECK (week_number_in_year BETWEEN 0 AND 53)
);
""",


    "location_dimension": """
CREATE TABLE location_dimension (
    location_key            NUMERIC(9, 0),
    latitude                NUMERIC(9, 6) NOT NULL,
    longitude               NUMERIC(9, 6) NOT NULL,
    state                   CHAR(2) NOT NULL,
--
    PRIMARY KEY (location_key),
--  
    CHECK (latitude BETWEEN -90 AND 90),
    CHECK (longitude BETWEEN -180 AND 180),
    CHECK (UPPER(state) in 
        ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')
    )
);
""",


    "vehicle_dimension": """
CREATE TABLE vehicle_dimension (
    vehicle_key             NUMERIC(9, 0),
    year                    NUMERIC(4, 0) NOT NULL,
    mileage                 VARCHAR(16) NOT NULL,
    make                    VARCHAR(32) NOT NULL,
    model                   VARCHAR(32) NOT NULL,
    fuel                    VARCHAR(32) NOT NULL,
    cylinders               VARCHAR(7) NOT NULL,
    engine                  VARCHAR(100) NOT NULL,
    transmission            VARCHAR(32) NOT NULL,
--
    PRIMARY KEY (vehicle_key),
--
    CHECK (year>0),
    CHECK (UPPER(mileage) in 
        ('[0, 26000)', '[26000, 60500)', '[60500, 98500)', 
            '[98500, 143400)', '[143400, 209000)', '[209000, ?)',
            'UNKNOWN')
    ),
    CHECK (UPPER(fuel) in
        ('GAS', 'DIESEL', 'ELECTRIC', 'UNKNOWN')
    ),
    CHECK (UPPER(cylinders) in 
        ('0', '1', '2', '3', '4', '5', '6',
        '7', '8', '9', '10', '11',
        '12', '13', '14', '15', '16', 'UNKNOWN')
    )
);
""",


    "review_dimension": """
CREATE TABLE review_dimension (
    review_key   NUMERIC(9, 0),
    username     VARCHAR(128) NOT NULL,
    review       TEXT NOT NULL,
    title        TEXT NOT NULL,
--
    PRIMARY KEY (review_key),
--
    CHECK (username != ''),
    CHECK (review != '')
);
""",


    "car_sales_fact": """
CREATE TABLE car_sales_fact (
    car_sale_key        SERIAL PRIMARY KEY,
    date_key            NUMERIC(9, 0) NOT NULL,
    location_key        NUMERIC(9, 0) NOT NULL,
    vehicle_key         NUMERIC(9, 0) NOT NULL,
    sale_price          NUMERIC(9, 2) NOT NULL,
    fuel_price          NUMERIC(3, 2) NOT NULL,
--
    FOREIGN KEY (date_key) REFERENCES date_dimension (date_key),
    FOREIGN KEY (location_key) REFERENCES location_dimension (location_key),
    FOREIGN KEY (vehicle_key) REFERENCES vehicle_dimension (vehicle_key),
--
    CHECK (sale_price>0),
    CHECK (fuel_price>0)
);
""",


    "car_rating_fact": """
CREATE TABLE car_rating_fact (
    car_rate_key        SERIAL PRIMARY KEY,
    date_key            NUMERIC(9, 0) NOT NULL,
    vehicle_key         NUMERIC(9, 0) NOT NULL,
    review_key          NUMERIC(9, 0) NOT NULL,
    rating              NUMERIC(2, 0) NOT NULL,
--
    FOREIGN KEY (date_key) REFERENCES date_dimension (date_key),
    FOREIGN KEY (vehicle_key) REFERENCES vehicle_dimension (vehicle_key),
    FOREIGN KEY (review_key) REFERENCES review_dimension (review_key),
--
    CHECK (rating BETWEEN 0 AND 5)
);
""",
}


def create_tables():
    """
    Function that creates the tables in the database if they don't exist.
    """
    try:
        for table_name in TABLE_CREATE_QUERIES:
            cursor = CONNECTION.cursor()
            cursor.execute(f"""SELECT EXISTS(
                SELECT FROM
                    pg_tables
                WHERE
                    schemaname = 'public' AND
                    tablename = '{table_name}'
            )""")

            #result = cursor.fetchone()[0]
            #print(result, type(result))

            if cursor.fetchone()[0]:
                print(f"\nTable {table_name} already exists!")
            else:
                print(f"\nCreating table {table_name}...")
                cursor.execute(TABLE_CREATE_QUERIES[table_name])
                CONNECTION.commit()
                print(f"Table {table_name} created!")
            cursor.close()
    except Exception as e:
        print(e)
        CONNECTION.rollback()
        raise Exception


def insert_data(df_data, table_name):
    try:
        cursor=CONNECTION.cursor()
        query = f"""
            INSERT INTO {table_name}({','.join(df_data.columns)}) 
            VALUES({",".join("%s" for _ in range(df_data.shape[1]))})
        """
        print(f"\nInserting data into {table_name}...")
        cursor.executemany(query, df_data.to_numpy().tolist())
        print(f"Operation successful!")
        CONNECTION.commit()
    except Exception as e:
        print(f"Error:", e)
        CONNECTION.rollback()
        raise Exception



if __name__ == "__main__":
    dim_date = pd.read_csv("tables/dim_date.csv", parse_dates=["date_full_description"])
    dim_location = pd.read_csv("tables/dim_location.csv")
    dim_vehicle = pd.read_csv("tables/dim_vehicle.csv")
    dim_review = pd.read_csv("tables/dim_review.csv")

    fact_ratings = pd.read_csv("tables/fact_car_rating.csv")    
    fact_sales = pd.read_csv("tables/fact_car_sales.csv")
    try:
        create_tables()
        
        #insert_data(dim_date, "date_dimension")
        #insert_data(dim_location, "location_dimension")
        #insert_data(dim_vehicle, "vehicle_dimension")
        insert_data(dim_review, "review_dimension")

        insert_data(fact_sales, "car_sales_fact")
        insert_data(fact_ratings, "car_rating_fact")
    finally:
        CONNECTION.close()
        exit(-1)

    
