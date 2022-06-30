
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from os import system, name
from time import sleep

import names

import logging




# Define App class
class App:

    # Initialise graph database using neo4j api credentials
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # Close driver connection
    def close(self):
        self.driver.close()

    # Create new Person vertex with random name
    def create_person(self):
        with self.driver.session() as session:
            
            # Get random name
            person_name = names.get_full_name()
            
            # Create person vertex
            session.write_transaction(self._create_person, person_name)
            
            # Create relationships from new person to existing
            session.write_transaction(self._create_relationships, person_name)

            # Return name string to display
            return person_name

    # Static method to create person vertex and return result
    @staticmethod
    def _create_person(tx, person_name):
        query = "CREATE (p:Person{name: '"+ person_name +"'}) RETURN p AS person"
        result = tx.run(query, person_name=person_name)

    # Create relationships from new person to existing at random (with 50% likelihood)
    @staticmethod
    def _create_relationships(tx, person_name):
        query = "MATCH (p:Person{name: '" + person_name + "'}),(o:Person) WHERE NOT(id(p)=id(o)) WITH p,o WHERE rand()<0.5 CREATE (p)-[:KNOWS]->(o), (p)<-[:KNOWS]-(o)"
        result = tx.run(query, person_name=person_name)

    # Clear graph database: delete all nodes and relationships
    def clear_graph_database(self):
        with self.driver.session() as session:
            query = "MATCH (n) DETACH DELETE n"
            session.run(query)

