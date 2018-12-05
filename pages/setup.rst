Setup
=====


RFID - Radio-Frequency Identification
Game Setup Instructions -- Windows/Mac -- program is not optimized for Linux distributions

1.) Follow the instructions on https://www.python.org/downloads/ to download and install python 3.7.

2.) Clone the repository onto your local machine.

.. code-block:: bash

   git clone https://github.com/tfredwell/cs4500.git

3.) Navigate to the repository.

.. code-block:: bash

   cd CozmoTasteProject.

4.) Install all dependencies located within the requirements text file installed -- download application and type pip install -r  requirements.txt

5.) Make sure to install Itunes on Windows machines: https://support.apple.com/downloads/itunes
 Install Android Debug Bridge for Android devices: http://cozmosdk.anki.com/docs/getstarted.html#starting-up-the-sdk.

6.) Once the programs have been installed, connect the USB cord to the USB port and to either the phone or tablet with the Cozmo app installed. (picture of setup)

7.) Connect the phone or tablet to Cozmo via wifi. Open the Cozmo app, once on screen hit connect, the app will then start searching for Cozmo. /ss/(phone) 
-- On the connected cell phone, turn off cellular data, make sure the device is not set to auto connect to any other network during gameplay. Possibly forget every network on the device and reconnect them at a later time. Otherwise, Cozmo will disconnect and will not respond.

8.) With a successful connection to Cozmo, Double click CozmoTasteGame app on computer Click on the start game button with Cozmos face under game controls. /ss/

9.) Cozmo will then instruct you on which food he would like to taste.

10.) To replay the game or to have Cozmo change which food group he would like to taste simply press the (start game) button again.

11.) To quit the game, simply hit the red X in the top corner. On your phone, click disable SDK or you may close the app. /sss/

Potential Issues with gameplay
-Do not try to use ios device on Linux as it will not work properly.
-Connect Cozmo and RFID readers to a computer that has the proper software installed ( Listed above) or the program will not work properly.
-Each food item is assigned to only one food group.
--Example-- Peanuts would be considered a grain in this game even though it can be used as a protein.
-iPhone issues-- could not connect to Cozmo unless you first launch iTunes, the initial opening of iTunes allows the successful communication of an IOS device to the Cozmo robot.

