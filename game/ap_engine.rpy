init python:
    import os
    import json

    if "localappdata" in os.environ:
        CONNECTIONS_PATH = os.path.expandvars(r"%localappdata%/AP Fighting Fantasy/Scorpion Swamp")
        CACHE_PATH = os.path.expandvars(r"%localappdata%/AP Fighting Fantasy/cache")
    else:
        CONNECTIONS_PATH = os.path.expandvars(r"$HOME/AP Fighting Fantasy/Scorpion Swamp")
        CACHE_PATH = os.path.expandvars(r"$HOME/AP Fighting Fantasy/cache")
    if not os.path.exists(CONNECTIONS_PATH):
        os.makedirs(CONNECTIONS_PATH)
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)

    def game_watcher():

        send_locations(store.checked)
        get_items()
        if not store.scouts:
            get_scouts_file()
    
    def send_locations(locations):

        for location in locations:
            with open(os.path.join(CONNECTIONS_PATH, "send" + str(LOCATION_NAME_TO_ID[location])), 'w') as f:
                f.close()
    
    def send_hints(locations):

        for location in locations:
            with open(os.path.join(CONNECTIONS_PATH, "hint" + str(LOCATION_NAME_TO_ID[location])), 'w') as f:
                f.close()
    
    def get_items():

        new_items = []

        for root, dirs, files in os.walk(CONNECTIONS_PATH):
            for f in files:
                if f.startswith("AP"):
                    if f not in store.collected:
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            new_items.append(int(current.readline()))
                            current.close()
                        store.collected.append(f)
        if new_items:
            renpy.call("receive_items", new_items, from_current=True)

    def get_scouts_file():
        for root, dirs, files in os.walk(CACHE_PATH):
            for f in files:
                if f.startswith(store.scouts_filename):
                    with open(os.path.join(CACHE_PATH, store.scouts_filename), 'r') as f:
                        store.scouts = json.loads(f.readline())
                        f.close()
    
    def read_files():

        found_files = 0

        for root, dirs, files in os.walk(CONNECTIONS_PATH):
            for f in files:
                if f.startswith("scouts"):
                    with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                        store.scouts_filename = current.readline()
                        current.close()
                    found_files += 1

                if f.endswith(".cfg"):
                    
                    if f.startswith("goal"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            g = current.readline()
                            match int(g):
                                case 0:
                                    store.goal = "any"
                                case 1:
                                    store.goal = "selator"
                                case 2:
                                    store.goal = "poomchukker"
                                case 3:
                                    store.goal = "grimslade"
                                case 4:
                                    store.goal = "all"
                            current.close()
                        found_files += 1
                    
                    if f.startswith("required_amulets"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.required_amulets = int(current.readline())
                            current.close()
                        found_files += 1

                    if f.startswith("clearingsanity"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.clearingsanity = True
                            current.close()
                        found_files += 1
                    
                    if f.startswith("spellsanity"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.spellsanity = True
                            current.close()
                        found_files += 1
                    
                    if f.startswith("wizardsanity"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.wizardsanity = True
                            current.close()
                        found_files += 1
                    
                    if f.startswith("extra_locations"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.extra_locations = True
                            current.close()
                        found_files += 1
        
        # Not enough files were found, so something has gone wrong
        if found_files < 7:
            renpy.call("file_error")
        
        get_scouts_file()
        
        # No scouts file found; request the client to send one
        if not store.scouts:
            with open(os.path.join(CONNECTIONS_PATH, "request_scouts"), 'w') as f:
                f.close()    
                
    def check_goal():
        for root, dirs, files in os.walk(CONNECTIONS_PATH):
            for f in files:
                if f.startswith("grimslade"):
                    if f not in store.goals_complete:
                        store.goals_complete.append(f)
                if f.startswith("selator"):
                    if f not in store.goals_complete:
                        store.goals_complete.append(f)
                if f.startswith("poomchukker"):
                    if f not in store.goals_complete:
                        store.goals_complete.append(f)
    
    def get_scout(location):

        return scouts[str(LOCATION_NAME_TO_ID[location])]

    def get_colour(flags):

        if flags & 0b001 == 0b001: # Progression
            return "#AF99EF"
        elif flags & 0b100 == 0b100: # Trap
            return "#FA8072"
        elif flags & 0b010 == 0b010: # Useful
            return "#6D8BE8"
        else: # Filler
            return "#00EEEE"

    def notify_item(location):

        renpy.notify("Found " + get_item_string(location) + "!")
    
    def get_item_string(location, mode="for"):
        # if mode is not "for", it will return "player's item" instead

        scout = get_scout(location)
        item = scout["item"]
        player = scout["player"]
        colour = get_colour(scout["flags"])

        if mode == "for":
            return "{color=" + colour + "}" + item + "{/color} for " + player
        return player + "'s {color=" + colour + "}" + item + "{/color}"

# This is the list of locations that have been checked by the player listed by their names
default checked = []
# This is the list of Archipelago Items that have been received by their filenames
default collected = []
# This should be True once the victory condition has been met
default victory_achieved = False
# This should be True if we want to receive items without displaying any messages
default receive_silently = True
# This tracks which goals are complete
default goals_complete = []
# This tracks the filename of the scouts file in the cache
default scouts_filename = ""

label after_load:
    # This ensures that the loaded save is from the same multiworld slot
    if ap:
        hide screen progression_watcher
        python:
            found_files = 0
            for root, dirs, files in os.walk(CONNECTIONS_PATH):
                for f in files:
                    if f.startswith("scouts"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if store.scouts_filename == current.readline():
                                found_files = 1
                            current.close()
                        break
        if found_files == 0:
            nvl clear
            """
            The loaded save file was not made while playing the currently connected slot. Either you are not connected to Archipelago, or you are not connected to the right
            slot. Returning to the title screen.
            """
            $ renpy.set_return_stack([])
            return
        show screen progression_watcher

    # This ensures that the victory file gets rewritten to connections if it somehow got missed
    if victory_achieved:
        python:
            if not renpy.loadable("victory", directory=CONNECTIONS_PATH):
                with open(os.path.join(CONNECTIONS_PATH, "victory"), 'w') as f:
                    f.close()
    return

label receive_items (items=[]):
    # This is called by the get_items function in ap_engine.rpy. It just calls receive_item for all the new items
    hide screen progression_watcher
    while items:
        call receive_item(items.pop(0)) from _call_recieve_item
    nvl clear
    show screen progression_watcher
    return

label receive_item (item=1):
    # This is only called by receive_items; it gives the passed item to the player
    # Add functionality in the next line if needed
    python:
        item_name = ID_TO_ITEM_NAME[item]

        if "Spell Gem" in item_name:
            if item_name in magic.keys():
                magic[item_name].add()
            else:
                if item_name in {"Skill Spell Gem", "Stamina Spell Gem", "Luck Spell Gem"}:
                    magic[item_name] = Item(item_name, 1, True, True)
                else:
                    magic[item_name] = Item(item_name)
        
        elif "Clearing" in item_name:
            number = item_name.split()[1] # This will strip "Clearing " from the item name, leaving just the number
            if number not in clearingPasses:
                clearingPasses.append(number)
                clearingPasses.sort(key = lambda n: int(n))
        
        elif "Progressive" in item_name:
            progressiveStats[item_name.split()[1]] += 1 # This will strip "Progressive " from the item name, leaving just the stat name to be incremented
        
        elif item_name == "Secret Word":
            wordKnown = True

        elif item_name in {"Selator", "Grimslade", "Poomchukker"}:
            if item_name not in wizards:
                wizards.append(item_name)

        else:
            if item_name in inventory.keys():
                inventory[item_name].add()
            else:
                if item_name == "Magic Potion":
                    inventory[item_name] = Item(item_name, 1, True, True)
                else:
                    inventory[item_name] = Item(item_name)

                    if item_name == "Great Magic Sword":
                        if stats:
                            ri_temp = stats["Skill"].initial - stats["Skill"].current
                            extraSkill += max(0, 2 - ri_temp)
                            stats["Skill"].restore(min(2, ri_temp))
                        else:
                            extraSkill += 2
                    elif item_name in {"Magic Sword", "Ranger's Helmet"}:
                        if stats:
                            ri_temp = stats["Skill"].initial - stats["Skill"].current
                            extraSkill += max(0, 1 - ri_temp)
                            stats["Skill"].restore(min(1, ri_temp))
                        else:
                            extraSkill += 1
    
    if not receive_silently:
        show screen get_item(item_name) with moveintop
        "{nw}"
    return

label send_victory:
    # This is called when the victory condition has been met
    python:
        victory_achieved = True
        with open(os.path.join(CONNECTIONS_PATH, "victory"), 'w') as f:
            f.close()
    return

label file_error:
    # This is called if something has gone wrong with the files
    "One or more files are missing. Make sure that you have the Scorpion Swamp Client running and connected to your room and slot."
    $ renpy.set_return_stack([])
    return
    

screen get_item(message):
    # This screen displays what item has just been received.

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _("Recieved [message]!"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("OK") action Hide(None, moveoutbottom)

    ## Right-click and escape also close.
    key "game_menu" action Hide(None, moveoutbottom)

screen progression_watcher():
    # This screen is a constantly running watcher for locations to send to Archipelago and for items received from Archipelago

    timer 0.1 action Function(game_watcher) repeat True
