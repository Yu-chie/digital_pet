import time

# Function for loading screen
def loading_screen(self):
    print("👶 A new baby pet is being born...")
    for i in range(3):
        time.sleep(1)
        print("Loading" + "." * (i + 1))
    print("✨ Your DigiPet is here!\n")