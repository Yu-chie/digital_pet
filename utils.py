import time
import os

# Function for loading screen
def loading_screen():
    print("👶 A new baby pet is being born...")
    for i in range(3):
        time.sleep(1)
        print("Loading" + "." * (i + 1))
    print("✨ Your DigiPet is here!\n")
    
# Function for clearing terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')