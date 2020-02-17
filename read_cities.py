'''
Pavlo Semchyshyn
17.02.2020
'''


import pandas as pd


DF_INFECTED = pd.read_csv("inf.csv")
DF_ALL_CITIES = pd.read_csv("city_coordinates.tsv", sep="\t")

def infected_places() -> tuple:
    """
    A function for getting a tuple of sets, which
    represent infected cities and countries
    """
    places = DF_INFECTED["Province/State"].astype(str) + "-" + DF_INFECTED["Country"]
    countries_set = set()
    chinese_cities = set()
    for line in places:
        ind = line.index("-")
        if "," in line or "Mainland" in line:
            continue
        elif "nan" in line:
            countries_set.add(line[ind + 1:])
        else:
            chinese_cities.add(line[: ind])
    return countries_set, chinese_cities


def check_with_all_cities() -> dict:
    """
    A function, which outputs a dictionary with
    string of city or country as a key and a tuple
    of langtitude and latitude as value
    """
    inf_countries, inf_cities = infected_places()
    countries = DF_ALL_CITIES["country"] + "|" + DF_ALL_CITIES["lat"] + "|" + DF_ALL_CITIES["lng"]
    cities = DF_ALL_CITIES["city_ascii"] + "|" + DF_ALL_CITIES["lat"] + "|" + DF_ALL_CITIES["lng"]
    dict_inf = {}
    for susp_con in countries:
        country_full = susp_con.split("|")
        if country_full[0] in inf_countries:
            dict_inf[country_full[0]] = float(country_full[1]), float(country_full[2])
    for susp_city in cities:
        city_full = susp_city.split("|")
        if city_full[0] in inf_cities:
            dict_inf[city_full[0]] = float(city_full[1]), float(city_full[2])
    return dict_inf
