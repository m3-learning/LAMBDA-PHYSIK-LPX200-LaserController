import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QPushButton, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer, QThread, Qt
import sqlite3
import time
from functools import partial
import pyvisa

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lambda Physik LPX 200 Laser Controller')
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.createStatusDisplay()  # Status display for laser system status
        self.createCommandResponseDisplays()  # Command and Response displays
        self.createButtons()

    def createStatusDisplay(self):
        """Create the status display for laser system updates."""
        self.statusLabel = QLabel("Laser Status:")  # Add a label for the status display
        self.generalLayout.addWidget(self.statusLabel)
        
        self.statusDisplay = QTextEdit()
        self.statusDisplay.setFixedHeight(50)
        self.statusDisplay.setReadOnly(True)
        self.generalLayout.addWidget(self.statusDisplay)

    def createCommandResponseDisplays(self):
        """Create command and response displays with labels."""
        # Layout to hold command and response display side by side
        commandResponseLayout = QHBoxLayout()

        # Command Display (on the left)
        self.commandLabel = QLabel("Command Entry:")  # Add a label for the command display
        self.generalLayout.addWidget(self.commandLabel)
        
        self.commandDisplay = QTextEdit()
        self.commandDisplay.setFixedHeight(70)
        self.commandDisplay.setReadOnly(True)  # Prevent user from typing, commands will be via buttons
        commandResponseLayout.addWidget(self.commandDisplay)

        # Response Display (on the right)
        self.responseLabel = QLabel("Responses:")  # Add a label for the responses display
        self.generalLayout.addWidget(self.responseLabel)
        
        self.responseDisplay = QTextEdit()
        self.responseDisplay.setFixedHeight(70)
        self.responseDisplay.setReadOnly(True)  # Read-only for responses
        self.responseDisplay.setAlignment(Qt.AlignRight)  # Align responses to the right
        commandResponseLayout.addWidget(self.responseDisplay)

        # Add the command and response display layout to the main layout
        self.generalLayout.addLayout(commandResponseLayout)


    def createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Restoring all buttons as per your original script
        buttons = {'RUN\nSTOP': (0, 0), 'TRIG\nINT/EXT': (0, 1), 'MODE': (0, 2),
                   'REP\nRATE': (0, 3), 'COUNTS\nSEL': (0, 4), 'NEW\nFILL': (0, 5),
                   'MENU\nSEL': (0, 6), 'F1': (0, 7), 'F6': (0, 8), '7': (1, 0),
                   '8': (1, 1), '9': (1, 2), 'HV': (1, 3), 'COUNTS\nRESET': (1, 4),
                   'FLUSH\nLINE': (1, 5), 'MENU\nRESET': (1, 6), 'F2': (1, 7), 'F7': (1, 8),
                   '4': (2, 0), '5': (2, 1), '6': (2, 2), 'EGY': (2, 3), 'EGY\nCAL': (2, 4),
                   'PURGE\nLINE': (2, 5), 'FILTER\nRESET': (2, 6), 'F3': (2, 7), 'F8': (2, 8),
                   '1': (3, 0), '2': (3, 1), '3': (3, 2), '<-': (3, 3), '->': (3, 4),
                   'PURGE\n(Reservoir)': (3, 5), 'STOP\nEGY\nLOG': (3, 6), 'F4': (3, 7), 'F9': (3, 8),
                   '0': (4, 0), '.': (4, 1), 'CLEAR': (4, 2), 'ENTER': (4, 3),
                   'EXE': (4, 4), 'BREAK': (4, 5), 'F5': (4, 7), 'F10': (4, 8)}

        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(60, 60)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        self.generalLayout.addLayout(buttonsLayout)

    def setStatusText(self, text):
        """Set the status display's text."""
        self.statusDisplay.setPlainText(text)

    def setCommandText(self, text):
        """Set the command display's text."""
        self.commandDisplay.setPlainText(text)

    def appendCommandText(self, text):
        """Append text to the command display."""
        current_text = self.commandDisplay.toPlainText()
        self.commandDisplay.setPlainText(current_text + text)

    def appendResponseText(self, text):
        """Append text to the response display aligned to the right."""
        current_text = self.responseDisplay.toPlainText()
        self.responseDisplay.setPlainText(current_text + text)

    def getCommandText(self):
        """Get the current text in the command display."""
        return self.commandDisplay.toPlainText()

    def clearCommandDisplay(self):
        """Clear the command display."""
        self.commandDisplay.setPlainText('')


class Control:
    def __init__(self, view, model):
        self.modes = ['HV', 'EGY PGR', 'EGY NGR']
        self.lines = ['BUFFER', 'HALOGEN', 'INERT', 'RARE']
        self.m=0
        self.l=0
        self.menus=1        

        self.view = view
        self.evaluate = model
        self.energy_logging_active = False  # Track the energy logging state
        self.energy_poll_thread = None  # Thread for energy polling

        # Poll laser system status every 1 second
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.poll_laser_status)
        self.status_timer.start(20)  # Poll every 1 second

        self.connectSignals()

    def laserbreak(self):
        """ Stops the laser and clears the display."""

        commRes('OPMODE=OFF')
        self.view.clearCommandDisplay()
        self.view.appendResponseText("Laser Stopped")
        

    def sendCommand(self):
        """Send the user command to the laser and handle parameter commands."""
        command = self.view.getCommandText().strip()

        if not command:
            self.view.setCommandText('No command entered')
            return

        # Check if it is a parameter command
        if '=' in command:
            # Send the parameter command
            commRes(command)

            # Extract the parameter name (before the =) and generate the polling command
            param_name = command.split('=')[0].strip()
            polling_command = f"{param_name}?"

            # Poll the parameter to confirm the change
            response = commRes(polling_command)

            # Display the response on the right side
            self.view.appendResponseText(f"{response.rjust(50)}")  # Align response to the right

        else:
            # Handle regular non-parameter commands
            response = self.evaluate(command)

            # Clear both command and response displays to prepare for the next command
        QTimer.singleShot(1000, self.view.clearCommandDisplay)  # Slight delay to keep the current command visible
        QTimer.singleShot(1000, self.view.responseDisplay.clear)  # Clear after 1 second to allow user to see the response   


    def poll_laser_status(self):
        """Poll the laser system status and update the status display."""
        status = "MODE: {MODE}\t{REPRATE} Hz {VOLTAGE} kV {ENERGY} mJ {PRESSURE} mbar\n".format(
            MODE=commRes("MODE?"),
            REPRATE=commRes("REPRATE?"),
            VOLTAGE=commRes("HV?"),
            ENERGY=commRes("EGY?"),
            PRESSURE=commRes("PRESSURE?")
        )
        self.view.setStatusText(status)

        # Extract the energy value to log it
        try:
            energy_value = float(commRes("EGY?"))  # Extract the energy value again
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            self.log_energy_to_db(timestamp, energy_value)  # Log the energy value with timestamp
        except Exception as e:
            print(f"Error logging energy: {e}")

    def connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self.view.buttons.items():
            if btnText not in {'ENTER','EXE','CLEAR','BREAK'}:
                btn.clicked.connect(partial(self.buildCommand, btnText))
            if btnText in {'F1','F2','F9', 'F10'}:
                btn.clicked.connect(self.view.clearCommandDisplay)
                btn.clicked.connect(partial(self.buildCommand, f"{btnText} Button Not Configured"))


        self.view.buttons['ENTER'].clicked.connect(self.sendCommand)
        self.view.buttons['EXE'].clicked.connect(self.sendCommand)        
        self.view.buttons['CLEAR'].clicked.connect(self.view.clearCommandDisplay)
        self.view.buttons['BREAK'].clicked.connect(self.laserbreak)


    def buildCommand(self, sub_comm):
        """Build a command based on the button pressed and append it to the command display."""
        
        # Clear the display if the previous command was invalid
        if self.view.getCommandText() == 'No command entered':
            self.view.clearCommandDisplay()

        # Handle different sub-commands based on the button pressed
        if sub_comm == 'RUN\nSTOP':
            self.view.clearCommandDisplay()
            if commRes('OPMODE?') == 'ON':
                command = 'OPMODE=OFF'
            else:
                command = 'OPMODE=ON'
            self.view.appendCommandText(f'{command}')  # Show command on the left

        elif sub_comm == 'TRIG\nINT/EXT':
            self.view.clearCommandDisplay()
            if commRes('TRIGGER?') == 'INT':
                command = 'TRIGGER=EXT'
            else:
                command = 'TRIGGER=INT'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'MODE':
            self.view.clearCommandDisplay()
            command = f'MODE={self.modes[self.m]}'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'BREAK':
            self.view.clearCommandDisplay()
            command = 'OPMODE=OFF'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'REP\nRATE':
            self.view.clearCommandDisplay()
            command = 'REPRATE='
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'COUNTS\nSEL':
            self.view.clearCommandDisplay()
            command = 'COUNTS='
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'NEW\nFILL':
            self.view.clearCommandDisplay()
            command = 'OPMODE=NEW FILL'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'MENU\nSEL':
            self.view.clearCommandDisplay()
            command = f'MENU={self.menus}'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'HV':
            self.view.clearCommandDisplay()
            command = 'HV='
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'COUNTS\nRESET':
            self.view.clearCommandDisplay()
            command = 'COUNTS=0'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'FLUSH\nLINE':
            self.view.clearCommandDisplay()
            command = f'OPMODE=FLUSH {self.lines[self.l]} LINE'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'MENU\nRESET':
            self.view.clearCommandDisplay()
            command = 'MENU=RESET'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'EGY':
            self.view.clearCommandDisplay()
            command = 'EGY='
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'EGY\nCAL':
            self.view.clearCommandDisplay()
            command = 'OPMODE=ENERGY CAL'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'PURGE\nLINE':
            self.view.clearCommandDisplay()
            command = f'OPMODE=PURGE {self.lines[self.l]} LINE'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'PURGE\n(Reservoir)':
            self.view.clearCommandDisplay()
            command = 'OPMODE=PURGE RESERVOIR'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'FILTER\nRESET':
            self.view.clearCommandDisplay()
            command = 'FILTER CONTAMINATION=RESET'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'F3':
            self.view.clearCommandDisplay()
            command = 'OPMODE=PASSIVATION FILL'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'F4':
            self.view.clearCommandDisplay()
            command = 'FILTER CONTAMINATION?'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'F5':
            self.view.clearCommandDisplay()
            if commRes('TEMP CONTROL?') == 'ON':
                command = 'TEMP CONTROL=OFF'
            else:
                command = 'TEMP CONTROL=ON'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'F6':
            self.view.clearCommandDisplay()
            command = 'OPMODE=TRANSPORT FILL'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'F7':
            self.view.clearCommandDisplay()
            command = 'OPMODE=HI'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == 'F8':
            self.view.clearCommandDisplay()
            if commRes('GASMODE?') == 'PREMIX':
                command = 'GASMODE=SINGLE GASES'
            else:
                command = 'GASMODE=PREMIX'
            self.view.appendCommandText(f'{command}')

        # Update the state instead of checking display content
        elif sub_comm == '->':
            # Handle state changes based on the internal command context
            if 'PURGE' in self.current_command:
                self.l += 1
                if self.l > 3:
                    self.l = 0
                self.view.clearCommandDisplay()
                command = f'OPMODE=PURGE {self.lines[self.l]} LINE'
            elif 'FLUSH' in self.current_command:
                self.l += 1
                if self.l > 3:
                    self.l = 0
                self.view.clearCommandDisplay()
                command = f'OPMODE=FLUSH {self.lines[self.l]} LINE'
            elif 'MODE=' in self.current_command:
                self.m += 1
                if self.m > 2:
                    self.m = 0
                self.view.clearCommandDisplay()
                command = f'MODE={self.modes[self.m]}'
            elif 'MENU' in self.current_command:
                self.menus += 1
                if self.menus > 6:
                    self.menus = 1
                self.view.clearCommandDisplay()
                command = f'MENU={self.menus}'
            else:
                self.view.clearCommandDisplay()
                command = 'No menu selected'
            self.view.appendCommandText(f'{command}')

        elif sub_comm == '<-':
            # Handle state changes based on the internal command context
            if 'PURGE' in self.current_command:
                self.l -= 1
                if self.l < 0:
                    self.l = 3
                self.view.clearCommandDisplay()
                command = f'OPMODE=PURGE {self.lines[self.l]} LINE'
            elif 'FLUSH' in self.current_command:
                self.l -= 1
                if self.l < 0:
                    self.l = 3
                self.view.clearCommandDisplay()
                command = f'OPMODE=FLUSH {self.lines[self.l]} LINE'
            elif 'MODE=' in self.current_command:
                self.m -= 1
                if self.m < 0:
                    self.m = 2
                self.view.clearCommandDisplay()
                command = f'MODE={self.modes[self.m]}'
            elif 'MENU' in self.current_command:
                self.menus -= 1
                if self.menus < 1:
                    self.menus = 6
                self.view.clearCommandDisplay()
                command = f'MENU={self.menus}'
            else:
                self.view.clearCommandDisplay()
                command = 'No menu selected'
            self.view.appendCommandText(f'{command}')

        else:
            # For all other button presses, simply display the button's text as the command
            command = sub_comm
            self.view.appendCommandText(f'{command}')

        # After building the command, store the current command for later use
        self.current_command = command

    def log_energy_to_db(self, timestamp, energy_value):
        """Log the energy value with a timestamp to the SQLite database."""
        conn = sqlite3.connect('laser_energy_log.db')  # Connect to SQLite database
        c = conn.cursor()
        
        # Create table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS energy_log (
                        timestamp TEXT, 
                        energy_value REAL
                    )''')
        
        # Insert the timestamp and energy value into the database
        c.execute("INSERT INTO energy_log (timestamp, energy_value) VALUES (?, ?)", (timestamp, energy_value))
        conn.commit()  # Commit the transaction
        conn.close()   # Close the connection



def commRes(command):
    """Send command to the laser and return the response."""
    try:
        res = laser_instr.query(command)  # Send command to the laser
    except Exception as e:
        res = f"Error communicating with the laser: {e}"
    return res


def main():
    """Main function."""
    # Set up pyvisa resource and port for communication
    global laser_instr
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    laser_instr = rm.open_resource('ASRL12::INSTR')
    laser_instr.write_termination = "\r"
    laser_instr.read_termination = "\r"
    laser_instr.timeout = 1000
    
    app = QApplication(sys.argv)
    view = View()
    control = Control(view=view, model=commRes)
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()