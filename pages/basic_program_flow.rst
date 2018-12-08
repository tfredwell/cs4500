Basic Program Flow
===================

Connect Cozmo and RFID readers to computer that has proper software installed. After making sure all connected devices are attached, launch software on the computer, prepare to begin scanning food items.

Image Capture
------------------

We are using a RFID reader in order to capture the "Image" of the food being placed on the plate. Each food item is assigned a specific RFID code used to indicate the taste and the name of the food item to be later used while the program is running.

Game Loop
------------

 After all necessary software has been installed and successful connection to the RFID reader, the game is played through once by pressing start game. Cozmo indicates what the type of food he is looking for, the user is notified whether the food is correct, incorrect, or unknown. Once a correct item has been scanned, Cozmo will make a happy gesture repeating back the food item and its taste then the game terminates. Press the Start Game button again in order to start the next iteration of gameplay. 
-- If at any time during the iteration you cannot find Cozmo's requested food group item simply press Start Game again to change the group.

Food Analyzer
----------------

 RFID reader scans a tag. If the tag is apart of the items.csv file then Cozmo will be able to identify it during gameplay. Otherwise, Cozmo will mention that the tag (food item) being scanned is unknown.

**References**

:mod:`cozmo_taste_game.image_recognition.response_analyzer`
