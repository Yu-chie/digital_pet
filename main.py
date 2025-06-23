from digital_pet import DigiPet
from utils import loading_screen, clear_screen

# Main Function
def main():
    # - Load existing pet or create new pet
    pet = DigiPet.load()
    if pet:
        print(f"\nWelcome back! You are continuing with {pet.name} the {pet.animal_type}.")
    else:
        loading_screen()
        pet_name = input("What do you want to name your pet?: ")
        pet = DigiPet(pet_name)

    input(f"\nHello! I am {pet.name} the {pet.animal_type}, and I am new here!\nPress Enter to start!")

    # Status and interaction menu
    try:
        while True:
            clear_screen()
            pet.show_status()
            print("""
*** INTERACT WITH YOUR PET ***

1. Feed your pet 🍽️
2. Talk with your pet 🗣️
3. Teach your pet a new word 📖
4. Play with your pet 🎾
5. Let your pet sleep 😴
0. Quit 🚪
""")
            choice = input("Enter your choice: ")

            if choice == "0":
                confirm = input("Are you sure you want to quit? (y/n): ").lower()
                if confirm == "y":
                    pet.save()
                    print("Goodbye! Take care of your DigiPet! 🐾")
                    break
            elif choice == "1":
                pet.feed()
            elif choice == "2":
                pet.talk()
            elif choice == "3":
                word = input("What word do you want to teach your pet?: ")
                pet.teach(word)
            elif choice == "4":
                pet.play()
            elif choice == "5":
                pet.sleep()
            else:
                print("❌ Invalid choice. Please select from the menu.")

            input("\nPress Enter to continue...")

    except Exception as e:
        print(str(e))
        pet.save()
        print("Game over. Thanks for playing!")

# Run main() program
if __name__ == "__main__":
    main()