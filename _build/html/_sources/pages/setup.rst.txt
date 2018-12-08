Setup
=====


RFID - Radio-Frequency Identification
Game Setup Instructions -- Windows/Mac -- program is not optimized for Linux distributions

1.) Follow the instructions on https://www.python.org/downloads/ to download and install python 3.7.  We used the Pycharm python community editor.  https://www.jetbrains.com/pycharm/download/#section=windows.

1a.) Clone the repository onto your local machine- on the command line type:

.. code-block:: bash

   git clone https://github.com/tfredwell/cs4500.git

1b.) Navigate to the repository.

.. code-block:: bash

   cd CozmoTasteProject.

1c.) Install the Wx Library - First you need to add the path:

 
    C:\Users\PCName\AppData\Local\Programs\Python\Python37-32\Scripts 

to Environment Variable

2.)  Next open the command prompt and type:

   pip install wxpython

3.)  After that, open PyCharm and add the recently installed library to your environment.

4.)  --Navigate to File -> Settings -> Project. Under Project, click the plus bottom and the list of available packages will show. When you find the wxpython package, click Install package.

5.) Install all dependencies located within the requirements text file installed -- download application and type pip install -r  requirements.txt

6.) Make sure to install Itunes on Windows machines: https://support.apple.com/downloads/itunes
 Install Android Debug Bridge for Android devices: http://cozmosdk.anki.com/docs/getstarted.html#starting-up-the-sdk.

7.) Once the programs have been installed, connect the USB cord to the USB port and to either the phone or tablet with the Cozmo app installed. (picture of setup)


8.) Connect the phone or tablet to Cozmo via wifi. Open the Cozmo app, once on screen hit connect, the app will then start searching for Cozmo. If Cozmo is not found, follow the onscreen instructions to continue.
 
-- On the connected cell phone, turn off cellular data, make sure the device is not set to auto connect to any other network during gameplay. Possibly forget every network on the device and reconnect them at a later time. Otherwise, Cozmo will disconnect and will not respond.
-- If you still need further assistance with this step Follow step 1-4 under Starting Up the SDK http://cozmosdk.anki.com/docs/getstarted.html#starting-up-the-sdk to connect Cozmo in SDK mode.

8.) After successfully connecting to Cozmo, Double click the downloaded CozmoTasteGame app on the computer and click the start game button with Cozmos face under game controls. 

9.) Cozmo will then instruct you on which food he would like to taste.

10.) To replay the game or to have Cozmo change which food group he would like to taste simply press the (start game) button again.

11.) To quit the game, hit the X in the top right corner of the Cozmo Taste Game. Alternatively, you may use your phone by pressing disable SDK or by simply closing the app. 

Potential Issues with gameplay:

-Do not try to use ios device on Linux as it will not work properly.

-Connect Cozmo and RFID readers to a computer that has the proper software installed ( Listed above) or the program will not work properly.

-Each food item is assigned to only one food group.

--Example-- Peanuts would be considered a grain in this game even though it can be used as a protein.

-iPhone issues-- could not connect to Cozmo unless you first launch iTunes, the initial opening of iTunes allows the successful communication of an IOS device to the Cozmo robot.

