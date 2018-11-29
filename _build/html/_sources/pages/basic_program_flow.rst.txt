Basic Program Flow
===================

Connect Cozmo and RFID readers to computer that has proper software installed. After making sure all connected devices are attached, launch software on the computer, prepare to begin scanning food items.

Image Capture
------------------

We are using a RFID reader in order to capture the "Image" of the food being placed on the plate. Each food item is assigned a specific RFID code used to indicate the taste and the name of the food item to be later used while the program is running.

Game Loop
------------

The game is played through once automatically after checking whether the RFID reader is active. After a full run through of the game, the user is prompted on whether or not they want to play the game again or they would like to quit.

Food Analyzer
----------------

RFID reader scans a tagtakes each fruit tag and compares it with a stored value to determine which fruit has been chosen. Once a full plate has been made from the different food groups the "Plate" is cleared and ready to accept food again.


**References**

:mod:`cozmo_taste_game.image_recognition.response_analyzer`
