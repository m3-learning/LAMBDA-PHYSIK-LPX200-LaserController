# LAMBDA-PHYSIK-LPX200-LaserController
- LPX200.py is a python script for controlling, monitoring and collecting data from a laser used for materials research
- LaserDataCollection.py is a script for colecting data about the laser and storing it in an hdf5 file 


This program creates a UI that is used to control the laser through the communication interface. The operating elements are breiefly described below. My program performs all the operations that the keypad does with the exception of the function keys.

![image](https://user-images.githubusercontent.com/61993180/186057836-513bcc6e-d6ec-43ef-ad39-239c5a09a9bc.png)




- A	RUN STOP key
- B	TRIGGER INT EXT key
- C	MODE key
- D	REPRATE / HV / EGY keys
- E	COUNTS keys
- F	GAS keys
- G	MENU keys
- H	Display
- I Function keys
- J	EGY CAL key
- K	BREAK key
- L	EXE key
- M	Cursor keys
- N	ENTER key
- O	Numerical input keys


![image](https://user-images.githubusercontent.com/61993180/186219386-27f01959-3cd1-4588-ac4d-2ede5d3dc2b3.png)




![image](https://user-images.githubusercontent.com/61993180/186057996-b0e5fcae-c638-4f1c-9a22-c652289f391d.png)


- A	Currently active operating mode (laser status) and status codea
- B	Running mode
- C	Repetition rate (internally set)
- D	Currently active charging voltage
- E	Currently emitted beam output energyb
- F	Laser tube pressure
- G	Gas mixture (gas menu)


After pressing one of the keys that enables a parameter setting to be changed (e.g. the MODE key), a prompt will appear in the bottom row of the display. Depending on the prompt, use the cursor buttons (right and left) to choose one of the items displayed in parenthesis or use the numerical input keys to enter a numerical value.

The numerical input keys (0 to 9 and decimal point) allow you to enter the numerical values that define parameters such as REPRATE (repetition rate), HV (charging voltage) and EGY (beam output power). The input is confirmed and executed by pressing the ENTER key.
Incorrect entries can be terminated prior to pressing ENTER, by pressing the CLEAR key.

The cursor keys (cursor left, cursor right) allow you to select a menu item, such as MENU, FLUSH and PURGE LINES and MODE. Press the cursor key that moves the cursor in the direction of the required item and then press ENTER to confirm the selection.

The ENTER key and the EXE (Execute) key is to be pressed to immediately start execution of the last selected function.

The BREAK key is to be pressed during data input or menu item selection to terminate the action. In this case, the previously active setting is retained.

The RUN STOP key starts and stops laser operation (emission of laser radiation) and prepares the laser device for shut down.
When the laser is off, press RUN STOP to start laser operation or shut down the laser device. When the laser is running, press RUN STOP to immediately stop laser emission.

The TRIGGER INT EXT key allows you to change between the internal and external trigger modes
When the laser is in EXT trigger mode, press the TRIGGER INT EXT key to change to the internal trigger mode. When the laser is in INT trigger mode, press the TRIGGER INT EXT key to change to the external trigger mode.

The MODE key allows you to select the desired running mode (HV/EGY PGR/ EGY NGR).
- HV selects the HV constant mode. In this mode, the high voltage remains constant. Consequently, the beam energy will slowly decrease during operation as the laser gas deteriorates.
- EGY PGR selects the energy constant mode with partial gas replacements. In this mode, the beam energy is kept constant by continuously increasing the high voltage (HV) to compensate for the deterioration of the laser gas. When the HV reaches a preset replacement value, the gas in the laser tube is replenished and the HV value is correspondingly reduced.
- EGY NGR selects the energy constant mode without partial gas replacements. When the HV has reached a given level, a message appears indicating that the gas in the laser tube requires replacing.

The keys REPRATE, HV and EGY allow you to change the repetition rate, charging voltage and beam output energy value.
- REPRATE enables the repetition rate to be changed for internally triggered laser operations. The repetition rate determines the number of laser pulses per second, i.e. the value is specified in Hz.
- HV enables the charging voltage to be set for laser operation in the HV constant mode. Pressing the HV key when an energy constant mode is currently active will display the HV value at which a partial gas replacement occurs.
- EGY enables the beam output energy value to be set for operations in the energy constant mode. The value is entered in mJ.
In each case press the appropriate key to select the parameter to be changed (REPRATE, HV or EGY), enter the value through the numerical input keys and confirm the input by pressing ENTER.

The COUNTS keys enable you to display and reset the laser device's pulse counters.
- SEL indicates the current reading of the Total Counter or the resettable User Counter:
 - The Total Counter counts the total number of laser pulses emitted by the laser since commissioning.
 - The User Counter counts the number of laser pulses emitted since the last counter reset.
After pressing COUNTS SEL, The desired counter is selected with the cursor keys and confirmed by pressing the ENTER key.
RESET allows you to reset the User Counter. After pressing COUNTS RESET, the user counter is reset to zero by pressing the EXE/ENTER key.

The MENU keys enable you to select or reset the laser device's gas menus.
- SEL allows different gas setting menus to be selected. If the COMPexPro is only to be operated with one gas mixture, this key has no function.
- RESET allows you to reset the values in the gas settings menu (gas partial pressures, gas mode, repetition rate and energy filter) to their factory settings. After pressing MENU RESET, the gas settings are reset to their factory settings by pressing the EXE/ENTER key.

The EGY CAL key selects a routine that allows the internal energy monitor to be calibrated according to an externally measured energy reading.

The function keys F1 to F10 allow various laser operating or display functions to be selected, but have not been configured yet.

The GAS keys allow various gas actions to be carried out. These gas actions are primarily required for maintenance purposes and should, therefore, only be carried out by correspondingly authorized and trained personnel.
- NEW FILL enables the program routine to be started that replaces the gases in the laser tube with fresh gas. .
- FLUSH LINE enables the program routine to be started that evacuates a specific gas line for two seconds. After pressing FLUSH LINE, a prompt appears indicating the currently selected gas line and displaying the further choices in parenthesis. A different gas line is selected with the cursor keys and confirmed by pressing ENTER.
- PURGE LINE enables the program routine to be started that evacuates a specific gas line for five seconds before filling the line with the gas connected to the inert gas connection. After pressing PURGE LINE, a prompt appears indicating the currently selected gas line and displaying the further choices in parenthesis. A different gas line is selected with the cursor keys and confirmed by pressing ENTER.
- PURGE RESERVOIR enables the program routine to be started that purges the laser tube. This routine is required for various maintenance work on the laser tube.
