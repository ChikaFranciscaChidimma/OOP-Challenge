from typing import List, Dict, Callable
import random
import time

class Needs:
    """Represents the basic needs of a pet."""
    def __init__(self, initial_hunger: int = 5, initial_energy: int = 7, initial_happiness: int = 5):
        self._hunger = max(0, min(10, initial_hunger))
        self._energy = max(0, min(10, initial_energy))
        self._happiness = max(0, min(10, initial_happiness))

    @property
    def hunger(self) -> int:
        return self._hunger

    @hunger.setter
    def hunger(self, value: int):
        self._hunger = max(0, min(10, value))

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value: int):
        self._energy = max(0, min(10, value))

    @property
    def happiness(self) -> int:
        return self._happiness

    @happiness.setter
    def happiness(self, value: int):
        self._happiness = max(0, min(10, value))

    def __str__(self) -> str:
        return f"Hunger: {self.hunger}/10, Energy: {self.energy}/10, Happiness: {self.happiness}/10"

class Personality:
    """Represents the personality traits of a pet, influencing its behavior."""
    def __init__(self, name: str, traits: Dict[str, float]):
        self.name = name
        self.traits = {trait: max(0.0, min(1.0, value)) for trait, value in traits.items()}

    def get_trait_influence(self, trait: str) -> float:
        return self.traits.get(trait, 0.5)  # Default to neutral if trait not found

class Pet:
    """Represents a digital pet with basic needs and actions."""
    def __init__(self, name: str, species: str = "Generic Pet", initial_hunger: int = 5, initial_energy: int = 7, initial_happiness: int = 5, personality_traits: Dict[str, float] = None):
        self.name = name
        self.species = species
        self.needs = Needs(initial_hunger, initial_energy, initial_happiness)
        self.tricks: List[str] = []
        self.personality = Personality(f"{name}'s Personality", personality_traits if personality_traits else {})
        self._is_alive = True
        self._last_interaction = time.time()
        self._mood_modifiers: List[Callable[['Pet'], None]] = []

    def eat(self) -> None:
        """Reduces hunger and increases happiness."""
        if not self._is_alive:
            print(f"{self.name} is no longer with us and cannot eat.")
            return
        print(f"{self.name} is eating...")
        hunger_reduction = 3 - 1 * self.personality.get_trait_influence("pickiness") # Pickier pets eat less
        self.needs.hunger = max(0, self.needs.hunger - int(hunger_reduction))
        happiness_increase = 1 + 0.5 * self.personality.get_trait_influence("joyfulness") # Joyful pets get happier
        self.needs.happiness = min(10, self.needs.happiness + int(happiness_increase))
        self._last_interaction = time.time()

    def sleep(self) -> None:
        """Increases energy."""
        if not self._is_alive:
            print(f"{self.name} is no longer with us and cannot sleep.")
            return
        print(f"{self.name} is sleeping...")
        energy_increase = 5 + 2 * self.personality.get_trait_influence("laziness") # Lazier pets sleep more deeply
        self.needs.energy = min(10, self.needs.energy + int(energy_increase))
        self._last_interaction = time.time()

    def play(self) -> None:
        """Decreases energy, increases happiness, and increases hunger."""
        if not self._is_alive:
            print(f"{self.name} is no longer with us and cannot play.")
            return
        print(f"{self.name} is playing!")
        energy_decrease = 2 + 1 * (1 - self.personality.get_trait_influence("playfulness")) # Less playful pets get tired faster
        self.needs.energy = max(0, self.needs.energy - int(energy_decrease))
        happiness_increase = 2 + 0.8 * self.personality.get_trait_influence("playfulness") # More playful pets get happier
        self.needs.happiness = min(10, self.needs.happiness + int(happiness_increase))
        hunger_increase = 1 + 0.3 * (1 - self.personality.get_trait_influence("fussiness")) # Less fussy pets get hungrier easier
        self.needs.hunger = min(10, self.needs.hunger + int(hunger_increase))
        self._last_interaction = time.time()

    def get_status(self) -> None:
        """Prints the current state of the pet."""
        if not self._is_alive:
            print(f"{self.name} has passed away.")
            return
        print(f"--- {self.name} ({self.species}) ---")
        print(self.needs)
        if self.tricks:
            print(f"Tricks learned: {', '.join(self.tricks)}")
        else:
            print(f"{self.name} hasn't learned any tricks yet.")

    def train(self, trick: str) -> None:
        """Teaches the pet a new trick."""
        if not self._is_alive:
            print(f"{self.name} is no longer with us and cannot learn any new tricks.")
            return
        if trick.lower() not in [t.lower() for t in self.tricks]:
            success_chance = 0.6 + 0.3 * self.personality.get_trait_influence("trainability") # More trainable pets learn faster
            if random.random() < success_chance:
                self.tricks.append(trick)
                print(f"{self.name} learned the trick '{trick}'!")
                self.needs.happiness = min(10, self.needs.happiness + 2) # Happy after learning
            else:
                print(f"{self.name} struggled to learn '{trick}'. Try again later!")
            self._last_interaction = time.time()
        else:
            print(f"{self.name} already knows the trick '{trick}'.")

    def show_tricks(self) -> None:
        """Prints all learned tricks."""
        if not self._is_alive:
            print(f"{self.name} is no longer with us and cannot show any tricks.")
            return
        if self.tricks:
            print(f"{self.name} knows the following tricks: {', '.join(self.tricks)}")
        else:
            print(f"{self.name} hasn't learned any tricks yet.")

    def add_mood_modifier(self, modifier: Callable[['Pet'], None]) -> None:
        """Adds a function to modify the pet's mood over time."""
        self._mood_modifiers.append(modifier)

    def update_mood(self) -> None:
        """Applies all mood modifiers to the pet."""
        for modifier in self._mood_modifiers:
            modifier(self)

    def time_passes(self, seconds: int) -> None:
        """Simulates the passage of time, affecting the pet's needs."""
        if not self._is_alive:
            return
        time_elapsed = time.time() - self._last_interaction
        if time_elapsed >= seconds:
            hunger_increase = int(time_elapsed / (3600 / (3 + 2 * self.personality.get_trait_influence("metabolism")))) # Metabolism affects hunger rate
            energy_decrease = int(time_elapsed / (7200 / (5 + 3 * self.personality.get_trait_influence("activity")))) # Activity affects energy drain
            happiness_decrease = int(time_elapsed / (10800 / (2 + 1 * self.personality.get_trait_influence("sociability")))) # Sociability affects happiness drop when alone

            self.needs.hunger = min(10, self.needs.hunger + hunger_increase)
            self.needs.energy = max(0, self.needs.energy - energy_decrease)
            self.needs.happiness = max(0, self.needs.happiness - happiness_decrease)
            self._last_interaction = time.time()

            if self.needs.hunger >= 10 or self.needs.energy <= 0 or self.needs.happiness <= 0:
                self._is_alive = False
                print(f"{self.name} has passed away due to neglect.")

    def is_alive(self) -> bool:
        """Checks if the pet is currently alive."""
        return self._is_alive

class AdvancedPet(Pet):
    """An advanced pet with more complex needs and behaviors."""
    def __init__(self, name: str, species: str = "Advanced Pet", initial_hunger: int = 5, initial_energy: int = 7, initial_happiness: int = 5, initial_health: int = 100, personality_traits: Dict[str, float] = None):
        super().__init__(name, species, initial_hunger, initial_energy, initial_happiness, personality_traits)
        self.health = max(0, min(100, initial_health))
        self._diseases: List[str] = []

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = max(0, min(100, value))
        if self._health <= 0 and self._is_alive:
            self._is_alive = False
            print(f"{self.name} has succumbed to illness.")

    def get_status(self) -> None:
        """Prints the current state of the advanced pet, including health and diseases."""
        super().get_status()
        if self._is_alive:
            print(f"Health: {self.health}/100")
            if self._diseases:
                print(f"Diseases: {', '.join(self._diseases)}")

    def eat(self) -> None:
        super().eat()
        # Certain foods might slightly improve health
        if random.random() < 0.3:
            health_increase = 2 + 1 * self.personality.get_trait_influence("constitution")
            self.health = min(100, self.health + int(health_increase))

    def play(self) -> None:
        super().play()
        # Overexertion might slightly decrease health
        if self.needs.energy < 3 and random.random() < 0.4:
            health_decrease = 3 - 1 * self.personality.get_trait_influence("resilience")
            self.health = max(0, self.health - int(health_decrease))

    def train(self, trick: str) -> None:
        super().train(trick)
        # Successful training might slightly boost health
        if trick.lower() in [t.lower() for t in self.tricks] and random.random() < 0.2:
            self.health = min(100, self.health + 1)

    def contract_disease(self, disease: str) -> None:
        """Makes the pet contract a disease."""
        if disease.lower() not in [d.lower() for d in self._diseases]:
            self._diseases.append(disease)
            print(f"{self.name} has contracted '{disease}'.")
            # Diseases can affect needs
            self.needs.hunger = min(10, self.needs.hunger + random.randint(1, 3))
            self.needs.energy = max(0, self.needs.energy - random.randint(1, 3))
            self.needs.happiness = max(0, self.needs.happiness - random.randint(2, 4))
            self.health = max(0, self.health - random.randint(5, 15))

    def treat_disease(self, disease: str) -> None:
        """Attempts to treat a specific disease."""
        if disease.lower() in [d.lower() for d in self._diseases]:
            treatment_success_chance = 0.7 * self.personality.get_trait_influence("cooperativeness") # More cooperative pets are easier to treat
            if random.random() < treatment_success_chance:
                self._diseases.remove(disease)
                print(f"{self.name} has been cured of '{disease}'.")
                self.health = min(100, self.health + random.randint(5, 10))
            else:
                print(f"Treatment for '{disease}' was unsuccessful.")
        else:
            print(f"{self.name} doesn't have '{disease}'.")

    def time_passes(self, seconds: int) -> None:
        super().time_passes(seconds)
        if self._is_alive:
            # Diseases might worsen over time
            for disease in list(self._diseases): # Iterate over a copy to allow modification
                if random.random() < 0.2:
                    print(f"{disease} is worsening for {self.name}.")
                    self.health = max(0, self.health - random.randint(3, 7))
                    self.needs.hunger = min(10, self.needs.hunger + random.randint(0, 2))
                    self.needs.energy = max(0, self.needs.energy - random.randint(0, 2))
                    self.needs.happiness = max(0, self.needs.happiness - random.randint(1, 3))