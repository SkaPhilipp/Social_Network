
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
            person_name = names.get_full_name()
            result = session.write_transaction(self._create_person, person_name)

            # Print that person vertex successful created
            for row in result:
                print(row)
                print("Created person: {p}".format(p = row['person']))

    # Static method to create person vertex and return result
    @staticmethod
    def _create_person(tx, person_name):
        query = "CREATE (p:Person{name: '"+ person_name +"'}) RETURN p AS person"
        result = tx.run(query, person_name=person_name)
        for row in result:
            print(row)
        #return [row[""] for row in result]

    # Clear graph database: delete all nodes and relationships
    def clear_graph_database(self):
        with self.driver.session() as session:
            query = "MATCH (n) DETACH DELETE n"
            session.run(query)















    def create_friendship(self, person1_name, person2_name):

        with self.driver.session() as session:

            # Write transactions allow the driver to handle retries and transient errors

            result = session.write_transaction(

                self._create_and_return_friendship, person1_name, person2_name)

            for row in result:

                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))









    @staticmethod

    def _create_and_return_friendship(tx, person1_name, person2_name):

        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/

        query = (

            "CREATE (p1:Person { name: $person1_name }) "

            "CREATE (p2:Person { name: $person2_name }) "

            "CREATE (p1)-[:KNOWS]->(p2) "

            "RETURN p1, p2"

        )

        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)

        try:

            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}

                    for row in result]

        # Capture any errors along with the query and data for traceability

        except ServiceUnavailable as exception:

            logging.error("{query} raised an error: \n {exception}".format(

                query=query, exception=exception))

            raise


    def find_person(self, person_name):

        with self.driver.session() as session:

            result = session.read_transaction(self._find_and_return_person, person_name)

            for row in result:

                print("Found person: {row}".format(row=row))


    @staticmethod

    def _find_and_return_person(tx, person_name):

        query = (

            "MATCH (p:Person) "

            "WHERE p.name = $person_name "

            "RETURN p.name AS name"

        )

        result = tx.run(query, person_name=person_name)

        return [row["name"] for row in result]