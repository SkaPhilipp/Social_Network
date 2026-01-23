import network_graph_database as graph 

from os import system, name
from time import sleep

import random 
import string

import webbrowser




# Display main menu with options for the user to choose from
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
    print(string_wrapping("5: Show degree of separation between two people"))
    print(string_wrapping("6: Clear graph"))
    print(string_wrapping("0: Exit"))
    print(blank_line)
    print(row_of_stars)
    print()

# Display heading (used before listing results)
def display_heading(heading):
    print(heading)
    print()
    print("-"*len(heading))
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


# Display result until user gets back to main menu
def get_back_to_menu():
    print()
    back_to_menu = ""

    while back_to_menu != "x":
        back_prompt = "Enter 'x' to return to menu: "
        back_to_menu = input(back_prompt)

        if back_to_menu != "x":
            print()
            print("Invalid input. Please enter 'x' to return to menu")
            sleep(2)


# Clear Graph Database (delete all nodes and edges)
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
        possible_options = range(7)

        # Display menu
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
            try:
                random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
                result_dicts = app.perform_page_rank(random_string) # method needs arbitrary graph name string for projection used in PageRank algorithm and cannot use same string twice as it would yield old result

            except:
                print("Problem displaying popularity of people (performing PageRank algorithm)")

            for result_dict in result_dicts:
                score = str(int(round(result_dict['score'],3)*1000)).rjust(5, " ")
                print(f"Popularity score: {score} -- Name: {result_dict['name']}")
            
            # Display result until user goes back to main menu
            get_back_to_menu()




        # Perform common neighbor algorithm to indicate likelihood of new relationship between nodes forming based on how many neighbors they have in common
        if option == 4:
            
            # Perform query and display result
            result_dictionaries = app.common_neighbors()

            # Display heading before listing results
            heading = "Score indicating chance for new relationship forming based on common neighbors"
            display_heading(heading)
            
            for result_dictionary in result_dictionaries:
                print("Score: " + str(result_dictionary['score']) + " for '" + result_dictionary['first'] + "' ---- '" + result_dictionary['second'] + "'")
            
            
            # Display result until user goes back to main menu
            get_back_to_menu()


        # Show degree of separation between two people using shortest path algorithm

        if option == 5:
            
            # Perform query to return names of all Person nodes
            result_dictionaries = app.return_all_names()

            # Display heading before listing results and store names
            name_set = set()

            heading = "List of people in social network"
            display_heading(heading)

            for count, result_dictionary in enumerate(result_dictionaries):
                print(("  " + str(count + 1))[-3:] + ": " + result_dictionary['name'])
                name_set.add(result_dictionary['name'])


            # Enter two names for shortest path / degree of separation query
            print()
            print("Please enter two names to display degree of separation between them")
            print()
            
            # Prompt user to enter first name
            prompt_1 = "Please enter first name (or 'x' to return to main menu): "
            first_name = input(prompt_1)

            while first_name != "x" and not(first_name in name_set):
                prompt_1 = "Invalid input, please enter first name (or 'x' to return to main menu): "
                first_name = input(prompt_1)
            
            # Prompt user to enter second name (different from first name)
            if first_name != "x":

                prompt_2 = "Please enter second name (or 'x' to return to main menu): "
                second_name = input(prompt_2)

                while (second_name != "x" and not(second_name in name_set)) or second_name == first_name :
                    
                    if second_name == first_name:
                        prompt_2 = "Please select different choice for second name than first name (or 'x' to return to main menu): "
                        second_name = input(prompt_2)
                    else:
                        prompt_2 = "Invalid input, please enter second name (or 'x' to return to main menu): "
                        second_name = input(prompt_2)
                

            # If user did not choose to return to main menu so far then clear screen and display result until user goes back to main menu
            if first_name != "x" and second_name != "x":
                
                name_set = app.return_shortest_path(first_name, second_name)

                # Clear screen before displaying names
                clear_screen()

                heading = "Shortest path between " + first_name + " and " + second_name + "illustrating degree of separation." 
                display_heading(heading)

                for count, name in enumerate(name_set):
                    counter = str(count+1).rjust(2, " ")
                    print(f"{counter}: {name}")
                    print()

                # Display result until user goes back to main menu
                get_back_to_menu() 


        # Clear graph
        if option == 6:
            clear_graph()





        # Wait and clear screen
        clear_screen()

    # Close connection to driver
    app.close()

