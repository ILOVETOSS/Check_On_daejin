import random

def read_temperature():
    return round(random.uniform(25, 40), 1)

def read_humidity():
    return round(random.uniform(40, 80), 1)
