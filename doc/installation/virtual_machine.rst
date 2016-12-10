Use G-OnRamp via Virtual Machine
================================

Requirements
------------

1. Download and install Virtual Box => https://www.virtualbox.org
2. Download our G-OnRamp image => https://wustl.box.com/s/nx5g5hfqbfkk0h7w4i1m6325s6fen7eu

Step by step installation
-------------------------
1. Import Appliance 

  First, start the VirtualBox and go to "File->Import Appliance". Then choose the G-OnRamp image to import and click on "Continue". Remember to check "Reinitialize the MAC address of all network cards" and then click on "Import".

2. Start the G-OnRamp VM instance

  - Start the G-OnRamp virtual machine in the VirtualBox.
  - Open the terminal in your computer. Type the command line "ssh galaxy@192.168.56.11"
  - Enter the password: 2016


3. Start the Galaxy server

  Go to the Galaxy directory (the folder named "galaxy") by typing command line "cd galaxy". Then start the server by typing command line "sh run.sh". You can access to the Galaxy => http://192.168.56.11:8080/gonramp/

  Login in to the Galaxy:
   
  - Admin user:
  
    - username: galaxyadmin    
    - password: 12341234

4. G-OnRamp workflow 

  G-OnRamp workflow is shared in the shared Workflow. All the G-OnRamp tools are already installed in the "G-OnRamp" section in the tool panel. 
  To run G-OnRamp, first import G-OnRamp workflow from shared Workflow, then upload your datasets, and finally run the G-OnRamp workflow. 




Modifying Galaxy (updates or customizations)
--------------------------------------------

  You can customize the current workflow by editing the workflow. If new tools are needed, login to the admin account and install the new tools.
  
