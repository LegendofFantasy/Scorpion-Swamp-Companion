# This transform is used to make the image fill the screen as best it can
# Usage should be something like:
# show selator at truecenter, fill
# with dissolve
transform fill:
    fit "contain"

# These are the lookup tables for converting between IDs and English names of items and locations for Archipelago
# Antherica Berry, Map to Willowbend, Wolf Amulet, False Bird Amulet, Frog Amulet, Flower Amulet, Spider Amulet are not going to be Archipelago items, 
# but still need to be added to inventory
define ITEM_NAME_TO_ID = {
    "Skill Spell Gem" : 1,
    "Stamina Spell Gem" : 2,
    "Luck Spell Gem" : 3,
    "Fire Spell Gem" : 4,
    "Ice Spell Gem" : 5,
    "Illusion Spell Gem" : 6,
    "Friendship Spell Gem" : 7,
    "Growth Spell Gem" : 8,
    "Bless Spell Gem" : 9,
    "Fear Spell Gem" : 10,
    "Withering Spell Gem" : 11,
    "Curse Spell Gem" : 12,
    "Golden Magnet" : 13,
    "Violet Jewel" : 14,
    "Secret Word" : 15,
    "Gold Chain" : 16,
    "Magic Sword" : 17,
    "Horn of a Unicorn" : 18,
    "Magic Potion" : 19,
    "Ranger's Helmet" : 20,
    "Sword Tree Seeds" : 21,
    "Red Cloak" : 22,
    "Great Magic Sword" : 23,
    "Parrot Feathers" : 24,
    "Dire Beast Claws" : 25,
    "Progressive Skill" : 26,
    "Progressive Stamina" : 27,
    "Progressive Luck" : 28,
    "Selator" : 29,
    "Grimslade" : 30,
    "Poomchukker" : 31,
    "Clearing 3" : 103,
    "Clearing 4" : 104,
    "Clearing 5" : 105,
    "Clearing 6" : 106,
    "Clearing 7" : 107,
    "Clearing 8" : 108,
    "Clearing 9" : 109,
    "Clearing 10" : 110,
    "Clearing 11" : 111,
    "Clearing 12" : 112,
    "Clearing 13" : 113,
    "Clearing 14" : 114,
    "Clearing 15" : 115,
    "Clearing 16" : 116,
    "Clearing 17" : 117,
    "Clearing 18" : 118,
    "Clearing 19" : 119,
    "Clearing 20" : 120,
    "Clearing 21" : 121,
    "Clearing 23" : 123,
    "Clearing 24" : 124,
    "Clearing 25" : 125,
    "Clearing 26" : 126,
    "Clearing 27" : 127,
    "Clearing 28" : 128,
    "Clearing 29" : 129,
    "Clearing 30" : 130,
    "Clearing 32" : 132,
    "Clearing 33" : 133,
    "Clearing 34" : 134,
    "Clearing 35" : 135,
}
define ID_TO_ITEM_NAME = {v: k for k, v in ITEM_NAME_TO_ID.items()}
define LOCATION_NAME_TO_ID = {
    "Fallen Fighter" : 1,
    "Slay the Parrot" : 2,
    "Eagle's Nest" : 3,
    "Slay the Dire Beast" : 4,
    "Slay Grimslade" : 5,
    "Gift from the Mistress of Birds" : 6,
    "Gift from the Master of Wolves" : 7,
    "Slay the Ranger" : 8,
    "Gift from Grimslade" : 9,
    "Slay the Unicorn" : 10,
    "Slay the Pool Beast" : 11,
    "Slay the Sword Trees" : 12,
    "Slay the Thief" : 13,
    "Game Over - A Feast for Rats" : 14,
    "Game Over - Crocodile Smile" : 15,
    "Game Over - A Hundred Pieces of Gold" : 16,
    "Game Over - Failing Selator's Quest" : 17,
    "Game Over - Itsy Bitsy Spider" : 18,
    "Game Over - Failing Poomchukker's Quest" : 19,
    "Game Over - Curse of the Birds" : 20,
    "Game Over - Magic Carpet Ride" : 21,
    "Game Over - Dragged Down Into the River" : 22,
    "Game Over - Grimslade's Trap" : 23,
    "Game Over - Out the Window and Into the Dungeons" : 24,
    "Game Over - A Feast for the Spiders" : 25,
    "Game Over - Slain by Poomchukker's Guards" : 26,
    "Game Over - Explosion of Hellfire" : 27,
    "Game Over - The Master of Spiders Has No Friends" : 28,
    "Game Over - Returning to Grimslade Empty-Handed" : 99,
    "Halicar's Shop 1" : 29,
    "Halicar's Shop 2" : 30,
    "Halicar's Shop 3" : 31,
    "Halicar's Shop 4" : 32,
    "Halicar's Shop 5" : 33,
    "Halicar's Shop 6" : 34,
    "Selator's Spell Gem 1" : 35,
    "Selator's Spell Gem 2" : 36,
    "Selator's Spell Gem 3" : 37,
    "Selator's Spell Gem 4" : 38,
    "Selator's Spell Gem 5" : 39,
    "Selator's Spell Gem 6" : 40,
    "Selator's Spell Gem 7" : 41,
    "Selator's Spell Gem 8" : 42,
    "Selator's Spell Gem 9" : 43,
    "Poomchukker's Spell Gem 1" : 44,
    "Poomchukker's Spell Gem 2" : 45,
    "Poomchukker's Spell Gem 3" : 46,
    "Poomchukker's Spell Gem 4" : 47,
    "Poomchukker's Spell Gem 5" : 48,
    "Poomchukker's Spell Gem 6" : 49,
    "Grimslade's Spell Gem 1" : 50,
    "Grimslade's Spell Gem 2" : 51,
    "Grimslade's Spell Gem 3" : 52,
    "Grimslade's Spell Gem 4" : 53,
    "Grimslade's Spell Gem 5" : 54,
    "Grimslade's Spell Gem 6" : 55,
    "Grimslade's Spell Gem 7" : 56,
    "Grimslade's Spell Gem 8" : 57,
    "Grimslade's Spell Gem 9" : 58,
    "Gift from the Master of Gardens 1" : 59,
    "Gift from the Master of Gardens 2" : 60,
    "Gift from the Master of Gardens 3" : 61,
    "Unicorn Clearing Spell Gem 1" : 62,
    "Unicorn Clearing Spell Gem 2" : 63,
    "Gronar - Directions to Selator" : 64,
    "Gronar - Directions to Poomchukker" : 65,
    "Gronar - Directions to Grimslade" : 66,
    "Clearing 1 Entered" : 101,
    "Clearing 3 Entered" : 103,
    "Clearing 4 Entered" : 104,
    "Clearing 5 Entered" : 105,
    "Clearing 6 Entered" : 106,
    "Clearing 7 Entered" : 107,
    "Clearing 8 Entered" : 108,
    "Clearing 9 Entered" : 109,
    "Clearing 10 Entered" : 110,
    "Clearing 11 Entered" : 111,
    "Clearing 12 Entered" : 112,
    "Clearing 13 Entered" : 113,
    "Clearing 14 Entered" : 114,
    "Clearing 15 Entered" : 115,
    "Clearing 16 Entered" : 116,
    "Clearing 17 Entered" : 117,
    "Clearing 18 Entered" : 118,
    "Clearing 19 Entered" : 119,
    "Clearing 20 Entered" : 120,
    "Clearing 21 Entered" : 121,
    "Clearing 23 Entered" : 123,
    "Clearing 24 Entered" : 124,
    "Clearing 25 Entered" : 125,
    "Clearing 26 Entered" : 126,
    "Clearing 27 Entered" : 127,
    "Clearing 28 Entered" : 128,
    "Clearing 29 Entered" : 129,
    "Clearing 30 Entered" : 130,
    "Clearing 32 Entered" : 132,
    "Clearing 33 Entered" : 133,
    "Clearing 34 Entered" : 134,
    "Clearing 35 Entered" : 135,
}

# These are the enemies for the game
default giant = Enemy("GIANT", 9, 12, 4)
default masterOfSpiders = Enemy("MASTER OF SPIDERS", 9, 6, 3)
default swordTrees = Enemy("SWORD TREES", 9, 12)
default masterOfWolves = Enemy("MASTER OF WOLVES", 11, 10)
default brigandLeader = Enemy("BRIGAND LEADER", 9, 10)
default poolBeast = Enemy("POOL BEAST", 8, 10)
default petWolf1 = Enemy("First WOLF", 7, 5)
default petWolf2 = Enemy("Second WOLF", 6, 6)
default grimslade = Enemy("GRIMSLADE", 13, 18, t="")
default grimslade2 = Enemy("GRIMSLADE", 9, 10, t="")
default crabGrass = Enemy("CRAB GRASS", 6, 16)
default giantFrog1 = Enemy("First GIANT FROG", 5, 6)
default giantFrog2 = Enemy("Second GIANT FROG", 6, 5)
default slime = Enemy("SLIME", 5, 17)
default direBeast = Enemy("DIRE BEAST", 9, 10)
default bear = Enemy("BEAR", 7, 8)
default wolf = Enemy("WOLF", 7, 6)
default unicorn = Enemy("UNICORN", 11, 4)
default demon = Enemy("DEMON", 16, 12)
default brigand2 = Enemy("Second BRIGAND", 8, 8)
default brigand3 = Enemy("Third BRIGAND", 8, 11)
default giantSpider = Enemy("GIANT SPIDER", 8, 9)
default thief = Enemy("THIEF", 10, 9)
default swampOrc1 = Enemy("First SWAMP ORC", 6, 7)
default swampOrc2 = Enemy("Second SWAMP ORC", 7, 7)
default swampOrc3 = Enemy("Third SWAMP ORC", 6, 5)
default goblinStatue = Enemy("GOBLIN STATUE", 7, 6)
default brigand1_2 = Enemy("First BRIGAND", 8, 10)
default brigand2_2 = Enemy("Second BRIGAND", 8, 11)
default giantScorpion = Enemy("GIANT SCORPION", 9, 10)
default poomchukker = Enemy("POOMCHUKKER", 9, 14, t="")
default cutpurse1 = Enemy("First CUTPURSE", 7, 5)
default cutpurse2 = Enemy("Second CUTPURSE", 8, 5)
default ranger = Enemy("RANGER", 10, 10)
default masterOfGardens = Enemy("MASTER OF GARDENS", 7, 10)
default eagle = Enemy("EAGLE", 7, 6)