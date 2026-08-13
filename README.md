# Scorpion Swamp Companion
A companion app for the gamebook Scorpion Swamp, primarily created to facilitate integration with the [Archipelago](https://archipelago.gg/) multiworld randomizer project.

## What does this do?
This program automates dice rolls, statistic tracking, and inventory management for Scorpion Swamp. It also ensures that the player cannot select any invalid options (usually due to lacking specific items). The program will tell the player what reference to read and list the valid options (if any) that the player can select from to go to next. As well, as many [errors](https://fightingfantasy.fandom.com/wiki/Scorpion_Swamp_(book)#Errors) as possible have been fixed. It can play the gamebook normally by default, but its main purpose is communication with the multiworld randomizer, Archipelago. By loading into Archipelago mode and connecting to a multiworld (TODO add link to the apworld's setup guide here), the player can play through the gamebook with its items in its various locations randomized per the player's settings. For example, when meeting Selator for the first time, rather than offering the player their choice of Spell Gems, he could instead offer the player nine items from the multiworld instead, some of which may be items for Scorpion Swamp, and some of which may be items for other games.

## What does this not do?
This program does not contain the text from the original book. The book is necessary to play the game, as it always has been. The program only does what is mentioned in the above section and is in no way a replacement for owning the book; it only offers automation and communication with Archipelago. Any text that appears is original and is for the facilitation of informing the player of Archipelago-specific changes. For example, in a vanilla playthrough of the gamebook, if the player is on either Selator or Poomchukker's questlines then the Mistress of Birds will call an Eagle to take the player to another clearing. In a randomized playthrough with certain options selected, it becomes necessary for the randomizer's logic that the player can then be brought back to the Mistress of Birds' clearing later from the clearing that they were brought to so text is added giving the player the option of returning using the Eagle. As this text is not present in the book, it has been added to this program. As well, text directly referencing gains or losses of statistics (for example: You lose 2 Stamina points) and text referencing statistic tests (for example: Test your Luck) has been retained for the sake of clarity. No surrounding text is included; all context must still be referenced from the book.

## Explaining the Preferences Menu
Several preferences are available in the Preferences menu that can be enabled or disabled as desired. Their purpose is both for quality of life and to help assist in reaching potentially difficult to reach sections of the book which can be important if the player wants to see everything in the gamebook or if they are playing in Arhcipelago mode and must visit certain references to send items into the multiworld. The Preferences are as follows:

### Ask for Luck in Combat?
If this is on then the player will be asked every round in combat whether they want to Test their Luck to potentially increase/decrease the damage done. This defaults to off as it is often undesirable to be repeatedly asked on a consistent basis, but this can be turned back on as the player wishes.

### Ask for Escape in Combat?
If this is on then the player will be asked every round in any combat that they can escape from whether they want to escape from the combat. This defaults to off as it is often undesirable to be repeatedly asked on a consistent basis, but this can be turned back on as the player wishes.

### Always Fail Statistic Tests?
If this is on then the player will always fail any tests of their statistics (for example: Test your Luck). This defaults to off as it is almost always undesirable but it can be useful for accessing certain references that require failing a roll when the player's statistics are high.

### Always Fail Combat Tests?
If this is on then the player will always lose in combat rounds. This defaults to off as it is almost always undesirable but it can be useful for accessing certain references that require doing poorly in a combat when the player's statistics are high.

### Ask to Connect to Archipelago?
If this is on then the player will be asked at the beginning of a new game if they want to connect to Archipelago. This defaults to on as connecting to Archipelago is the primary purpose of this program and the player can always just choose no when prompted to play the vanilla game instead, but if the player has no need of this functionality this can be turned off so that they do not receive the prompt at the start of every playthrough.

### Show Images?
If this is on then the images from the gamebook will be displayed in the program. The images are not included with the program by default; see below for more information. Because of that, this defaults to off as the notification that the images could not be loaded being shown where the images would be is likely undesirable. This should be turned on only if the player has supplied the images to avoid that.

## Supplying Images
The images from Scorpion Swamp are not included in this project but can be found on the [Fighting Fantasy wiki](https://fightingfantasy.fandom.com/wiki/Category:Images_from_Scorpion_Swamp) as they have more permissions than a project like this. From there, the player can download all of the images for their own personal use and can supply them to this program. To do so, open the "game/" directory in your installation directory and create a new directory called "images". Simply put all of the images downloaded from the wiki in that directory without changing their names. If this is done correctly and the Show Images preference (see above) is turned on, the images will be shown at the appropriate times during a playthrough, lasting for as long as they are relevant rather than just appearing at one reference.
