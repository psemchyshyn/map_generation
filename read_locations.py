from collections import defaultdict


def read_file(path):
    with open(path, "r", encoding="latin1") as f:
        line = f.readline()
        while not line.startswith("="):
            line = f.readline()
        while not line.startswith("\""):
            line = f.readline()
        for line in f:
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
    dict_of_films = defaultdict(list)
    for year, film, location in lines:
        dict_of_films[year].append((film, location))
    return dict_of_films


def all_films_in_year(year, dict_of_films):
    film_location = {}
    if str(year) in dict_of_films:
        for film, location in dict_of_films[str(year)]:
            film_location[film] = location
    return film_location


contents = read_file("locations.list")
dict_of_films = films_by_year(contents)


if __name__ == "__main__":
    film_in_year = all_films_in_year(2010, dict_of_films)



