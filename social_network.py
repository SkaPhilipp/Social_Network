import network_graph_database as graph

from os import system, name
from time import sleep

import webbrowser




# Display menu with options to choose from
def display_menu():
    menu_width = 75
    blank_line = "*" + " "*(menu_width-2) + "*"
    row_of_stars = "*"*menu_width
    indent = " "*10

    # Adjust string to menu width
    def string_wrapping(input_string):
        return ("*" + indent + input_string + " "*(menu_width-2))[:menu_width-1] + "*"

    # Print menu options
    print(row_of_stars)
    print(blank_line)
    print(string_wrapping("Enter option to choose:"))
    print(blank_line)
    print(string_wrapping("1: Display graph"))
    print(string_wrapping("2: Add Person (with random name)"))
    print(string_wrapping("3: Check popularity of person"))
    print(string_wrapping("4: Check likelihood of new relationship forming"))
    print(string_wrapping("5: Clear graph"))
    print(string_wrapping("0: Exit"))
    print(blank_line)
    print(row_of_stars)
    print()


# Clear screen
def clear_screen():
    time_before_clearing = 2
    sleep(time_before_clearing)

    # Clear screen depending on operating system
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def clear_graph():
    app.clear_graph_database()
    print("Graph Database is empty. Time to start from scratch :-)")




# Main function
if __name__ == "__main__":


    # Local bolt and http port, etc:
    local_bolt = '<neo4j-local-bolt>'
    local_http = '<neo4j-local-http>'
    local_pw = '<neo4j-pw>'
    local_user = '<neo4j-user>'

    # Create graph database instance
    app = graph.App(local_bolt, local_user, local_pw)


    # Start menu to select options 
    option = -1
    
    while option != 0:

        # Allowed options
        possible_options = range(6)

        # Display menu3
        display_menu()

        prompt = "Please enter option: "

        option = input(prompt)
        print()

        # Only allow valid options
        try:
            option = int(option)
            if not(option in possible_options):
                print("Please select a valid option")
        except:
            print("Please select a valid option")

       
        # Execute selected option

        # Display graph in web broswer
        if option == 1:
            try:
                webbrowser.open_new_tab('display_graph.html')
            except:
                print("Problem displaying graph in web browser")

        # Add new person node
        if option == 2:
            person_name = app.create_person()
            print("New person node for '" + person_name + "' has been created.")
            print()
            print("Relationships to existing nodes created at random.")
            # Give extra time to read printed output
            sleep(2)


        # Display popularity of people using PageRank scores
        if option == 3:
            print("Displaying popularity score not available yet")


        # Perform common neighbor algorithm to indicate likelihood of new relationship between nodes forming based on how many neighbors they have in common
        if option == 4:
            
            # Perform query and display result
            result_list = app.common_neighbors()

            heading = "Score indicating chance for new relationship forming based on common neighbors"
            print(heading)
            print()
            print("-"*len(heading))
            print()
            
            for result_dictionary in result_list:
                print("Score: " + str(result_dictionary['score']) + " for '" + result_dictionary['first'] + "' ---- '" + result_dictionary['second'] + "'")
            
            
            # Display result until user goes back to main menu4
            print()
            back_to_menu = ""

            while back_to_menu != "x":
                back_prompt = "Enter 'x' to return to menu: "
                back_to_menu = input(back_prompt)

                if back_to_menu != "x":
                    print()
                    print("Invalid input. Please enter 'x' to return to menu")
                    sleep(2)


        # Clear graph
        if option == 5:
            clear_graph()





        # Wait and clear screen
        clear_screen()


    app.close()

    
