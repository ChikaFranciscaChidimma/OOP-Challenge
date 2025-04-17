from pet import Pet
import time  # Import the time module

if __name__ == "__main__":
    my_basic_pet = Pet(name="Buddy", species="Dog")

    print("--- Initial Status ---")
    my_basic_pet.get_status()

    print("\n--- Interacting with Buddy ---")
    my_basic_pet.eat()
    my_basic_pet.play()
    my_basic_pet.train("Sit")
    my_basic_pet.show_tricks()
    my_basic_pet.sleep()

    print("\n--- Status After Interaction ---")
    my_basic_pet.get_status()

    print("\n--- Time Passing (Simulated) ---")
    for _ in range(3):
        my_basic_pet.time_passes(3600) # Simulate 1 hour passing
        my_basic_pet.get_status()
        if not my_basic_pet.is_alive():
            break
        time.sleep(0.5) # Small delay for output readability

    if my_basic_pet.is_alive():
        print("\nBuddy is still doing well!")