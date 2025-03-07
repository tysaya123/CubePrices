#!/usr/bin/env python3

import csv
import json

# Function to read the JSON files
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to read the text file (cube-list.txt)
def read_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()  # Read lines as a list
    
def read_owned_list_csv(file_path):
    # Initialize an empty list to store the CSV data
    cards = set()
    # Open the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Read the header (optional, can be skipped)
        _ = next(csvreader)
        
        # Append each row to the data list
        for row in csvreader:
            cards.add(row[0])
            
    return cards  # Return both header and data rows
    
def normalize_card_name(card_name):
    return card_name.replace(" // ", "/")

def is_allowed_card(card_name):
    return card_name != "Cogwork Librarian" and card_name != ""

def get_all_card_ids(card_definitions):
    card_ids = {}
    for id,card in card_definitions.items():
        card_ids.setdefault(card["name"],[]).append(id)
    return card_ids

def clean_list(cube_list):
    maybeboard_idx = cube_list.index("# maybeboard")
    cube_list = cube_list[1:maybeboard_idx] # Filter mainboard tag and anything after maybeboard
    cube_list = filter(is_allowed_card, cube_list)
    cube_list = [normalize_card_name(card_name) for card_name in cube_list]
    return cube_list
    
def get_cheapest_version(card_definitions, price_history):
    card_ids = get_all_card_ids(card_definitions)
    
    cheapest_cards = {}
    for name, ids in card_ids.items():
        prices = [price_history[id] for id in ids]
        cheapest_cards[name] = min(prices)
    
    return cheapest_cards

def main():
    # Define file paths
    card_definitions_file = "card-definitions.json"
    price_history_file = "price-history.json"
    cube_list_file = "south-side-stone-rain-list.txt"
    owned_cards_file = "owned-cards.txt"

    # Read data from files
    card_definitions = read_json(card_definitions_file)
    price_history = read_json(price_history_file)
    cube_list = read_txt(cube_list_file)
    owned_list = read_owned_list_csv(owned_cards_file)

    cube_list = clean_list(cube_list)

    cheapest_version = get_cheapest_version(card_definitions, price_history)

    cheapest_cube = {card_name:cheapest_version[card_name] for card_name in cube_list}
    
    cheapest_cube_unowned = {card_name:price for card_name, price in cheapest_cube.items() if card_name not in owned_list}
    owned_cards = {card_name:price for card_name, price in cheapest_cube.items() if card_name in owned_list}

    print("CHEAPEST CUBE")
    print(cheapest_cube)
    
    print("CHEAPEST CUBE UNOWNED")
    print(cheapest_cube_unowned)

    print("OWNED CARDS")
    print(sorted(owned_cards.items(), key=lambda item: item[1]))

    print("TOTAL COST")
    print(sum(cheapest_cube.values()))

    print("TOTAL COST UNOWNED")
    print(sum(cheapest_cube_unowned.values()))

if __name__ == "__main__":
    main()