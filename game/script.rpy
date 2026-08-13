define bn = Character(None) # This is the battle narrator
define bp = Character(None, image="gui/bubble.png", kind=dynamic_bubble) # These are the characters to source the dice bubbles from
define be = Character(None, image="gui/bubble.png", kind=dynamic_bubble)
define bpBubble = {"area": [160,360,160,90],"properties": "top_left"}
define beBubble = {"area": [1520,360,160,90],"properties": "top_right"}
define narrator = nvl_narrator
define menu = nvl_menu
define playerDamage = 2 # This is the damage that the player does when they hit
default stats = {} # These are the player's stats (usually Skill, Stamina, and Luck)
default progressiveStats = {"Skill" : 0, "Stamina" : 0, "Luck" : 0} # These are the bonuses added to stats from Archipelago items
default inventory = {} # These are the items the player has
default magic = {} # These are the spell gems the player has
default wizards = [] # These are the wizards the player can meet in wizardsanity in Archipelago mode
default clearingPasses = ["1"] # These are the clearings the player can access if playing with clearingsanity in Archipelago mode
default visited = [] # These are the clearings the player has visited
default quest = "" # This is used to track which quest the player is doing
default fearFlowersDefeated = False # This is used to track whether the player has defeated the Fear Flowers
default orcsDefeated = False # This is used to track whether the player has defeated the orcs
default quicksandGrowth = False # This is used to track whether the player cast Growth on the quicksand
default bearOutcome = "" # This is used to track the outcome of the Bear encounter
default rangerOutcome = "" # This is used to track the outcome of the Ranger encounter
default brigandOutcome = "" # This is used to track the outcome of the Brigand encounter
default canUseEagle = False # This is used to determine if the player has flown on the eagle in clearingsanity
default canUseIceFlow = False # This is used to determine if the player has taken the ice flow from clearing 33 to 35 in clearingsanity
default dwarfPotion = False # This is used to track if the player drank the potion that temporarily reduces Skill by 1 for one combat
default extraSkill = 0 # This is used to track extra skill from a magic sword or helmet
default wordKnown = False # This is used to track if the player knows the Secret Word
default preferences.askLuck = False # This is for the preferences menu to determine if luck can be used in combat
default preferences.failTests = False # This is for the preferences menu to determine if you should fail all statistic tests (useful for reaching certain references)
default preferences.failCombat = False # This is for the preferences menu to determine if you should fail all combat tests (useful for reaching certain references)
default preferences.askEscape = False # This is for the preferences menu to determine if escape will be offered in combat
default preferences.askAP = True # This is for the preferences menu to determine if the player should be asked if they want to connect to Archipelago
default preferences.showImages = False # This is for the preferences menu to determine if images should be shown (the player must provide the images)
default ap = False # This is used to determine if the game is being run in Archipelago mode
default goal = "" # This is used to store the goal value from Archipelago
default scouts = {} # This is used to store the scouts for all of the locations from Archipelago
default extra_locations = False # This is used to store the extra_locations value from Archipelago
default clearingsanity = False # This is used to store the clearingsanity value from Archipelago
default spellsanity = False # This is used to store the spellsanity value from Archipelago
default wizardsanity = False # This is used to store the wizardsanity value from Archipelago
default required_amulets = -1 # This is used to store the required_amulets value from Archipelago. -1 is vanilla behaviour
default has_required_amulets = False # This is set to True if the player returns to Grimslade with sufficient amulets
default playerRoll = [] # This is used to store a roll the player makes
default enemyRoll = [] # This is used to store a roll an enemy makes
default currentDamage = 0 # This is used to set the current damage in a combat round
default temp = False # This is used for temporary values throughout the game
default line = "" # This is used for a new bit of text being added in for Archipelago

# The game starts here.

label start:

    if preferences.askAP:
        if renpy.confirm("Do you want to connect to Archipelago?"):
            $ ap = True
           
            $ read_files()

            if goal == "all": # Check if the goal has been completed
                $ check_goal()
                if len(goals_complete) >= 3:
                    call send_victory from _call_send_victory
            
            $ get_items()
            # This makes items announce that they have been received. It starts True so that the initial items don't flood the player
            $ receive_silently = False

            # This is a timer that runs the function that checks for new locations checked and items received
            show screen progression_watcher

    python:
        stats["Skill"] = Statistic("Skill", min(12, roll() + 6 + progressiveStats["Skill"]))
        stats["Stamina"] = Statistic("Stamina", min(24, roll() + roll() + 12 + progressiveStats["Stamina"] * 2))
        stats["Luck"] = Statistic("Luck", min(12, roll() + 6 + progressiveStats["Luck"]))

    
    show screen statScreen with moveinleft
    show screen itemMenu with moveinright
    "{nw}"
    nvl clear

    """
    BACKGROUND

    {clear}
    """
    
    jump r1

label r1:
    if preferences.showImages:
        window hide
        show fenmargetavern at truecenter, fill
        with dissolve
        pause
        window show
    "1"

    menu:
        "48":
            jump r48

        "95":
            jump r95

label r2:
    """
    {clear}

    2
    """
    
    menu:
        "49":
            jump r49
        "173":
            jump r173

label r3:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - A Feast for Rats"])
            $ notify_item("Game Over - A Feast for Rats")
    """
    {clear}

    3
    """
    jump gameover

label r4:
    if preferences.showImages:
        window hide
        show goblin_statue at truecenter, fill
        with dissolve
        pause
        window show
    nvl clear
    "4"
    
    menu:
        "284":
            jump r284
        "123":
            if preferences.showImages:
                hide goblin_statue with dissolve
            jump r123

label r5:
    "{i}Test your Luck.{/i}"

    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r273
    else:
        $ stats["Luck"].damage(1)
        jump r297

label r6:
    """
    {clear}

    6
    """ 
    if "Antherica Berry" in inventory.keys():
        jump r175
    else:
        jump r52

label r7:
    """
    {clear}

    7
    """
    
    menu:
        "266":
            jump r266
        "207":
            jump r207

label r8:
    """
    {clear}

    8
    """
    
    python:
        temp = ("Skill Spell Gem" in magic.keys() or "Stamina Spell Gem" in magic.keys() or "Luck Spell Gem" in magic.keys() or 
            "Fire Spell Gem" in magic.keys() or "Ice Spell Gem" in magic.keys() or "Illusion Spell Gem" in magic.keys())

    menu:
        "141" if temp:
            jump r141
        "316":
            jump r316
        "341":
            jump r341

label r9:
    """
    {clear}

    9
    """
    jump r195

label r10:
    """
    {clear}

    10
    """
    if "5" in visited:
        jump r142
    $ visited.append("5")
    if clearingsanity:
        $ checked.append("Clearing 5 Entered")
        $ notify_item("Clearing 5 Entered")
    menu:
        "59":
            jump r59
        "227":
            jump r227

label r11:
    """
    {clear}

    11
    """
    if "6" in visited:
        jump r210
    $ visited.append("6")
    if clearingsanity:
        $ checked.append("Clearing 6 Entered")
        $ notify_item("Clearing 6 Entered")
    menu r11menu:
        "176":
            jump r176
        "102":
            jump r102
        "374":
            jump r374

label r12:
    """
    {clear}

    12
    """
    call battle(giant, True, 6) from _call_battle

    if _return == "escaped":
        if preferences.showImages:
            hide giant with dissolve
        jump r161
    else:
        jump r61

label r13:
    """
    {clear}

    13
    """
    if quest == "Selator":
        jump r212
    elif quest == "Grimslade":
        jump r287
    elif quest == "Poomchukker":
        jump r376

label r14:
    """
    {clear}

    14
    """
    if "32" in visited:
        jump r338
    $ visited.append("32")
    if clearingsanity:
        $ checked.append("Clearing 32 Entered")
        $ notify_item("Clearing 32 Entered")
    if preferences.showImages:
        window hide
        show scorpionfight at truecenter, fill
        with dissolve
        pause
        window show
    menu:
        "88":
            if preferences.showImages:
                hide scorpionfight with dissolve
            jump r88
        "312":
            jump r312

label r15:
    python:
        temp = False
        for k in inventory.keys():
            if "Amulet" in k:
                temp = True
                break

    menu:
        "15"

        "63" if "Golden Magnet" in inventory.keys():
            jump r63
        "198" if temp:
            jump r198
        "276" if "Violet Jewel" in inventory.keys():
            jump r276
        "212":
            jump r212menu

label r16:
    """
    {clear}

    16
    """
    jump r198

label r17:
    """
    {clear}

    17
    """
    $ stats["Stamina"].damage(3)
    "You lose 3 STAMINA points."
    if stats["Stamina"].current <= 0:
        jump gameover
    
    python:
        if "Map to Willowbend" in inventory.keys():
            temp = True
        inventory = {}
        magic = {}
        extraSkill = 0
        if temp:
            inventory["Map to Willowbend"] = Item("Map to Willowbend")

    jump r179

label r18:
    """
    {clear}

    18
    """
    jump r19

label r19:
    nvl clear
    "19"
    
    menu:
        "280":
            jump r280
        "137":
            jump r137

label r20:
    nvl clear
    $ stats["Stamina"].restore(2)
    $ stats["Luck"].restore(1)
    "20
    
    You regain 2 STAMINA points and 1 LUCK point."
    jump r342

label r21:
    nvl clear
    $ stats["Stamina"].restore(1)
    "21\nYou regain 1 STAMINA point."
    
    menu:
        "55":
            jump r55
        "390":
            jump r390

label r22:
    nvl clear
    "22"

    menu:
        "320" if not clearingsanity or "29" in clearingPasses:
            $ temp = "south"
            jump r320
        "90" if not clearingsanity or "34" in clearingPasses:
            jump r90
        "11" if not clearingsanity or "6" in clearingPasses:
            jump r11

label r23:
    """
    {clear}

    23
    """
    if not clearingsanity or "16" in clearingPasses:
        nvl clear
    else:
        "You worry about losing your way and instead choose to return back the way you came."
        if preferences.showImages:
            hide mistress_of_birds with dissolve
        jump r217
    if clearingsanity:
        $ canUseEagle = True
    jump r248

label r24:
    """
    {clear}

    24\n{i}Test your Luck.{/i}
    """
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
    else:
        $ stats["Luck"].damage(1)
        $ stats["Stamina"].damage(2)
        "You lose 2 points of STAMINA."
        if stats["Stamina"].current <= 0:
            jump gameover
    jump r249

label r25:
    nvl clear
    "25"
    if preferences.showImages:
        hide eaglesnest with dissolve
    jump r202

label r26:
    """
    {clear}

    26
    """
    call battle(masterOfSpiders) from _call_battle_1
    if preferences.showImages:
        hide master_of_spiders with dissolve
    jump r354

label r27:
    if wizardsanity:
        $ checked.append("Gronar - Directions to Poomchukker")
        $ notify_item("Gronar - Directions to Poomchukker")
    if preferences.showImages:
        window hide
        show poomchukker at truecenter, fill
        with dissolve
        pause
        window show
    """
    {clear}

    27
    """
    
    menu:        
        "2":
            jump r2
        "173":
            jump r173

label r28:
    """
    {clear}

    28
    """
    call battle(swordTrees) from _call_battle_2
    jump r362

label r29:
    """
    {clear}

    29\n{i}Test your Luck.{/i}
    """
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r185
    else:
        $ stats["Luck"].damage(1)
        jump r378

label r30:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Crocodile Smile"])
            $ notify_item("Game Over - Crocodile Smile")
    """
    {clear}

    30
    """
    jump gameover

label r31:
    """
    {clear}

    31
    """
    if "21" in visited:
        jump r364
    $ visited.append("21")
    if clearingsanity:
        $ checked.append("Clearing 21 Entered")
        $ notify_item("Clearing 21 Entered")
    
    menu:        
        "47":
            jump r47
        "394":
            jump r394
        "77":
            jump r77

label r32:
    nvl clear
    "32"
    python:
        stats["Stamina"].damage(2)
        if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 1
        else:
            stats["Skill"].damage(1)
    "You lose 2 STAMINA points and 1 SKILL point."
    if stats["Stamina"].current <= 0:
        jump gameover
    
    menu:
        "269":
            jump r269
        "80":
            jump r80

label r33:
    if preferences.showImages:
        window hide
        show crab_grass at truecenter, fill
        with dissolve
        pause
        window show
    """
    {clear}

    33
    """
    menu:
        "134":
            jump r134
        "167":
            jump r167

label r34:
    menu:
        "34"

        "237" if "Withering Spell Gem" in magic.keys():
            jump r237
        "291" if "Fire Spell Gem" in magic.keys():
            jump r291
        "356" if "Fear Spell Gem" in magic.keys():
            jump r356
        "209":
            jump r209menu

label r35:
    """
    {clear}

    35
    """
    $ stats["Stamina"].damage(1)
    "You lose 1 STAMINA point."
    if stats["Stamina"].current <= 0:
        jump gameover
    
    menu:
        "281":
            jump r281
        "399":
            jump r399
        "309":
            if preferences.showImages:
                hide swamporcs with dissolve
            jump r309

label r36:
    "36"
    if "Antherica Berry" in inventory.keys():
        jump r283
    else:
        jump r396

label r37:
    menu:
        "37"

        "292":
            jump r292
        "220":
            jump r220

label r38:
    "38"
    jump r153

label r39:
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    39
    """
    if preferences.showImages:
        hide unicorn with dissolve
    jump r348

label r40:
    nvl clear
    if preferences.showImages:
        window hide
        show grimsladestower at truecenter, fill
        with dissolve
        pause
        window show
    """
    40
    """
    menu:
        "4":
            if preferences.showImages:
                hide grimsladestower with dissolve
            jump r4
        "50":
            if preferences.showImages:
                hide grimsladestower with dissolve
            jump r50
        "97":
            if preferences.showImages:
                hide grimsladestower with dissolve
            jump r97

label r41:
    """
    {clear}

    41
    """
    if "30" in visited:
        jump r382
    $ visited.append("30")
    if clearingsanity:
        $ checked.append("Clearing 30 Entered")
        $ notify_item("Clearing 30 Entered")
    "{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        $ stats["Stamina"].damage(2)
        "You lose 2 STAMINA points."
        if stats["Stamina"].current <= 0:
            jump gameover
        jump r270
    else:
        $ stats["Luck"].damage(1)
        jump r87

label r42:
    """
    {clear}

    42
    """
    
    menu:        
        "253":
            jump r253
        "88":
            jump r88

label r43:
    "{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r339
    else:
        $ stats["Luck"].damage(1)
        jump r313

label r44:
    """
    {clear}

    44
    """
    $ temp = roll2()
    $ diceBubble(bp, bpBubble, temp)
    $ temp = min(temp)
    $ stats["Stamina"].damage(temp)
    "You lose [temp] STAMINA points."
    if stats["Stamina"].current <= 0:
        jump gameover
    
    menu:
        "157" if not clearingsanity or "18" in clearingPasses:
            jump r157
        "398" if not clearingsanity or "4" in clearingPasses:
            jump r398

label r45:
    nvl clear
    "45"
    if temp == "south":
        jump r331
    else:
        jump r303

label r46:
    "46"
    jump r314

label r47:
    nvl clear
    "47"
    if "3" not in visited:
        $ visited.append("3")
        if clearingsanity:
            $ checked.append("Clearing 3 Entered")
            $ notify_item("Clearing 3 Entered")

    menu:
        "290" if not clearingsanity or "26" in clearingPasses:
            jump r290
        "31" if not clearingsanity or "21" in clearingPasses:
            jump r31
        "118" if not clearingsanity or "13" in clearingPasses:
            jump r118

label r48:
    """
    {clear}

    48
    """
    $ stats["Luck"].damage(1)
    "You lose 1 LUCK point."
    jump r95

label r49:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - A Hundred Pieces of Gold"])
            $ notify_item("Game Over - A Hundred Pieces of Gold")
    """
    {clear}

    49
    """
    jump gameover

label r50:
    """
    {clear}

    50
    """

    menu:
        "373":
            jump r373
        "222":
            jump r222
        "315":
            jump r315

label r51:
    """
    {clear}

    51
    """

    menu:
        "296":
            jump r296
        "5":
            jump r5

label r52:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Failing Selator's Quest"])
            $ notify_item("Game Over - Failing Selator's Quest")
    """
    {clear}

    52
    """
    jump gameover

label r53:
    """
    {clear}

    53
    """
    if "8" in visited:
        jump r329
    $ visited.append("8")
    if clearingsanity:
        $ checked.append("Clearing 8 Entered")
        $ notify_item("Clearing 8 Entered")
    if preferences.showImages:
        window hide
        show master_of_frogs at truecenter, fill
        with dissolve
        pause
        window show

    menu:
        "13":
            jump r13
        "62":
            jump r62

label r54:
    nvl clear
    "54\n{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r109
    else:
        $ stats["Luck"].damage(1)
        jump r285

label r55:
    """
    {clear}

    55
    """

    menu:
        "R390":
            $ bearOutcome = "ran"
            jump r390
        "200":
            jump r200

label r56:
    """
    {clear}

    56
    """
    if "Map to Willowbend" in inventory.keys():
        jump r158
    else:
        jump r8

label r57:
    "57"
    jump r124

label r58:
    nvl clear
    "58\n{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
    else:
        $ stats["Luck"].damage(1)
        $ stats["Stamina"].damage(1)
        "You lose 1 STAMINA point."
        if stats["Stamina"].current <= 0:
            jump gameover

    menu:
        "398" if not clearingsanity or "4" in clearingPasses:
            jump r398
        "105" if not clearingsanity or "12" in clearingPasses:
            jump r105
        "208":
            jump r208

label r59:
    if preferences.showImages:
        window hide
        show slewnwarrior at truecenter, fill
        with dissolve
        pause
        window show
    if not ap:
        """
        {clear}

        59
        """
        menu:
            "Take the pendant?"

            "Yes":
                $ inventory["Golden Magnet"] = Item("Golden Magnet")
            "No":
                pass
    else:
        $ line = get_item_string("Fallen Fighter", "'s")
        """
        {clear}
        
        59\nYou found [line]!
        """
        $ checked.append("Fallen Fighter")
            
    if preferences.showImages:
        hide slewnwarrior with dissolve
    jump r227

label r60:
    $ magic["Illusion Spell Gem"].expend()
    """
    {clear}

    60
    """
    jump r279

label r61:
    nvl clear
    "61"

    menu:
        "229":
            jump r229
        "366":
            call battle(giant) from _call_battle_3
            jump r366

label r62:
    """
    {clear}

    62
    """
    if preferences.showImages:
        hide master_of_frogs with dissolve

    menu:
        "323":
            jump r323
        "146":
            jump r146

label r63:
    """
    {clear}

    63
    """
    $ inventory.pop("Golden Magnet")

    menu:
        "15":
            jump r15
        "212":
            jump r212menu

label r64:
    """
    {clear}
    
    64\nLose 3 SKILL points and 1 STAMINA point.
    """
    python:
        if extraSkill >= 0 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            stats["Skill"].damage(max(0, 3 - extraSkill))
            extraSkill = max(extraSkill - 3, 0)
        else:
            stats["Skill"].damage(3)
        stats["Stamina"].damage(1)
        magic["Fire Spell Gem"].expend()

    if stats["Stamina"].current <= 0:
        jump gameover

    call battle(masterOfWolves, True) from _call_battle_4
    if preferences.showImages:
        hide master_of_wolves with dissolve

    if _return == "escaped":
        jump r314
    else:
        jump r154

label r65:
    """
    {clear}

    65
    """
    if "10" in visited:
        jump r343
    $ visited.append("10")
    if clearingsanity:
        $ checked.append("Clearing 10 Entered")
        $ notify_item("Clearing 10 Entered")

    menu r65menu:
        "137":
            jump r137
        "231":
            jump r231
        "387":
            jump r387
        "163":
            jump r163

label r66:
    """
    {clear}

    66
    """
    if "9" in visited:
        jump r192
    $ visited.append("9")
    if clearingsanity:
        $ checked.append("Clearing 9 Entered")
        $ notify_item("Clearing 9 Entered")
    if preferences.showImages:
        window hide
        show thief1 at truecenter, fill
        with dissolve
        pause
        window show

    menu:
        "267":
            jump r267
        "17":
            if preferences.showImages:
                hide thief1 with dissolve
            jump r17
        "147":
            jump r147

label r67:
    "67\nGain 2 STAMINA points."
    $ stats["Stamina"].restore(2)
    jump r19

label r68:
    if wordKnown:
        jump r302
    else:
        jump r215

label r69:
    "69"
    $ bearOutcome = "slain"
    jump r390

label r70:
    "70"

    menu:
        "216":
            jump r216
        "110" if "Fire Spell Gem" in magic.keys():
            jump r110
        "377":
            jump r377

label r71:
    if not ap:
        """
        {clear}

        71
        """
        $ inventory["Parrot Feathers"] = Item("Parrot Feathers")
    else:
        $ line = get_item_string("Slay the Parrot", "'s")
        """
        {clear}

        71\nYou found [line].
        """
        $ checked.append("Slay the Parrot")
    jump r149

label r72:
    "72"

    menu:
        "249":
            jump r249
        "24":
            jump r24

label r73:
    "73\n{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
    else:
        $ stats["Luck"].damage(1)
        $ stats["Stamina"].damage(2)
        "You lose 2 STAMINA points."
        if stats["Stamina"].current <= 0:
            jump gameover
    
    if not ap:
        
        menu:
            "Will you take it?"

            "Yes":
                $ inventory["Gold Chain"] = Item("Gold Chain")
            "No":
                pass

    elif "Eagle's Nest" in checked:
        "You find nothing in the nest."

    else:
        $ line = get_item_string("Eagle's Nest", "'s")
        "You found [line]."
        $ checked.append("Eagle's Nest")
    
    if preferences.showImages:
        hide eaglesnest with dissolve
    jump r202

label r74:
    nvl clear
    "74"

    menu:
        "361" if "Friendship Spell Gem" in magic.keys():
            jump r361
        "261" if "Curse Spell Gem" in magic.keys():
            jump r261
        "113" if "Fire Spell Gem" in magic.keys():
            jump r113
        "144":
            jump r144menu

label r75:
    $ magic["Fire Spell Gem"].expend()
    "75"
    $ swordTrees.damage(2)
    call battle(swordTrees) from _call_battle_5
    jump r362

label r76:
    """
    {clear}

    76\nYou restore 1 SKILL point.
    """
    $ rangerOutcome = "friendly"
    $ stats["Skill"].restore(1)
    if "Antherica Berry" in inventory.keys():
        jump r166
    else:
        jump r333

label r77:
    $ stats["Stamina"].restore(3)
    """
    {clear}

    77\nYou regain 3 STAMINA points.
    """
    jump r47

label r78:
    """
    {clear}

    78\nYou regain 2 STAMINA points.
    """
    $ stats["Stamina"].restore(2)

    menu:
        "150":
            jump r150
        "343":
            jump r343

label r79:
    nvl clear
    if preferences.showImages:
        window hide
        show brigandduel at truecenter, fill
        with dissolve
        pause
        window show
    """
    79
    """

    hide screen itemMenu with moveoutright
    show screen enemyStatScreen(brigandLeader) with moveinright

    bn "The [brigandLeader.name] attacks!"

    if dwarfPotion:
        bn "The dwarven potion you drank takes effect..."
        $ stats["Skill"].damage(1)

label r79loop:

    python:
        playerRoll = roll2()
        diceBubble(bp, bpBubble, playerRoll)
        enemyRoll = roll2()
        diceBubble(be, beBubble, enemyRoll)
        
    if not preferences.failCombat and ((stats["Skill"].current + playerRoll[0] + playerRoll[1]) > (brigandLeader.skill + enemyRoll[0] + enemyRoll[1])):

        bn "You hit the [brigandLeader.name]!"
        $ currentDamage = playerDamage

        if preferences.askLuck:
            if renpy.confirm("Do you want to test your luck?"):
                if stats["Luck"].test():
                    $ currentDamage += 2
                else:
                    $ currentDamage -= 1

                $ stats["Luck"].damage(1)
            
        $ brigandLeader.damage(currentDamage)
        bn "You dealt [currentDamage] damage!"
        $ temp = True 
        
    elif preferences.failCombat or ((stats["Skill"].current + playerRoll[0] + playerRoll[1]) < (brigandLeader.skill + enemyRoll[0] + enemyRoll[1])):

        bn "The [brigandLeader.name] hit you!"
        $ currentDamage = brigandLeader.strength

        if preferences.askLuck:
            if renpy.confirm("Do you want to test your luck?"):

                if stats["Luck"].test():
                    $ currentDamage -= 1
                else:
                    $ currentDamage += 1
                    
                $ stats["Luck"].damage(1)
            
        $ stats["Stamina"].damage(currentDamage)
        bn "You took [currentDamage] damage!"
        $ temp = False
        
    else:

        bn "You and the [brigandLeader.name] were tied! No one takes any damage this round!"
        jump r79loop
    
    if stats["Stamina"].current <= 0:
        jump gameover
    
    hide screen enemyStatScreen with moveoutright
    show screen itemMenu with moveinright

    if dwarfPotion:
        bn "The effects of the dwarven potion end!"
        $ stats["Skill"].restore(1)
        $ dwarfPotion = False

    if preferences.showImages:
        hide brigandduel with dissolve

    if temp:
        jump r360
    else:
        jump r128

label r80:
    menu:
        "80"

        "307" if "Fire Spell Gem" in magic.keys():
            jump r307
        "196" if "Withering Spell Gem" in magic.keys():
            jump r196
        "204":
            jump r204menu

label r81:
    """
    {clear}

    81
    """
    jump r187

label r82:
    "82"

    call battle(poolBeast, True) from _call_battle_6

    if _return == "escaped":
        if preferences.showImages:
            hide poolbeast with dissolve
        jump r330
    else:
        jump r308

label r83:
    "83\n{i}Test your Luck.{/i}"

    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r35
    else:
        $ stats["Luck"].damage(1)
        jump r357

label r84:
    """
    {clear}

    84
    """
    if preferences.showImages:
        hide master_of_gardens with dissolve
    jump r363

label r85:
    "85"
    $ temp = "fled"
    jump r153

label r86:
    "86\n{i}Test your Luck.{/i}"

    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r189
    else:
        $ stats["Luck"].damage(1)
        jump r348

label r87:
    """
    {clear}

    87\nYou lose 2 SKILL points and reduce your Initial SKILL level by 2.
    """
    python:
        if extraSkill >= 2 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 2
        elif extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 1
            stats["Skill"].damage(1)
        else:
            stats["Skill"].damage(2)
    $ stats["Skill"].increase(-2)
    jump r270

label r88:
    "88"

    menu:
        "121":
            jump r121
        "331" if not clearingsanity or "16" in clearingPasses:
            jump r331

label r89:
    if preferences.showImages:
        hide foulbrood_river with dissolve
    $ magic["Ice Spell Gem"].expend()
    "89"

    menu:
        "325":
            jump r325
        "295":
            jump r295menu

label r90:
    """
    {clear}

    90
    """
    if "34" not in visited:
        $ visited.append("34")
        if clearingsanity:
            $ checked.append("Clearing 34 Entered")
            $ notify_item("Clearing 34 Entered")
    
    menu:
        "370" if "Ice Spell Gem" in magic.keys():
            jump r370
        "254" if "Withering Spell Gem" in magic.keys():
            jump r254
        "44":
            jump r44

label r91:
    "91\n{i}Test your Stamina.{/i}"
    if stats["Stamina"].test():
        pass
    else:
        "You lose 1 point of SKILL."
        if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            $ extraSkill -= 1
        else:
            $ stats["Skill"].damage(1)

    menu:
        "398" if not clearingsanity or "4" in clearingPasses:
            jump r398
        "105" if not clearingsanity or "12" in clearingPasses:
            jump r105
        "208":
            jump r208

label r92:
    """
    {clear}

    92
    """
    if "11" in visited:
        jump r108
    $ visited.append("11")
    if clearingsanity:
        $ checked.append("Clearing 11 Entered")
        $ notify_item("Clearing 11 Entered")
    if preferences.showImages:
        window hide
        show twowolves at truecenter, fill
        with dissolve
        pause
        window show
    
    if "Wolf Amulet" in inventory.keys():
        jump r344
    else:
        jump r68

label r93:
    $ magic["Curse Spell Gem"].expend()
    """
    {clear}

    93
    """
    $ temp = roll()
    $ dieBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover
    
    $ masterOfWolves.skill -= 2
    $ masterOfWolves.damage(2)
    jump r120

label r94:
    """
    {clear}

    94\nYou lose 2 STAMINA points.
    """
    $ stats["Stamina"].damage(2)
    if stats["Stamina"].current <= 0:
        jump gameover
    
    menu:
        "295" if not clearingsanity or "33" in clearingPasses:
            jump r295
        "320" if not clearingsanity or "29" in clearingPasses:
            $ temp = "north"
            jump r320

label r95:
    if preferences.showImages:
        hide fenmargetavern with dissolve
    """
    {clear}
    
    95
    """

    # This is the last point before the opening route splits and we need to be sure we have scouts so we confirm that here
    if ap and not scouts:
        call file_error from _call_file_error

    menu:
        "240":
            jump r240
        "122":
            jump r122

label r96:
    "96"
    jump r371

label r97:
    nvl clear
    if preferences.showImages:
        window hide
        show goblin_statue at truecenter, fill
        with dissolve
        pause
        window show
    "97"

    menu:
        "315":
            if preferences.showImages:
                hide goblin_statue with dissolve
            jump r315
        "284":
            jump r284

label r98:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Itsy Bitsy Spider"])
            $ notify_item("Game Over - Itsy Bitsy Spider")
    """
    {clear}

    98
    """
    jump gameover

label r99:
    """
    {clear}

    99
    """
    jump r242

label r100:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Failing Poomchukker's Quest"])
            $ notify_item("Game Over - Failing Poomchukker's Quest")
    """
    {clear}

    100
    """
    jump gameover

label r101:
    "101"

    menu:
        "350" if not clearingsanity or "16" in clearingPasses:
            jump r350
        "118" if not clearingsanity or "13" in clearingPasses:
            jump r118
        "Ride the ice flow\nback up the river" if canUseIceFlow:
            "You recreate your ice flow with the lingering traces of magic and paddle your way back upstream."
            jump r295

label r102:
    "102\nYou lose 1 point of STAMINA."
    $ stats["Stamina"].damage(1)
    if stats["Stamina"].current <= 0:
        jump gameover
    jump r11menu

label r103:
    """
    {clear}
    
    103
    """
    if preferences.showImages:
        hide giant with dissolve
    jump r161

label r104:
    """
    {clear}

    104
    """
    if preferences.showImages:
        hide master_of_frogs with dissolve
    jump r352

label r105:
    """
    {clear}

    105
    """
    if "12" in visited:
        jump r330
    $ visited.append("12")
    if clearingsanity:
        $ checked.append("Clearing 12 Entered")
        $ notify_item("Clearing 12 Entered")
    if preferences.showImages:
        window hide
        show clearing at truecenter, fill
        with dissolve
        pause
        window show

    menu:
        "21":
            jump r21
        "55":
            jump r55
        "390":
            jump r390

label r106:
    """
    {clear}

    106\nYou lose 2 STAMINA points.
    """
    $ stats["Stamina"].damage(2)
    if stats["Stamina"].current <= 0:
        jump gameover

    menu:
        "267":
            jump r267
        "179":
            if preferences.showImages:
                hide thief1 with dissolve
            jump r179

label r107:
    $ magic["Curse Spell Gem"].expend()
    """
    {clear}
    
    107
    """
    $ temp = roll()
    $ diceBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover
    jump r19

label r108:
    """
    {clear}

    108
    """
    jump r342

label r109:
    "109"

    menu:
        "349":
            jump r349
        "124":
            jump r124
        "256":
            jump r256

label r110:
    $ magic["Fire Spell Gem"].expend()
    """
    {clear}

    110
    """
    if preferences.showImages:
        hide swampscorpions with dissolve
    jump r319

label r111:
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    111
    """
    jump r184

label r112:
    "112"

    menu:
        "73":
            jump r73
        "202":
            if preferences.showImages:
                hide eaglesnest with dissolve
            jump r202

label r113:
    $ magic["Fire Spell Gem"].expend()
    """
    {clear}

    113\nYou lose 3 STAMINA points.
    """
    if preferences.showImages:
        hide master_of_spiders with dissolve
    $ stats["Stamina"].damage(3)
    if stats["Stamina"].current <= 0:
        jump gameover
    jump r165

label r114:
    $ magic["Growth Spell Gem"].expend()
    """
    {clear}

    114
    """
    $ swordTrees.stamina = 24
    jump r28

label r115:
    """
    {clear}

    115
    """
    if preferences.showImages:
        hide ranger with dissolve
    jump r234

label r116:
    """
    {clear}

    116
    """
    jump r343

label r117:
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    117
    """
    if preferences.showImages:
        hide master_of_gardens with dissolve
    jump r363

label r118:
    """
    {clear}

    118
    """
    if "13" in visited:
        jump r303
    $ visited.append("13")
    if clearingsanity:
        $ checked.append("Clearing 13 Entered")
        $ notify_item("Clearing 13 Entered")
    if preferences.showImages:
        window hide
        show swampscorpions at truecenter, fill
        with dissolve
        pause
        window show
    "{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r70
    else:
        $ stats["Luck"].damage(1)
        jump r182

label r119:
    menu:
        "39" if "Friendship Spell Gem" in magic.keys():
            jump r39
        "293" if "Fear Spell Gem" in magic.keys():
            jump r293
        "381" if "Bless Spell Gem" in magic.keys():
            jump r381
        "337" if "Fire Spell Gem" in magic.keys():
            jump r337
        "320":
            jump r320menu

label r120:
    "120"
    call battle(petWolf1, True) from _call_battle_7
    if _return == "escaped":
        jump r314
    call battle(petWolf2, True) from _call_battle_8
    if _return == "escaped":
        jump r314
    call battle(masterOfWolves, True) from _call_battle_9
    if preferences.showImages:
        hide master_of_wolves with dissolve
    if _return == "escaped":
        jump r314
    else:
        jump r154

label r121:
    nvl clear
    "121"

    menu:
        "170" if not clearingsanity or "19" in clearingPasses:
            jump r170
        "14" if not clearingsanity or "32" in clearingPasses:
            jump r14
        "275" if not clearingsanity or "7" in clearingPasses:
            jump r275
        "218" if not clearingsanity or "15" in clearingPasses:
            jump r218

label r122:
    """
    {clear}

    122
    """

    menu:
        "240":
            jump r240
        "296":
            jump r296

label r123:
    """
    {clear}

    123
    """

    menu:
        "225":
            jump r225
        "315":
            jump r315

label r124:
    """
    {clear}

    124
    """
    call battle(grimslade) from _call_battle_10
    jump r340

label r125:
    if not ap:
        """
        {clear}

        125
        """
        $ inventory["Dire Beast Claws"] = Item("Dire Beast Claws")
    else:
        $ line = get_item_string("Slay the Dire Beast", "'s")
        """
        {clear}

        125\nYou find [line].
        """
        $ checked.append("Slay the Dire Beast")
    jump r279

label r126:
    $ magic["Ice Spell Gem"].expend()
    """
    126
    """
    jump r145menu

label r127:
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    127
    """
    jump r104

label r128:
    """
    {clear}

    128
    """
    if inventory == {}:
        jump r180
    python:
        while True:
            temp = renpy.input(prompt="Enter the item you will give him:")
            if temp in inventory.keys():
                break
            narrator(f"{temp} is not in your inventory.")
        
        inventory[temp].expend()
    nvl clear
    $ brigandOutcome = "friendly"
    jump r19

label r129:
    if bearOutcome == "slain":
        jump r268
    else:
        jump r181

label r130:
    menu:
        "130"

        "260" if "Curse Spell Gem" in magic.keys():
            jump r260
        "111" if "Friendship Spell Gem" in magic.keys():
            jump r111
        "201" if "Fear Spell Gem" in magic.keys():
            jump r201
        "288":
            jump r288menu

label r131:
    """
    {clear}

    131
    """
    if preferences.showImages:
        window hide
        show mistress_of_birds at truecenter, fill
        with dissolve
        pause
        window show
    
    if quest == "Poomchukker":
        jump r23
    elif quest == "Selator":
        jump r164
    else:
        jump r288

label r132:
    "132"

    menu:
        "73":
            jump r73
        "202":
            if preferences.showImages:
                hide eaglesnest with dissolve
            jump r202

label r133:
    "133"
    jump r234

label r134:
    """
    {clear}

    134
    """
    call battle(crabGrass, True) from _call_battle_11
    if preferences.showImages:
        hide crab_grass with dissolve
    if _return == "escaped":
        jump r187
    else:
        jump r81

label r135:
    """
    {clear}

    135
    """
    jump r309

label r136:
    $ magic["Fire Spell Gem"].expend()
    "136"
    jump r379

label r137:
    if slime.stamina <= 0:
        jump r153
    else:
        jump r336

label r138:
    """
    {clear}

    138
    """
    if "35" not in visited:
        $ visited.append("35")
        if clearingsanity:
            $ checked.append("Clearing 35 Entered")
            $ notify_item("Clearing 35 Entered")

    menu:
        "101":
            jump r101
        "45":
            jump r45

label r139:
    """
    {clear}

    139
    """

    menu:
        "335" if not wizardsanity or "Selator" in wizards:
            jump r335
        "27" if not wizardsanity or "Poomchukker" in wizards:
            jump r27
    "Unfortunately, you don't know of any other wizards to see."
    jump gameover # If you have no options, just end the game

label r140:
    if not ap:
        """
        {clear}

        140
        """
        python:
            inventory["Great Magic Sword"] = Item("Great Magic Sword")
            temp = stats["Skill"].initial - stats["Skill"].current
            extraSkill += max(0, 2 - temp)
            stats["Skill"].restore(min(2, temp))
    else:
        $ line = get_item_string("Slay Grimslade", "'s")
        """
        {clear}

        140\nYou find [line].
        """
        $ checked.append("Slay Grimslade")

    menu:
        "375":
            jump r375
        "335" if not wizardsanity or "Selator" in wizards:
            jump r335
        "27" if not wizardsanity or "Poomchukker" in wizards:
            jump r27

label r141:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Failing Poomchukker's Quest"])
            $ notify_item("Game Over - Failing Poomchukker's Quest")
    """
    {clear}

    141
    """
    jump gameover

label r142:
    "142"
    jump r227

label r143:
    "143"

    menu:
        "374":
            jump r374
        "176":
            jump r176

label r144:
    """
    {clear}
    
    144
    """
    if "17" in visited:
        jump r345
    $ visited.append("17")
    if clearingsanity:
        $ checked.append("Clearing 17 Entered")
        $ notify_item("Clearing 17 Entered")
    if preferences.showImages:
        window hide
        show master_of_spiders at truecenter, fill
        with dissolve
        pause
        window show

    menu r144menu:
        "74":
            jump r74
        "26":
            jump r26
        "332":
            jump r332

label r145:
    "145"

    menu r145menu:
        "252" if "Curse Spell Gem" in magic.keys():
            jump r252
        "328" if "Friendship Spell Gem" in magic.keys():
            jump r328
        "211" if "Fire Spell Gem" in magic.keys():
            jump r211
        "126" if "Ice Spell Gem" in magic.keys():
            jump r126
        "275":
            jump r275menu

label r146:
    "146"
    call multibattle([giantFrog1, giantFrog2]) from _call_multibattle
    jump r230

label r147:
    """
    {clear}

    147\n{i}Test your Luck.{/i}
    """
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r213
    else:
        $ stats["Luck"].damage(1)
        jump r106

label r148:
    $ magic["Illusion Spell Gem"].expend()
    """
    {clear}

    148
    """
    jump r19

label r149:
    """
    149
    """
    jump r217

label r150:
    """
    {clear}

    150
    """
    $ temp = 0

    menu r150menu1:
        "What will you offer for trade?"

        "Violet Jewel" if "Violet Jewel" in inventory.keys():
            $ inventory["Violet Jewel"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Gold Chain" if "Gold Chain" in inventory.keys():
            $ inventory["Gold Chain"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Golden Magnet" if "Golden Magnet" in inventory.keys():
            $ inventory["Golden Magnet"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Horn of a Unicorn" if "Horn of a Unicorn" in inventory.keys():
            $ inventory["Horn of a Unicorn"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Wolf Amulet" if "Wolf Amulet" in inventory.keys():
            $ inventory["Wolf Amulet"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Bird Amulet" if "False Bird Amulet" in inventory.keys():
            $ inventory["False Bird Amulet"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Frog Amulet" if "Frog Amulet" in inventory.keys():
            $ inventory["Frog Amulet"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Flower Amulet" if "Flower Amulet" in inventory.keys():
            $ inventory["Flower Amulet"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Spider Amulet" if "Spider Amulet" in inventory.keys():
            $ inventory["Spider Amulet"].expend()
            $ temp += 1
            if temp < 3:
                jump r150menu1
        "Nothing else":
            pass

    if temp:
        if spellsanity:
            call halicarShop(temp) from _call_halicarShop
        else:
            call pickMagic(temp) from _call_pickMagic
    nvl clear
    jump r343

label r151:
    "151\nLose 1 SKILL point."
    if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
        $ extraSkill -= 1
    else:
        $ stats["Skill"].damage(1)
    
    menu:
        "281":
            jump r281
        "399":
            jump r399
        "309":
            if preferences.showImages:
                hide swamporcs with dissolve
            jump r309
    
label r152:
    menu:
        "152"

        "136" if "Fire Spell Gem" in magic.keys():
            jump r136
        "264" if "Withering Spell Gem" in magic.keys():
            jump r264
        "347" if "Illusion Spell Gem" in magic.keys():
            jump r347
        "117" if "Friendship Spell Gem" in magic.keys():
            jump r117
        "334":
            jump r334

label r153:
    "153"

    if temp == "fled":
        jump r218

    menu:
        "218" if not clearingsanity or "15" in clearingPasses:
            jump r218
        "65" if not clearingsanity or "10" in clearingPasses:
            jump r65

label r154:
    "154"
    $ inventory["Wolf Amulet"] = Item("Wolf Amulet")
    jump r46

label r155:
    """
    {clear}

    155\nRaise your Initial LUCK score by 2.
    """
    $ stats["Luck"].increase(2)
    $ stats["Luck"].restore(2)
    jump r335

label r156:
    if preferences.showImages:
        hide goblin_statue with dissolve
    """
    {clear}

    156
    """
    $ temp = stats["Stamina"].initial - stats["Stamina"].current

    if temp == 0:
        jump r241
    elif temp <= 5:
        jump r193
    else:
        jump r326

label r157:
    """
    {clear}

    157
    """
    if "18" in visited:
        jump r279
    $ visited.append("18")
    if clearingsanity:
        $ checked.append("Clearing 18 Entered")
        $ notify_item("Clearing 18 Entered")
    if preferences.showImages:
        window hide
        show sword_trees at truecenter, fill
        with dissolve
        pause
        window show

    menu:
        "28":
            jump r28
        "203":
            jump r203

label r158:
    if ap:
        hide screen progression_watcher
        if goal in {"any", "poomchukker"}:
            call send_victory from _call_send_victory_1
        if goal == "all":
            $ check_goal()
            if "selator" in goals_complete and "grimslade" in goals_complete:
                call send_victory from _call_send_victory_2
            python:
                if not renpy.loadable("v_poomchukker", directory=CONNECTIONS_PATH):
                    with open(os.path.join(CONNECTIONS_PATH, "v_poomchukker"), 'w') as f:
                        f.close()
    """
    {clear}

    158
    """
    jump gameComplete

label r159:
    """
    {clear}

    159
    """
    if quest == "Selator":
        jump r6
    elif quest == "Grimslade":
        jump r226
    elif quest == "Poomchukker":
        jump r56

label r160:
    $ magic["Friendship Spell Gem"].expend()
    """
    160
    """
    jump r176

label r161:
    "161"

    menu:
        "92" if not clearingsanity or "11" in clearingPasses:
            jump r92
        "41" if not clearingsanity or "30" in clearingPasses:
            $ temp = "south"
            jump r41
        "121":
            jump r121

label r162:
    """
    {clear}

    162
    """

    menu:
        "352":
            if preferences.showImages:
                hide master_of_frogs with dissolve
            jump r352
        "245" if "Illusion Spell Gem" in magic:
            jump r245
        "62":
            jump r62

label r163:
    """
    {clear}

    163
    """

    menu:
        "79":
            jump r79
        "353":
            jump r353

label r164:
    if not ap:
        """
        {clear}

        164
        """
        $ inventory["Magic Potion"] = Item("Magic Potion", 1, True, True)
    else:
        $ line = get_item_string("Gift from the Mistress of Birds", "'s")
        """
        {clear}

        164\nYou find [line].
        """
        $ checked.append("Gift from the Mistress of Birds")
        if not clearingsanity or "16" in clearingPasses:
            pass
        else:
            "You worry about losing your way and instead choose to return back the way you came."
            if preferences.showImages:
                hide mistress_of_birds with dissolve
            jump r217
        if clearingsanity:
            $ canUseEagle = True
    jump r248

label r165:
    "165"

    menu:
        "388" if not clearingsanity or "24" in clearingPasses:
            jump r388
        "105" if not clearingsanity or "12" in clearingPasses:
            jump r105

label r166:
    """
    {clear}

    166
    """
    if preferences.showImages:
        hide ranger with dissolve
    jump r234

label r167:
    "167"

    menu:
        "322" if "Withering Spell Gem" in magic.keys():
            jump r322
        "310" if "Fire Spell Gem" in magic.keys():
            jump r310
        "134":
            jump r134

label r168:
    nvl clear
    "168"
    if poolBeast.stamina <= 0:
        jump r330
    jump r209menu

label r169:
    $ magic["Illusion Spell Gem"].expend()
    """
    {clear}
    
    169
    """
    jump r281

label r170:
    """
    {clear}

    170
    """
    if "19" in visited:
        jump r363
    $ visited.append("19")
    if clearingsanity:
        $ checked.append("Clearing 19 Entered")
        $ notify_item("Clearing 19 Entered")
    if preferences.showImages:
        window hide
        show ranger at truecenter, fill
        with dissolve
        pause
        window show
    if quest == "Selator":
        jump r76
    elif quest == "Grimslade":
        jump r29
    elif quest == "Poomchukker":
        jump r262

label r171:
    "171"

    call battle(slime, True) from _call_battle_12

    if _return == "escaped":
        $ temp = "fled"
        jump r153
    else:
        jump r38

label r172:
    if not ap:
        """
        172
        """
        $ wordKnown = True
    else:
        $ line = get_item_string("Gift from the Master of Wolves", "'s")
        """
        172\nYou find [line].
        """
        $ checked.append("Gift from the Master of Wolves")

    if preferences.showImages:
        hide master_of_wolves with dissolve
    jump r314

label r173:
    """
    {clear}

    173
    """
    if spellsanity:
        call poomchukkerShop(5) from _call_poomchukkerShop
    else:
        call pickMagic(5) from _call_pickMagic_1
    if preferences.showImages:
        hide poomchukker with dissolve
    $ quest = "Poomchukker"
    jump r9

label r174:
    "174"

    menu:
        "225":
            jump r225
        "193":
            jump r193

label r175:
    if ap:
        hide screen progression_watcher
        if goal in {"any", "selator"}:
            call send_victory from _call_send_victory_3
        if goal == "all":
            $ check_goal()
            if "poomchukker" in goals_complete and "grimslade" in goals_complete:
                call send_victory from _call_send_victory_4
            python:
                if not renpy.loadable("v_selator", directory=CONNECTIONS_PATH):
                    with open(os.path.join(CONNECTIONS_PATH, "v_selator"), 'w') as f:
                        f.close()
    """
    {clear}

    175
    """
    jump gameComplete

label r176:
    """
    {clear}

    176
    """
    call battle(direBeast) from _call_battle_13
    jump r125

label r177:
    "177"
    if preferences.showImages:
        hide giant with dissolve
    jump r161

label r178:
    "178\nYou lose 1 LUCK point."
    $ stats["Luck"].damage(1)
    jump r352

label r179:
    "179"

    menu:
        "183" if not clearingsanity or "20" in clearingPasses:
            jump r183
        "10" if not clearingsanity or "5" in clearingPasses:
            jump r10
        "118" if not clearingsanity or "13" in clearingPasses:
            jump r118

label r180:
    """
    {clear}

    180
    """
    jump r214

label r181:
    "181"
    if bear.stamina < 8:
        $ bear.stamina += 1
    jump r200

label r182:
    "182"
    $ temp = roll()
    $ dieBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover
    if preferences.showImages:
        hide swampscorpions with dissolve
    jump r319

label r183:
    """
    {clear}

    183
    """
    if preferences.showImages:
        if not renpy.showing("foulbrood_river"):
            window hide
            show foulbrood_river at truecenter, fill
            with dissolve
            pause
            window show
    if "20" not in visited:
        $ visited.append("20")
        if clearingsanity:
            $ checked.append("Clearing 20 Entered")
            $ notify_item("Clearing 20 Entered")

    menu:
        "66" if not clearingsanity or "9" in clearingPasses:
            if preferences.showImages:
                hide foulbrood_river with dissolve
            jump r66
        "295" if not clearingsanity or "33" in clearingPasses:
            jump r295
        "30":
            jump r30
        "321":
            jump r321

label r184:
    """
    {clear}

    184
    """
    if preferences.showImages:
        hide mistress_of_birds with dissolve
    $ inventory["False Bird Amulet"] = Item("False Bird Amulet")
    jump r217

label r185:
    """
    {clear}

    185
    """
    $ rangerOutcome = "friendly"
    if preferences.showImages:
        hide ranger with dissolve
    jump r234

label r186:
    """
    {clear}

    186
    """
    jump r343

label r187:
    "187"

    menu:
        "144" if not clearingsanity or "17" in clearingPasses:
            $ temp = "north"
            jump r144
        "290" if not clearingsanity or "26" in clearingPasses:
            jump r290
        "10" if not clearingsanity or "5" in clearingPasses:
            jump r10

label r188:
    $ magic["Fire Spell Gem"].expend()
    "188"

    menu:
        "400":
            jump r400
        "336":
            jump r336menu

label r189:
    if not spellsanity:
        """
        {clear}

        189
        """
        python:
            if "Friendship Spell Gem" in magic.keys():
                magic["Friendship Spell Gem"].add()
            else:
                magic["Friendship Spell Gem"] = Item("Friendship Spell Gem")
            if "Luck Spell Gem" in magic.keys():
                magic["Luck Spell Gem"].add()
            else:
                magic["Luck Spell Gem"] = Item("Luck Spell Gem", 1, True, True)
    else:
        $ line = get_item_string("Unicorn Clearing Spell Gem 1", "'s")
        $ line2 = get_item_string("Unicorn Clearing Spell Gem 2", "'s")
        """
        {clear}

        189\nYou find [line] and [line2].
        """
        $ checked.extend(["Unicorn Clearing Spell Gem 1", "Unicorn Clearing Spell Gem 2"])
    jump r348

label r190:
    "190 {i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
    else:
        $ stats["Luck"].damage(1)
        "You lose 2 STAMINA points."
        $ stats["Stamina"].damage(2)
        if stats["Stamina"].current <= 0:
            jump gameover
    jump r270

label r191:
    menu:
        "191"

        "224" if "Fear Spell Gem" in magic.keys():
            jump r224
        "294" if "Friendship Spell Gem" in magic.keys():
            jump r294
        "93" if "Curse Spell Gem" in magic.keys():
            jump r93
        "64" if "Fire Spell Gem" in magic.keys():
            jump r64
        "398":
            jump r398menu

label r192:
    nvl clear
    "192"
    if thief.stamina <= 0:
        jump r179
    else:
        jump r267

label r193:
    """
    {clear}

    193
    """
    python:
        for s in stats:
            stats[s].restore(100)
    jump r206

label r194:
    "194"

    menu:
        "99":
            jump r99
        "207":
            jump r207

label r195:
    """
    {clear}

    195
    """
    if "1" not in visited:
        $ visited.append("1")
        if clearingsanity:
            $ checked.append("Clearing 1 Entered")
            $ notify_item("Clearing 1 Entered")

    menu:
        "58":
            jump r58
        "91":
            jump r91

label r196:
    $ magic["Withering Spell Gem"].expend()
    $ fearFlowersDefeated = True
    "196"
    if preferences.showImages:
        window hide
        show fearflowers at truecenter, fill
        with dissolve
        pause
        window show
        hide fearflowers with dissolve
    jump r367

label r197:
    """
    {clear}

    197\nYou lose 2 LUCK points.
    """
    $ stats["Luck"].damage(2)
    jump r161

label r198:
    """
    {clear}

    198
    """
    if preferences.showImages:
        hide master_of_frogs with dissolve
    jump r146

label r199:
    "199"
    jump r19

label r200:
    "200"
    call battle(bear, True) from _call_battle_14

    if _return == "escaped":
        $ bearOutcome = "ran"
        jump r390
    else:
        jump r69

label r201:
    $ magic["Fear Spell Gem"].expend()
    """
    201
    """
    if preferences.showImages:
        hide mistress_of_birds with dissolve
    jump r217

label r202:
    "202"

    if canUseEagle:
        "You think that you can get the Eagle to bring you back to the Mistress of Birds' clearing."

        menu:
            "Will you try?"

            "Yes":
                if preferences.showImages:
                    show gianteagle at truecenter, fill
                    with dissolve
                "The Eagle flies you back. {i}You are in Clearing 14.{/i}"
                nvl clear
                if preferences.showImages:
                    hide gianteagle with dissolve
                    jump r149
            "No":
                pass

    menu:
        "138" if not clearingsanity or "35" in clearingPasses:
            $ temp = "south"
            jump r138
        "41" if not clearingsanity or "30" in clearingPasses:
            $ temp = "east"
            jump r41
        "14" if not clearingsanity or "32" in clearingPasses:
            jump r14

label r203:
    "203"

    menu:
        "75" if "Fire Spell Gem" in magic.keys():
            jump r75
        "393" if "Withering Spell Gem" in magic.keys():
            jump r393
        "114" if "Growth Spell Gem" in magic.keys():
            jump r114
        "28":
            jump r28

label r204:
    """
    {clear}

    204
    """
    if "23" in visited:
        jump r250
    $ visited.append("23")
    if clearingsanity:
        $ checked.append("Clearing 23 Entered")
        $ notify_item("Clearing 23 Entered")
    """
    You lose 1 SKILL point.
    """
    if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
        $ extraSkill -= 1
    else:
        $ stats["Skill"].damage(1)

    menu r204menu:
        "269":
            jump r269
        "32":
            jump r32
        "80":
            jump r80

label r205:
    """
    {clear}

    205
    """

    menu:
        "335" if not wizardsanity or "Selator" in wizards:
            jump r335
        "255" if not wizardsanity or "Grimslade" in wizards:
            jump r255
        "27" if not wizardsanity or "Poomchukker" in wizards:
            jump r27

label r206:
    """
    {clear}

    206
    """
    if spellsanity:
        call grimsladeShop(6) from _call_grimsladeShop
    else:
        call pickMagic(6, 'evil') from _call_pickMagic_2
    nvl clear
    $ quest = "Grimslade"
    jump r9

label r207:
    """
    {clear}

    207
    """
    jump r358

label r208:
    """
    {clear}

    208
    """

    menu:
        "195":
            jump r195
        "159":
            jump r159

label r209:
    """
    {clear}

    209
    """
    if "25" in visited:
        jump r168
    $ visited.append("25")
    if clearingsanity:
        $ checked.append("Clearing 25 Entered")
        $ notify_item("Clearing 25 Entered")
    if preferences.showImages:
        window hide
        show poolbeast at truecenter, fill
        with dissolve
        pause
        window show

    menu r209menu:
        "397":
            if preferences.showImages:
                hide poolbeast with dissolve
            jump r397
        "82":
            jump r82
        "34l":
            jump r34

label r210:
    "210"
    if direBeast.stamina <= 0:
        jump r243
    else:
        jump r143

label r211:
    $ magic["Fire Spell Gem"].expend()
    """
    {clear}

    211
    """
    $ giant.skill = 6
    call battle(giant) from _call_battle_15
    jump r366

label r212:
    """
    {clear}

    212
    """
    menu r212menu:        
        "62":
            jump r62
        "258":
            jump r258
        "15":
            jump r15

label r213:
    """
    213
    """
    jump r267

label r214:
    $ brigandOutcome = "friendly"
    """
    {clear}

    214
    """
    jump r19

label r215:
    """
    {clear}

    215
    """
    call battle(wolf) from _call_battle_16
    jump r247

label r216:
    """
    {clear}

    216
    """
    $ temp = roll()
    $ dieBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover
    if preferences.showImages:
        hide swampscorpions with dissolve
    jump r319

label r217:
    "217"
    if canUseEagle:
        "You think that you can get the Eagle to bring you back to its clearing."

        menu:
            "Will you try?"

            "Yes":
                if preferences.showImages:
                    show gianteagle at truecenter, fill
                    with dissolve
                "The Eagle flies you back. {i}You are in Clearing 16.{/i}"
                nvl clear
                if preferences.showImages:
                    hide gianteagle with dissolve
                jump r331
            "No":
                pass
    jump r250

label r218:
    """
    {clear}

    218
    """
    if "15" not in visited:
        $ visited.append("15")
        if clearingsanity:
            $ checked.append("Clearing 15 Entered")
            $ notify_item("Clearing 15 Entered")

    menu:
        "72":
            jump r72
        "336" if not clearingsanity or "28" in clearingPasses:
            jump r336
        "121":
            jump r121

label r219:
    if not ap:
        """
        {clear}

        219
        """
        python:
            inventory["Ranger's Helmet"] = Item("Ranger's Helmet")
            temp = stats["Skill"].initial - stats["Skill"].current
            extraSkill += max(0, 1 - temp)
            stats["Skill"].restore(min(1, temp))
    else:
        $ line = get_item_string("Slay the Ranger", "'s")
        """
        {clear}

        219\nYou find [line].
        """
        $ checked.append("Slay the Ranger")
    jump r234

label r220:
    "220"

    menu:
        "292":
            jump r292
        "334":
            jump r334

label r221:
    """
    {clear}

    221
    """
    call battle(unicorn, True, 0, 2) from _call_battle_17
    if preferences.showImages:
        hide unicorn with dissolve
    if _return == "escaped":
        jump r348
    else:
        jump r277

label r222:
    if preferences.showImages:
        window hide
        show spikedemon at truecenter, fill
        with dissolve
        pause
        window show
    """
    {clear}

    222
    """
    call battle(demon) from _call_battle_18
    if preferences.showImages:
        hide spikedemon with dissolve
    jump r174

label r223:
    "223"
    if temp == "south":
        jump r275
    elif temp == "east":
        jump r331

label r224:
    $ magic["Fear Spell Gem"].expend()
    if preferences.showImages:
        hide master_of_wolves with dissolve
    "224"
    call multibattle([petWolf1, petWolf2], True) from _call_multibattle_1
    if _return == "escaped":
        jump r314
    else:
        jump r46

label r225:
    """
    {clear}

    225
    """
    call battle(grimslade2) from _call_battle_19
    jump r140

label r226:
    """
    {clear}

    226
    """
    python:
        temp = 0
        for k in inventory.keys():
            if "Amulet" in k:
                temp += 1
    
    if required_amulets > -1:
        if temp >= required_amulets:
            $ has_required_amulets = True
            jump r194
        else:
            jump r54

    if temp <= 0:
        jump r54
    elif 1 <= temp <= 2:
        jump r7
    elif temp >= 3:
        jump r194

label r227:
    nvl clear
    "227"

    menu:
        "66" if not clearingsanity or "9" in clearingPasses:
            jump r66
        "388" if not clearingsanity or "24" in clearingPasses:
            jump r388
        "29" if not clearingsanity or "29" in clearingPasses:
            $ temp = "east"
            jump r320

label r228:
    $ magic["Growth Spell Gem"].expend()
    $ inventory["Sword Tree Seeds"].expend()
    """
    {clear}

    228
    """
    jump r279

label r229:
    """
    {clear}
    
    229
    """
    if "Red Cloak" in inventory.keys():
        jump r286
    else:
        jump r177

label r230:
    """
    {clear}

    230
    """
    jump r352

label r231:
    "231\n{i}Test your luck.{/i}"

    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r18
    else:
        $ stats["Luck"].damage(1)
        jump r259

label r232:
    "232"
    if quest == "Selator":
        jump r389
    else:
        "342"
        jump r342

label r233:
    "233"

    menu:
        "392":
            jump r392
        "25":
            jump r25

label r234:
    "234"

    menu:
        "305" if not clearingsanity or "27" in clearingPasses:
            jump r305
        "121":
            jump r121

label r235:
    if preferences.showImages:
        window hide
        show brigand_leader at truecenter, fill
        with dissolve
        pause
        window show
    """
    {clear}

    235
    """
    call multibattle([brigandLeader, brigand2, brigand3]) from _call_multibattle_2
    if preferences.showImages:
        hide brigand_leader with dissolve
    jump r19

label r236:
    """
    {clear}

    236\nYou lose 2 SKILL points.
    """
    python:
        if extraSkill >= 2 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 2
        elif extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 1
            stats["Skill"].damage(1)
        else:
            stats["Skill"].damage(2)
    jump r116

label r237:
    $ magic["Withering Spell Gem"].expend()
    "237"
    jump r82

label r238:
    "238"
    jump r363

label r239:
    "239"
    jump r314

label r240:
    """
    {clear}

    240
    """

    menu:
        "205":
            jump r205
        "155" if not wizardsanity or "Selator" in wizards:
            jump r155

label r241:
    if not ap:
        """
        {clear}

        241
        """
        $ stats["Luck"].restore(100)
        python:
            inventory["Magic Sword"] = Item("Magic Sword")
            temp = stats["Skill"].initial - stats["Skill"].current
            extraSkill += max(0, 2 - temp)
            stats["Skill"].restore(min(2, temp))
    else:
        $ line = get_item_string("Gift from Grimslade", "'s")
        """
        {clear}

        241\nYou find [line].
        """
        $ stats["Luck"].restore(100)
        $ checked.append("Gift from Grimslade")
    jump r206

label r242:
    """
    {clear}

    242
    """

    menu:
        "124":
            jump r124
        "256":
            jump r256
        "358":
            jump r358

label r243:
    """
    243
    """
    jump r279

label r244:
    """
    {clear}

    244
    """
    if preferences.showImages:
        hide giant with dissolve
    jump r161

label r245:
    $ magic["Illusion Spell Gem"].expend()
    """
    245
    """
    if preferences.showImages:
        hide master_of_frogs with dissolve
    $ inventory["Frog Amulet"] = Item("Frog Amulet")
    jump r352

label r246:
    "246"

    menu:
        "19":
            jump r19
        "67":
            jump r67

label r247:
    if preferences.showImages:
        hide twowolves with dissolve
    """
    {clear}

    247
    """

    menu:
        "20":
            jump r20
        "232":
            jump r232
        "342":
            jump r342

label r248:
    """
    {clear}

    248
    """
    if preferences.showImages:
        hide mistress_of_birds with dissolve
        window hide
        show gianteagle at truecenter, fill
        with dissolve
        pause
        window show
    nvl clear
    if "16" not in visited:
        $ visited.append("16")
        if clearingsanity:
            $ checked.append("Clearing 16 Entered")
            $ notify_item("Clearing 16 Entered")
    if preferences.showImages:
        hide gianteagle with dissolve
    jump r202

label r249:
    "249\n{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
    else:
        $ stats["Luck"].damage(1)
        "You lose 1 point of SKILL."
        if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            $ extraSkill -= 1
        else:
            $ stats["Skill"].damage(1)

    menu:
        "336" if not clearingsanity or "28" in clearingPasses:
            jump r336
        "121":
            jump r121

label r250:
    "250"
    if fearFlowersDefeated:
        jump r367
    else:
        jump r269

label r251:
    """
    {clear}

    251\nYou lose 3 LUCK.
    """
    $ stats["Luck"].damage(3)
    $ inventory["Flower Amulet"] = Item("Flower Amulet")
    jump r363

label r252:
    $ magic["Curse Spell Gem"].expend()
    """
    {clear}

    252
    """
    if preferences.showImages:
        hide giant with dissolve
    $ temp = roll()
    $ dieBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover
    jump r161

label r253:
    """
    {clear}

    253
    """
    $ dwarfPotion = True
    jump r88

label r254:
    $ magic["Withering Spell Gem"].expend()
    """
    {clear}

    254
    """

    menu:
        "157" if not clearingsanity or "18" in clearingPasses:
            jump r157
        "398" if not clearingsanity or "4" in clearingPasses:
            jump r398

label r255:
    if wizardsanity:
        $ checked.append("Gronar - Directions to Grimslade")
        $ notify_item("Gronar - Directions to Grimslade")
    """
    {clear}

    255
    """

    menu:
        "40":
            jump r40
        "139" if not wizardsanity or "Poomchukker" in wizards or "Selator" in wizards:
            jump r139

label r256:
    "256"

    menu r256menu:
        "274" if "Curse Spell Gem" in magic.keys():
            jump r274
        "365" if "Fear Spell Gem" in magic.keys():
            jump r365
        "385" if "Fire Spell Gem" in magic.keys():
            jump r385
        "351" if "Illusion Spell Gem" in magic.keys():
            jump r351
        "57":
            jump r57

label r257:
    "257\n{i}Test your Skill.{/i}"

    if stats["Skill"].test():
        $ stats["Luck"].restore(2)
        jump r153
    else:
        jump r311

label r258:
    "258"

    menu:
        "198" if "Fear Spell Gem" in magic.keys():
            $ magic["Fear Spell Gem"].expend()
            jump r198
        "127" if "Friendship Spell Gem" in magic.keys():
            jump r127
        "212":
            jump r212menu

label r259:
    """
    {clear}

    235
    """
    jump r235

label r260:
    $ magic["Curse Spell Gem"].expend()
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Curse of the Birds"])
            $ notify_item("Game Over - Curse of the Birds")
    """
    260
    """
    jump gameover

label r261:
    $ magic["Curse Spell Gem"].expend()
    if preferences.showImages:
        window hide
        hide master_of_spiders with dissolve
        show spidercurse at truecenter, fill
        with dissolve
        pause
        window show
    """
    261
    """
    $ temp = roll()
    $ dieBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover
    call battle(giantSpider) from _call_battle_20
    if preferences.showImages:
        hide spidercurse with dissolve
    jump r354

label r262:
    "262"
    $ rangerOutcome = "friendly"
    if "Map to Willowbend" in inventory.keys():
        jump r166
    else:
        jump r115

label r263:
    "263"
    if crabGrass.stamina <= 0:
        jump r187
    else:
        jump r33

label r264:
    $ magic["Withering Spell Gem"].expend()
    """
    {clear}

    264\nYou lose 2 points of Stamina.
    """
    $ stats["Stamina"].damage(2)
    if stats["Stamina"].current <= 0:
        jump gameover
    jump r379

label r265:
    "265"
    jump r348

label r266:
    "266"
    jump r242

label r267:
    "267"
    call battle(thief) from _call_battle_21
    if preferences.showImages:
        hide thief1 with dissolve
    jump r386

label r268:
    "268"
    jump r390

label r269:
    "269\nYou lose 1 point of Skill."
    if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
        $ extraSkill -= 1
    else:
        $ stats["Skill"].damage(1)
    jump r367

label r270:
    "270"

    menu:
        "275" if not clearingsanity or "7" in clearingPasses:
            jump r275
        "331" if not clearingsanity or "16" in clearingPasses:
            jump r331

label r271:
    "271\nYou lose 1 point of Luck."
    $ stats["Luck"].damage(1)
    $ masterOfWolves.stamina -= 2
    jump r120

label r272:
    """
    {clear}

    272\nYou lose 2 points of Luck.
    """
    $ stats['Luck'].damage(2)
    jump r205

label r273:
    """
    {clear}

    273
    """

    menu:
        "335" if not wizardsanity or "Selator" in wizards:
            jump r335
        "27" if not wizardsanity or "Poomchukker" in wizards:
            jump r27
    "Unfortunately, you don't know of any others."
    jump gameover # If you have no options, just end the game

label r274:
    $ magic["Curse Spell Gem"].expend()
    """
    {clear}

    274
    """
    $ temp = roll()
    $ dieBubble(bp, bpBubble, temp)
    $ stats["Stamina"].damage(temp)
    if stats["Stamina"].current <= 0:
        jump gameover

    menu:
        "375":
            jump r375
        "298":
            jump r298

label r275:
    """
    {clear}

    275
    """
    if "7" in visited:
        jump r342
    $ visited.append("7")
    if clearingsanity:
        $ checked.append("Clearing 7 Entered")
        $ notify_item("Clearing 7 Entered")
    if preferences.showImages:
        window hide
        show giant at truecenter, fill
        with dissolve
        pause
        window show

    menu r275menu:
        "12":
            jump r12
        "229":
            jump r229
        "145":
            jump r145

label r276:
    """
    {clear}
    
    276
    """
    $ inventory["Violet Jewel"].expend()
    jump r104

label r277:
    nvl clear
    if not ap:
        "277"
        $ inventory["Horn of a Unicorn"] = Item("Horn of a Unicorn")
    else:
        $ line = get_item_string("Slay the Unicorn", "'s")
        "277\nYou find [line]."
        $ checked.append("Slay the Unicorn")

    menu:
        "348":
            jump r348
        "86":
            jump r86

label r278:
    $ magic["Fear Spell Gem"].expend()
    """
    {clear}

    278
    """
    jump r19

label r279:
    if preferences.showImages:
        window hide
        show sword_trees at truecenter, fill
        with dissolve
        pause
        window show
    $ swordTrees.stamina = 12
    "279"

    menu:
        "28":
            jump r28
        "203":
            jump r203

label r280:
    """
    {clear}

    280
    """
    if "Map to Willowbend" in inventory.keys():
        jump r355
    $ inventory["Map to Willowbend"] = Item("Map to Willowbend")

    menu:
        "395":
            jump r395
        "78":
            jump r78
        "289":
            jump r289

label r281:
    """
    {clear}

    281
    """
    if temp == "orc_feared":
        call multibattle([swampOrc1, swampOrc2]) from _call_multibattle_3
    else:
        call multibattle([swampOrc1, swampOrc2, swampOrc3]) from _call_multibattle_4
    $ orcsDefeated = True
    if preferences.showImages:
        hide swamporcs with dissolve
    jump r135

label r282:
    $ magic["Ice Spell Gem"].expend()
    "282"
    $ slime.stamina = 0
    jump r38

label r283:
    """
    {clear}

    283
    """
    if spellsanity:
        call masterOfGardensShop(1) from _call_masterOfGardensShop
    else:
        call pickMagic(1, "onlyGood") from _call_pickMagic_3
    if preferences.showImages:
        hide master_of_gardens with dissolve
    nvl clear
    jump r363

label r284:
    """
    {clear}

    284
    """
    call battle(goblinStatue, True) from _call_battle_22
    if _return == "escaped":
        if preferences.showImages:
            hide goblin_statue with dissolve
        jump r315
    else:
        jump r156

label r285:
    """
    {clear}

    285\nYour STAMINA is cut in half.
    """
    $ stats["Stamina"].damage(stats["Stamina"].current // 2)

    menu:
        "124":
            jump r124
        "256":
            jump r256

label r286:
    """
    286
    """
    $ inventory["Red Cloak"].expend()
    if quest == "Selator":
        jump r244
    elif quest == "Grimslade":
        jump r317
    elif quest == "Poomchukker":
        jump r103

label r287:
    "287"

    menu:
        "198":
            jump r198
        "359":
            jump r359

label r288:
    "288"

    menu r288menu:
        "391":
            jump r391
        "184":
            jump r184
        "130":
            jump r130

label r289:
    """
    {clear}

    289\nYou regain 2 STAMINA points.
    """
    $ stats["Stamina"].restore(2)
    python:
        temp = []
        temp2 = ""
        if inventory or magic:
            temp.extend(inventory.keys())
            temp.extend(magic.keys())
            temp2 = renpy.random.choice(temp)
        if temp2 in inventory.keys():
            inventory[temp2].expend()
        elif temp2 in magic.keys():
            magic[temp2].expend()
    if temp:
        "Lost [temp2]..."
    python:
        temp = []
        if inventory or magic:
            temp.extend(inventory.keys())
            temp.extend(magic.keys())
            temp2 = renpy.random.choice(temp)
        if temp2 in inventory.keys():
            inventory[temp2].expend()
        elif temp2 in magic.keys():
            magic[temp2].expend()
    if temp:
        "Lost [temp2]..."
    
    "{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r150
    else:
        $ stats["Luck"].damage(1)
        jump r343

label r290:
    """
    {clear}

    290
    """
    if "26" in visited:
        jump r323
    $ visited.append("26")
    if clearingsanity:
        $ checked.append("Clearing 26 Entered")
        $ notify_item("Clearing 26 Entered")
    if preferences.showImages:
        window hide
        show swamporcs at truecenter, fill
        with dissolve
        pause
        window show
    if "Golden Magnet" in inventory.keys():
        jump r83
    else:
        jump r151

label r291:
    $ magic["Fire Spell Gem"].expend()
    "291"
    jump r82

label r292:
    """
    {clear}

    292
    """
    if preferences.showImages:
        hide master_of_gardens with dissolve
    jump r363

label r293:
    $ magic["Fear Spell Gem"].expend()
    "293"
    if preferences.showImages:
        hide unicorn with dissolve
    jump r348

label r294:
    $ magic["Friendship Spell Gem"].expend()
    """
    294
    """

    menu:
        "271":
            jump r271
        "172":
            jump r172

label r295:
    if not renpy.showing("foulbrood_river"):
        if preferences.showImages:
            window hide
            show foulbrood_river at truecenter, fill
            with dissolve
            pause
            window show
    """
    {clear}

    295
    """
    if "33" not in visited:
        $ visited.append("33")
        if clearingsanity:
            $ checked.append("Clearing 33 Entered")
            $ notify_item("Clearing 33 Entered")
    
    menu r295menu:
        "295" if not clearingsanity or "20" in clearingPasses:
            jump r183
        "94":
            if preferences.showImages:
                hide foulbrood_river with dissolve
            jump r94
        "89" if "Ice Spell Gem" in magic.keys():
            jump r89

label r296:
    """
    {clear}

    296\n{i}Test your Luck.{/i}
    """
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r272
    else:
        $ stats["Luck"].damage(1)
        jump r3

label r297:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Magic Carpet Ride"])
            $ notify_item("Game Over - Magic Carpet Ride")
    """
    {clear}

    297
    """
    jump gameover

label r298:
    if ap:
        hide screen progression_watcher
        if has_required_amulets or required_amulets == -1:
            if goal in {"any", "grimslade"}:
                call send_victory from _call_send_victory_5
            if goal == "all":
                $ check_goal()
                if "selator" in goals_complete and "poomchukker" in goals_complete:
                    call send_victory from _call_send_victory_6
                python:
                    if not renpy.loadable("v_grimslade", directory=CONNECTIONS_PATH):
                        with open(os.path.join(CONNECTIONS_PATH, "v_grimslade"), 'w') as f:
                            f.close()
    """
    {clear}

    298
    """
    if ap and not (has_required_amulets or required_amulets == -1):
        jump gameover
    jump gameComplete

label r299:
    $ magic["Fear Spell Gem"].expend()
    """
    {clear}

    299
    """

    menu:
        "176":
            jump r176
        "279":
            jump r279

label r300:
    "300"
    jump r161

label r301:
    "301"
    call multibattle([brigand1_2, brigand2_2], True) from _call_multibattle_5
    if _return == "escaped":
        jump r19
    else:
        jump r246

label r302:
    """
    302
    """
    jump r247

label r303:
    """
    303
    """
    jump r70

label r304:
    """
    {clear}

    304
    """
    if "14" in visited:
        jump r149
    $ visited.append("14")
    if clearingsanity:
        $ checked.append("Clearing 14 Entered")
        $ notify_item("Clearing 14 Entered")

    menu:
        "71":
            jump r71
        "131":
            jump r131

label r305:
    """
    {clear}

    305
    """
    if "27" in visited:
        jump r238
    $ visited.append("27")
    if clearingsanity:
        $ checked.append("Clearing 27 Entered")
        $ notify_item("Clearing 27 Entered")
    if preferences.showImages:
        window hide
        show master_of_gardens at truecenter, fill
        with dissolve
        pause
        window show

    if quest == "Selator":
        jump r36
    elif quest == "Poomchukker":
        jump r84
    elif quest == "Grimslade":
        jump r334

label r306:
    "306"
    $ ranger.stamina = 10
    jump r378

label r307:
    $ magic["Fire Spell Gem"].expend()
    "307"
    jump r269

label r308:
    if not ap:
        """
        {clear}

        308
        """
        $ inventory["Violet Jewel"] = Item("Violet Jewel")
    else:
        $ line = get_item_string("Slay the Pool Beast", "'s")
        """
        {clear}

        308\nYou find [line].
        """
        $ checked.append("Slay the Pool Beast")
    if preferences.showImages:
        hide poolbeast with dissolve
    jump r330

label r309:
    "309"

    menu:
        "47" if not clearingsanity or "3" in clearingPasses:
            jump r47
        "53" if not clearingsanity or "8" in clearingPasses:
            jump r53
        "388" if not clearingsanity or "24" in clearingPasses:
            jump r388

label r310:
    $ magic["Fire Spell Gem"].expend()
    "310"
    if preferences.showImages:
        hide crab_grass with dissolve
    jump r187

label r311:
    "311\nYou lose 2 points of Skill."
    python:
        if extraSkill >= 2 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 2
        elif extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 1
            stats["Skill"].damage(1)
        else:
            stats["Skill"].damage(2)
    
    menu:
        "85":
            jump r85
        "171":
            jump r171

label r312:
    "312"
    call battle(giantScorpion, True) from _call_battle_23
    if preferences.showImages:
        hide scorpionfight with dissolve
    if _return == "escaped":
        jump r88
    else:
        jump r324

label r313:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Dragged Down Into the River"])
            $ notify_item("Game Over - Dragged Down Into the River")
    """
    {clear}

    313
    """
    jump gameover

label r314:
    "314"

    menu:
        "90" if not clearingsanity or "34" in clearingPasses:
            jump r90
        "195":
            jump r195

label r315:
    "315\n{i}Test your Luck.{/i}"
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r51
    else:
        if ap:
            hide screen progression_watcher
            if extra_locations:
                $ send_locations(["Game Over - Grimslade's Trap"])
                $ notify_item("Game Over - Grimslade's Trap")
        $ stats["Luck"].damage(1)
        jump gameover

label r316:
    """
    316
    """
    menu:
        "100":
            jump r100
        "341":
            jump r341

label r317:
    """
    {clear}

    317
    """
    if preferences.showImages:
        hide giant with dissolve
    jump r161

label r318:
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    318
    """
    jump r214

label r319:
    "319"

    menu:
        "138" if not clearingsanity or "35" in clearingPasses:
            $ temp = "north"
            jump r138
        "47" if not clearingsanity or "3" in clearingPasses:
            jump r47
        "66" if not clearingsanity or "9" in clearingPasses:
            jump r66

label r320:
    """
    {clear}

    320
    """
    if "29" in visited:
        jump r265
    $ visited.append("29")
    if clearingsanity:
        $ checked.append("Clearing 29 Entered")
        $ notify_item("Clearing 29 Entered")
    if preferences.showImages:
        window hide
        show unicorn at truecenter, fill
        with dissolve
        pause
        window show

    menu r320menu:
        "368":
            if preferences.showImages:
                hide unicorn with dissolve
            jump r368
        "221":
            jump r221
        "119":
            jump r119

label r321:
    """
    321
    """
    jump r30

label r322:
    $ magic["Withering Spell Gem"].expend()
    "322"
    $ crabGrass.stamina = 0
    if preferences.showImages:
        hide crab_grass with dissolve
    jump r81

label r323:
    "323"
    if orcsDefeated:
        jump r309
    else:
        if preferences.showImages:
            window hide
            show swamporcs at truecenter, fill
            with dissolve
            pause
            window show
        jump r281

label r324:
    nvl clear
    "324"

    menu r324menu:
        "88":
            jump r88
        "383" if "Bless Spell Gem" in magic.keys():
            jump r383
        "42":
            jump r42

label r325:
    "325"

    if "Ice Spell Gem" in magic.keys():
        jump r369
    else:
        jump r43

label r326:
    """
    {clear}

    326
    """

    menu:
        "98":
            jump r98
        "315":
            jump r315
        "225":
            jump r225

label r327:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Out the Window and Into the Dungeons"])
            $ notify_item("Game Over - Out the Window and Into the Dungeons")
    """
    {clear}

    327
    """
    jump gameover

label r328:
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    328
    """

    if quest == "Selator":
        jump r244
    elif quest == "Grimslade":
        jump r317
    elif quest == "Poomchukker":
        jump r103

label r329:
    """
    329
    """

    menu:
        "178":
            jump r178
        "352":
            jump r352

label r330:
    "330"
    if bearOutcome:
        jump r129
    else:
        jump r268

label r331:
    "331"

    if eagle.stamina <= 0:
        if preferences.showImages:
            hide eaglesnest with dissolve
        jump r202
    else:
        jump r112

label r332:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - A Feast for the Spiders"])
            $ notify_item("Game Over - A Feast for the Spiders")
    """
    {clear}

    332
    """
    jump gameover

label r333:
    """
    {clear}

    333
    """
    if preferences.showImages:
        hide ranger with dissolve
    jump r234

label r334:
    "334"

    menu:        
        "379":
            jump r379
        "152":
            jump r152
        "37":
            jump r37

label r335:
    if wizardsanity:
        $ checked.append("Gronar - Directions to Selator")
        $ notify_item("Gronar - Directions to Selator")
    """
    {clear}

    335
    """
    if preferences.showImages:
        window hide
        show selator at truecenter, fill
        with dissolve
        pause
        window show

    menu:
        "371":
            jump r371
        "96":
            jump r96

label r336:
    """
    {clear}
    
    336
    """
    if "28" in visited and slime.stamina <= 0:
        jump r137
    if "28" not in visited:
        $ visited.append("28")
        if clearingsanity:
            $ checked.append("Clearing 28 Entered")
            $ notify_item("Clearing 28 Entered")

    menu r336menu:
        "85":
            jump r85
        "257":
            jump r257
        "171":
            jump r171
        "400":
            jump r400

label r337:
    $ magic["Fire Spell Gem"].expend()
    "337"
    jump r221

label r338:
    "338"
    jump r88

label r339:
    """
    {clear}

    339
    """

    menu:
        "384" if not clearingsanity or "35" in clearingPasses:
            if "35" not in visited:
                $ visited.append("35")
                if clearingsanity:
                    $ checked.append("Clearing 35 Entered")
                    $ notify_item("Clearing 35 Entered")
                    $ canUseIceFlow = True
            jump r384
        "313":
            jump r313

label r340:
    if not ap:
        """
        {clear}

        340
        """
    else:
        $ line = get_item_string("Slay Grimslade", "'s")
        """
        {clear}

        340\nYou find [line].
        """
        $ checked.append("Slay Grimslade")

    menu:
        "375":
            jump r375
        "298":
            jump r298

label r341:
    """
    {clear}

    341
    """
    call battle(poomchukker, True, 6) from _call_battle_24
    if _return == "escaped":
        jump r327
    else:
        jump r372

label r342:
    "341"

    if giant.stamina <= 0:
        jump r197
    else:
        jump r300

label r343:
    "343"

    if brigandOutcome == "friendly":
        jump r199
    else:
        jump r301

label r344:
    "344"
    jump r247

label r345:
    if clearingsanity: # We need to be able to pass through here for clearingsanity so that the connection doesn't get broken
        """
        {clear}

        345\nYou lose 1 point of Stamina but manage to pass through the flaming clearing.
        """
        $ stats["Stamina"].damage(1)
        if stats["Stamina"].current <= 0:
            jump gameOver
        
        if temp == "north":
            if "12" in clearingPasses:
                jump r105
            else:
                "You get lost and decide to turn back around after all."
                jump r388
        else:
            if "24" in clearingPasses:
                jump r388
            else:
                "You get lost and decide to turn back around after all."
                jump r105
    """
    {clear}

    345\nYou lose 1 point of Stamina."
    """
    $ stats["Stamina"].damage(1)
    if stats["Stamina"].current <= 0:
        jump gameOver
    
    if temp == "north":
        jump r388
    else:
        jump r105

label r346:
    $ magic["Fear Spell Gem"].expend()
    "346"
    $ temp = "orc_feared"
    jump r281

label r347:
    $ magic["Illusion Spell Gem"].expend()
    """
    {clear}

    347
    """

    menu:
        "379":
            jump r379
        "363":
            if preferences.showImages:
                hide master_of_gardens with dissolve
            jump r363

label r348:
    "348"

    menu:
        "94":
            jump r94
        "157" if not clearingsanity or "18" in clearingPasses:
            jump r157
        "10" if not clearingsanity or "5" in clearingPasses:
            jump r10
        "204" if not clearingsanity or "23" in clearingPasses:
            jump r204

label r349:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Returning to Grimslade Empty-Handed"])
            $ notify_item("Game Over - Returning to Grimslade Empty-Handed")
    """
    {clear}

    349
    """
    jump gameover

label r350:
    """
    {clear}

    350
    """
    if preferences.showImages:
        window hide
        show eaglesnest at truecenter, fill
        with dissolve
        pause
        window show
    if "16" in visited:
        jump r331
    $ visited.append("16")
    if clearingsanity:
        $ checked.append("Clearing 16 Entered")
        $ notify_item("Clearing 16 Entered")
    if "False Bird Amulet" in inventory.keys():
        jump r25
    elif "Parrot Feathers" in inventory.keys():
        jump r392
    else:
        jump r233

label r351:
    $ magic["Illusion Spell Gem"].expend()
    """
    {clear}

    351
    """
    jump r124

label r352:
    """
    {clear}

    352
    """
    jump r323

label r353:
    """
    {clear}

    353
    """
    jump r235

label r354:
    """
    {clear}

    354
    """
    $ inventory["Spider Amulet"] = Item("Spider Amulet")
    jump r165

label r355:
    """
    {clear}

    355
    """
    call battle(cutpurse1) from _call_battle_25
    call battle(cutpurse2) from _call_battle_26
    jump r186

label r356:
    $ magic["Fear Spell Gem"].expend()
    "356"
    jump r82

label r357:
    "357\nYou lose 5 points of STAMINA."
    $ stats["Stamina"].damage(5)
    if stats["Stamina"].current <= 0:
        jump gameover

    menu:
        "281":
            jump r281
        "399":
            jump r399
        "309":
            if preferences.showImages:
                hide swamporcs with dissolve
            jump r309

label r358:
    if ap:
        hide screen progression_watcher
        if has_required_amulets or required_amulets == -1:
            if goal in {"any", "grimslade"}:
                call send_victory from _call_send_victory_7
            if goal == "all":
                $ check_goal()
                if "selator" in goals_complete and "poomchukker" in goals_complete:
                    call send_victory from _call_send_victory_8
                python:
                    if not renpy.loadable("v_grimslade", directory=CONNECTIONS_PATH):
                        with open(os.path.join(CONNECTIONS_PATH, "v_grimslade"), 'w') as f:
                            f.close()
    """
    {clear}

    358
    """
    if ap and not (has_required_amulets or required_amulets == -1):
        jump gameover
    jump gameComplete

label r359:
    """
    {clear}

    359\n{i}Test your Luck.{/i}
    """
    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        jump r162
    else:
        $ stats["Luck"].damage(1)
        jump r16

label r360:
    """
    360
    """
    jump r214

label r361:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - The Master of Spiders Has No Friends"])
            $ notify_item("Game Over - The Master of Spiders Has No Friends")
    $ magic["Friendship Spell Gem"].expend()
    """
    {clear}

    361
    """
    jump gameover

label r362:
    if preferences.showImages:
        hide sword_trees with dissolve
    if not ap:
        """
        {clear}

        362
        """
        $ inventory["Sword Tree Seeds"] = Item("Sword Tree Seeds")
    elif "Slay the Sword Trees" not in checked:
        $ line = get_item_string("Slay the Sword Trees", "'s")
        """
        {clear}

        362\nYou find [line].
        """
        $ checked.append("Slay the Sword Trees")
    else:
        """
        {clear}

        362
        """

    jump r22

label r363:
    "363"
    if rangerOutcome == "friendly":
        jump r133
    elif ranger.stamina <= 0:
        jump r234
    else:
        jump r306

label r364:
    """
    364
    """
    jump r47

label r365:
    $ magic["Fear Spell Gem"].expend()
    """
    {clear}

    365\nYou lose 1 SKILL point.
    """
    python:
        if extraSkill >= 1 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            extraSkill -= 1
        else:
            stats["Skill"].damage(1)
    jump r124

label r366:
    nvl clear
    "366"
    if preferences.showImages:
        hide giant with dissolve
    jump r161

label r367:
    "367"

    menu:

        "304" if not clearingsanity or "14" in clearingPasses:
            jump r304
        "265":
            jump r265

label r368:
    if temp == "north":
        jump r94
    elif temp == "south":
        jump r157
    elif temp == "east":
        jump r10
    else:
        jump r204

label r369:
    $ magic["Ice Spell Gem"].expend()
    """
    369
    """

    menu:

        "384" if not clearingsanity or "35" in clearingPasses:
            if "35" not in visited:
                $ visited.append("35")
                if clearingsanity:
                    $ checked.append("Clearing 35 Entered")
                    $ notify_item("Clearing 35 Entered")
                    $ canUseIceFlow = True
            jump r384
        "313":
            jump r313

label r370:
    $ magic["Ice Spell Gem"].expend()
    "370"

    menu:

        "157" if not clearingsanity or "18" in clearingPasses:
            jump r157
        "398" if not clearingsanity or "4" in clearingPasses:
            jump r398

label r371:
    """
    {clear}

    371
    """
    if spellsanity:
        call selatorShop(6) from _call_selatorShop
    else:
        call pickMagic(6, "good") from _call_pickMagic_4
    if preferences.showImages:
        hide selator with dissolve
    nvl clear
    $ quest = "Selator"
    jump r9

label r372:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Slain by Poomchukker's Guards"])
            $ notify_item("Game Over - Slain by Poomchukker's Guards")
    """
    {clear}

    372
    """
    jump gameover

label r373:
    "373\n{i}Test your Luck.{/i}"

    if stats["Luck"].test():
        $ stats["Luck"].damage(1)
        $ grimslade2.stamina -= 2
        jump r225
    else:
        $ stats["Luck"].damage(1)
        jump r225

label r374:
    "374"

    menu:

        "299" if "Fear Spell Gem" in magic.keys():
            jump r299
        "60" if "Illusion Spell Gem" in magic.keys():
            jump r60
        "228" if "Growth Spell Gem" in magic.keys() and "Sword Tree Seeds" in inventory.keys():
            jump r228
        "160" if "Friendship Spell Gem" in magic.keys():
            jump r160
        "11":
            jump r11menu

label r375:
    if ap:
        hide screen progression_watcher
        if extra_locations:
            $ send_locations(["Game Over - Explosion of Hellfire"])
            $ notify_item("Game Over - Explosion of Hellfire")
    """
    {clear}

    375
    """
    if preferences.showImages:
        window hide
        show hellfiremaster at truecenter, fill
        with dissolve
        pause
        window show
    jump gameover

label r376:
    if preferences.showImages:
        hide master_of_frogs with dissolve
    """
    376
    """
    jump r323

label r377:
    "377\n{i}Test your Stamina.{/i}"
    if stats["Stamina"].test():
        pass
    else:
        "You lose 3 STAMINA points."
        $ stats["Stamina"].damage(3)
        if stats["Stamina"].current <= 0:
            jump gameover
    if preferences.showImages:
        hide swampscorpions with dissolve
    jump r319

label r378:
    "378"
    call battle(ranger, True) from _call_battle_27
    if preferences.showImages:
        hide ranger with dissolve
    if _return == "escaped":
        jump r234
    else:
        jump r219

label r379:
    """
    {clear}

    379\nYou lose 3 SKILL points.
    """
    python:
        if extraSkill >= 0 and ("Magic Sword" in inventory.keys() or "Ranger's Helmet" in inventory.keys() or "Great Magic Sword" in inventory.keys()):
            stats["Skill"].damage(max(0, 3 - extraSkill))
            extraSkill = max(extraSkill - 3, 0)
        else:
            stats["Skill"].damage(3)
    call battle(masterOfGardens, True) from _call_battle_28
    if preferences.showImages:
        hide master_of_gardens with dissolve
    if _return == "escaped":
        jump r363
    else:
        jump r251

label r380:
    $ magic["Withering Spell Gem"].expend()
    "380"

    menu:

        "400":
            jump r400
        "336":
            jump r336menu

label r381:
    $ magic["Bless Spell Gem"].expend()
    if not spellsanity:
        """
        {clear}

        381
        """
        python:
            if "Friendship Spell Gem" in magic.keys():
                magic["Friendship Spell Gem"].add()
            else:
                magic["Friendship Spell Gem"] = Item("Friendship Spell Gem")
            if "Luck Spell Gem" in magic.keys():
                magic["Luck Spell Gem"].add()
            else:
                magic["Luck Spell Gem"] = Item("Luck Spell Gem", 1, True, True)
    else:
        $ line = get_item_string("Unicorn Clearing Spell Gem 1", "'s")
        $ line2 = get_item_string("Unicorn Clearing Spell Gem 2", "'s")
        """
        {clear}

        381\nYou find [line] and [line2].
        """
        $ checked.extend(["Unicorn Clearing Spell Gem 1", "Unicorn Clearing Spell Gem 2"])
        
    if preferences.showImages:
        hide unicorn with dissolve
    jump r348

label r382:
    "382"
    if quicksandGrowth:
        jump r270

    menu:

        "270 - Ice" if "Ice Spell Gem" in magic.keys():
            $ magic["Ice Spell Gem"].expend()
            jump r270
        "270 - Growth" if "Growth Spell Gem" in magic.keys():
            $ magic["Growth Spell Gem"].expend()
            $ quicksandGrowth = True
            jump r270
        "190":
            jump r190
        "223":
            jump r223

label r383:
    $ magic["Bless Spell Gem"].expend()
    """
    383
    """
    jump r324menu

label r384:
    """
    {clear}

    384
    """
    jump r101

label r385:
    $ magic["Fire Spell Gem"].expend()
    """
    385
    """
    jump r124

label r386:
    if not ap:
        """
        386
        """
        $ inventory["Red Cloak"] = Item("Red Cloak")
    else:
        $ line = get_item_string("Slay the Thief", "'s")
        """
        386\nYou find [line].
        """
        $ checked.append("Slay the Thief")
    jump r179

label r387:
    "387"

    menu:

        "107" if "Curse Spell Gem" in magic.keys():
            jump r107
        "278" if "Fear Spell Gem" in magic.keys():
            jump r278
        "148" if "Illusion Spell Gem" in magic.keys():
            jump r148
        "318" if "Friendship Spell Gem" in magic.keys():
            jump r318
        "65":
            jump r65menu

label r388:
    """
    {clear}
    
    388
    """
    if "24" in visited:
        jump r263
    $ visited.append("24")
    if clearingsanity:
        $ checked.append("Clearing 24 Entered")
        $ notify_item("Clearing 24 Entered")
    if preferences.showImages:
        window hide
        show crab_grass at truecenter, fill
        with dissolve
        pause
        window show

    menu:

        "134":
            jump r134
        "167":
            jump r167

label r389:
    """
    389
    """
    $ inventory["Antherica Berry"] = Item("Antherica Berry")
    jump r342

label r390:
    if preferences.showImages:
        hide clearing with dissolve
    nvl clear
    "390"

    menu:

        "144" if not clearingsanity or "17" in clearingPasses:
            $ temp = "south"
            jump r144
        "209" if not clearingsanity or "25" in clearingPasses:
            jump r209
        "195":
            jump r195

label r391:
    nvl clear
    "391\nYou lose 2 LUCK points."
    if preferences.showImages:
        hide mistress_of_birds with dissolve
    $ stats["Luck"].damage(2)
    jump r217

label r392:
    "392"
    call battle(eagle) from _call_battle_29
    jump r132

label r393:
    $ magic["Withering Spell Gem"].expend()
    if preferences.showImages:
        hide sword_trees with dissolve
    nvl clear
    if not ap:
        "393"
        $ inventory["Sword Tree Seeds"] = Item("Sword Tree Seeds")
    elif "Slay the Sword Trees" not in checked:
        $ line = get_item_string("Slay the Sword Trees", "'s")
        "393\nYou find [line]."
        $ checked.append("Slay the Sword Trees")
    else:
        "393"
    jump r22

label r394:
    "394"

    menu:

        "47":
            jump r47
        "77":
            jump r77

label r395:
    nvl clear
    "395"
    $ stats["Stamina"].damage(1)
    "You lose 1 STAMINA point."
    if stats["Stamina"].current <= 0:
        jump gameover
    
    menu:

        "116":
            jump r116
        "236":
            jump r236
        "78":
            jump r78
        "289":
            jump r289

label r396:
    nvl clear
    "396"
    if spellsanity:
        call masterOfGardensShop(1) from _call_masterOfGardensShop_1
    else:
        call pickMagic(1, "onlyGood") from _call_pickMagic_5
    if preferences.showImages:
        hide master_of_gardens with dissolve
    jump r363

label r397:
    "397"
    jump r330

label r398:
    nvl clear
    "398"
    if "4" in visited:
        jump r239
    $ visited.append("4")
    if clearingsanity:
        $ checked.append("Clearing 4 Entered")
        $ notify_item("Clearing 4 Entered")
    if preferences.showImages:
        window hide
        show master_of_wolves at truecenter, fill
        with dissolve
        pause
        window show

    menu r398menu:

        "314":
            if preferences.showImages:
                hide master_of_wolves with dissolve
            jump r314
        "191":
            jump r191
        "120":
            jump r120

label r399:
    menu:
        "399"

        "346" if "Fear Spell Gem" in magic.keys():
            jump r346
        "169" if "Illusion Spell Gem" in magic.keys():
            jump r169
        "281":
            jump r281

label r400:
    menu:
        "400"

        "188" if "Fire Spell Gem" in magic.keys():
            jump r188
        "380" if "Withering Spell Gem" in magic.keys():
            jump r380
        "282" if "Ice Spell Gem" in magic.keys():
            jump r282
        "336":
            jump r336menu

label gameover():
    $ renpy.set_return_stack([])
    hide screen statScreen with moveoutleft
    hide screen itemMenu with {"master" : moveoutright}
    hide screen enemyStatScreen with moveoutright
    show screen gameOver with dissolve
    pause
    return

label gameComplete():
    $ renpy.set_return_stack([])
    hide screen statScreen with moveoutleft
    hide screen itemMenu with {"master" : moveoutright}
    hide screen enemyStatScreen with moveoutright
    show screen victory with dissolve
    pause
    return

label useMagicPotion:
    menu:
        "Which will you recover?"

        "Skill":
            $ stats["Skill"].restore(100)
        "Stamina":
            $ stats["Stamina"].restore(100)
        "Luck":
            $ stats["Luck"].restore(100)
    return

label pickMagic(count=1, alignment="neutral"):
    # Lists all of the spells allowed by 'alignment', letting the player choose 'count' spells to add to their inventory
    nvl clear
    menu pickMagicMenu:
        "Which spell are you interested in?"

        "Skill" if not alignment == "onlyGood":
            "Check page 18 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Skill Spell Gem" in magic.keys():
                        $ magic["Skill Spell Gem"].add()
                    else:
                        $ magic["Skill Spell Gem"] = Item("Skill Spell Gem", 1, True, True)
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Stamina" if not alignment == "onlyGood":
            "Check page 18 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Stamina Spell Gem" in magic.keys():
                        $ magic["Stamina Spell Gem"].add()
                    else:
                        $ magic["Stamina Spell Gem"] = Item("Stamina Spell Gem", 1, True, True)
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Luck" if not alignment == "onlyGood":
            "Check page 18 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Luck Spell Gem" in magic.keys():
                        $ magic["Luck Spell Gem"].add()
                    else:
                        $ magic["Luck Spell Gem"] = Item("Luck Spell Gem", 1, True, True)
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Fire" if not alignment == "onlyGood":
            "Check page 18 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Fire Spell Gem" in magic.keys():
                        $ magic["Fire Spell Gem"].add()
                    else:
                        $ magic["Fire Spell Gem"] = Item("Fire Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Ice" if not alignment == "onlyGood":
            "Check page 18 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Ice Spell Gem" in magic.keys():
                        $ magic["Ice Spell Gem"].add()
                    else:
                        $ magic["Ice Spell Gem"] = Item("Ice Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Illusion" if not alignment == "onlyGood":
            "Check page 18 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Illusion Spell Gem" in magic.keys():
                        $ magic["Illusion Spell Gem"].add()
                    else:
                        $ magic["Illusion Spell Gem"] = Item("Illusion Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Friendship" if alignment == "good" or alignment == "onlyGood":
            "Check page 19 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Friendship Spell Gem" in magic.keys():
                        $ magic["Friendship Spell Gem"].add()
                    else:
                        $ magic["Friendship Spell Gem"] = Item("Friendship Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Growth" if alignment == "good" or alignment == "onlyGood":
            "Check page 19 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Growth Spell Gem" in magic.keys():
                        $ magic["Growth Spell Gem"].add()
                    else:
                        $ magic["Growth Spell Gem"] = Item("Growth Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Bless" if alignment == "good" or alignment == "onlyGood":
            "Check page 19 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Bless Spell Gem" in magic.keys():
                        $ magic["Bless Spell Gem"].add()
                    else:
                        $ magic["Bless Spell Gem"] = Item("Bless Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Fear" if alignment == "evil":
            "Check page 19 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Fear Spell Gem" in magic.keys():
                        $ magic["Fear Spell Gem"].add()
                    else:
                        $ magic["Fear Spell Gem"] = Item("Fear Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Withering" if alignment == "evil":
            "Check page 19 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Withering Spell Gem" in magic.keys():
                        $ magic["Withering Spell Gem"].add()
                    else:
                        $ magic["Withering Spell Gem"] = Item("Withering Spell Gem")
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return
        "Curse" if alignment == "evil":
            "Check page 19 for the spell's description."
            menu:
                "Do you want this spell gem?"

                "Yes":
                    $ count -= 1
                    if "Curse Spell Gem" in magic.keys():
                        $ magic["Curse Spell Gem" ].add()
                    else:
                        $ magic["Curse Spell Gem" ] = Item("Curse Spell Gem" )
                "No":
                    pass
            
            if count > 0:
                nvl clear
                jump pickMagicMenu
            else:
                return

label halicarShop(count=1):

    nvl clear
    "As Halicar shows you his spell gems, they open to reveal other items instead!"

    python:
        line = ["" for _ in range(7)]
        hints = []
        for i in range(1, 7):
            line[i] = get_item_string(f"Halicar's Shop {i}", "for")
            hints.append(f"Halicar's Shop {i}")
        send_hints(hints)

    menu halicarShopMenu:
        "Which item do you want?"

        "[line[1]]" if "Halicar's Shop 1" not in checked:
            $ count -= 1
            $ checked.append("Halicar's Shop 1")
            
            if count > 0:
                nvl clear
                jump halicarShopMenu
            else:
                return
        
        "[line[2]]" if "Halicar's Shop 2" not in checked:
            $ count -= 1
            $ checked.append("Halicar's Shop 2")
            
            if count > 0:
                nvl clear
                jump halicarShopMenu
            else:
                return
        
        "[line[3]]" if "Halicar's Shop 3" not in checked:
            $ count -= 1
            $ checked.append("Halicar's Shop 3")
            
            if count > 0:
                nvl clear
                jump halicarShopMenu
            else:
                return

        "[line[4]]" if "Halicar's Shop 4" not in checked:
            $ count -= 1
            $ checked.append("Halicar's Shop 4")
            
            if count > 0:
                nvl clear
                jump halicarShopMenu
            else:
                return

        "[line[5]]" if "Halicar's Shop 5" not in checked:
            $ count -= 1
            $ checked.append("Halicar's Shop 5")
            
            if count > 0:
                nvl clear
                jump halicarShopMenu
            else:
                return

        "[line[6]]" if "Halicar's Shop 6" not in checked:
            $ count -= 1
            $ checked.append("Halicar's Shop 6")
            
            if count > 0:
                nvl clear
                jump halicarShopMenu
            else:
                return

label selatorShop(count=1):
    nvl clear
    "As Selator shows you his spell gems, they open to reveal other items instead!"

    python:
        line = ["" for _ in range(10)]
        hints = []
        for i in range(1, 10):
            line[i] = get_item_string(f"Selator's Spell Gem {i}", "for")
            hints.append(f"Selator's Spell Gem {i}")
        send_hints(hints)

    menu selatorShopMenu:
        "Which item do you want?"

        "[line[1]]" if "Selator's Spell Gem 1" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 1")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return
        
        "[line[2]]" if "Selator's Spell Gem 2" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 2")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return
        
        "[line[3]]" if "Selator's Spell Gem 3" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 3")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return

        "[line[4]]" if "Selator's Spell Gem 4" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 4")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return

        "[line[5]]" if "Selator's Spell Gem 5" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 5")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return

        "[line[6]]" if "Selator's Spell Gem 6" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 6")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return
        
        "[line[7]]" if "Selator's Spell Gem 7" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 7")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return
        
        "[line[8]]" if "Selator's Spell Gem 8" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 8")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return

        "[line[9]]" if "Selator's Spell Gem 9" not in checked:
            $ count -= 1
            $ checked.append("Selator's Spell Gem 9")
            
            if count > 0:
                nvl clear
                jump selatorShopMenu
            else:
                return

label poomchukkerShop(count=1):
    nvl clear
    "As Poomchukker shows you his spell gems, they open to reveal other items instead!"

    python:
        line = ["" for _ in range(7)]
        hints = []
        for i in range(1, 7):
            line[i] = get_item_string(f"Poomchukker's Spell Gem {i}", "for")
            hints.append(f"Poomchukker's Spell Gem {i}")
        send_hints(hints)

    menu poomchukkerShopMenu:
        "Which item do you want?"

        "[line[1]]" if "Poomchukker's Spell Gem 1" not in checked:
            $ count -= 1
            $ checked.append("Poomchukker's Spell Gem 1")
            
            if count > 0:
                nvl clear
                jump poomchukkerShopMenu
            else:
                return
        
        "[line[2]]" if "Poomchukker's Spell Gem 2" not in checked:
            $ count -= 1
            $ checked.append("Poomchukker's Spell Gem 2")
            
            if count > 0:
                nvl clear
                jump poomchukkerShopMenu
            else:
                return
        
        "[line[3]]" if "Poomchukker's Spell Gem 3" not in checked:
            $ count -= 1
            $ checked.append("Poomchukker's Spell Gem 3")
            
            if count > 0:
                nvl clear
                jump poomchukkerShopMenu
            else:
                return

        "[line[4]]" if "Poomchukker's Spell Gem 4" not in checked:
            $ count -= 1
            $ checked.append("Poomchukker's Spell Gem 4")
            
            if count > 0:
                nvl clear
                jump poomchukkerShopMenu
            else:
                return

        "[line[5]]" if "Poomchukker's Spell Gem 5" not in checked:
            $ count -= 1
            $ checked.append("Poomchukker's Spell Gem 5")
            
            if count > 0:
                nvl clear
                jump poomchukkerShopMenu
            else:
                return

        "[line[6]]" if "Poomchukker's Spell Gem 6" not in checked:
            $ count -= 1
            $ checked.append("Poomchukker's Spell Gem 6")
            
            if count > 0:
                nvl clear
                jump poomchukkerShopMenu
            else:
                return

label grimsladeShop(count=1):
    nvl clear
    "As Grimslade shows you his spell gems, they open to reveal other items instead!"

    python:
        line = ["" for _ in range(10)]
        hints = []
        for i in range(1, 10):
            line[i] = get_item_string(f"Grimslade's Spell Gem {i}", "for")
            hints.append(f"Grimslade's Spell Gem {i}")
        send_hints(hints)

    menu grimsladeShopMenu:
        "Which item do you want?"

        "[line[1]]" if "Grimslade's Spell Gem 1" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 1")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return
        
        "[line[2]]" if "Grimslade's Spell Gem 2" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 2")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return
        
        "[line[3]]" if "Grimslade's Spell Gem 3" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 3")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return

        "[line[4]]" if "Grimslade's Spell Gem 4" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 4")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return

        "[line[5]]" if "Grimslade's Spell Gem 5" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 5")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return

        "[line[6]]" if "Grimslade's Spell Gem 6" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 6")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return
        
        "[line[7]]" if "Grimslade's Spell Gem 7" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 7")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return
        
        "[line[8]]" if "Grimslade's Spell Gem 8" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 8")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return

        "[line[9]]" if "Grimslade's Spell Gem 9" not in checked:
            $ count -= 1
            $ checked.append("Grimslade's Spell Gem 9")
            
            if count > 0:
                nvl clear
                jump grimsladeShopMenu
            else:
                return

label masterOfGardensShop(count=1):
    nvl clear
    "As the Master of Gardens shows you his spell gems, they open to reveal other items instead!"

    python:
        line = ["" for _ in range(4)]
        hints = []
        for i in range(1, 4):
            line[i] = get_item_string(f"Gift from the Master of Gardens {i}", "for")
            hints.append(f"Gift from the Master of Gardens {i}")
        send_hints(hints)

    menu gardensShopMenu:
        "Which item do you want?"

        "[line[1]]" if "Gift from the Master of Gardens 1" not in checked:
            $ count -= 1
            $ checked.append("Gift from the Master of Gardens 1")
            
            if count > 0:
                nvl clear
                jump gardensShopMenu
            else:
                return
        
        "[line[2]]" if "Gift from the Master of Gardens 2" not in checked:
            $ count -= 1
            $ checked.append("Gift from the Master of Gardens 2")
            
            if count > 0:
                nvl clear
                jump gardensShopMenu
            else:
                return
        
        "[line[3]]" if "Gift from the Master of Gardens 3" not in checked:
            $ count -= 1
            $ checked.append("Gift from the Master of Gardens 3")
            
            if count > 0:
                nvl clear
                jump gardensShopMenu
            else:
                return