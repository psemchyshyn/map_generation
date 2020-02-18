# map_generation
Building a map for finding film locations in a particular year


Usage:
___________________________________________
The programm consists of 3 python modules, the module, which runs the programm is main.py.
In github repository there are also files for locations.list with films, the year
in which they are shot and their locations, inf.csv with infected by coronavirus places and cities_coordinates.tsv
with coordiantes of some places on the globe.
___________________________________________
The main role of the module is to allow the user by inputting a year and random coordiantes in latitude and longtitude get ~10 closest film locations, which were shot in that year. The result of running the programm is a generated html file, which represents an interactive map.(three layers)
-Initial layer:
-Second layer: represents a markers with films(description above) 
-Third layer: on the basis of information in inf.csv file shows places(countries, cities - as circle markers),
which were infected by Coronavirus. Data is actual on 09.02.2020


HTML - structure:
__________________________________________

Conclusions:
__________________________________________
The programm is useful, for analysing films and their locations by providing a year and coordinates

Examples:
__________________________________________
![alt text]https://raw.githubusercontent.com/psemchyshyn/map_generation/master/Input_example.png
(https://raw.githubusercontent.com/psemchyshyn/map_generation/master/Corona_virus_example.png)
![]https://raw.githubusercontent.com/psemchyshyn/map_generation/master/Example_run.png

