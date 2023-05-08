import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    pokedex_number = arg
    # Open a connection to the database
    conn = sqlite3.connect("pokemon.sqlite")

    # Construct the SQL query to retrieve the Pokemon data
    query = f"SELECT name, type1, type2, {'against_' + ' REAL, against_'.join(types) + ' REAL'} FROM imported_pokemon_data WHERE pokedex_number = {pokedex_number};"

    # Execute the query and retrieve the data
    cursor = conn.execute(query)
    data = cursor.fetchone()

    if data is None:
        print(f"No Pokemon found with Pokedex number {pokedex_number}")
        continue

    # Extract the data from the retrieved row
    name, type1, type2, *against_values = data

    # Construct the list of types the Pokemon is strong against
    strong_against = [t for t, v in zip(types, against_values) if isinstance(v, float) and v > 1]

    # Construct the list of types the Pokemon is weak against
    weak_against = [t for t, v in zip(types, against_values) if isinstance(v, float) and v < 1]

    # Print the results for this Pokemon
    print(f"Analyzing {pokedex_number}")
    print(f"{name} ({type1}{' ' + type2 if type2 else ''}) is strong against {strong_against} but weak against {weak_against}")

    # Add the Pokemon to the team list
    team.append(name)

    # Close the database connection
    conn.close()

# Ask the user if they want to save the team
answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Open a connection to the database
    conn = sqlite3.connect("pokemon.sqlite")
    c = conn.cursor()

    # Check if the teams table exists, and create it if it doesn't
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams'")
    table_exists = c.fetchone()
    if not table_exists:
        c.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT, pokemon1 TEXT, pokemon2 TEXT, pokemon3 TEXT, pokemon4 TEXT, pokemon5 TEXT, pokemon6 TEXT)")

    # Construct the SQL query to insert the team data into the database
    query = f"INSERT INTO teams (name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6) VALUES ('{teamName}', '{team[0]}', '{team[1]}', '{team[2]}', '{team[3]}', '{team[4]}', '{team[5]}');"

    # Execute the query to insert the team data into the database
    conn.execute(query)

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

    # Print a message indicating that the team was saved
    print(f"Saving {teamName} ...")
else:
    print("Bye for now!")
