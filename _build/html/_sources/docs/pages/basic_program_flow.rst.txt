Basic Program Flow
===================

Connect Cozmo and RFID readers to the computer that has the proper software installed. After making sure all connected devices are attached, launch the Cozmo Taste Game Application on the computer, start the game and prepare to begin scanning food items.


Image Capture
------------------
We are using an RFID reader in order to capture the "Image" of the food items being scanned. Each food item is assigned a specific RFID code used to indicate the taste and the name of the food item.


Game Loop
------------

After all necessary software has been installed and a successful connection to the RFID reader has been made, the game is played through once by pressing Start Game button. Cozmo indicates the food group he is looking for the user to scan, the user is notified whether the food is correct, incorrect, or unknown. Once a correct item has been scanned, Cozmo will make a happy gesture repeating back the food item and its taste then the game terminates. Press the Start Game button again in order to start the next round of gameplay. Cozmo asks for food groups at random.

If at any time during the iteration you cannot find Cozmo's requested food group item press Start Game again to change the group, or add a new item to the items.csv file.



Food Analyzer
----------------
RFID reader scans a tag. If the tag is apart of the items.csv file then Cozmo will be able to identify it during gameplay. Otherwise, Cozmo will mention that the tag (food item) being scanned is unknown.
