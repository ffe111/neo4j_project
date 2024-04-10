# neo4j_project

## About project:

Project Highway Eastern seaboard of Thailand with Neo4j
from Bangna to Koh Chang.
First of all, I would like to thank my friends
for their cooperation in collecting data from Google Map.
from this data consists of 1. nodes, represented to areas,
collecting properties about:
name: is a area name.
type: is a ['district', 'sub-district', 'intersection'].
latitude: is latitude.
longitude: is longitude.
gas_station: is number of gas station from area.
and 2. relationships, represented to roads.
collecting properties about:
name: is a road name.
distance: is a distance from this road.
toll: is a toll from this road.

My project is developed on Windows operating system.
Program ask about intialize database for insert data
make CURD such as - Create is Add Node for added according to desired
destinations and can add inserted nodes between
connected nodes. - Update is Update Properties from Node and Relationship. - Read is Get this data node from database by
Search Short Path can find a path from the
starting point to the ending point. and can
find the shortest distance. - Delete is Delete Node from database.

## Requirement:

```
Python 3.11.7 or better.
(https://www.python.org/downloads/)
pip install neo4j
Openjdk 17.0.10 or better.
(https://jdk.java.net/archive/)
Neo4j 5.18.1
(https://neo4j.com/docs/operations-manual/current/installation/)
Graph Data Science 2.6.2
(https://neo4j.com/docs/graph-data-science/current/installation/)
```

## Before use Program:

```
   1. read README.txt see about detail and Requirement.
   2. you should check this neo4j is start or use command:

   neo4j start (for Window)

   3. you should create python environment command:

   python -m venv --clear --copies --upgrade-deps --prompt ’neo4jvenv’ neo4jvenv

   4. when create environment success you can see ./neo4jvenv directory
      you should active python environment by command:

   neo4jvenv/Scripts/activate (for Window)

      and install library by requirement.txt by command:

   python -m pip install -r requirement.txt (For Window)

   5. you must change the username and password in AUTH to match your database.
   (in 'main.py' line: 1129) Before starting to use this program.

   6. if not found problem, That's mean
   you ready to use This Project Program!!!
```

## About File in Project:

```
64160118/                  | head folder
64160118/README.txt        | this file. tell about project
64160118/requirement.txt   | library requirement for python pip install
64160118/highway_data.txt  | highway data for insert to database
64160118/compass_16point.py| program for tell direction from latitude longitude
64160118/main.py           | program for use manage database [CURD, Search path]
64160118/menu.py           | program for display menu text interface
```

## How to use:

```
1. before run this program
   you must change the username and password
   in AUTH (in 'main.py' line: 1129)
   to match your database.

2. run main.py to use program
   program will ask you for intialize database
   you should enter Yes or y to
   Can you initialize database (Yes/No): y
   Success to initialize database.

3. second step before you initialize database
   Success. program will ask you again for
   intialize database, you sholud enter No or n
   to start this program menu
   Can you initialize database (Yes/No): n
   program will display menu interface.

4. you can use this function from interface menu
```
