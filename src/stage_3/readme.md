
# Claimer
To run this stage files all the processing from *Stage 1* must be performed.
This stages uses the results from *Stage 1* stored in **/stage1/data/processedData**.

The following files (pos-processing) should be put in *source* folder:
 - *tn_mvr.csv*
 - *used_car_sales.csv*
 - *fuel_prices.csv*
 - *vehicles.csv*
 - *review.csv*


# ETL Processing

## Tutorial on etl_sales
Before running the ETL file related to the car sales *fuel_prices_optimizer.ipynb* must be run, to build a structure that speed ups the process of matching the fuel price for an entry. 

The ETL automated process is run with following command:
```bash
python etl_sales.py {path_to_source_file} {source_indicator}
```

{source_indicator} values: 
 * $1$, refers to *tn_mvr.csv*
 * $2$, refers to *used_car_sales.csv*
 * $3$, refers to *vehicles.csv*

## Tutorial on etl_reviews
For this second Fact table, since there is only one source the command to run is:
```bash
python etl_reviews.py {path_to_source_file}
```


