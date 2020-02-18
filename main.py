'''
Pavlo Semchyshyn
18.02.2020
'''

import re
import time
import mpu
from geopy.geocoders import Nominatim
import folium
from read_locations import DICT_OF_FILMS, all_films_in_year
from read_cities import check_with_all_cities


def location_to_coordinates(year: int) -> dict:
    """
    A function, which returns a ditionary with a films,
    shot in [year], as a key, and tuple of coordinates
    of location, as value
    """
    film_location = all_films_in_year(year, DICT_OF_FILMS)
    film_location_in_coor = {}
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    count = 0
    print("Map is generating ...")
    start = time.perf_counter()
    for film, location in film_location.items():
        try:
            film_coordiantes = geolocator.geocode(location)
            if film_coordiantes is None:
                continue
            elif abs(film_coordiantes.longitude) > 180 or abs(film_coordiantes.latitude) > 90:
                continue
        except Exception:
            continue
        film_location_in_coor[film] = (film_coordiantes.latitude, film_coordiantes.longitude)
        count += 1
        if time.perf_counter() - start > 180:
            break
    return film_location_in_coor



def closest_films_locations(longtitude: float, latitude: float, year: int) -> dict:
    """
    A function for getting a sorted dictionary of films
    and location (sorting elements by haversine_distance)
    """
    film_location = location_to_coordinates(year)
    current_point = latitude, longtitude
    distance_haver = lambda x: mpu.haversine_distance(current_point, x[1])
    tp_by_haversine = sorted(film_location.items(), key=distance_haver)
    closest_points = {k: v for k, v in tp_by_haversine}
    return closest_points


def location_checker(*coor) -> bool:
    """
    A function to check if a given coordinate is valid
    >>> location_checker(34.34, 2.234)
    True
    >>> location_checker(27.23, 1.234)
    True
    """
    latitude_checker = re.compile(r"^[-]?(\d|[1-8]\d|90)\.\d+")
    longtitude_checker = re.compile(r"^[-]?(\d|\d\d|1[0-7]\d|180)\.\d+")
    if not latitude_checker.fullmatch(coor[0]):
        print("Wrong latitude")
        res = False
    elif not longtitude_checker.fullmatch(coor[1]):
        print("Wrong longtitude")
        res = False
    else:
        res = True
    return res


def user_input() -> tuple:
    """
    A function, which provides
    user input, and checks if it is valid
    """
    year_input = input("Please enter a year you would like to have a map for: ")
    if not year_input.isdigit():
        print(f"{year_input} is not a year")
        return
    elif int(year_input) not in range(1950, 2018):
        print("The year should be between 1950 and 2018")
        return
    location_input = input("Please enter your location (format: lat, long): ")
    try:
        latitude, longtitude = location_input.split(",")
        latitude = latitude.strip()
        longtitude = longtitude.strip()
        if not location_checker(latitude, longtitude):
            return
    except Exception:
        print("Location in a wrong format")
        return
    return int(year_input), float(longtitude), float(latitude)


def map_builder(year: int, longtitude: float, latitude: float, num=10) -> None:
    """
    A function for building a map using folium library
    """
    mapp = folium.Map(location=[latitude, longtitude], zoom_start=5)
    fg_1_layer = folium.FeatureGroup("Films nearby")
    fg_2_layer = folium.FeatureGroup("Indected places")
    closest_locations = closest_films_locations(longtitude, latitude, year)
    inf_places = check_with_all_cities()
    print("Please wait...")
    time.sleep(3)
    for film in closest_locations:
        loc1 = closest_locations.get(film)
        fg_1_layer.add_child(folium.Marker(location=loc1, popup=film,
                                           icon=folium.Icon(color='red', icon='info-sign')))
        num -= 1
        if not num:
            break
    for place in inf_places:
        loc2 = inf_places.get(place)
        fg_2_layer.add_child(folium.CircleMarker(location=loc2, color="#164217",
                                                 fill_color="#164217",
                                                 popup=place, radius=3))
    mapp.add_child(fg_1_layer)
    mapp.add_child(fg_2_layer)
    mapp.save("map_1.html")


def run() -> None:
    """
    Runs the programm
    """
    us_input = user_input()
    if us_input is not None:
        year, longtitude, latitude = us_input
        map_builder(year, longtitude, latitude)
        print("Finished. Please have look at the map map_1.html")
    else:
        return


if __name__ == "__main__":
    run()
