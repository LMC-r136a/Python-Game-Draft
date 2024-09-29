# import from random library
from random import randint, choice
import time
import os
from os import system

# Hero attributes

def create_hero(name, health, ability, special_skill):
    return {
        "name": name,
        "health": health,
        "max_health": health,   # Store max health for health restoration
        "ability": ability,
        "special_skill": special_skill,
        "inventory": {"Healing Potion": 3},
        "experience": 0,
        "relics": []            # Track collected relics
    }

# Enemy attributes - 5 enemies per world except for the Centre World
def create_enemy(world):
    if world == "North World":
        enemies = [
            {"name": "Frost Giant", "health": 70},
            {"name": "Ice Dragon", "health": 60},
            {"name": "Snow Wolf", "health": 60},
            {"name": "Frozen Ogre", "health": 60},
            {"name": "Blizzard Bear", "health": 65}
        ]
    elif world == "South World":
        enemies = [
            {"name": "Forest Spirit", "health": 70},
            {"name": "Tree Ent", "health": 75},
            {"name": "Poisonous Vine", "health": 65},
            {"name": "Enchanted Boar", "health": 65},
            {"name": "Cursed Dryad", "health": 70}
        ]
    elif world == "East World":
        enemies = [
            {"name": "Fire Phantom", "health": 70},
            {"name": "Lava Beast", "health": 75},
            {"name": "Cinder Wraith", "health": 60},
            {"name": "Flame Scorpion", "health": 70},
            {"name": "Molten Serpent", "health": 75}
        ]
    elif world == "West World":
        enemies = [
            {"name": "Stone Golem", "health": 80},
            {"name": "Earth Elemental", "health": 75},
            {"name": "Rock Serpent", "health": 75},
            {"name": "Ancient Gargoyle", "health": 75},
            {"name": "Crystal Turtle", "health": 80}
        ]
    elif world == "Centre World":
        enemies = [
            {"name": "Dark Sorcerer", "health": 100}  # Only one enemy in Centre World
        ]
    return choice(enemies)  # Randomly select one enemy from the list

# Loot system
def generate_loot(enemy, character):
    loot = []
    relic_won = False  # Track if a relic is won

    if enemy["name"] == "Dark Sorcerer":
        loot.append("Legendary Magic Wand")
        loot.append("Healing Potion")
    else:
        loot.append("Healing Potion")

        # Add relics depending on defeated world
        if enemy["name"] in ["Frost Giant", "Ice Dragon", "Snow Wolf", "Frozen Ogre", "Blizzard Bear"]:
            character["relics"].append("Amulet of Light")
            loot.append("You have collected the Amulet of Light!")
            relic_won = True  # Relic won
        elif enemy["name"] in ["Forest Spirit", "Tree Ent", "Poisonous Vine", "Enchanted Boar", "Cursed Dryad"]:
            character["relics"].append("Sword of Destiny")
            loot.append("You have collected the Sword of Destiny!")
            relic_won = True  # Relic won
        elif enemy["name"] in ["Fire Phantom", "Lava Beast", "Cinder Wraith", "Flame Scorpion", "Molten Serpent"]:
            character["relics"].append("Helm of Power")
            loot.append("You have collected the Helm of Power!")
            relic_won = True  # Relic won
        elif enemy["name"] in ["Stone Golem", "Earth Elemental", "Rock Serpent", "Ancient Gargoyle", "Crystal Turtle"]:
            character["relics"].append("Shield of Hope")
            loot.append("You have collected the Shield of Hope!")
            relic_won = True  # Relic won

    # Add 15 health points if a relic is won
    if relic_won:
        character["health"] += 15
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]
        loot.append(f"{character['name']} gains 15 health points! Current health: {character['health']}")

    loot.append(f"{randint(5, 15)} Gold")
    return loot

# Attack function
def attack(character, enemy):
    damage = randint(5, 15)
    enemy["health"] -= damage
    print(f"{character['name']} attacks {enemy['name']} for {damage} damage!")

# Use special ability
def use_special(character, enemy):
    if character["special_skill"] == "Shield slam":
        damage = randint(10, 25)
        enemy["health"] -= damage
        print(f"{character['name']} uses Shield slam on {enemy['name']} for {damage} damage!")
        print(f"{enemy['name']} is stunned and can't attack this turn!")
        return True  # Indicate that the enemy is stunned
    elif character["special_skill"] == "Magic Blast":
        damage = randint(15, 30)
        enemy["health"] -= damage
        print(f"{character['name']} uses Magic Blast on {enemy['name']} for {damage} damage!")
        return False  # Not stunning
    elif character["special_skill"] == "Stealth":
        damage = randint(20, 40)
        enemy["health"] -= damage
        print(f"{character['name']} uses Stealth on {enemy['name']} for {damage} damage!")
        return False  # Not stunning

# Heal function
def heal(character):
    if character["inventory"]["Healing Potion"] > 0:
        healing_amount = randint(15, 30)
        character["health"] += healing_amount
        character["inventory"]["Healing Potion"] -= 1
        print(f"{character['name']} uses a Healing Potion and restores {healing_amount} health!")
        print(f"{character['name']}'s health is now {character['health']}.")
    else:
        print(f"{character['name']} has no Healing Potions left!")

# Show player stats
def show_stats(character):
    print("\nPlayer Stats:")
    print(f"Name: {character['name']}")
    print(f"Health: {character['health']} / {character['max_health']}")
    print(f"Experience: {character['experience']}")
    print("Inventory:")
    for item, count in character["inventory"].items():
        print(f"- {item}: {count}")
    print("Relics Collected:")
    for relic in character["relics"]:
        print(f"- {relic}")

# Ending function
def end_game():
    print("\n*******************************************************************")
    print("The Kingdom has been saved. Glory to our heroes and the King.")
    print("The Evil Sorcerer has been destroyed for eternity.")
    print("*******************************************************************\n")
    print("Thank you for playing Quest of the Fallen Kingdom!")
    exit()  # End the game

#Handle player's normal attack
def player_attack(character, enemy):    
    attack(character, enemy)
    print(f"{enemy['name']}'s health: {enemy['health']}")

#Handle player's special ability
def player_special(character, enemy):
    stunned = use_special(character, enemy)
    print(f"{enemy['name']}'s health: {enemy['health']}")
    return stunned  # Return if the enemy is stunned

#Handle healing the player
def player_heal(character):
    heal(character)

#Ask the player to choose an action and perform it
def choose_player_action(character, enemy):

    while True:
        action = input(f"\n{character['name']}, do you want to (attack, use special, heal)? ").strip().lower()

        if action == "attack":
            player_attack(character, enemy)
            return False  # No stun, move to enemy's turn
        elif action == "use special":
            return player_special(character, enemy)  # Return whether enemy is stunned
        elif action == "heal":
            player_heal(character)
            continue  # Healing doesn't take the enemy's turn, so continue asking for input
        else:
            print("Invalid action. Please choose again.")

#Handle enemy's turn to attack the player
def enemy_attack(character, enemy):

    enemy_damage = randint(5, 15)
    character["health"] -= enemy_damage
    print(f"{enemy['name']} attacks {character['name']} for {enemy_damage} damage!")
    print(f"{character['name']}'s health: {character['health']}")

#Check if the battle is over
def check_battle_outcome(character, enemy):
    
    if enemy["health"] <= 0:
        print(f"SUCCESS. The {enemy['name']} has been defeated!")
        return "enemy_defeated"
    elif character["health"] <= 0:
        print(f"{character['name']} has been defeated!")
        return "character_defeated"
    return None

#Handle loot collection and health restoration after defeating an enemy
def handle_victory(character, enemy):

    loot = generate_loot(enemy, character)
    print("You collected the following loot:")
    for item in loot:
        print(f"- {item}")

    # Restore 25 health points after defeating the enemy
    character["health"] += 25
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    print(f"{character['name']} restores 25 health points! Current health: {character['health']}")
    character["experience"] += 10  # Award experience points
    print(f"{character['name']} gains 10 experience points!")

    show_stats(character)  # Show updated stats

#Manage battle between the player and the enemy
def battle(character, enemy, world):
    
    print(f"A wild {enemy['name']} appears!\n")
    final_boss_defeated = False  # Track if the final boss is defeated

    while character["health"] > 0 and enemy["health"] > 0:
        # Player's turn
        enemy_stunned = choose_player_action(character, enemy)

        # Check if the enemy is defeated
        outcome = check_battle_outcome(character, enemy)
        if outcome == "enemy_defeated":
            if enemy["name"] == "Dark Sorcerer":
                final_boss_defeated = True  # Mark final boss defeated
            handle_victory(character, enemy)
            break
        elif outcome == "character_defeated":
            break

        # Enemy's turn, only if not stunned
        if not enemy_stunned:
            enemy_attack(character, enemy)

        # Check if the player is defeated
        outcome = check_battle_outcome(character, enemy)
        if outcome == "character_defeated":
            break

    return final_boss_defeated  # Return if the final boss was defeated

# Explore a world
def explore_world(world):
    print(f"You are exploring the {world}.")
    if world == "North World":
        print("The North is filled with towering mountains and fierce creatures.\n")
    elif world == "South World":
        print("The South is a lush forest, home to many magical beings.\n")
    elif world == "East World":
        print("The East is a desolate wasteland, haunted by shadows of the past.\n")
    elif world == "West World":
        print("The West has ancient ruins, filled with lost treasures and dangers.\n")
    elif world == "Centre World":
        print("The Centre is where the Evil Sorcerer resides and is where the final battle awaits.\n")

# Function to select a character
def select_character():
    print("Choose your character:\n")
    print("1. Eric the Knight - Health: 120, Ability: Sword master, Special Skill: Shield slam")
    print("2. Eli the Elven Mage - Health: 80, Ability: Powerful magic, Special Skill: Magic Blast")
    print("3. Kye the Rogue - Health: 100, Ability: High agility, Special Skill: Stealth")

    while True:
        choice = input("\nEnter the number of your character (1-3): ")
        if choice == '1':
            return create_hero("Eric the Knight", 120, "Sword master", "Shield slam")
        elif choice == '2':
            return create_hero("Eli the Elven Mage", 80, "Powerful magic", "Magic Blast")
        elif choice == '3':
            return create_hero("Kye the Rogue", 100, "High agility", "Stealth")
        else:
            print("Invalid choice. Please try again.")

# Main game loop
def main_game():
    current_character = select_character()  # Allow player to choose character

    print(f"\nYou are playing as {current_character['name']}.")

    completed_worlds = []  # Track completed worlds
    unlocked_worlds = ['North World', 'South World', 'East World', 'West World']  # Initially unlocked worlds

    while True:
        print("\nChoose a world to explore: North, South, East, or West, or type 'exit' to quit.")

        # Unlock Centre World after completing all others
        if len(completed_worlds) == 4 and "Centre World" not in unlocked_worlds:
            unlocked_worlds.append("Centre World")
            print("\nYou have unlocked the Centre World! Face the Dark Sorcerer!")

        if "Centre World" not in unlocked_worlds:
            print("The Centre World is only accessible after you've completed all other Worlds.\n")
        else:
            print("You can now enter the Centre World for the final battle!\n")

        choice = input("Your choice: ").strip().lower()

        # Map short input to full world names
        world_map = {
            'north': 'North World',
            'south': 'South World',
            'east': 'East World',
            'west': 'West World',
            'centre': 'Centre World',
        }

        if choice in world_map:
            world = world_map[choice]
            if world in unlocked_worlds:
                if world not in completed_worlds:  # Allow exploring only if not completed
                    explore_world(world)
                    enemy = create_enemy(world)
                    final_boss_defeated = battle(current_character, enemy, world)  # Pass the world to battle

                    if current_character["health"] > 0:  # Only add to completed if not defeated
                        completed_worlds.append(world)

                        # End the game if the final boss is defeated
                        if final_boss_defeated:
                            end_game()  # Call the end game function
                else:
                    print(f"You have already completed the {world}!")
            else:
                print(f"You cannot access the {world} yet. Complete other worlds first.")
        elif choice == 'exit':
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

def clear_screen():
    # Clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')

def print_large_title(title):
    # Define a simple ASCII art for the game title
    ascii_art = r"""

  ###    ##   ##  #######   #####   ########           #####   #######           ########  ##  ##  #######           
 ## ##   ##   ##   ##   #  ##   ##  ## ## ##          ### ###   ##   #           ## ## ##  ##  ##   ##   #           
##   ##  ##   ##   ##      ##          ##             ##   ##   ##                  ##     ##  ##   ##               
##   ##  ##   ##   ####     #####      ##             ##   ##   ####                ##     ######   ####             
##   ##  ##   ##   ##           ##     ##             ##   ##   ##                  ##     ##  ##   ##               
 ## ##   ##   ##   ##   #  ##   ##     ##             ### ###   ##                  ##     ##  ##   ##   #           
  ####    #####   #######   #####     ####             #####   ####                ####    ##  ##  #######
                                                                                                              
####      #####    #####   ########          ### ###   ######  ##   ##   #####   #####     #####   ##   ##   #####   
 ##      ### ###  ##   ##  ## ## ##           ## ##      ##    ###  ##  ##   ##   ## ##   ### ###  ### ###  ##   ##  
 ##      ##   ##  ##          ##              ####       ##    #### ##  ##        ##  ##  ##   ##  #######  ##       
 ##      ##   ##   #####      ##              ###        ##    #######  ## ####   ##  ##  ##   ##  ## # ##   #####   
 ##      ##   ##       ##     ##              ####       ##    ## ####  ##   ##   ##  ##  ##   ##  ##   ##       ##  
 ##  ##  ### ###  ##   ##     ##              ## ##      ##    ##  ###  ##   ##   ## ##   ### ###  ##   ##  ##   ##  
#######   #####    #####     ####            ### ###   ######  ##   ##   #####   #####     #####   ### ###   #####

    """
    print(ascii_art)
    time.sleep(5)  # Display the title for 5 seconds

def print_story():
    story_lines = [
        "Oh heroes of the Kingdom of Gdom, you have been summoned by the King to go on a quest.",
        "",
        "Your quest is to defeat the Evil Sorcerer who threatens our way of life.",
        "",
        "You must go to the North World and recover the Amulet of Light.",
        "You must go to the South World and recover the Sword of Destiny.",
        "You must go to the East World and recover the Shield of Hope.",
        "And you must go to the West World and recover the Helm of Power.",
        "Only then should you proceed to the Centre World where you must face the Evil Sorcerer.",
        "It is only with these powerful relics will you have the necessary tools that can defeat Evil.",
        "",
        "Our fate rests in your hands, you must not fail us!!!!!", 
        "Go, and tread with care, and may the fates be kind."
    ]
    
    for line in story_lines:
        print(line)
        time.sleep(2)  # Wait for 2 seconds before printing the next line


# Start the game

clear_screen()
print_large_title("Quest of the Lost Kingdoms")
print_story()
clear_screen()
main_game()