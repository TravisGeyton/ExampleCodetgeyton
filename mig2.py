import random

class MagicalItemGenerator:
    def __init__(self):
        # Base item types
        self.base_items = [
            "sword", "blade", "dagger", "axe", "hammer", "staff", "wand", "orb", "crystal",
            "ring", "amulet", "pendant", "crown", "helm", "armor", "shield", "gauntlets",
            "boots", "cloak", "robe", "bow", "crossbow", "spear", "mace", "tome", "scroll"
        ]
        
        # Descriptive adjectives/verbs (past participle form)
        self.descriptors = [
            "flaming", "burning", "blazing", "scorching", "searing",
            "frozen", "icy", "chilling", "glacial", "arctic",
            "shocking", "electrifying", "sparking", "crackling", "charged",
            "poisonous", "venomous", "toxic", "corrupted", "cursed",
            "holy", "blessed", "divine", "sacred", "radiant",
            "dark", "shadow", "void", "abyssal", "demonic",
            "enchanted", "mystical", "arcane", "ethereal", "spectral",
            "ancient", "forgotten", "legendary", "mythical", "eternal",
            "sharp", "keen", "deadly", "brutal", "savage",
            "glowing", "shimmering", "pulsing", "humming", "whispering"
        ]
        
        # Elements and forces
        self.elements = [
            "fire", "flame", "inferno", "ember", "magma",
            "ice", "frost", "snow", "blizzard", "hail",
            "lightning", "thunder", "storm", "tempest", "wind",
            "earth", "stone", "mountain", "crystal", "gem",
            "water", "ocean", "tide", "mist", "rain",
            "light", "sun", "moon", "star", "dawn",
            "shadow", "darkness", "night", "void", "chaos",
            "life", "death", "soul", "spirit", "dream",
            "time", "fate", "destiny", "fortune", "luck"
        ]
        
        # Creatures and beings
        self.creatures = [
            "dragon", "phoenix", "griffin", "wyvern", "basilisk",
            "demon", "devil", "angel", "seraph", "valkyrie",
            "titan", "giant", "colossus", "behemoth", "leviathan",
            "sphinx", "chimera", "hydra", "kraken", "roc",
            "lich", "wraith", "specter", "phantom", "revenant",
            "elemental", "djinn", "ifrit", "sylph", "undine",
            "wolf", "bear", "eagle", "serpent", "spider",
            "sage", "wizard", "sorcerer", "warlock", "oracle"
        ]
        
        # Mythical places and concepts
        self.places_concepts = [
            "avalon", "asgard", "olympus", "valhalla", "elysium",
            "atlantis", "lemuria", "shangri-la", "camelot", "babylon",
            "eternity", "infinity", "cosmos", "nexus", "zenith",
            "dominion", "sovereignty", "mastery", "supremacy", "ascendance",
            "vengeance", "justice", "mercy", "wrath", "fury",
            "wisdom", "knowledge", "truth", "enlightenment", "revelation",
            "power", "might", "strength", "vigor", "prowess"
        ]
    
    def generate_item_name(self, min_parts=1, max_parts=5):
        """Generate a random magical item name with 1-5 parts"""
        num_parts = random.randint(min_parts, max_parts)
        
        # Always start with a base item
        base_item = random.choice(self.base_items)
        
        # Create a list to hold all parts
        name_parts = []
        
        # Randomly select word categories to use
        available_categories = [
            self.descriptors,
            self.elements,
            self.creatures,
            self.places_concepts
        ]
        
        # Generate the specified number of parts (excluding the base item)
        for _ in range(num_parts):
            category = random.choice(available_categories)
            word = random.choice(category)
            
            # Avoid duplicates
            if word not in name_parts:
                name_parts.append(word)
        
        # Randomly decide the structure of the name
        structure_type = random.randint(1, 4)
        
        if structure_type == 1:
            # Pattern: [Descriptor] [Element] [BaseItem]
            # Example: "Flaming Fire Sword"
            final_name = " ".join(name_parts + [base_item])
            
        elif structure_type == 2:
            # Pattern: [BaseItem] of [Concept/Creature]
            # Example: "Sword of Dragons"
            if name_parts:
                final_name = f"{base_item} of {' '.join(name_parts)}"
            else:
                final_name = base_item
                
        elif structure_type == 3:
            # Pattern: [Descriptor] [BaseItem] of [Place/Concept]
            # Example: "Flaming Sword of Eternity"
            if len(name_parts) >= 2:
                mid_point = len(name_parts) // 2
                prefix = " ".join(name_parts[:mid_point])
                suffix = " ".join(name_parts[mid_point:])
                final_name = f"{prefix} {base_item} of {suffix}"
            else:
                final_name = f"{' '.join(name_parts)} {base_item}"
                
        else:
            # Pattern: [All descriptors] [BaseItem]
            # Example: "Ancient Flaming Crystal Sword"
            final_name = " ".join(name_parts + [base_item])
        
        # Capitalize each word
        return " ".join(word.capitalize() for word in final_name.split())
    
    def generate_multiple_items(self, count=10, min_parts=1, max_parts=5):
        """Generate multiple magical item names"""
        items = []
        for _ in range(count):
            items.append(self.generate_item_name(min_parts, max_parts))
        return items
    
    def print_items(self, count=10, min_parts=1, max_parts=5):
        """Print generated magical item names"""
        print(f"Generated {count} Magical Items:")
        print("=" * 40)
        
        items = self.generate_multiple_items(count, min_parts, max_parts)
        for i, item in enumerate(items, 1):
            print(f"{i:2d}. {item}")


    def interactive_generator(self):
        """Interactive prompt-based item generator"""
        print("🗡️  MAGICAL ITEM NAME GENERATOR  🗡️")
        print("=" * 45)
        
        while True:
            try:
                # Get number of items to generate
                while True:
                    try:
                        count = input("\nHow many magical items would you like to generate? (1-100, default 10): ").strip()
                        if not count:
                            count = 10
                            break
                        count = int(count)
                        if 1 <= count <= 100:
                            break
                        else:
                            print("Please enter a number between 1 and 100.")
                    except ValueError:
                        print("Please enter a valid number.")
                
                # Get complexity preference
                print("\nChoose complexity level:")
                print("1. Simple (1-2 words)")
                print("2. Moderate (2-3 words)")
                print("3. Complex (3-5 words)")
                print("4. Random (1-5 words)")
                print("5. Custom range")
                
                while True:
                    complexity = input("\nSelect complexity (1-5, default 4): ").strip()
                    if not complexity:
                        min_parts, max_parts = 1, 5
                        break
                    
                    if complexity == "1":
                        min_parts, max_parts = 1, 2
                        break
                    elif complexity == "2":
                        min_parts, max_parts = 2, 3
                        break
                    elif complexity == "3":
                        min_parts, max_parts = 3, 5
                        break
                    elif complexity == "4":
                        min_parts, max_parts = 1, 5
                        break
                    elif complexity == "5":
                        # Custom range
                        while True:
                            try:
                                min_parts = int(input("Minimum word count (1-5): "))
                                max_parts = int(input("Maximum word count (1-5): "))
                                if 1 <= min_parts <= max_parts <= 5:
                                    break
                                else:
                                    print("Min must be ≤ Max, both between 1-5")
                            except ValueError:
                                print("Please enter valid numbers.")
                        break
                    else:
                        print("Please enter 1, 2, 3, 4, or 5.")
                
                # Generate and display items
                print(f"\n🎲 Generating {count} magical items...")
                print("=" * 45)
                
                items = self.generate_multiple_items(count, min_parts, max_parts)
                for i, item in enumerate(items, 1):
                    print(f"{i:3d}. {item}")
                
                # Ask if user wants to continue
                print("\n" + "=" * 45)
                while True:
                    continue_choice = input("Generate more items? (y/n, default y): ").strip().lower()
                    if not continue_choice or continue_choice in ['y', 'yes']:
                        break
                    elif continue_choice in ['n', 'no']:
                        print("\nThanks for using the Magical Item Generator! 🎮")
                        return
                    else:
                        print("Please enter 'y' or 'n'.")
                        
            except KeyboardInterrupt:
                print("\n\nThanks for using the Magical Item Generator! 🎮")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Let's try again...")

def quick_demo():
    """Run a quick demonstration of the generator"""
    generator = MagicalItemGenerator()
    
    print("🗡️  MAGICAL ITEM GENERATOR - QUICK DEMO  🗡️")
    print("=" * 50)
    
    demos = [
        ("Simple items (1-2 words)", 1, 2, 5),
        ("Moderate items (2-3 words)", 2, 3, 5),
        ("Complex items (3-5 words)", 3, 5, 5),
        ("Random complexity (1-5 words)", 1, 5, 10)
    ]
    
    for title, min_parts, max_parts, count in demos:
        print(f"\n{title}:")
        print("-" * len(title))
        items = generator.generate_multiple_items(count, min_parts, max_parts)
        for i, item in enumerate(items, 1):
            print(f"{i:2d}. {item}")

# Example usage and main program
if __name__ == "__main__":
    print("Choose an option:")
    print("1. Interactive Generator (with prompts)")
    print("2. Quick Demo (see examples)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            generator = MagicalItemGenerator()
            generator.interactive_generator()
            break
        elif choice == "2":
            quick_demo()
            break
        elif choice == "3":
            print("Goodbye! 🎮")
            break
        else:
            print("Please enter 1, 2, or 3.")
