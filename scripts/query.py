from pymongo import MongoClient
from bson.son import SON
import collections

def query():
    """Carry out the queries reported in the
    project description"""

    # Open mongodb
    client = MongoClient('localhost:27017')
    db = client.elements

    # How many elements are there by type?
    print('*' * 50)
    print("Nodes: {}".format(db.nodes.count()))
    print("Ways: {}".format(db.ways.count()))
    print("Relations: {}".format(db.relations.count()))

    # How many users contributed to the map?
    print('*' * 50)
    users_nodes = db.nodes.distinct('created.user')
    users_ways = db.ways.distinct('created.user')
    users_relations = db.relations.distinct('created.user')

    users = users_nodes + users_ways + users_relations

    print("{} users contributed to the map".format(len(set(users))))

    # Who are the most popular users?
    print('*' * 50)
    pipeline = [
        {"$unwind": "$created"},
        {"$unwind": "$created.user"},
        {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    most_popular_keys = list(db.nodes.aggregate(pipeline))[1:10]

    for index, top_user in enumerate(most_popular_keys):
        print("{}. {} contributed {} elements".format(index + 1, \
        most_popular_keys[index]["_id"], most_popular_keys[index]["count"]))

    # What are the most common amenities
    print('*' * 50)
    pipeline = [
        {"$unwind": "$amenity"},
        {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    most_important_amenities = list(db.nodes.aggregate(pipeline))[1:10]

    for index, top_amenity in enumerate(most_important_amenities):
        print("{}. {} occurs {} times".format(index + 1, top_amenity["_id"], top_amenity["count"]))

    # How many asian restaurants are there?
    print('*' * 50)
    amenities = db.nodes.find({'cuisine': 'asian', 'amenity': 'restaurant'})

    print("There are {} asian restaurants".format(amenities.count()))

    for amenity in amenities:
        print("{}".format(amenity['name']))

    # How many places are accessible for wheelchair users?
    print('*' * 50)
    non_accessible = db.nodes.find({'wheelchair': 'yes'}).count()
    accessible     = db.nodes.find({'wheelchair': 'no'}).count()

    print("{} % of places are accessible for wheelchair users".format(round(accessible / (float(accessible) + non_accessible), 4) * 100))


if __name__ == "__main__":
    query()
