
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

TABLE_NAMES = [
    #"date_dimension", 
    #"location_dimension",
    #"vehicle_dimension", 
    #"review_dimension",
    "car_sales_fact",
    "car_rating_fact"
]


if __name__ == "__main__":
    try:
        for table in TABLE_NAMES:
            cursor = CONNECTION.cursor()
            cursor.execute(f"DROP table IF EXISTS {table} CASCADE;")

            cursor.close()
            CONNECTION.commit()
    except Exception as e:
        print(e)
        CONNECTION.rollback()