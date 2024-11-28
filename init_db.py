
from neo4j import GraphDatabase, basic_auth


def init_neo4j():
    neo4j_driver = GraphDatabase.driver(
        "bolt://3.89.131.242:7687",
        auth=basic_auth("neo4j", "windings-life-harm"))
    return neo4j_driver