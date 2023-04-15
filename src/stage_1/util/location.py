import numpy as np
from pyzipcode import ZipCodeDatabase

zdb = ZipCodeDatabase()

def get_state(code):
    try:
        data = zdb[code]
        return data.state.lower()
    except:
        return np.nan
    
def get_long(code):
    try:
        data = zdb[code]
        return data.longitude
    except:
        return np.nan
    
def get_lat(code):
    try:
        data = zdb[code]
        return data.latitude
    except:
        return np.nan