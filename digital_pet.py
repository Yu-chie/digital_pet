# Step 1: Import necessary modules
import time     # - time (for loading delays)
import json     # - json (to save/load pet state)
from random import randrange        # - randrange (for random stat changes)
import os       # - os (to check file existence)

# Step 2: Define DigiPet class
# - Set Class Variables: max_age, save_file
# - Attributes: name, animal_type, age, energy, hunger, life, vocabulary

# Step 3: Implement __init__ method to initialize pet with default or loaded values

# Step 4: Implement __clock_tick() private method to simulate time passing:
# - Increase age
# - Decrease energy
# - Increase hunger
# - Clamp stats within limits
# - Check for life status (age limit, hunger, energy)
# - Raise Exception if pet dies

# Step 5: Implement stage() method to return pet life stage based on age

# Step 6: Implement __clamp_stats() private method to keep stats in valid range

# Step 7: Implement mood() method to return current pet mood based on stats

# Step 8: Implement mood_message() method to print a message based on pet's mood

# Step 9: Implement interactive methods:
# - talk(): pet says a random word, triggers clock tick, shows mood, saves game
# - feed(): reduce hunger by random amount, triggers clock tick, shows mood, saves
# - sleep(): increase energy by random amount, triggers clock tick, shows mood, saves
# - play(): decrease energy, increase hunger, triggers clock tick, shows mood, saves
# - teach(word): add new word to vocab if not known, reduce energy, triggers clock tick, shows mood, saves

# Step 10: Implement show_status() to print all pet stats and mood

# Step 11: Implement save() method to write pet data to JSON file

# Step 12: Implement load() class method to load pet data from JSON file or return None

# Step 13: Implement loading_screen() function to simulate loading animation on startup

# Step 14: Implement main() function to:
# - Load existing pet or create new pet
# - Greet user
# - Loop showing status and interaction menu
# - Accept user input and call corresponding pet methods
# - Handle quitting and saving
# - Catch pet death exception and exit gracefully

# Step 15: Add if __name__ == "__main__" to run main()