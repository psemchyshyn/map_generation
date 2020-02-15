import folium
from collections import defaultdict
from read_locations import all_films_in_year, dict_of_films
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import mpu
import re
import time



def location_to_coordinates(year):
    film_location = all_films_in_year(year, dict_of_films)
    film_location_in_coor = {}
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode =  RateLimiter(geolocator.geocode, min_delay_seconds=1)
    count = 0
    print("Map is generating ...")
    for film, location in film_location.items():
        try:
            film_coordiantes = geolocator.geocode(location)
            if film_coordiantes == None:
                continue
            elif abs(film_coordiantes.longitude) > 180 or abs(film_coordiantes.latitude) > 90:
                continue
        except:
            continue
        film_location_in_coor[film] = (film_coordiantes.longitude, film_coordiantes.latitude)
        count += 1
        if count > 100:
            break
    return film_location_in_coor


def distance(point1, point2):
    x = point1[0] - point2[0]
    y = point2[1] - point2[1]
    return (x**2 + y**2)**(1/2)


def closest_films_locations(longtitude, latitude, year):
    film_location = location_to_coordinates(year)
    current_point = longtitude, latitude
    closest_points = {k: v for k, v in sorted(film_location.items(), key=lambda x: mpu.haversine_distance(current_point, x[1]))}
    return closest_points

film_location = {"a": (120, 2), "b": (2, 1), "c":(77, 0)}
closest_points = {k: v for k, v in sorted(film_location.items(), key=lambda x: sum(x[1]))}
print(closest_points)



def location_checker(*coor):
    latitude_checker = re.compile(r"^(\d|[1-8]\d|90)\.\d+")
    longtitude_checker = re.compile(r"^(\d|\d\d|1[0-7]\d|180)\.\d+")
    if not latitude_checker.fullmatch(coor[0]):
        print("Wrong latitude")
        res = False
    elif not longtitude_checker.fullmatch(coor[1]):
        print("Wrong longtitude")
        res = False
    else:
        res = True
    return res


def user_input():
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
        if not location_checker(longtitude, latitude):
            return
    except:
        print("Location in a wrong format")
        return
    return int(year_input), float(longtitude), float(latitude)


def map_builder(year, longtitude, latitude, num=10):
    mapp = folium.Map()
    fg = folium.FeatureGroup("Films nearby")
    closest_locations = closest_films_locations(longtitude, latitude, year)
    num = num
    print("Please wait...")
    for film in closest_locations:
        loc = closest_locations.get(film)
        fg.add_child(folium.Marker(location=loc, popup=film, icon=folium.Icon()))
        num -= 1
        if not num:
            break
    mapp.add_child(fg)
    mapp.save("map_1.html")


def run():
    us_input = user_input()
    if user_input != None:
        year, longtitude, latitude = us_input
        map_builder(year, longtitude, latitude)
        print("Finished. Please have look at the map map_1.html")
    else:
        return


if __name__ == "__main__":
    # run()
    pass

