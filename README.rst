.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/LAMBDA-PHYSIK-LPX200-LaserController.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/LAMBDA-PHYSIK-LPX200-LaserController
    .. image:: https://readthedocs.org/projects/LAMBDA-PHYSIK-LPX200-LaserController/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://LAMBDA-PHYSIK-LPX200-LaserController.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/LAMBDA-PHYSIK-LPX200-LaserController/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/LAMBDA-PHYSIK-LPX200-LaserController
    .. image:: https://img.shields.io/pypi/v/LAMBDA-PHYSIK-LPX200-LaserController.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/LAMBDA-PHYSIK-LPX200-LaserController/
    .. image:: https://img.shields.io/conda/vn/conda-forge/LAMBDA-PHYSIK-LPX200-LaserController.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/LAMBDA-PHYSIK-LPX200-LaserController
    .. image:: https://pepy.tech/badge/LAMBDA-PHYSIK-LPX200-LaserController/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/LAMBDA-PHYSIK-LPX200-LaserController
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/LAMBDA-PHYSIK-LPX200-LaserController

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|
LPX 200 Laser Controller
========================

**LPX 200 Laser Controller** is a Python-based application that provides a graphical user interface (GUI) to control the Lambda Physik LPX 200 Laser. It allows users to poll the system status, execute commands, and log energy readings from the laser system into an SQLite database.

Features
--------

- **Automatic Serial Port Detection**: Automatically finds and connects to the correct serial port where the laser is connected.
- **Control Laser Operations**: Perform operations like starting, stopping, and setting laser parameters such as voltage and energy.
- **Real-time Status Polling**: The GUI continuously polls and updates the laser status every second.
- **Energy Logging**: Automatically logs energy data into an SQLite database when the laser is active.
- **PyQt5 Interface**: A PyQt5-based user interface for ease of use.

Installation
------------
1. **Clone the repository**:
   
   Clone the repository to your local machine:

   .. code-block:: bash

      git clone https://github.com/m3-learning/LAMBDA-PHYSIK-LPX200-LaserController.git
      cd LAMBDA-PHYSIK-LPX200-LaserController

2. **Install the package**:

   Use the following command to install the package along with its dependencies. This will install the `lpx200` package in editable mode (useful for development and modifications):

   .. code-block:: bash

      pip install -e .

3. **Verify installation**:

   After installation, verify that the package is installed correctly by listing the installed packages:

   .. code-block:: bash

      pip list

   You should see `lpx200` listed as an installed package.


Initializing the Laser Controller GUI
=====================================

To start the Lambda Physik LPX 200 laser controller GUI, follow these steps:

1. Ensure that the necessary dependencies are installed by running the following command:

   .. code-block:: bash

      pip install -r requirements.txt

2. Run the script to initialize the GUI:

   .. code-block:: bash

      python src/lpx/LPX200.py

3. The GUI will open, displaying various buttons and text areas for controlling and monitoring the laser. Below is an image of the initial GUI interface:

.. image:: ../images/laser_controller_initial_gui.png
   :alt: Initial Laser Controller GUI
   :width: 500px

* The "Laser Status" section displays the current mode, repetition rate, high voltage, energy, and pressure.
* The "Command Entry" section allows you to enter commands, while the "Responses" section shows feedback from the laser controller.
* Various buttons are available for controlling different aspects of the laser system (e.g., `RUN STOP`, `MODE`, `HV`, etc.).

Once the GUI is open, you can use the buttons to control the laser and monitor its status.


The program will automatically detect the correct serial port that the laser is connected to and establish communication. Once started, you can interact with the laser via the buttons and commands provided in the interface.


Control Commands
================

This section explains how to send different control commands to the Lambda Physik LPX 200 laser using the buttons in the GUI. Each command is sent by clicking a specific button, and the response or status updates are displayed in the **Responses** and **Laser Status** sections.

Below are examples of commonly used commands and their expected output in the display.

1. **Starting the Laser (RUN STOP)**
   ---------------------------------
   To start the laser, use the `RUN STOP` button.

   - **Action**: Click the `RUN STOP` button.
   - **Expected Output**: The **Command Entry** section will update to show that the laser is being set to "OPMODE=ON" mode. 
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.The system will initiate the laser start sequence with a starting delay of approximately 4.1 seconds (as noted in section 3.8).
   - **Responses**: The **Responses** section will display the status of the laser operation. 
      Potential states include:
         - ON: Laser is on, with no warnings or messages.
         - ON:0: Laser is on, with no warnings or messages (only available for certain laser types).
   - **Possible Warnings During OPMODE=ON**:
      When the `ENTER` button is pressed, the following warnings may appear in the **Responses** section if issues are detected during operation:

      - **ON:2**: Preset energy too high; Charging HV exceeds the threshold.
      - **ON:03**: Duty cycle exceeded (more than 12,000 pulses in 20 minutes).
      - **ON:8**: New gas fill needed; Charging HV exceeds HV\ :sub:`repl`.
      - **ON:9**: No vacuum detected during halogen injection; pressure did not reach 30 mbar after 130 seconds.
      - **ON:10**: Low pressure during new fill procedure; fluorine source may be empty.
      - **ON:13**: Fluorine valve not open; valve test failed.
      - **ON:34**: Halogen injection in preparation.
      - **ON:36**: Charge On Demand (COD) mode is active.
      - **ON:37**: Repetition rate warning; COD mode running above 50 Hz.
      - **ON:40**: Input energy is too low; output energy remains above setpoint.
      - **ON:41**: Energy value too high; entered energy exceeds the menu parameter by more than 5%.


   .. image:: ../images/run_button_example.png
      :alt: RUN STOP Button Example
      :width: 500px

   *Example Output in Laser Status:*
   ::
      
      MODE: HV   1 Hz 18.0 kV 150 mJ 4000 mbar

2. **Stopping the Laser (RUN STOP)**
   ---------------------------------

   To stop the laser, use the `RUN STOP` button.

   - **Action**: Click the `RUN STOP` button.
   - **Expected Output**: The **Command Entry** section will update to show that the laser is being set to "OPMODE=OFF" mode.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser. The system will switch off the laser.
   - **Responses**: The **Responses** section will display the status of the laser operation. Potential states include:
     - OFF: Laser is off, no messages or warnings.
     - OFF:0: Laser is off, no messages or warnings (only available with certain lasers).
     - OFF, WAIT: Laser is waiting for power supply standby and gas circulation fan powering up (duration: 4.1 seconds).

   **Possible Warnings During OPMODE=OFF**:

   When the `ENTER` button is pressed, the following warnings may appear in the **Responses** section if issues are detected:

   - **OFF:1**: Laser off, an **INTERLOCK** occurred.
   - **OFF:2**: Laser off, **PRESET ENERGY TOO HIGH**; charging HV exceeds HV\ :sub:`max`.
   - **OFF:4**: Laser off, a **WATCHDOG** has been activated.
   - **OFF:5**: Laser off, **FATAL ERROR**; LWL-DATALINK failed (LWL Datalink means the Data Ring).
   - **OFF:6**: Laser off, **POLLING**; at least one laser module did not respond.
   - **OFF:7**: Laser off, **ENERGY CAL. ERROR**; monitor calibration values cannot be adjusted within a range of 99 to 200.
   - **OFF:8**: Laser off, **NEW GAS FILL NEEDED**; charging HV exceeds HV\ :sub:`max`.
   - **OFF:9**: Laser off, **NO VACUUM**; tube may be leaky, but a safety fill was performed successfully.
   - **OFF:10**: (with a fluorine source only) Laser off, **LOW PRESSURE**; sixth fluorine fill did not succeed, source is empty.
   - **OFF:11**: (with a halogen source only) Laser off, **NO CAPACITY LEFT**; halogen source is empty.
   - **OFF:12**: (with a halogen source only) Laser off, **ERROR TEMPERATURE MEASUREMENT**; halogen source temperature measurement failed.
   - **OFF:13**: (with a fluorine source only) Laser off, **FLUORINE VALVE NOT OPEN**; valve test failed or malfunction during filling.
   - **OFF:21**: **WARM-UP 8 min**; laser devices are in the warm-up phase as required by the thyratron.
   - **OFF:26**: Laser off, **LOW LIGHT**; energy monitor does not detect pulses after trigger pulses. This occurs if at least 30% of pulses within 10 seconds are missing.

   .. image:: ../images/stop_button_example.png
      :alt: RUN STOP Button Example
      :width: 500px

   *Example Output in Laser Status:*

   ::
      
      MODE: HV   1 Hz 18.0 kV 150 mJ 4000 mbar

3. **Setting High Voltage (HV)**
   -----------------------------
   The `HV` button allows you to set the high voltage level.

   - **Action**: Click the `HV` button to open the voltage setting dialog, then enter the desired voltage using the number buttons.
   - **Expected Output**: The **Command Entry** section will update to show the set voltage level.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.

   **Details for HV Setting**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Description**: Sets the charging voltage for the HV constant mode. Ignored in other modes.
   - **Availability**: This command is available in all operating modes.
   - **Parameter Range**: Depends on the factory settings for the gas menu. This command accepts values to one decimal place.

   .. image:: ../images/hv_button_example.png
      :alt: HV Button Example
      :width: 500px

   *Example Output in Laser Status if HV=1:*
   ::
      
      MODE: HV   1 Hz 18.0 kV 0 mJ 3611 mbar

4. **Changing the Repetition Rate (REP RATE)**
   -------------------------------------------
   The `REP RATE` button allows you to set the repetition rate of the laser.

   - **Action**: Click the `REP RATE` button, then enter the desired repetition rate using the number buttons.
   - **Expected Output**: The **Laser Status** section will display the updated repetition rate.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.

   **Details for REP RATE Setting**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Description**: Sets the internal repetition rate if `TRIGGER=INT` has been set. If not, the value is remembered as the repetition rate when switched to `TRIGGER=INT`.
   - **Availability**: This command is available in **ON** and **OFF** operating modes only.
   - **Parameter Range**: Depends on the factory settings of the Gas Menu. High repetition rates may be declined for high HV values.


   .. image:: ../images/rep_rate_button_example.png
      :alt: REP RATE Button Example
      :width: 500px

   *Example Output in Laser Status:*
   ::
      
      MODE: HV   10 Hz 18.0 kV 150 mJ 4000 mbar

5. **Switching Trigger Mode (TRIG INT/EXT)**
   -----------------------------------------
   To switch between internal and external trigger modes, use the `TRIG INT/EXT` button.

   - **Action**: Click the `TRIG INT/EXT` button to toggle between internal and external modes.
   - **Expected Output**: The **Laser Status** section will indicate the trigger mode, 'TRIGGER=EXT' or 'TRIGGER=INT'.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.

   .. image:: ../images/trig_mode_button_example.png
      :alt: Trigger Mode Button Example
      :width: 500px

   *Example Output in Command Entry Window:*
   ::
      
      'TRIGGER=EXT'

6. **Setting Energy Levels (EGY)**
   -------------------------------
   To set the energy value at which the laser shall be stabilized in energy constant mode(HV).

   - **Action**: Click the `EGY` button, then enter the desired energy level.
   - **Expected Output**: The **Responses** section will show the measured energy level.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.


   **Details for EGY Setting**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **1st function**: In energy constant mode, it sets the energy value at which the laser shall be stabilized ("preset energy"). This will be reset during the next start of the laser device. On some lasers, this function is done by the parameter command `EGY SET`.
   - **2nd function**: During energy calibration, this setting is needed to input the external energy reading.
   
   - **Availability**: This command is available in **ON** and **OFF** operating modes only.
   - **Parameter Range**: Depends on the factory settings of the Gas Menu.

   .. image:: ../images/energy_button_example.png
      :alt: EGY Button Example
      :width: 500px

   *Example Output in Command Entry Window:*
   ::
      
      EGY=120 (mJ, NOT INCLUDED IN WINDOW)

7. **Starting the Energy Calibration (ENERGY CAL)**
    ------------------------------------------------
    The `ENERGY CAL` command initiates the energy calibration procedure.

    - **Action**: Click the `EGY CAL` button to start the energy calibration process.
    - **Command Format**: The command sent will be `OPMODE=ENERGY CAL`.
    - **Expected Output**: The **Command Entry** section will display the command, and the energy calibration procedure will begin.

   .. image:: ../images/energy_cal_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for ENERGY CAL Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Corresponding States**:
      - **ENERGY CAL**: Indicates that the energy calibration procedure is running.
      - **ENERGY CAL CONT**: Waiting for input from an external energy meter during the calibration procedure. You must input the reading using the parameter command `EGY=` or `EGY SET=` (refer to sections 4.5 and 4.7 of the user manual).

    - **Corresponding Errors**:
      - **None**


8. **Setting the Laser Mode (MODE)**
   ---------------------------------
   The `MODE` button allows you to switch between different laser operation modes.

   - **Action**: Click the `MODE` button to open the mode selection dialog.
   - **Expected Output**: The **Command Entry** section will update to show the selected mode.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.

   **Details for MODE Setting**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Description**: Default is set to MODE=HV. To change laser operation mode, modify 'MODE'button command in 'LPX200.py' 
                     This switches between different laser operation modes HV, EGY PGR or EGY NGR.
   - **Availability**: This command is available in all operating modes.
   - **Parameter Range**: The available modes depend on the factory settings of the Gas Menu.

   .. image:: ../images/mode_button_example.png
      :alt: MODE Button Example
      :width: 500px

   *Example Output in Command Entry Window:*
   ::
      
      MODE=HV

Additional Commands
-------------------
Explore other buttons in the GUI for more controls, such as `PURGE LINE`, `MENU SEL`, and `COUNTS RESET`. Each button provides a unique functionality, enabling a full range of control over the laser’s settings and parameters.

**Note**: The status display and response display will automatically update to reflect the results of each command.

9. **Setting Countdown Value (COUNTS\nSEL)**
   ------------------------------------
   The `COUNTS SEL` button allows you to set the countdown value for external trigger pulses.

   - **Action**: Click the `COUNTS SEL` button, then enter the desired number of trigger pulses.
   - **Expected Output**: The **Command Entry** section will display the current countdown value set for the laser.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.

   .. image:: ../images/counts_sel_button_example.png
      :alt: MODE Button Example
      :width: 500px

   *Example Output in Command Entry Window:*
   ::
      
      COUNTS=1000

   **Details for COUNTS Setting**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Description**: Sets the value for a countdown. The laser will now only accept external trigger pulses up to the specified `COUNTS` value. Once the countdown reaches zero, the laser stops and `COUNTS` is reset to zero.
   - **Availability**: This command is available in **OFF** operating modes only.
   - **Parameter Range**: 0–65535.

10. **Resetting the Pulse Counter (COUNTS RESET)**
   -------------------------------------------
   The `COUNTS RESET` button allows you to reset the pulse counter to zero.

   - **Action**: Click the `COUNTS RESET` button.
   - **Expected Output**: The **Command Entry** section will display the reset pulse counter value.
   - **Action**: Click the `ENTER` button to confirm and send the command to the laser.

   .. image:: ../images/counts_reset_button_example.png
      :alt: MODE Button Example
      :width: 500px

   *Example Output in Command Entry Window:*
   ::
      
      COUNTS=0

   **Details for COUNTS RESET**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Description**: Resets the pulse counter to zero.
   - **Availability**: This command is available in **OFF** operating modes only.

11. **Purging the Line (PURGE LINE)**
   ---------------------------------
   The `PURGE LINE` command allows you to fill a specified line with the gas connected to the inert gas line.

   - **Action**: Click the `PURGE LINE` button. The system will use the currently selected line from the `self.lines` array (`BUFFER`, `HALOGEN`, `INERT`, `RARE`). 
   - **Command Format**: The command sent will be `OPMODE=PURGE <xy> LINE`, where `<xy>` represents the selected line name.
   - **Example**: 

   .. image:: ../images/purge_line_button_example.png
      :alt: MODE Button Example
      :width: 500px  

     *Example Output in Command Entry Window:*
      ::

        OPMODE=PURGE HALOGEN LINE

     This command fills the halogen line with inert gas.

   - **Expected Output**: The **Command Entry** section will update to display the purge command. The process will continue, and the vacuum pump will remain switched on for three minutes after completion if the halogen line is used.

   **Details for PURGE LINE Command**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Corresponding States**: 
     - **PURGE <xy> LINE**: Indicates that the filling of `<xy>` line is in progress.
   - **Corresponding Errors**: 
     - **None**

   **Note**: The vacuum pump remains switched on for three minutes after the completion of the procedure, but only for the halogen line.

12. **Purging the Reservoir (PURGE RESERVOIR)**
   -------------------------------------------
   The `PURGE RESERVOIR` command starts the purge reservoir procedure.

   - **Action**: Click the `PURGE (Reservoir)` button to initiate the reservoir purge process.
   - **Command Format**: The command sent will be `OPMODE=PURGE RESERVOIR`.
   - **Expected Output**: The **Command Entry** section will update to display the command, and the procedure will start. The vacuum pump will remain switched on for three minutes after the completion of the procedure.

   .. image:: ../images/purge_reservoir_button_example.png
      :alt: MODE Button Example
      :width: 500px

   **Details for PURGE RESERVOIR Command**
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Corresponding States**:
     - **PURGE RESERVOIR**: Indicates that the purge reservoir procedure is running.
   - **Corresponding Errors**:
     - **PURGE RESERVOIR:3**: **NO GAS FLOW**; while refilling, during the purge reservoir procedure, no gas flow was detected in one of the gas lines.

   **Note**: The vacuum pump remains switched on for three minutes after the completion of the procedure.

13. **Starting the New Fill Procedure (NEW FILL)**
    ----------------------------------------------
    The `NEW FILL` command initiates the new fill procedure for the laser.

    - **Action**: Click the `NEW FILL` button to start the new fill process.
    - **Command Format**: The command sent will be `OPMODE=NEW FILL`.
    - **Expected Output**: The **Command Entry** section will display the command, and the procedure for filling will begin.

   .. image:: ../images/new_fill_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for NEW FILL Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Corresponding States (In Responses Window)**:
      - **NEW FILL**: Indicates that the new fill procedure has been started.
      - **NEW FILL, EVAC**: The tube is being evacuated.
      - **NEW FILL, WAIT**: (only with a fluorine source) Indicates that a leak test is being performed in the evacuated tube, or the halogen source is being heated during the new fill procedure.
      - **NEW FILL, FILL**: The tube is being refilled with a new gas fill.

    - **Corresponding Errors**:
      - **NEW FILL:3**: **NO GAS FLOW**; no gas flow was detected in one of the gas lines during the procedure.

    **Note**: The vacuum pump remains switched on for three minutes after the completion of the procedure.

14. **Flushing the Line (FLUSH LINE)**
    ----------------------------------
    The `FLUSH LINE` command evacuates the specified line for two seconds.

    - **Action**: Click the `FLUSH LINE` button to initiate the flush process. The system will use the currently selected line from the `self.lines` array (`BUFFER`, `HALOGEN`, `INERT`, `RARE`).
    - **Command Format**: The command sent will be `OPMODE=FLUSH <xy> LINE`, where `<xy>` represents the selected line name.
    - **Example**:
      
      .. code-block:: text

         OPMODE=FLUSH HALOGEN LINE

      This command evacuates the halogen line.

    - **Expected Output**: The **Command Entry** section will display the command, and the flushing process will begin.
   .. image:: ../images/flush_line_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for FLUSH LINE Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Corresponding States**:
      - **FLUSH <xy> LINE**: Indicates that the flushing of `<xy>` line is in progress, where `<xy>` represents `BUFFER`, `HALOGEN`, `INERT`, or `RARE`.

    - **Corresponding Errors**:
      - **None**

    **Note**: The vacuum pump remains switched on for three minutes after the completion of the procedure, but only for the halogen line.

15. **Selecting and Navigating the Gas Menu (MENU)**
    ------------------------------------------------
    The `MENU` command allows you to select the Gas Menu by number, which determines various parameters for the laser operation.

    - **Action**: Click the `MENU SEL` button to select the appropriate gas menu. The system will use the value stored in `self.menus`.
    - **Command Format**: The command sent will be `MENU=<number>`, where `<number>` represents the chosen gas menu.
    - **Expected Output**: The **Command Entry** section will display the command for selecting the gas menu, and the laser controller will adjust its parameters based on the selected menu.

    **Details for MENU Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Determines the following:
        - Name of the gas,
        - Wavelength,
        - Default gas mode (see `GASMODE`),
        - Partial pressures of the gases,
        - Default tube pressure (see `OFF 27`),
        - HV\ :sub:`min`, HV\ :sub:`max`,
        - Default beam output energy constant value.
      - The `MENU` command can also reset the current Gas Menu to factory settings using `MENU=RESET`.

    - **Availability**: This command is available in **OFF** operating modes only.
    - **Parameter Range**: 1–6 (depends on the number of available Gas Menus) or `RESET`.

    **Navigating Menus**
    ^^^^^^^^^^^^^^^^^^^^

    - **Incrementing Menus**: The `->` button increments the current menu selection by 1. If the menu exceeds 6, it wraps around to 1.
    - **Decrementing Menus**: The `<-` button decrements the current menu selection by 1. If the menu is less than 1, it wraps around to 6.

16. **Resetting the Gas Menu (MENU RESET)**
    ---------------------------------------
    The `MENU RESET` command allows you to reset the current Gas Menu to factory settings.

    - **Action**: Click the `MENU RESET` button to reset the gas menu.
    - **Command Format**: The command sent will be `MENU=RESET`.
    - **Expected Output**: The **Command Entry** section will display the reset command, and the laser controller will revert the selected gas menu to its factory settings.

   .. image:: ../images/menu_reset_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for MENU RESET Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Resets the actual Gas Menu to factory settings, including:
        - Name of the gas,
        - Wavelength,
        - Default gas mode (see `GASMODE`),
        - Partial pressures of the gases,
        - Default tube pressure (see `OFF 27`),
        - HV\ :sub:`min`, HV\ :sub:`max`,
        - Default beam output energy constant value.
      
    - **Availability**: This command is available in **OFF** operating modes only.
    - **Parameter Range**: `RESET`.

17. **Resetting the Halogen Filter (FILTER RESET)**
    -----------------------------------------------
    The `FILTER RESET` command resets the halogen filter capacity percentage after the halogen filter has been replaced.

    - **Action**: Click the `FILTER RESET` button to reset the halogen filter capacity.
    - **Command Format**: The command sent will be `FILTER CONTAMINATION=RESET`.
    - **Expected Output**: The **Command Entry** section will display the reset command, and the filter capacity will be reset.

   .. image:: ../images/filter_reset_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for FILTER RESET Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Resets the halogen filter capacity in percent after the halogen filter has been replaced.
      
    - **Availability**: This command is available in all operating modes.
    - **Parameter Range**: `RESET`.

18. **CLearing the Command Entry (CLEAR)**
    --------------------------------------
    The `CLEAR` command clears the command entry window.

    - **Action**: Click the `CLEAR` button to clear the command entry window.
    - **Expected Output**: The **Command Entry** section will be cleared of any text.

    **Details for CLEAR Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Clears the command entry window.
      
    - **Availability**: This command is available in all operating modes.
    - **Parameter Range**: `None`.

19. **Entering Laser Commands (ENTER)**
    -----------------------------------
    The `ENTER` command sends the entered command to the laser.

    - **Action**: Click the `ENTER` button to send the entered command to the laser.
    - **Expected Output**: The command will be sent to the laser for execution.

    **Details for ENTER Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Sends the entered command in the command Entry window to the laser for execution.
      
    - **Availability**: This command is available in all operating modes.
    - **Parameter Range**: `None`.

20. **Emergency Break for the Laser (BREAK)**
      ----------------------------------------
    The `BREAK` command is used to stop the laser in case of an emergency.

    - **Action**: Click the `BREAK` button to stop the laser immediately.
    - **Expected Output**: The laser will be stopped immediately.

   .. image:: ../images/break_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for BREAK Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Stops the laser immediately in case of an emergency.
      
    - **Availability**: This command is available in all operating modes.
    - **Parameter Range**: `None`.

21. **Starting a Passivation Fill (PASSIVATION FILL)**
    --------------------------------------------------
    The `PASSIVATION FILL` command starts a passivation fill procedure.

    - **Action**: Click the `F3` button to initiate the passivation fill process.
    - **Command Format**: The command sent will be `OPMODE=PASSIVATION FILL`.
    - **Expected Output**: The **Command Entry** section will display the command, and the passivation fill will commence.

   .. image:: ../images/passivation_fill_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for PASSIVATION FILL Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Corresponding States**:
      - **PASSIVATION FILL**: Indicates that the passivation fill is running.

    - **Corresponding Errors**:
      - **PASSIVATION FILL:3**: **NO GAS FLOW**; while refilling during the passivation fill, no gas flow was detected in the halogen line.

    **Note**: The vacuum pump remains switched on for three minutes after the completion of the procedure.

22. **Displaying Halogen Filter Capacity (FILTER CONTAMINATION?)**
    ---------------------------------------------------------------
    The `FILTER CONTAMINATION?` command displays the current capacity of the halogen filter in percent.

    - **Action**: Click the `F4` button to query the halogen filter capacity.
    - **Command Format**: The command sent will be `FILTER CONTAMINATION?`.
    - **Expected Output**: The **Responses** section will display the current capacity of the halogen filter in percent.

   .. image:: ../images/filter_contamination_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for FILTER CONTAMINATION? Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Displays the capacity of the halogen filter in percent, which indicates the remaining usable life of the filter.

23. **Switching Temperature Control (TEMP CONTROL)**
    -------------------------------------------------
    The `TEMP CONTROL` command toggles the temperature control module on or off.

    - **Action**: Click the `F5` button to toggle the temperature control. The system will query the current state and switch it accordingly.
    - **Command Format**:
      - `TEMP CONTROL=ON` to switch the temperature control on.
      - `TEMP CONTROL=OFF` to switch the temperature control off.
    - **Expected Output**: The **Command Entry** section will display the command for turning the temperature control on or off.

   .. image:: ../images/temp_control_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for TEMP CONTROL Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Switches the temperature control module on (`ON`) or off (`OFF`).
      
    - **Availability**: This command is available in all operating modes.
    - **Parameter Range**: `ON`, `OFF`.

24. **Starting a Transport Fill (TRANSPORT FILL)**
    ----------------------------------------------
    The `TRANSPORT FILL` command starts a transport fill procedure.

    - **Action**: Click the `F6` button to initiate the transport fill process.
    - **Command Format**: The command sent will be `OPMODE=TRANSPORT FILL`.
    - **Expected Output**: The **Command Entry** section will display the command, and the transport fill will commence.

   .. image:: ../images/transport_fill_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for TRANSPORT FILL Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Corresponding States**:
      - **TRANSPORT FILL**: Indicates that the transport fill is running.

    - **Corresponding Errors**:
      - **TRANSPORT FILL:3**: **NO GAS FLOW**; while refilling during the transport fill, no gas flow was detected at the buffer line.

    **Note**: The vacuum pump remains switched on for three minutes after the completion of the procedure.

25. **Performing a Halogen Injection (HI)**
    ---------------------------------------
    The `HI` command performs a halogen injection. The partial pressure of halogen injected depends on the value entered in the Gas Menu.

    - **Action**: Click the `F7` button to initiate the halogen injection.
    - **Command Format**: The command sent will be `OPMODE=HI`.
    - **Expected Output**: The **Command Entry** section will display the command, and the halogen injection process will commence.

   .. image:: ../images/halogen_injection_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for HI Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Corresponding States**:
      - None.

    - **Corresponding Errors**:
      - None.

26. **Switching Gas Mode (GASMODE)**
    --------------------------------
    The `GASMODE` command toggles between premix and single gas operation modes.

    - **Action**: Click the `F8` button to toggle the gas mode. The system will query the current gas mode and switch it accordingly.
    - **Command Format**:
      - `GASMODE=SINGLE GASES` to switch to single gas operation.
      - `GASMODE=PREMIX` to switch to premix gas operation.
    - **Expected Output**: The **Command Entry** section will display the command for changing the gas mode.

   .. image:: ../images/gas_mode_button_example.png
      :alt: MODE Button Example
      :width: 500px

    **Details for GASMODE Command**
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - **Functionality**:
      - Displays the current gas mode using `GASMODE?`, which can be either `PREMIX` or `SINGLE GASES`.
      - Switches between `PREMIX` and `SINGLE GASES` modes.

    - **Availability**: This command is available in **OFF** operating modes only.
    - **Parameter Range**: `SINGLE GASES`, `PREMIX`.

Example Commands
~~~~~~~~~~~~~~~~

- **RUN/STOP**: Start or stop the laser operation.
- **TRIG INT/EXT**: Toggle between internal and external triggers.
- **MODE**: Switch between different laser operation modes.

Configuration
-------------

- Ensure that your system is configured with the appropriate COM ports for laser communication. 
- The application automatically detects the correct serial port. If it fails to detect the port, ensure that the laser is connected and powered on, and that the correct driver is installed.

Dependencies
------------

- **PyQt5**: For building the graphical user interface.
- **PyVISA**: For communication with the Lambda Physik LPX 200 Laser.
- **SQLite3**: For logging energy data.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
