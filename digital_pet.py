# Step 1: Import necessary modules
import time     # - time (for loading delays)
import json     # - json (to save/load pet state)
from random import randrange    # - randrange (for random stat changes)
import os       # - os (to check file existence)

# Step 2: Define DigiPet class
class DigiPet:
    max_age = 10
    save_file = "save.json"
    
    # Initialize pet with default or loaded values
    def __init__(self, name, age=0, energy=100, hunger=0, life=100, vocab=None):
        self.name = name
        self.age = age
        self.energy = energy
        self.hunger = hunger
        self.life = life
        self.vocab = vocab if vocab is not None else ["Grrr...", "Meow", "Purr~"]
        
    # Private method to simulate time passing
    def __clock_tick(self):
        self.age += 1       # - Increase age
        self.energy -= 5    # - Decrease energy
        self.hunger += 5    # - Increase hunger
        
        self.__clamp_stats()       # - Clamp stats within limits
        
        # - Check for life status (age limit, hunger, energy)
        if self.age == 5:
            print(f"\n✨ {self.name} is growing up!")
        
        if self.age >= DigiPet.max_age:
            print(f"\n💀 {self.name} has grown very old and passed away peacefully...")
            self.life = 0
        
        if self.hunger >= 100:
            self.hunger = 100
            self.life -= 10
            print(f"\n⚠️ {self.name} is starving!")
            
        if self.energy <= 0:
            self.energy = 0
            self.life -= 5
            print(f"\n⚠️ {self.name} is exhausted!")
            
        if self.life <= 0:
            self.life = 0
            print(f"\n💀 {self.name} has passed away... Take better care next time.")
            raise Exception("Pet has died.")
        
    # Method to return pet life stage based on age
    def stage(self):
        if self.age < 3:
            return "Baby"
        elif self.age < 7:
            return "Adolescent"
        else:
            return "Adult"
        
    # Private method to keep stats in valid range
    def __clamp_stats(self):
        self.energy = max(0, min(self.energy, 100))
        self.hunger = max(0, min(self.hunger, 100))
        self.life = max(0, min(self.life, 100))
        
    # Method to return current pet mood based on stats
    def mood(self):
        if self.life <= 0:
            return "gone"
        if self.hunger > 80:
            return "hungry"
        if self.energy < 20:
            return "tired"
        if self.energy > 50 and self.hunger < 50:
            return "bored"
        return "happy"
    
    # Method to print a message based on pet's mood
    def mood_message(self):
        current_mood = self.mood()
        if current_mood == "bored":
            print(f"\n😐 {self.name} looks bored. Maybe play with them?")
        elif current_mood == "tired":
            print(f"\n😴 {self.name} looks very tired. Let them sleep!")
        elif current_mood == "hungry":
            print(f"\n⚠️ {self.name} is very hungry!")
        elif current_mood == "gone":
            print(f"\n💀 {self.name} is no longer with us...")
        else:
            print(f"\n😊 {self.name} is feeling {current_mood}!")


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