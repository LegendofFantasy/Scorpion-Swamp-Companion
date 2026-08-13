init python:

    def dice(n):
        """Return the dice character matching the number n"""
        if n == 1:
            return "{size=+10}⚀{/size}"
        elif n == 2:
            return "{size=+10}⚁{/size}"
        elif n == 3:
            return "{size=+10}⚂{/size}"
        elif n == 4:
            return "{size=+10}⚃{/size}"
        elif n == 5:
            return "{size=+10}⚄{/size}"
        elif n == 6:
            return "{size=+10}⚅{/size}"
        return ""

    def roll():
        """Return a random integer from 1-6"""
        return renpy.random.randint(1, 6)

    def roll2():
        """Return two random integers from 1-6 in a list"""
        return [roll(), roll()]

    def diceBubble(c, b, rolls):
        """Displays a bubble from character c in bubble b showing the dice values in rolls"""
        set_dynamic_bubble(c, b)
        c("" + dice(rolls[0]) + dice(rolls[1]))
    
    def dieBubble(c, b, roll):
        """Displays a bubble from character c in bubble b showing the dice value in roll"""
        set_dynamic_bubble(c, b)
        c("" + dice(roll))

    class Statistic:
        """Models one of the player's statistics. n is the statistic's name and init is the inital value"""

        def __init__(self, n, init):
            """n is the statistic's name and init is the inital value"""
            self.name = n
            self.initial = init
            self.current = init
        
        def restore(self, x):
            """Restores statistic by x"""
            self.current = min(self.current + x, self.initial)

        def damage(self, x):
            """Damages statistic by x"""
            self.current = max(self.current - x, 0)
        
        def increase(self, x=1, fill=False):
            """Increases initial value by x and sets current to the new initial if fill is true"""
            self.initial += x
            if fill:
                self.current = self.initial
        
        def test(self, equal=True):
            """Rolls and displays 2d6. Returns True and notifies the player if they are successful and the opposite if not. Equal is false if the roll must be strictly lower"""
            if preferences.failTests:
                renpy.notify("Automatically failing test...")
                return False

            playerRoll = roll2()
            diceBubble(bp, bpBubble, playerRoll)
            if not equal:
                playerRoll[0] += 1
            if self.current >= (playerRoll[0] + playerRoll[1]):
                renpy.notify("Success!")
                return True
            else:
                renpy.notify("Failure...")
                return False

    class Item:
        """Models an inventory item. n is the item's name, q is the quantity, u is True if the item is usable, c is True if the item is consumed on use"""

        def __init__(self, n, q=1, u=False, c=False):
            self.name = n
            self.quantity = q
            self.usable = u
            self.consumed = c
        
        def add(self, x=1):
            """Increases quantity by x"""
            self.quantity += x
        
        def expend(self, x=1):
            """Reduces quantity by x, removing the item from the inventory if quantity becomes 0"""
            self.quantity -= x
            if self.quantity <= 0:
                if self.name in inventory.keys():
                    inventory.pop(self.name)
                if self.name in magic.keys():
                    magic.pop(self.name)
        
        def use(self):
            """Uses the item, executing appropriate code based on its name"""

            if self.name == "Skill Spell Gem":
                stats["Skill"].restore(stats["Skill"].initial // 2)
            if self.name == "Stamina Spell Gem":
                stats["Stamina"].restore(stats["Stamina"].initial // 2)
            if self.name == "Luck Spell Gem":
                stats["Luck"].restore(stats["Luck"].initial // 2)
            if self.name == "Magic Potion":
                nvl_clear()
                renpy.call("useMagicPotion", from_current=True)
                
            renpy.notify("Used " + self.name)
            if self.consumed:
                self.expend()
    
    class Provisions:
        """Models the current provisions in inventory. q is the starting quantity"""

        def __init__(self, q=10):
            self.quantity = q
        
        def eat(self, x=4):
            """Reduces provisions by 1 and increases Stamina by x"""
            self.quantity -= 1
            stats["Stamina"].restore(x)
        
        def add(self, x):
            """Increases provisions by x. x can be negative"""
            self.quantity = max(self.quantity + x, 0)
    
    class Enemy:
        """Models an enemy that the player fights against. n is the name, sk is its Skill, st is its Stamina, s is its damage done, t is placed before the name in combat"""

        def __init__(self, n, sk, st, s=2, t="the "):
            self.name = n
            self.skill = sk
            self.stamina = st
            self.strength = s
            self.the = t
        
        def damage(self, x=2):
            """Reduces the enemy's Stamina by x"""
            self.stamina = max(self.stamina - x, 0)

screen gameOver():
    # Shows the text 'Game Over'
    zorder 20

    vbox:
        at transform:
            xalign .5
            yalign .5
        
        text "GAME OVER":
            size 72
            color "#ff0000"
            outlines [(2, "#000000", 0, 0)]

screen victory():
    # Shows the text 'Victory!'
    zorder 20

    vbox:
        at transform:
            xalign .5
            yalign .5
        
        text "VICTORY!":
            size 72
            color "#ffd000"
            outlines [(2, "#000000", 0, 0)]

screen statScreen():
    # Shows all of the player's stats on the left side of the screen
    zorder 10

    frame:
        at transform:
            pos (5, 10)
        vbox:

            for s in stats:
                text "[stats[s].name]" xalign .5
                text "[stats[s].current]/[stats[s].initial]\n" xalign .5

screen itemMenu():
    # Shows the player's inventories on the right side of the screen
    zorder 10

    frame:
        at topright
        at transform:
            offset (-5, 10)
        vbox:
        
            textbutton "Inventory" action Show("inventoryScreen")
            if magic:
                textbutton "Magic" action Show("inventoryScreen", inv=magic)
            if ap:
                textbutton "Goal" action Show("goalScreen")
            if wizardsanity:
                textbutton "Wizards" action Show("listInventoryScreen", inv=wizards)
            if clearingsanity:
                textbutton "Clearings" action Show("listInventoryScreen", inv=clearingPasses, pf="Clearing ")
            #if provisions.quantity > 1:
            #    textbutton "Provisions" action Confirm("You have [provisions.quantity] provisions left. Eat one now?", Function(provisions.eat))
            #if provisions.quantity == 1:
            #    textbutton "Provisions" action Confirm("You have 1 provision left. Eat one now?", Function(provisions.eat))

screen inventoryScreen(inv=inventory):
    # Shows the player's inventory inv
    modal True

    zorder 20

    add "gui/overlay/confirm.png"

    if len(inv) >= 16:
        frame:
            at transform:
                xalign .5
                yalign .5
            vbox:
                grid int(1 + len(inv) / 15) int(len(inv) / int(1 + len(inv) / 15) + min(len(inv) % int(1 + len(inv) / 15), 1)):
                    spacing 15

                    for i in inv:
                        if inv[i].usable:
                            if inv[i].quantity > 1:
                                textbutton "[inv[i].name] x[inv[i].quantity]" action Function(inv[i].use) xalign .5
                            else:
                                textbutton "[inv[i].name]" action Function(inv[i].use) xalign .5
                        else:
                            if inv[i].quantity > 1:
                                text "[inv[i].name] x[inv[i].quantity]" xalign .5
                            else:
                                text "[inv[i].name]" xalign .5
            
                textbutton "Close" action Hide("inventoryScreen") xalign .5
    
    else:
        frame:
            at transform:
                xalign .5
                yalign .5
            vbox:

                for i in inv:
                    if inv[i].usable:
                        if inv[i].quantity > 1:
                            textbutton "[inv[i].name] x[inv[i].quantity]" action Function(inv[i].use) xalign .5
                        else:
                            textbutton "[inv[i].name]" action Function(inv[i].use) xalign .5
                    else:
                        if inv[i].quantity > 1:
                            text "[inv[i].name] x[inv[i].quantity]" xalign .5
                        else:
                            text "[inv[i].name]" xalign .5
            
                textbutton "Close" action Hide("inventoryScreen") xalign .5

screen listInventoryScreen(inv=clearingPasses, pf=""):
    # Shows the player's inventory inv that is a list instead of a dict, with prefix pf
    modal True

    zorder 20

    add "gui/overlay/confirm.png"

    if len(inv) >= 16:
        frame:
            at transform:
                xalign .5
                yalign .5
            vbox:
                grid int(1 + len(inv) / 15) int(len(inv) / int(1 + len(inv) / 15) + min(len(inv) % int(1 + len(inv) / 15), 1)):
                    spacing 15

                    for i in inv:
                        text "[pf][i]" xalign .5
            
                textbutton "Close" action Hide("listInventoryScreen") xalign .5
    
    else:
        frame:
            at transform:
                xalign .5
                yalign .5
            vbox:

                for i in inv:
                    text "[pf][i]" xalign .5
            
                textbutton "Close" action Hide("listInventoryScreen") xalign .5

screen goalScreen():
    modal True

    zorder 20

    add "gui/overlay/confirm.png"

    frame:
        at transform:
            xalign .5
            yalign .5
        vbox:

            if goal == "any":
                text "Complete any quest"
            elif goal == "grimslade":
                text "Complete Grimslade's quest"
            elif goal == "selator":
                text "Complete Selator's quest"
            elif goal == "poomchukker":
                text "Complete Poomchukker's quest"
            elif goal == "all":
                if "selator" in goals_complete:
                    text "{s}Complete Selator's quest{/s}"
                else:
                    text "Complete Selator's quest"
                if "poomchukker" in goals_complete:
                    text "{s}Complete Poomchukker's quest{/s}"
                else:
                    text "Complete Poomchukker's quest"
                if "grimslade" in goals_complete:
                    text "{s}Complete Grimslade's quest{/s}"
                else:
                    text "Complete Grimslade's quest"
            
            textbutton "Close" action Hide("goalScreen") xalign .5

screen enemyStatScreen(e):
    # Shows the current enemy's (e) stats on the right side of the screen
    zorder 10

    frame:
        at topright
        at transform:
            offset (-5, 10)
        vbox:

            text "[e.name]\n" xalign .5
            text "Skill" xalign .5
            text "[e.skill]\n" xalign .5
            text "Stamina" xalign .5
            text "[e.stamina]\n" xalign .5

label battle(e, escapable=False, returnStamina=0, escapeTurn=0):
    # Runs a battle against enemy e, returning when the enemy's stamina is returnStamina. escapable is true if escape is possible and escapeTurn is how many turns have to pass before escape is possible

    nvl clear
    window hide

    hide screen itemMenu with moveoutright
    show screen enemyStatScreen(e) with moveinright

    bn "[e.the!cl][e.name] attacks!"

    if dwarfPotion:
        bn "The dwarven potion you drank takes effect..."
        $ stats["Skill"].damage(1)

    while True:

        if preferences.askEscape and escapable and escapeTurn <= 0:
            if renpy.confirm("Do you want to escape?"):

                bn "[e.the!cl][e.name] hit you as you escape!"
                $ currentDamage = e.strength

                if preferences.askLuck:
                    if renpy.confirm("Do you want to test your luck?"):

                        if stats["Luck"].test():
                            $ currentDamage -= 1
                        else:
                            $ currentDamage += 1
                    
                        $ stats["Luck"].damage(1)
            
                $ stats["Stamina"].damage(currentDamage)
                bn "You took [currentDamage] damage!"
                window show
                return "escaped"

        python:
            playerRoll = roll2()
            diceBubble(bp, bpBubble, playerRoll)
            enemyRoll = roll2()
            diceBubble(be, beBubble, enemyRoll)
        
        if not preferences.failCombat and ((stats["Skill"].current + playerRoll[0] + playerRoll[1]) > (e.skill + enemyRoll[0] + enemyRoll[1])):

            bn "You hit [e.the][e.name]!"
            $ currentDamage = playerDamage

            if askLuck:
                if renpy.confirm("Do you want to test your luck?"):
                    if stats["Luck"].test():
                        $ currentDamage += 2
                    else:
                        $ currentDamage -= 1

                    $ stats["Luck"].damage(1)
            
            $ e.damage(currentDamage)
            bn "You dealt [currentDamage] damage!"
        
        elif preferences.failCombat or ((stats["Skill"].current + playerRoll[0] + playerRoll[1]) < (e.skill + enemyRoll[0] + enemyRoll[1])):

            bn "[e.the!cl][e.name] hit you!"
            $ currentDamage = e.strength

            if preferences.askLuck:
                if renpy.confirm("Do you want to test your luck?"):

                    if stats["Luck"].test():
                        $ currentDamage -= 1
                    else:
                        $ currentDamage += 1
                    
                    $ stats["Luck"].damage(1)
            
            $ stats["Stamina"].damage(currentDamage)
            bn "You took [currentDamage] damage!"
        
        else:

            bn "You and [e.the][e.name] were tied! No one takes any damage this round!"
        
        if stats["Stamina"].current == 0:
            
            bn "[e.the!cl][e.name] has slain you..."
            jump gameover
        
        if e.stamina == 0:

            bn "You have slain [e.the][e.name]!"

            hide screen enemyStatScreen with moveoutright
            show screen itemMenu with moveinright

            if dwarfPotion:
                bn "The effects of the dwarven potion end!"
                $ stats["Skill"].restore(1)
                $ dwarfPotion = False

            return
        
        if e.stamina <= returnStamina:

            hide screen enemyStatScreen with moveoutright
            show screen itemMenu with moveinright

            if dwarfPotion:
                bn "The effects of the dwarven potion end!"
                $ stats["Skill"].restore(1)
                $ dwarfPotion = False

            window show
            return
        
        if escapeTurn:
            $ escapeTurn -= 1

label multibattle(enemies, escapable=False, escapeTurn=0):
    # Runs a battle against enemies fighting all at once. escapable is true if escape is possible and escapeTurn is how many turns have to pass before escape is possible

    nvl clear
    window hide
    hide screen itemMenu with moveoutright

    $ i = 0
    $ j = len(enemies) - 1
    $ attackers = ""

    if not j == 1:
        while i < j:
            $ attackers +=  enemies[i].name + ", "
            $ i += 1
    else:
        $ attackers += enemies[i].name + " "
    
    $ attackers += "and " + enemies[j].name

    if not j == 1:
        $ attackers += " all attack!"
    else:
        $ attackers += " both attack!"

    bn "[attackers]"

    if dwarfPotion:
        bn "The dwarven potion you drank takes effect..."
        $ stats["Skill"].damage(1)

    while True:
        $ firstEnemy = True
        $ currentEnemy = 0
        while currentEnemy < len(enemies):
            $ e = enemies[currentEnemy]
            show screen enemyStatScreen(e) with moveinright

            if preferences.askEscape and escapable and escapeTurn <= 0:
                if renpy.confirm("Do you want to escape?"):

                    bn "[e.the!cl][e.name] hit you as you escape!"
                    $ currentDamage = e.strength

                    if preferences.askLuck:
                        if renpy.confirm("Do you want to test your luck?"):

                            if stats["Luck"].test():
                                $ currentDamage -= 1
                            else:
                                $ currentDamage += 1
                    
                            $ stats["Luck"].damage(1)
            
                    $ stats["Stamina"].damage(currentDamage)
                    bn "You took [currentDamage] damage!"
                    window show
                    return "escaped"
            python:
                playerRoll = roll2()
                diceBubble(bp, bpBubble, playerRoll)
                enemyRoll = roll2()
                diceBubble(be, beBubble, enemyRoll)
        
            if not preferences.failCombat and ((stats["Skill"].current + playerRoll[0] + playerRoll[1]) > (e.skill + enemyRoll[0] + enemyRoll[1])):

                if firstEnemy:

                    bn "You hit [e.the][e.name]!"
                    $ currentDamage = playerDamage

                    if preferences.askLuck:
                        if renpy.confirm("Do you want to test your luck?"):

                            if stats["Luck"].test():
                                $ currentDamage += 2
                            else:
                                $ currentDamage -= 1
                    
                            $ stats["Luck"].damage(1)
            
                    $ e.damage(currentDamage)
                    bn "You dealt [currentDamage] damage!"

                else:

                    bn "You blocked the attack from [e.the][e.name]!"
        
            elif preferences.failCombat or ((stats["Skill"].current + playerRoll[0] + playerRoll[1]) < (e.skill + enemyRoll[0] + enemyRoll[1])):

                bn "[e.the!cl][e.name] hit you!"
                $ currentDamage = e.strength

                if preferences.askLuck:
                    if renpy.confirm("Do you want to test your luck?"):

                        if stats["Luck"].test():
                            $ currentDamage -= 1
                        else:
                            $ currentDamage += 1
                    
                        $ stats["Luck"].damage(1)
            
                $ stats["Stamina"].damage(currentDamage)
                bn "You took [currentDamage] damage!"
        
            else:

                bn "You and [e.the][e.name] were tied! No one takes any damage this round!"
        
            if stats["Stamina"].current == 0:
            
                bn "[e.the!cl][e.name] has slain you..."
                jump gameover
        
            if e.stamina == 0:

                bn "You have slain [e.the][e.name]!"
                hide screen enemyStatScreen with moveoutright
                $ enemies.remove(e)

                if len(enemies) == 0:

                    show screen itemMenu with moveinright

                    if dwarfPotion:
                        bn "The effects of the dwarven potion end!"
                        $ stats["Skill"].restore(1)
                        $ dwarfPotion = False
                    
                    window show

                    return
            else:
                $ firstEnemy = False
                $ currentEnemy += 1
            
                if not len(enemies) == 1:
                    hide screen enemyStatScreen with moveoutright