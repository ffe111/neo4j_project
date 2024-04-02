#! /usr/bin/env python3
"""
64160118 Thanakrit Nupim
Project 3: Highway Neo4j
This program is 'main.py'
program 
"""
import neo4j
from compass_16point import *
from menu import *


""" RUN CYPHER PROCESS """
def check_retval(*, msg, retval):
    if retval == EXIT_FAILURE:
        # print(f'{msg}')
        raise ValueError(msg)

def isfloat(value):
    try:
        float_value = float(value)
        if str(float_value) != value:  
            return False
        if value.startswith("0") and len(value) > 1 and '.' not in value:  
            return False
        return True
    except ValueError:
        return False

def call_error(*, the_cypher, badnews, records, summary):
    """ For Call Cypher error message """
    # we have any bad news
    print(the_cypher)
    print("Oh no:")
    for itemno, item in enumerate(badnews,start=1):
        print(itemno,item)
    print("records:",records)
    print("summary.result_available_after:", summary.result_available_after)
    print("summary.summary_notifications:", summary.summary_notifications)

def run_void_cypher(*, driver, the_cypher):
    """ For Cypher code that does not return anything normally """
    try:
        records, summary, keys = driver.execute_query(the_cypher, database_=DBNAME)
        if summary.notifications is not None:
            badnews=[]
            for item in summary.notifications:
                if item['severity']!='INFORMATION': # ignore
                    badnews.append(item)
            if len(badnews)==0: # hey, no problems we care about
                return EXIT_SUCCESS
            # we have any bad news
            call_error(the_cypher=the_cypher, badnews=badnews, records=records, summary=summary)
            return EXIT_FAILURE
    except neo4j.exceptions.ClientError as xcpn:
        if xcpn.code == "Neo.ClientError.Schema.ConstraintValidationFailed":
            return EXIT_SUCCESS
        print(the_cypher)
        print(xcpn)
        return EXIT_FAILURE
    return EXIT_SUCCESS

def run_cypher(*, driver, the_cypher):
    """ For Cypher code that does return something normally """
    try:
        records, summary, keys = driver.execute_query(the_cypher, database_=DBNAME)
        if summary.notifications is not None:
            badnews=[]
            for item in summary.notifications:
                if item['severity']!='INFORMATION': # ignore
                    badnews.append(item)
            if len(badnews)==0: # hey, no problems we care about
                return EXIT_SUCCESS, records, summary, keys
            # we have any bad news
            call_error(the_cypher=the_cypher, badnews=badnews, records=records, summary=summary)
            return EXIT_FAILURE, None, None, None
    except neo4j.exceptions.ClientError as xcpn:
        print(the_cypher)
        print(xcpn)
        return EXIT_FAILURE, None, None, None
    return EXIT_SUCCESS, records, summary, keys
    """ For Cypher code that does return something normally """
    try:
        records, summary, keys = driver.execute_query(the_cypher, database_=DBNAME)
        if summary.notifications is not None:
            badnews=[]
            for item in summary.notifications:
                if item['severity']!='INFORMATION': # ignore
                    badnews.append(item)
            if len(badnews)==0: # hey, no problems we care about
                return EXIT_SUCCESS, records, summary, keys
            # we have any bad news
            call_error(the_cypher=the_cypher, badnews=badnews, records=records, summary=summary)
            return EXIT_FAILURE, None, None, None
    except neo4j.exceptions.ClientError as xcpn:
        print(the_cypher)
        print(xcpn)
        return EXIT_FAILURE, None, None, None
    return EXIT_SUCCESS, records, summary, keys


""" INTIALIZE PROCESS """
def drop_constraint(*, driver):
    # drop unique constraint on node names, if it exists
    drop_constraint_cypher = f"""\
    DROP CONSTRAINT nodes_are_unique IF EXISTS;
    """
    retcode = run_void_cypher(driver=driver, the_cypher=drop_constraint_cypher)
    if retcode == EXIT_FAILURE:
        return retcode

def create_constraint(*, driver):
    # create constraint that node names are unique
    create_constraint_cypher = """\
    CREATE CONSTRAINT nodes_are_unique IF NOT EXISTS FOR (p:Place) REQUIRE (p.name) IS UNIQUE;
    """
    retcode = run_void_cypher(driver=driver, the_cypher=create_constraint_cypher)
    if retcode == EXIT_FAILURE:
        return retcode

def drop_index(*, driver):
    # drop index node and relation , if it exists
    drop_indexs_cypher = ["DROP INDEX name_index IF EXISTS;", "DROP INDEX relation_index IF EXISTS;"]
    for cypher in drop_indexs_cypher:
        retcode = run_void_cypher(driver=driver, the_cypher=cypher)
        if retcode == EXIT_FAILURE:
            return retcode

def create_index(*, driver):
    # create index node on place name
    create_index_cypher = """\
    CREATE INDEX name_index IF NOT EXISTS FOR (p:Place) ON (p.name);
    """
    retcode = run_void_cypher(driver=driver, the_cypher=create_index_cypher)
    if retcode == EXIT_FAILURE:
        return retcode

    # create index relation on road name
    create_index_cypher2 = """\
    CREATE INDEX relation_index IF NOT EXISTS FOR ()-[r:CONNECTS_TO]-() ON (r.name);
    """
    retcode = run_void_cypher(driver=driver, the_cypher=create_index_cypher2)
    if retcode == EXIT_FAILURE:
        return retcode

def bulk_loader(*, driver):
    delete_all_cypher = "MATCH (N) DETACH DELETE N"
    retval = run_void_cypher(driver=driver, the_cypher=delete_all_cypher)
    if retval == EXIT_FAILURE:
        return EXIT_FAILURE
    
    with open("highway_data.txt", "r") as f:
        data = f.read()
        retval = run_void_cypher(driver=driver, the_cypher=data)
        if retval == EXIT_FAILURE:
            return EXIT_FAILURE
    return EXIT_SUCCESS

    delete_all_cypher = "MATCH (N) DETACH DELETE N"
    retval = run_void_cypher(driver=driver, the_cypher=delete_all_cypher)
    if retval == EXIT_FAILURE:
        return EXIT_FAILURE
    
    with open("highway_data.txt", "r") as f:
        data = f.read()
        retval = run_void_cypher(driver=driver, the_cypher=data)
        if retval == EXIT_FAILURE:
            return EXIT_FAILURE
    return EXIT_SUCCESS

def initialize_db(*, driver):
    """ For intialize database """
    retval = drop_constraint(driver=driver)
    msg = "Failed to drop_constraint."
    check_retval(msg=msg, retval=retval)
    
    retval = create_constraint(driver=driver)
    msg = "Failed to create_constraint."
    check_retval(msg=msg, retval=retval)
    
    retval = drop_index(driver=driver)        
    msg = "Failed to drop_index."
    check_retval(msg=msg, retval=retval)
    
    retval = create_index(driver=driver)
    msg = "Failed to create_index."
    check_retval(msg=msg, retval=retval)
    
    retval = bulk_loader(driver=driver)
    msg = "Failed to load_data."
    check_retval(msg=msg, retval=retval)


""" ADD NODE & RELATION PROCESS """
def choose_nodes(*, driver):
    # node_type = "MATCH (n:Place) RETURN DISTINCT n.type AS type"
    # retcode, records, summary, keys = run_cypher(
    #     driver=driver, the_cypher=node_type)
    # if retcode == EXIT_FAILURE:
    #     return retcode
    
    per_page = 5
    skip = 0
    # types = [i.data()['type'] for i in records]
    types = ['district', 'sub-district', 'intersection']
    selected_type=''
    while True:
        if selected_type == '':
            print("Select Node Type")
            selected_type = get_choice(msg="Choose type of nodes: ", choice_data=types)
            # Find number of node by type
            count_node_cypher = "MATCH (n:Place {{type: '{0}'}}) RETURN count(n) AS number"
            retcode, records, summary, keys = run_cypher(
            driver=driver, the_cypher=count_node_cypher.format(selected_type))
            max_num = records[0].data()["number"]
        
        get_node_by_type = "MATCH (n:Place {{type: '{type}'}}) RETURN n ORDER BY n.name SKIP {skip} LIMIT {per_page}"
        retcode, records, summary, keys = run_cypher(driver=driver, 
        the_cypher=get_node_by_type.format(
            type=selected_type ,skip=skip, per_page=per_page
            ))
        nodes_name = [i.data()["n"]["name"] for i in records]

        if skip + per_page < max_num:
            nodes_name.append("Next")
        if skip > 0:
            nodes_name.append("Previous")
        nodes_name.append("Back")
        
        print(f"Select {selected_type.upper()} Name")
        selected_node = get_choice(choice_data=nodes_name)

        match selected_node:
            case "Next":
                skip += per_page
            case "Previous":
                skip -= per_page
            case "Back":
                selected_type=''
            case _:
                return selected_node

def node_name_input():
    while True:
        node_name = input("Enter Node name: ")
        if node_name == "":
            print("Node name cannot be empty.")
            continue
        break
    return node_name

def node_type_input():
    types = ['district', 'sub-district', 'intersection']
    max_len = len(types)
    while True:
        for numb, data in enumerate(types, start=1):
            print(f"{numb}: {data}")
        try:
            choice = int(input("Choose numba for Node type: "))
            if choice <= max_len and choice > 0:
                print(f"You choose {choice} is '{types[choice-1]}'")
                node_type = types[choice-1]
            else:
                raise ValueError("Invalid input")
        except (ValueError, EOFError) as xcpn:
            print(f"Please enter value choice. (between 1-{max_len})")

        break
    return node_type

def node_latitude_input():
    while True:
        node_latitude = input("Enter Node latitude: ")
        if node_latitude == "":
            print("Node latitude cannot be empty.")
            continue
        if node_latitude[0] == "-":
            if not isfloat(node_latitude[1:]):
                print("Node latitude must be a float number.")
                continue
        else:
            if not isfloat(node_latitude):
                print("Node latitude must be a float number.")
                continue
        break
    return node_latitude

def node_longitude_input():
    while True:
        node_longitude = input("Enter Node longitude: ")
        if node_longitude == "":
            print("Node longitude cannot be empty.")
            continue
        if node_longitude[0] == "-":
            if not isfloat(node_longitude[1:]):
                print("Node longitude must be a float number.")
                continue
        else:
            if not isfloat(node_longitude):
                print("Node longitude must be a float number.")
                continue
        break
    return node_longitude

def node_gas_station_input():
    while True:
        node_gas_station = input("Enter gas station number: ")
        if node_gas_station == "":
            print("Gas station cannot be empty.")
            continue
        elif not node_gas_station.isdigit():
            print("Gas station must be a number.")
            continue
        break
    return node_gas_station

def road_name_input():
    while True:
        road_name = input("Enter Road name: ")
        if road_name == "":
            print("Road name cannot be empty.")
            continue
        break
    return road_name

def road_distance_input():
    while True:
        road_distance = input("Enter Road distance: ")
        if road_distance == "":
            print("Road distance cannot be empty.")
            continue
        if road_distance[0] == "-":
            if not isfloat(road_distance[1:]):
                print("Road distance must be a float number.")
                continue
        else:
            if not isfloat(road_distance):
                print("Road distance must be a float number.")
                continue
        break
    return road_distance

def road_toll_input():
    road_toll=''
    while True:
        road_toll = input("Enter Node toll (Yes/No): ")
        if road_toll == "":
            print("Node toll cannot be empty.")
            continue
        if road_toll not in ["Yes", "No", "yes", "no", "y", "n"]:
            print("Node toll must be 'Yes' or 'No'.")
            continue
        if road_toll == "Yes" or road_toll == "yes" or road_toll == "y":
            road_toll = True
        else:
            road_toll = False
        break
    return road_toll

def add_road(*, driver):
    print("═"*70)
    print(f"{'Add Node (Road)':^70s}")
    print("*"*70)
    print("─"*70)
    print("Add new road")
    node_name = node_name_input()
    node_type = node_type_input()
    node_latitude = node_latitude_input()
    node_longitude = node_longitude_input()
    node_gas_station = node_gas_station_input()

    print("─"*70)
    print("Select start node")
    start_node = choose_nodes(driver=driver)
    road_name_from_start = road_name_input()
    road_distance_from_start = road_distance_input()
    road_toll_from_start = road_toll_input()
    create_node_with_start_node = CREATE_NODE_WITH_RELATION.format(
        start_node,
        node_name,
        node_type,
        node_latitude,
        node_longitude,
        node_gas_station,
        road_name_from_start,
        road_distance_from_start,
        road_toll_from_start,
        road_name_from_start,
        road_distance_from_start,
        road_toll_from_start,
    )
    retval = run_void_cypher(driver=driver, the_cypher=create_node_with_start_node)
    msg = "Failed to create node with start node."
    check_retval(msg=msg, retval=retval)

    while True:
        have_end_node = input("Do you have end node? (Yes/No): ")
        if have_end_node == "":
            print("Have end node cannot be empty.")
            continue
        if have_end_node not in ["Yes", "No", "yes", "no", "y", "n"]:
            print("Have end node must be 'Yes' or 'No'.")
            continue
        if have_end_node == "Yes" or have_end_node == "yes" or have_end_node == "y":
            have_end_node = True
        else:
            have_end_node = False
        break

    if have_end_node:
        print("─"*70)
        print("Select end node")
        end_node = choose_nodes(driver=driver)
        if start_node == end_node:
            print("Start place and end place must be different.")
            return EXIT_FAILURE
        road_name_from_end = road_name_input()
        road_distance_from_end = road_distance_input()
        road_toll_from_end = road_toll_input()
        create_node_with_end_node = CREATE_NODE_WITH_RELATION.format(
            end_node,
            node_name,
            node_type,
            node_latitude,
            node_longitude,
            node_gas_station,
            road_name_from_end,
            road_distance_from_end,
            road_toll_from_end,
            road_name_from_end,
            road_distance_from_end,
            road_toll_from_end
        )
        retval = run_void_cypher(driver=driver, the_cypher=create_node_with_end_node)
        msg = "Failed to create node with end node."
        check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def add_intersect(*, driver):
    print("═"*70)
    print(f"{'Add Node (Intersect)':^70s}")
    print("*"*70)
    print("─"*70)
    print("Add new intersect")
    node_name = node_name_input()
    node_type = node_type_input()
    node_latitude = node_latitude_input()
    node_longitude = node_longitude_input()
    node_gas_station = node_gas_station_input()

    print("─"*70)
    print("Select start node")
    start_node = choose_nodes(driver=driver)
    road_name_from_start = road_name_input()
    road_distance_from_start = road_distance_input()
    road_toll_from_start = road_toll_input()

    print("─"*70)
    print("Select end node")
    end_node = choose_nodes(driver=driver)
    if start_node == end_node:
        print("Start place and end place must be different.")
        return EXIT_FAILURE
    road_name_from_end = road_name_input()
    road_toll_from_end = road_toll_input()
    # road_distance_from_end = road_distance_input()
    relation_data = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) return r.distance AS distance"
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=relation_data.format(start_node, end_node)
    )
    check_retval(msg="", retval=retval)
    if records:
        road_distance_from_end = records[0].data()["distance"] - int(
            road_distance_from_start
        )
        if road_distance_from_end < 0:
            print(
                f"Old distance from start to end is {records[0].data()['distance']}"
            )
            print(f"New distance from start to end is {road_distance_from_end}")
            print(f"New distance from start to end must be greater than 0.")
            return EXIT_FAILURE
    else:
        road_distance_from_end = road_distance_input()
    delete_old_relation = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) DELETE r"
    retval = run_void_cypher(
        driver=driver, the_cypher=delete_old_relation.format(start_node, end_node)
    )
    msg = "Failed to delete old relation."
    check_retval(msg=msg, retval=retval)

    create_node_with_start_node = CREATE_NODE_WITH_RELATION.format(
        start_node,
        node_name,
        node_type,
        node_latitude,
        node_longitude,
        node_gas_station,
        road_name_from_start,
        road_distance_from_start,
        road_toll_from_start,
        road_name_from_start,
        road_distance_from_start,
        road_toll_from_start,
    )
    retval = run_void_cypher(driver=driver, the_cypher=create_node_with_start_node)
    msg = "Failed to create node with start node."
    check_retval(msg=msg, retval=retval)

    create_node_with_end_node = CREATE_NODE_WITH_RELATION.format(
        end_node,
        node_name,
        node_type,
        node_latitude,
        node_longitude,
        node_gas_station,
        road_name_from_end,
        road_distance_from_end,
        road_toll_from_end,
        road_name_from_end,
        road_distance_from_end,
        road_toll_from_end
    )
    retval = run_void_cypher(driver=driver, the_cypher=create_node_with_end_node)
    msg = "Failed to create node with end node."
    check_retval(msg=msg, retval=retval)

    return EXIT_SUCCESS


""" UPDATE NODE & RELATION PROCESS """
def update_node_type(*, driver, selected_node):
    update_node_type_cypher = "MATCH (n:Place {{name: '{}'}}) SET n.type = '{}'"
    node_type = node_type_input()
    retval = run_void_cypher(
        driver=driver, the_cypher=update_node_type_cypher.format(selected_node, node_type)
    )
    msg = "Failed to update node type."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def update_node_latitude(*, driver, selected_node):
    update_node_latitude_cypher = "MATCH (n:Place {{name: '{}'}}) SET n.latitude = {}"
    node_latitude = node_latitude_input()
    retval = run_void_cypher(
        driver=driver,
        the_cypher=update_node_latitude_cypher.format(selected_node, node_latitude),
    )
    msg = "Failed to update node latitude."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def update_node_longitude(*, driver, selected_node):
    update_node_longitude_cypher = "MATCH (n:Place {{name: '{}'}}) SET n.longitude = {}"
    node_longitude = node_longitude_input()
    retval = run_void_cypher(
        driver=driver,
        the_cypher=update_node_longitude_cypher.format(selected_node, node_longitude),
    )
    msg = "Failed to update node longitude."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def update_node_gas_station(*, driver, selected_node):
    update_node_gas_station_cypher = "MATCH (n:Place {{name: '{}'}}) SET n.gas_station = {}"
    node_gas_station = node_gas_station_input()
    retval = run_void_cypher(
        driver=driver,
        the_cypher=update_node_gas_station_cypher.format(selected_node, node_gas_station),
    )
    msg = "Failed to update node gas station."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def display_node_properties(*, driver, selected_node):
    get_node_properties = "MATCH (n:Place {{name: '{}'}}) RETURN n"
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=get_node_properties.format(selected_node)
    )
    check_retval(msg='', retval=retval)

    node = records[0].data()["n"]
    print("─"*70)
    print(f"{'{selected_node} properties':^70s}".format(selected_node=selected_node))
    print("="*70)
    print(f"Name       : {node['name']}")
    print(f"Type       : {node['type']}")
    print(f"Latitude   : {node['latitude']}")
    print(f"Longitude  : {node['longitude']}")
    print(f"Gas Station: {node['gas_station']}")
    print("─"*70)
    return EXIT_SUCCESS

def update_node_properties(*, driver, selected_node):
    retval = display_node_properties(driver=driver, selected_node=selected_node)
    check_retval(msg='', retval=retval)

    selected_property = get_choice(
        msg="Please enter property to update: ",
        choice_data=["Name", "Type", "Latitude", "Longitude", "Gas_Station", "Back"],
    )
    match selected_property:
        case "Name":
            retval = update_node_name(driver=driver, selected_node=selected_node)
            msg = "Failed to update name."
            check_retval(msg=msg, retval=retval)
        case "Type":
            retval = update_node_type(driver=driver, selected_node=selected_node)
            msg = "Failed to update type."
            check_retval(msg=msg, retval=retval)
        case "Latitude":
            retval = update_node_latitude(driver=driver, selected_node=selected_node)
            msg = "Failed to update latitude."
            check_retval(msg=msg, retval=retval)
        case "Longitude":
            retval = update_node_longitude(driver=driver, selected_node=selected_node)
            msg = "Failed to update longitude."
            check_retval(msg=msg, retval=retval)
        case "Gas_Station":
            retval = update_node_gas_station(driver=driver, selected_node=selected_node)
            msg = "Failed to update light."
            check_retval(msg=msg, retval=retval)
        case "Back":
            update_properties(driver=driver)
    return EXIT_SUCCESS

def update_relation_name(*, driver, node1, node2):
    update_relation_name_cypher = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) SET r.name = '{}'"
    new_name = road_name_input()
    retval = run_void_cypher(
        driver=driver,
        the_cypher=update_relation_name_cypher.format(node1, node2, new_name),
    )
    msg = "Failed to update relation name."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def update_relation_distance(*, driver, node1, node2):
    update_relation_distance_cypher = (
        "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) "
        "SET r.distance = {}"
    )
    new_distance = road_distance_input()
    retval = run_void_cypher(
        driver=driver,
        the_cypher=update_relation_distance_cypher.format(node1, node2, new_distance),
    )
    msg = "Failed to update relation distance."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def update_relation_toll(*, driver, node1, node2):
    update_relation_toll_cypher = (
        "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) "
        "SET r.toll = {}"
    )
    new_toll = road_toll_input()
    retval = run_void_cypher(
        driver=driver,
        the_cypher=update_relation_toll_cypher.format(node1, node2, new_toll),
    )
    msg = "Failed to update relation toll."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def update_relation_properties(*, driver, selected_node):
    related_nodes_cypher = (
        "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place) RETURN DISTINCT m"
    )
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=related_nodes_cypher.format(selected_node)
    )
    check_retval(msg='', retval=retval)

    related_nodes = [i.data()["m"]["name"] for i in records]
    selected_related_node = get_choice(
        msg="Please enter related node to update: ", choice_data=related_nodes
    )

    relation_detail_cypher = (
        "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) "
        "RETURN r.name, r.distance, r.toll"
    )
    retval, records, summary, keys = run_cypher(
        driver=driver,
        the_cypher=relation_detail_cypher.format(selected_node, selected_related_node),
    )
    check_retval(msg='', retval=retval)

    relation = records[0].data()
    # print(relation)
    print("─"*70)
    print(f"{'relation properties':^70s}")
    print("="*70)
    print(f"Name    : {relation['r.name']}")
    print(f"Distance: {relation['r.distance']}")
    print(f"Toll    : {relation['r.toll']}")
    print("─"*70)

    selected_property = get_choice(
        msg="Please enter property to update: ", choice_data=["Name", "Distance", "Toll"]
    )
    match selected_property:
        case "Name":
            retval = update_relation_name(
                driver=driver, node1=selected_node, node2=selected_related_node
            )
            msg = "Failed to update relation name."
            check_retval(msg=msg, retval=retval)
        case "Distance":
            retval = update_relation_distance(
                driver=driver, node1=selected_node, node2=selected_related_node
            )
            msg = "Failed to update relation distance."
            check_retval(msg=msg, retval=retval)
        case "Toll":
            retval = update_relation_toll(
                driver=driver, node1=selected_node, node2=selected_related_node
            )
            msg = "Failed to update relation toll."
            check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def add_relation(*, driver, selected_node):
    not_related_nodes_cypher = """
        MATCH (n:Place)
        WHERE NOT (n)-[:CONNECTS_TO]-(:Place {{name: '{}'}})
        RETURN n.name AS name
    """
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=not_related_nodes_cypher.format(selected_node)
    )
    check_retval(msg='', retval=retval)

    not_related_nodes = [
        record.data()["name"]
        for record in records
        if record.data()["name"] != selected_node
    ]

    if len(not_related_nodes) == 0:
        print("No node that not related to this node")
        return EXIT_SUCCESS

    selected_related_node = get_choice(
        msg="Please enter what your want to connect with: ",
        choice_data=not_related_nodes,
    )

    road_name = road_name_input()
    road_distance = road_distance_input()
    road_toll = road_toll_input()

    create_relation_cypher = (
        "MATCH (n:Place {{name: '{}'}}), (m:Place {{name: '{}'}})"
        "CREATE (n)-[:CONNECTS_TO {{name: '{}', distance: {}}}]->(m),"
        "(m)-[:CONNECTS_TO {{name: '{}', distance: {}, toll: {}}}]->(n)"
    )

    retval = run_void_cypher(
        driver=driver,
        the_cypher=create_relation_cypher.format(
            selected_node,
            selected_related_node,
            road_name,
            road_distance,
            road_name,
            road_distance,
            road_toll
        ),
    )
    msg = "Failed to create relation."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def delete_relation(*, driver, selected_node):
    related_nodes_cypher = """
        MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place) RETURN DISTINCT m
    """
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=related_nodes_cypher.format(selected_node)
    )
    check_retval(msg='', retval=retval)

    related_nodes = [i.data()["m"]["name"] for i in records]
    selected_related_node = get_choice(
        msg="Please enter related node to delete: ", choice_data=related_nodes
    )

    while True:
        confirm = input("Are you sure to delete this relation? (Yes/No): ")
        if confirm == "":
            print("Confirm cannot be empty.")
            continue
        if confirm not in ["Yes", "No", "yes", "no", "y", "n"]:
            print("Confirm must be 'Yes' or 'No'.")
            continue
        if confirm == "Yes" or confirm == "yes" or confirm == "y":
            confirm = True
        else:
            confirm = False
        break

    if not confirm:
        return EXIT_SUCCESS

    delete_relation_cypher = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) DELETE r"
    retval = run_void_cypher(
        driver=driver,
        the_cypher=delete_relation_cypher.format(selected_node, selected_related_node),
    )
    msg = "Failed to delete relation."
    check_retval(msg=msg, retval=retval)
    return EXIT_SUCCESS

def relation_properties_menu(*, driver, selected_node):
    selected_action = get_choice(
        msg="Please enter action: ", choice_data=["Add", "Edit", "Delete", "Back"]
    )
    match selected_action:
        case "Add":
            add_relation(driver=driver, selected_node=selected_node)
        case "Edit":
            update_relation_properties(driver=driver, selected_node=selected_node)
        case "Delete":
            delete_relation(driver=driver, selected_node=selected_node)
        case "Back":
            update_properties(driver=driver)

def update_properties(*, driver):
    print("═"*70)
    print(f"{'Update Properties':^70s}")
    print("*"*70)
    print("Select choice of update")
    selected_place = choose_nodes(driver=driver)

    print(f"update properties of {selected_place}")
    selected_update = get_choice(
        msg="Please enter update: ", choice_data=["Node", "Relation", "Exit"]
    )
    match selected_update:
        case "Node":
            update_node_properties(driver=driver, selected_node=selected_place)
        case "Relation":
            relation_properties_menu(driver=driver, selected_node=selected_place)
        case "Exit":
            return EXIT_SUCCESS
    return EXIT_SUCCESS


""" DELETE NODE PROCESS """
def delete_node(*, driver):
    print("═"*70)
    print(f"{'Delete Node':^70s}")
    print("*"*70)
    print("Select node to delete")
    selected_node = choose_nodes(driver=driver)

    # check node related of selected_node
    related_nodes_check = (
        "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place) RETURN DISTINCT m AS node"
    )

    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=related_nodes_check.format(selected_node)
    )
    check_retval(msg='', retval=retval)

    related_nodes = [i.data()["node"]["name"] for i in records]
    
    road_dict = {}
    road_properties_cypher = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) RETURN r.distance AS distance, r.toll AS toll"
    for node in related_nodes:
        retval, records, summary, keys = run_cypher(
            driver=driver, the_cypher=road_properties_cypher.format(selected_node, node)
        )
        check_retval(msg='', retval=retval)
        road_dict[node] = records[0].data()

    pair_related_nodes = []
    for i in range(len(related_nodes)):
        for j in range(i + 1, len(related_nodes)):
            pair_related_nodes.append((related_nodes[i], related_nodes[j]))

    for pair in pair_related_nodes:
        start_node = pair[0]
        end_node = pair[1]
        total_distance = road_dict[start_node]['distance'] + road_dict[end_node]['distance']
        if road_dict[start_node]['toll'] == True or road_dict[end_node]['toll'] == True: 
            toll = True 
        else:
            toll = False

        check_exist_relation = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) RETURN count(r) AS count"
        retval, records, summary, keys = run_cypher(
            driver=driver, the_cypher=check_exist_relation.format(start_node, end_node)
        )
        check_retval(msg='', retval=retval)

        if records[0].data()["count"] == 0:
            create_relation = """\
                MATCH (n:Place) WHERE n.name = '{}' 
                MATCH (m:Place) WHERE m.name = '{}' 
                CREATE (n)-[:CONNECTS_TO {{name: '{}', distance: {}, toll: {}}}]->(m),
                (m)-[:CONNECTS_TO {{name: '{}', distance: {}, toll: {}}}]->(n)
            """
            retval = run_void_cypher(
                driver=driver,
                the_cypher=create_relation.format(
                    start_node,
                    end_node,
                    f"{start_node} to {end_node}",
                    total_distance, toll,
                    f"{start_node} to {end_node}",
                    total_distance, toll
                ),
            )
            msg = "Failed to create relation."
            check_retval(msg=msg, retval=retval)

    delete_node_cypher = "MATCH (n:Place {{name: '{}'}}) DETACH DELETE n"
    retval = run_void_cypher(
        driver=driver, the_cypher=delete_node_cypher.format(selected_node)
    )
    msg = "Failed to delete node."
    check_retval(msg=msg, retval=retval)

    return EXIT_SUCCESS


""" FIND PATH SHORT PROCESS """
def display_shortest_path(*, map, driver):
    # map = [("A", "B"), ("B", "C"), ("C", "D")]
    print("═"*70)
    print(f"{'Short Path Plan':^70s}")
    print("*"*70)
    for i in range(len(map)):
        if i == 0:
            print(f"Shortest path from {map[i][0][0]} {map[i][0][1]} to {map[-1][0][0]} {map[-1][1][1]}")
            print(f"Start at {map[i][0][0]} {map[i][0][1]}")

        node_data = "MATCH (n:Place {{name: '{}'}}), (m:Place {{name:'{}'}}) RETURN n,m"
        retval, records, summary, keys = run_cypher(
            driver=driver, the_cypher=node_data.format(map[i][0][1], map[i][1][1])
        )
        if retval == EXIT_FAILURE:
            return EXIT_FAILURE

        result = records[0].data()
        n, m = result["n"], result["m"]
        vector = [(n["longitude"], n["latitude"]), (m["longitude"], m["latitude"])]
        direction = get_compass_direction(vector=vector)

        relation_data = "MATCH (n:Place {{name: '{}'}})-[r:CONNECTS_TO]-(m:Place {{name: '{}'}}) RETURN r.name, r.distance, r.toll"
        retval, records, summary, keys = run_cypher(
            driver=driver, the_cypher=relation_data.format(map[i][0][1], map[i][1][1])
        )
        if retval == EXIT_FAILURE:
            return EXIT_FAILURE

        relation = records[0].data()
        print(f"Head {direction}")
        if relation['r.toll'] == False:
            print(
                f"then go to {map[i][1][0]} {map[i][1][1]} on {relation['r.name']} ({relation['r.distance']} km), road no toll,",
                end=" ",
            )
            if m["gas_station"] > 0:
                print(f"has a",m["gas_station"],"gas station.")
            else:
                print("no gas station.")
            if i == len(map) - 1:
                print(f"and you have arrived at at your destination {map[i][1][0]} {map[i][1][1]}")
        else:
            print(
                f"then go to {map[i][1][0]} {map[i][1][1]} on {relation['r.name']} ({relation['r.distance']}) km), road have toll,",
                end=" ",
            )
            if m["gas_station"] > 0:
                print(f"has a",m["gas_station"],"gas station.")
            else:
                print("no gas station.")
            if i == len(map) - 1:
                print(f"and you have arrived at at your destination {map[i][1][0]} {map[i][1][1]}")

def get_shortest_path_by_distance(*, driver):
    print("═"*70)
    print(f"{'Get the shortest path by distance':^70s}")
    print("*"*70)
    print("Select start node")
    start_node = choose_nodes(driver=driver)
    print("Select end node")
    end_node = choose_nodes(driver=driver)
    if start_node == end_node:
        print("Start place and end place must be different.")
        return EXIT_FAILURE

    drop_graph = "CALL gds.graph.drop('myGraph', false) YIELD graphName;"
    retval = run_void_cypher(driver=driver, the_cypher=drop_graph)
    msg = "Failed to drop graph."
    check_retval(msg=msg, retval=retval)
    
    create_graph = """\
    CALL gds.graph.project(
        'myGraph',
        'Place',
        {CONNECTS_TO: {orientation: 'UNDIRECTED'}},
        {
            relationshipProperties: 'distance'
        }
    );
    """

    retval = run_void_cypher(driver=driver, the_cypher=create_graph)
    msg = "Failed to create graph."
    check_retval(msg=msg, retval=retval)

    dijkstra_cypher = """
    MATCH (source:Place {{name: '{}'}}), (target:Place {{name: '{}'}})
    CALL gds.shortestPath.dijkstra.stream('myGraph', {{
        sourceNode: source,
        targetNode: target,
        relationshipWeightProperty: 'distance'
    }})
    YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
    RETURN
        index,
        gds.util.asNode(sourceNode).name AS sourceNodeName,
        gds.util.asNode(targetNode).name AS targetNodeName,
        totalCost,
        [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
        costs,
        nodes(path) as path
    ORDER BY index;
    """
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=dijkstra_cypher.format(start_node, end_node)
    )
    check_retval(msg='', retval=retval)

    for record in records:
        data = record.data()["path"]
        name_map = [[i["type"], i["name"]] for i in data]
        bob = list(zip(name_map, name_map[1:]))
        display_shortest_path(driver=driver, map=bob)

def get_shortest_path_by_node(*, driver):
    print("═"*70)
    print(f"{'Get the shortest path by node':^70s}")
    print("*"*70)
    print("Select start node")
    start_node = choose_nodes(driver=driver)
    print("Select end node")
    end_node = choose_nodes(driver=driver)
    if start_node == end_node:
        print("Start place and end place must be different.")
        return EXIT_FAILURE

    cypher = """
    MATCH
      (start:Place {{name: '{}'}}),
      (end:Place {{name: '{}'}}),
      p = shortestPath((start)-[*]-(end))
    WHERE length(p) > 1
    RETURN p
    """
    retval, records, summary, keys = run_cypher(
        driver=driver, the_cypher=cypher.format(start_node, end_node)
    )
    check_retval(msg='', retval=retval)

    for record in records:
        path = record.data()["p"]
        print("Shortest path:")

        node_names = []
        for i in range(len(path)):
            print(path[i])
            if i % 2 == 0:
                node_names.append([path[i]["type"], path[i]["name"]])
        bob = list(zip(node_names, node_names[1:]))
        display_shortest_path(driver=driver, map=bob)


def main():
    try:
        with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
            while True:
                choose = input("Can you initialize database (Yes/No): ")
                match choose:
                    case "Yes" | "yes" | "y":
                        # run initialize database
                        retval = initialize_db(driver=driver)
                        if retval == EXIT_FAILURE:
                            print("Failed to initialize database.")
                            return EXIT_FAILURE
                        print("Success to initialize database.")
                        choosed = 'No'
                    case  "No" | "no" | "n":
                        while True:
                            try:
                                # run menu main
                                retcode = main_menu(mdata=[
                                    ("Get the shortest path by distance", get_shortest_path_by_distance),
                                    ("Get the shortest path by node", get_shortest_path_by_node),
                                    ("Add Node (Road)", add_road),
                                    ("Add Node (Intersect)", add_intersect),
                                    ("Update Properties", update_properties),
                                    ("Delete Node", delete_node),
                                    ],
                                driver=driver)
                                if retcode == EXIT_SUCCESS:
                                    return EXIT_SUCCESS
                            except BackMenu as go_main:
                                print(go_main)
                            except ValueError as err_msg:
                                print(err_msg)
 
    except neo4j.exceptions.ServiceUnavailable as xcpn:
        print(f"Can't Connect Database: \n{xcpn}")
    except KeyboardInterrupt:
        print("User: Exit with Ctrl-C ")
        return EXIT_SUCCESS

CREATE_NODE_WITH_RELATION = """
    MATCH (n:Place) WHERE n.name = '{}'
    MERGE (m:Place {{name: '{}', type: '{}', latitude: {}, longitude: {}, gas_station: {}}})
    CREATE (n)-[:CONNECTS_TO {{name: '{}', distance: {}, toll: {}}}]->(m),
    (m)-[:CONNECTS_TO {{name: '{}', distance: {}, toll: {}}}]->(n)
"""

DBNAME = "neo4j"
URI, AUTH = "neo4j://localhost", ("neo4j", "64160118")
EXIT_SUCCESS, EXIT_FAILURE = 0, 1
if __name__ == "__main__":
    raise SystemExit(main())