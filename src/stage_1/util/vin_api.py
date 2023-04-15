import requests
import json
import numpy as np

ENDPOINT = "https://auto.dev/api/vin/" 
key = "ZrQEPSkKam9lbHBvbGl2ZWlyYTIwMDFAZ21haWwuY29t"

def call_vin(vin:str)->str:
    header = {"Authorization": f"Bearer {key}"}
    url = ENDPOINT+f"{vin}"
    
    try:
        data = requests.get(url, headers=header)
        data = json.loads(data.text)
        return data
    except:
        return None

    
def call_vin2(vin:str)->str:
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    
    try:
        data = requests.get(url)
        data = json.loads(data.text)
        return data
    except:
        return None
    
def get_model(vin:str)->str:
    data = call_vin2(vin)
    if data == None:
        return np.nan
    
    data = list(
        filter(
        lambda x: 
            x["Variable"]=="Model", 
        call_vin2(vin)["Results"])
    )
    if data==None:
        return np.nan
    return data[0]["Value"]

def get_model2(vin:str)->str:
    data = call_vin(vin)
    
    if "status" in data:
        return np.nan
    return data["model"]["niceName"]


def get_model3(vin:str)->str:
    url = "https://vin-decoder19.p.rapidapi.com/vin_decoder_lite"

    params = {"vin":vin}

    headers = {
        "X-RapidAPI-Key": "968b157004msh1a06ddf2903c644p1d9194jsne36d36379ec2",
        "X-RapidAPI-Host": "vin-decoder19.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)

    return json.load(response.text)["Model"]

if __name__=="__main__":
    pass
    