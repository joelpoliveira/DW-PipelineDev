



def mileage_to_miles_band(mile):
    if mile < 26000:
        return "[0, 26000)"
    if mile < 60500:
        return "[26000, 60500)"
    if mile < 98500:
        return "[60500, 98500)"
    if mile < 143400:
        return "[98500, 143400)"
    if mile < 209000:
        return "[143400, 209000)"
    return "[209000, ?)"


fuel_map = {
    "gas":"gas",
    "diesel":"diesel",
    "hybrid":"gas",
    "other":"gas",
    "electric":"electric",
    "eletric":"electric"
}