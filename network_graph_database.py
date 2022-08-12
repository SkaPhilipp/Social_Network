
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

import names





# Define App class
class App:

    # Initialise graph database using neo4j api credentials
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print("Connection to Driver failed: ", e)


    # Close driver connection
    def close(self):
        self.driver.close()

    # Clear graph database: delete all nodes and all relationships
    def clear_graph_database(self):
        with self.driver.session() as session:
            query = "MATCH (n) DETACH DELETE n"
            session.run(query)



    # Create new Person node with random name
    def create_person(self):
        with self.driver.session() as session:
            
            # Get random name
            person_name = names.get_full_name()
            
            # Create person node
            session.write_transaction(self._create_person, person_name)
            
            # Create relationships from new person to existing
            session.write_transaction(self._create_relationships, person_name)

            # Return name string to display
            return person_name


    # Static method to create person node and return result
    @staticmethod
    def _create_person(tx, person_name):
        query = "CREATE (p:Person{name: '"+ person_name +"'}) RETURN p AS person"
        result = tx.run(query, person_name=person_name)

    # Create relationships from new person to existing at random (with 50% likelihood), set property 'weight' to 1 for visualisation
    @staticmethod
    def _create_relationships(tx, person_name):
        query = "MATCH (p:Person{name: '" + person_name + "'}),(o:Person) WHERE NOT(id(p)=id(o)) WITH p,o WHERE rand()<0.5 CREATE (p)-[:KNOWS {weight: 1}]->(o), (p)<-[:KNOWS {weight: 1}]-(o)"
        result = tx.run(query, person_name=person_name)




    # Show likelihood of new connection between nodes forming based on common neighbor algorithm
    def common_neighbors(self):
        with self.driver.session() as session:
            
            # Query to perform common neighbors algorithm
            query = "MATCH (p1:Person), (p2:Person) WHERE id(p1)<id(p2) AND NOT (p1)-[:KNOWS]-(p2) WITH p1.name AS first, p2.name AS second, gds.alpha.linkprediction.commonNeighbors(p1, p2, {relationshipQuery: 'KNOWS'}) AS score RETURN first, second, score"

            # Execute query
            result = session.run(query)

            # Return result
            return [dict(res) for res in result]

    # Perform PageRank algorithm
    def perform_page_rank(self, graph_name):

        # Define projection (which nodes and which relationships / property value) for PageRank algorithm 
        projection = "CALL gds.graph.project('"+ graph_name +"','Person','KNOWS',{relationshipProperties: 'weight'})"
        with self.driver.session() as session:
            session.run(projection)

        # Perform cypher query to execute PageRank algorithm
        page_rank_query = "CALL gds.pageRank.stream('"+ graph_name +"') YIELD nodeId, score RETURN gds.util.asNode(nodeId).name AS name, score ORDER BY score DESC, name ASC"
        with self.driver.session() as session:
            result = session.run(page_rank_query)
            return [dict(i) for i in result]


    # Return names of all people in network
    def return_all_names(self):
        return_all_names_query = "MATCH (p:Person) RETURN p.name AS name"
        
        # Perform query to return all names
        with self.driver.session() as session:
            result = session.run(return_all_names_query)
            return [dict(i) for i in result]


    # Return nodes along shortest path between two nodes
    def return_shortest_path(self, first_person, second_person):
        
        shortest_path_query = "MATCH (p1:Person{name: '" + first_person + "'}), (p2:Person{name: '" + second_person + "'}), path = allShortestPaths((p1)-[*]-(p2)) WITH nodes(path) AS nodes_list UNWIND nodes_list AS nodes RETURN nodes.name AS name"
        
        # Perform query to return names along shortest path between first_person and second_person
        with self.driver.session() as session:
            result = session.run(shortest_path_query)

            # Store names in set and return set
            name_set = set()

            for res in result:
                name_set.add(dict(res)['name'])
            return name_set
