# DigiPet - Virtual Pet Simulation

# Import necessary modules
import time
import json     # For saving/loading pet state
from random import randrange    # For random stat changes
import os       # For checking file existence

# Define DigiPet class
class DigiPet:
    max_age = 10            # Maximum age before pet passes away
    save_file = "save.json"     # Filename for saving/loading pet data
    max_energy = 100        # Maximum energy value
    max_hunger = 100        # Maximum hunger value
    max_life = 100          # Maximum life value
    hunger_warning = 80     # Hunger level to trigger warning
    energy_warning = 20     # Energy level to trigger warning
    
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
        """Simulate time passing after each interaction."""
        messages = []
        self.age += 0.1     # - Increase age
        self.energy -= 5    # - Decrease energy
        self.hunger += 5    # - Increase hunger
        
        self.__clamp_stats()       # Clamp stats within limits
        
        # - Check for life status (age limit, hunger, energy)
        # Notify when pet is growing up
        if int(self.age) == 5:
            messages.append(f"✨ {self.name} is growing up!")
        
        # Check if pet reached max age and should pass away peacefully
        if self.age >= DigiPet.max_age:
            self.life = 0
            messages.append(f"💀 {self.name} has grown very old and passed away peacefully...")

        # If hunger maxes out, decrease life and warn user
        if self.hunger >= 100:
            self.hunger = 100
            self.life -= 10
            messages.append(f"⚠️ {self.name} is starving!")

        # If energy depletes, decrease life and warn user
        if self.energy <= 0:
            self.energy = 0
            self.life -= 5
            messages.append(f"⚠️ {self.name} is exhausted!")

        # If life drops to zero or below, pet dies, raise exception to end game
        if self.life <= 0:
            self.life = 0
            messages.append(f"💀 {self.name} has passed away... Take better care next time.")
            # For GUI, you can check if pet.life == 0 and handle accordingly
        return "\n".join(messages)

    # Method to update pet stats automatically based on real time elapsed  
    def update_stats_based_on_time(self):
        """Update pet stats based on real time elapsed."""
        messages = []
        current_time = time.time()
        elapsed = current_time - self.last_update
        intervals = int(elapsed // (5 * 60))  # Calculate how many 5-minute intervals passed

        if intervals > 0:
            for _ in range(intervals):
                msg = self.__clock_tick()
                if msg:
                    messages.append(msg)
            self.last_update += intervals * 5 * 60
            self.__clamp_stats()
            
            # Notifications similar to clock_tick
            if int(self.age) == 5:
                messages.append(f"✨ {self.name} is growing up!")
            if self.hunger >= DigiPet.hunger_warning:
                messages.append(f"⚠️ {self.name} is getting very hungry!")
            if self.energy <= DigiPet.energy_warning:
                messages.append(f"😴 {self.name} is getting tired...")
            if self.age >= DigiPet.max_age:
                self.life = 0
                messages.append(f"💀 {self.name} has grown very old and passed away peacefully...")
        return "\n".join(messages)

    # Method to return pet life stage based on age
    def stage(self):
        """Return pet life stage based on age."""
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
        """Return a message based on the pet's current mood."""
        current_mood = self.mood()
        if current_mood == "bored":
            return f"😐 {self.name} looks bored. Maybe play with them?"
        elif current_mood == "tired":
            return f"😴 {self.name} looks very tired. Let them sleep!"
        elif current_mood == "hungry":
            return f"⚠️ {self.name} is very hungry!"
        elif current_mood == "gone":
            return f"💀 {self.name} is no longer with us..."
        else:
            return f"😊 {self.name} is feeling {current_mood}!"

    # --- Interactive Methods ---
    # Pet talks, randomly choosing a known word from vocab
    def talk(self):
        """Pet talks, randomly choosing a known word from vocab."""
        if self.life <= 0:
            return self.mood_message()
        msg = f"🗣️ I am {self.name}, a {self.animal_type}. I feel {self.mood()} right now.\n"
        msg += f"{self.name} says: {self.vocab[randrange(len(self.vocab))]}"
        tick_msg = self.__clock_tick()
        mood_msg = self.mood_message()
        self.save()
        return "\n".join([msg, tick_msg, mood_msg]).strip()

    def feed(self):
        """Feed the pet to reduce hunger."""
        if self.life <= 0:
            return self.mood_message()
        if self.hunger == 0:
            msg = f"{self.name} isn't hungry."
        else:
            amount = randrange(10, 30)
            self.hunger -= amount
            msg = f"🍽️ {self.name} munches happily! Hunger -{amount}"
        tick_msg = self.__clock_tick()
        self.__clamp_stats()
        mood_msg = self.mood_message()
        self.save()
        return "\n".join([msg, tick_msg, mood_msg]).strip()

    def sleep(self):
        """Let the pet sleep to regain energy."""
        if self.life <= 0:
            return self.mood_message()
        gain = randrange(20, 40)
        self.energy += gain
        msg = f"😴 {self.name} took a nap and feels better! Energy +{gain}"
        tick_msg = self.__clock_tick()
        self.__clamp_stats()
        mood_msg = self.mood_message()
        self.save()
        return "\n".join([msg, tick_msg, mood_msg]).strip()

    def play(self):
        """Play with the pet, costing energy but increasing hunger."""
        if self.life <= 0:
            return self.mood_message()
        if self.energy < 15:
            return f"{self.name} is too tired to play!"
        fun = randrange(10, 30)
        self.energy -= fun
        self.hunger += 10
        msg = f"🎾 {self.name} had fun playing! Energy -{fun}, Hunger +10"
        tick_msg = self.__clock_tick()
        self.__clamp_stats()
        mood_msg = self.mood_message()
        self.save()
        return "\n".join([msg, tick_msg, mood_msg]).strip()

    def teach(self, word):
        """Teach the pet a new word, costing some energy."""
        if self.life <= 0:
            return self.mood_message()
        if word in self.vocab:
            return f"{self.name} already knows the word '{word}'!"
        elif self.energy < 5:
            return f"{self.name} is too tired to learn a new word!"
        self.vocab.append(word)
        self.energy -= 5
        msg = f"🧠 You taught {self.name} to say '{word}'!"
        tick_msg = self.__clock_tick()
        self.__clamp_stats()
        mood_msg = self.mood_message()
        self.save()
        return "\n".join([msg, tick_msg, mood_msg]).strip()

    def show_status(self):
        """Return all pet stats and mood as a string."""
        return f"""
📋 STATUS
Name: {self.name}
Stage: {self.stage()}
Type: {self.animal_type}
Age: {self.age:.1f}
Energy: {self.energy}/{DigiPet.max_energy}
Hunger: {self.hunger}/{DigiPet.max_hunger}
Life: {self.life}/{DigiPet.max_life}
Mood: {self.mood()}
"""

    def save(self):
        """Save pet data to JSON file."""
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
        except Exception as e:
            # For GUI, you might want to log this error
            pass

    # Class method to load pet data from JSON file or return None
    @classmethod
    def load(cls):
        """Load pet data from JSON file or return None."""
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
            # For GUI, you might want to log this error
            return None