#DigiPet

# Step 1: Import necessary modules
import time
import json     # - json (to save/load pet state)
from random import randrange    # - randrange (for random stat changes)
import os       # - os (to check file existence)
from utils import loading_screen, clear_screen

# Step 2: Define DigiPet class
class DigiPet:
    max_age = 10                # Maximum age before pet passes away
    save_file = "save.json"     # Filename for saving/loading pet data
    max_energy = 100
    max_hunger = 100
    max_life = 100
    hunger_warning = 80
    energy_warning = 20
    
    
    # Initialize pet with default or loaded values
    def __init__(self, name, age=0, energy=100, hunger=0, life=100, vocab=None, last_update=None):
        self.name = name
        self.animal_type = "Cat"
        self.age = age
        self.energy = energy
        self.hunger = hunger
        self.life = life
        self.vocab = vocab if vocab is not None else ["Grrr...", "Meow", "Purr~"]
        self.last_update = last_update or time.time()
        
        
    # Private method to simulate time passing after each interaction
    def __clock_tick(self):
        self.age += 0.1     # - Increase age
        self.energy -= 5    # - Decrease energy
        self.hunger += 5    # - Increase hunger
        
        self.__clamp_stats()       # - Clamp stats within limits
        
        # - Check for life status (age limit, hunger, energy)
        
        # Notify when pet is growing up
        if int(self.age) == 5:
            print(f"\n✨ {self.name} is growing up!")
        
        # Check if pet reached max age and should pass away peacefully
        if self.age >= DigiPet.max_age:
            print(f"\n💀 {self.name} has grown very old and passed away peacefully...")
            self.life = 0
        
        # If hunger maxes out, decrease life and warn user
        if self.hunger >= 100:
            self.hunger = 100
            self.life -= 10
            print(f"\n⚠️ {self.name} is starving!")
        
        # If energy depletes, decrease life and warn user
        if self.energy <= 0:
            self.energy = 0
            self.life -= 5
            print(f"\n⚠️ {self.name} is exhausted!")
        
        # If life drops to zero or below, pet dies, raise exception to end game
        if self.life <= 0:
            self.life = 0
            print(f"\n💀 {self.name} has passed away... Take better care next time.")
            raise Exception("Pet has died.")
    
    # Method to update pet stats automatically based on real time elapsed  
    def update_stats_based_on_time(self):
        current_time = time.time()
        elapsed = current_time - self.last_update
        intervals = int(elapsed // (5 * 60))  # Calculate how many 5-minute intervals passed

        if intervals > 0:
            for _ in range(intervals):
                self.__clock_tick()
            self.last_update += intervals * 5 * 60
            
            # Notifications similar to clock_tick
            if int(self.age) == 5:
                print(f"\n✨ {self.name} is growing up!")

            if self.hunger >= DigiPet.hunger_warning:
                print(f"\n⚠️ {self.name} is getting very hungry!")
                
            if self.energy <= DigiPet.energy_warning:
                print(f"\n😴 {self.name} is getting tired...")

            if self.age >= DigiPet.max_age:
                print(f"\n💀 {self.name} has grown very old and passed away peacefully...")
                self.life = 0
            if self.hunger >= 100 or self.energy <= 0:
                pass
            
        
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
        """Clamp energy, hunger, and life stats within valid ranges."""
        self.energy = max(0, min(self.energy, DigiPet.max_energy))
        self.hunger = max(0, min(self.hunger, DigiPet.max_hunger))
        self.life = max(0, min(self.life, DigiPet.max_life))
        
        
    # Method to return current pet mood based on stats
    def mood(self):
        """Return the pet's mood based on current stats."""
        if self.life <= 0:
            return "gone"
        if self.hunger > DigiPet.hunger_warning:
            return "hungry"
        if self.energy < DigiPet.energy_warning:
            return "tired"
        if self.energy > DigiPet.max_energy // 2 and self.hunger < DigiPet.max_hunger // 2:
            return "happy"
        return "bored"

    # Method to print a message based on pet's mood
    def mood_message(self):
        """Print a message based on the pet's current mood."""
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

    # --- Interactive Methods ---
    # Pet talks, randomly choosing a known word from vocab
    def talk(self):
        clear_screen()
        print(f"\n🗣️ I am {self.name}, a {self.animal_type}. I feel {self.mood()} right now.")
        print(f"{self.name} says: {self.vocab[randrange(len(self.vocab))]}")
        self.__clock_tick()
        self.mood_message()
        self.save()
        
        
    def feed(self):
        """Feed the pet to reduce hunger."""
        clear_screen()
        if self.hunger == 0:
            print(f"\n{self.name} isn't hungry.")
        else:
            amount = randrange(10, 30)
            self.hunger -= amount
            print(f"\n🍽️ {self.name} munches happily! Hunger -{amount}")
        self.__clock_tick()
        self.__clamp_stats()
        self.mood_message()
        self.save()

    def sleep(self):
        """Let the pet sleep to regain energy."""
        clear_screen()
        gain = randrange(20, 40)
        self.energy += gain
        print(f"\n😴 {self.name} took a nap and feels better! Energy +{gain}")
        self.__clock_tick()
        self.__clamp_stats()
        self.mood_message()
        self.save()

    def play(self):
        """Play with the pet, costing energy but increasing hunger."""
        clear_screen()
        if self.energy < 15:
            print(f"\n{self.name} is too tired to play!")
            return
        else:
            fun = randrange(10, 30)
            self.energy -= fun
            self.hunger += 10
            print(f"\n🎾 {self.name} had fun playing! Energy -{fun}, Hunger +10")
        self.__clock_tick()
        self.__clamp_stats()
        self.mood_message()
        self.save()

    def teach(self, word):
        """Teach the pet a new word, costing some energy."""
        clear_screen()
        if word in self.vocab:
            print(f"\n{self.name} already knows the word '{word}'!")
        else:
            self.vocab.append(word)
            self.energy -= 5
            print(f"\n🧠 You taught {self.name} to say '{word}'!")
            self.__clock_tick()
            self.__clamp_stats()
            self.mood_message()
            self.save()

    def show_status(self):
        """Display all pet stats and mood."""
        print(f"""
📋 STATUS
Name: {self.name}
Stage: {self.stage()}
Type: {self.animal_type}
Age: {self.age}
Energy: {self.energy}/{DigiPet.max_energy}
Hunger: {self.hunger}/{DigiPet.max_hunger}
Life: {self.life}/{DigiPet.max_life}
Mood: {self.mood()}
""")
        
        
    # Method to save/write pet data to JSON file
    def save(self):
        self.last_update = time.time()  # Update last interaction time
        data = {
            "name": self.name,
            "age": self.age,
            "energy": self.energy,
            "hunger": self.hunger,
            "life": self.life,
            "vocab": self.vocab,
            "last_update": self.last_update
        }
        try:
            with open(DigiPet.save_file, "w") as file:
                json.dump(data, file)
            print("\n💾 Game saved!")
        except Exception as e:
            print(f"\n❌ Error saving game: {e}")  


    # Class method to load pet data from JSON file or return None
    @classmethod
    def load(cls):
        if not os.path.exists(cls.save_file):
            return None
        try:
            with open(cls.save_file, "r") as file:
                data = json.load(file)
            return cls(
                name=data.get("name", "NoName"),
                age=data.get("age", 0),
                energy=data.get("energy", 100),
                hunger=data.get("hunger", 0),
                life=data.get("life", 100),
                vocab=data.get("vocab", ["Grrr...", "Meow", "Purr~"]),
                last_update=data.get("last_update", time.time())
            )
        except Exception as e:
            print(f"\n❌ Error loading game: {e}")
            return None