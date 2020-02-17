'''
Pavlo Semchyshyn

'''

from collections import defaultdict


def read_file(path):
    """
    Reads file and returns a generator, which
    yields year, film and location as a tuple
    """
    with open(path, "r", encoding="latin1") as file_to_read:
        line = file_to_read.readline()
        while not line.startswith("="):
            line = file_to_read.readline()
        while not line.startswith("\""):
            line = file_to_read.readline()
        for line in file_to_read:
            if "}" in line:
                continue
            line = line.strip()
            first_point = line.find("(")
            second_point = line.find(")")
            year = line[first_point + 1: second_point]
            if not year.isdigit():
                continue
            film = line[: first_point].strip().strip("\"")
            if ")" in line[second_point + 1:]:
                third_point = line.find(")", second_point + 1)
                location = line[third_point + 1:].strip()
            else:
                location = line[second_point + 1:].strip()
            if len(location) < 2:
                continue
            yield year, film, location


def films_by_year(lines):
    """
    Returns a dictionary with year as a key,
    and list of the name of film and location
    as value
    """
    dict_of_films = defaultdict(list)
    for year, film, location in lines:
        dict_of_films[year].append((film, location))
    return dict_of_films


def all_films_in_year(year, dict_of_films):
    """
    Returns a dictionary of films, shot in one year,
    as name of film as key and location as value
    """
    film_location = {}
    if str(year) in dict_of_films:
        for film, location in dict_of_films[str(year)]:
            film_location[film] = location
    return film_location


CONTENTS = read_file("locations.list")
DICT_OF_FILMS = films_by_year(CONTENTS)


if __name__ == "__main__":
    FILM_IN_YEAR = all_films_in_year(2010, DICT_OF_FILMS)
