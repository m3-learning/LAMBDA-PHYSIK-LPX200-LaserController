#Lambda Physik LPX 200 Laser Controller

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from functools import partial

import pyvisa
import h5py
import time
import numpy as np

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the main window's properties
        self.setWindowTitle('Lambda Physik')
        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self.createDisplay()
        self.createButtons()
        
    def createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'RUN\nSTOP': (0, 0),'TRIG\nINT/EXT': (0, 1),'MODE': (0, 2),'REP\nRATE': (0, 3),'COUNTS\nSEL': (0, 4),'NEW\nFILL': (0, 5),'MENU\nSEL': (0, 6),'F1': (0, 7),'F6': (0, 8),
                   '7': (1, 0),'8': (1, 1),'9': (1, 2),'HV': (1, 3),'COUNTS\nRESET': (1, 4),'FLUSH\nLINE': (1, 5),'MENU\nRESET': (1, 6),'F2': (1, 7),'F7': (1, 8),
                   '4': (2, 0),'5': (2, 1),'6': (2, 2),'EGY': (2, 3),'EGY\nCAL': (2, 4),'PURGE\nLINE': (2, 5),'FILTER\nRESET':(2,6),'F3': (2, 7),'F8': (2, 8),
                   '1': (3, 0),'2': (3, 1),'3': (3, 2),'<-': (3, 3),'->': (3, 4),'PURGE\n(Reservoir)': (3, 5),'STOP\nEGY\nLOG': (3, 6),'F4': (3, 7),'F9': (3, 8),
                   '0': (4, 0),'.': (4, 1),'CLEAR': (4, 2),'ENTER': (4, 3),'EXE': (4, 4),'BREAK': (4, 5),'F5': (4, 7),'F10': (4, 8)
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(60, 60)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)
        
    def createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QTextEdit()
        # Set some display's properties
        self.display.setFixedHeight(70)
        self.display.setReadOnly(True)
        #Set the laser status display
        self.display.setPlainText("MODE : {MODE}\t\t{REPRATE} Hz  {VOLTAGE} kV  {ENERGY} mJ  {PRESSURE} mbar  {GasMix} \n".format(MODE=commRes("MODE?"),REPRATE=commRes("REPRATE?"),VOLTAGE=commRes("HV?"),ENERGY=commRes("EGY?"),PRESSURE=commRes("PRESSURE?"),GasMix=commRes("Menu?").split()[2]))
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)
        
    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setPlainText('')
        self.display.setPlainText(text)
        #self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.toPlainText()

    def clearDisplay(self):
        """Clear the display."""
        self.display.setPlainText('')
        ##Set the laser status display
        self.display.setPlainText("MODE : {MODE}\t\t{REPRATE} Hz  {VOLTAGE} kV  {ENERGY} mJ  {PRESSURE} mbar  {GasMix} \n".format(MODE=commRes("MODE?"),REPRATE=commRes("REPRATE?"),VOLTAGE=commRes("HV?"),ENERGY=commRes("EGY?"),PRESSURE=commRes("PRESSURE?"),GasMix=commRes("Menu?").split()[2]))
        
        
        
        
class Control:
    def __init__(self,view,model):
        self.modes = ['HV', 'EGY PGR', 'EGY NGR']
        self.lines = ['BUFFER', 'HALOGEN', 'INERT', 'RARE']
        self.m=0
        self.l=0
        self.menus=1
        self.view = view
        self.evaluate=model

        self.energy_logging_active = False # Flag to indicate if energy logging is active
        self.energy_poll_thread = None # Thread for energy polling

        # Set up polling laser system status every 1 second
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.poll_laser_status)
        self.status_timer.start(1000) # 1 second interval

        self.connectSignals()
        
        
    def sendCommand(self):
        """ Sets second line of the display text to PlainText.
        Sends the command to the laser and shows the response (if any).
        """
        command = self.view.displayText().split('\n')[1].strip()  # Get the second line (the command)
        
        if not command:  # Check if the command is empty
            self.view.clearDisplay()
            self.view.displayText()+'No command entered'
            return
        
        if '=' in command:  # Parameter command (no response from laser)
            commRes(command)  # Send the command (write the parameter to the laser)
            # Instead of waiting for a response, show the updated status
            status = "MODE : {MODE}\t\t{REPRATE} Hz  {VOLTAGE} kV  {ENERGY} mJ  {PRESSURE} mbar  {GasMix} \n".format(
                MODE=commRes("MODE?"), 
                REPRATE=commRes("REPRATE?"), 
                VOLTAGE=commRes("HV?"), 
                ENERGY=commRes("EGY?"), 
                PRESSURE=commRes("PRESSURE?"), 
                GasMix=commRes("Menu?").split()[2]
            )
            self.view.setDisplayText(status)
        else:  # Non-parameter commands (expecting a response from the laser)
            resp = self.evaluate(command)  # Send the command and get the response
            self.view.clearDisplay()
            self.view.displayText()+ resp.strip()  # Display the response

            # After the command is sent, check the laser status and start/stop logging
        if commRes('OPMODE?') == 'ON':
            self.start_energy_logging()  # Start logging when the laser is on
        else:
            self.stop_energy_logging()  # Stop logging when the laser is off

       
    def buildCommand(self,sub_comm):
        if self.view.displayText() == 'Not a valid Command':
            self.view.clearDisplay()
        
        if sub_comm == 'RUN\nSTOP' :
            self.view.clearDisplay()
            if commRes('OPMODE?') == 'ON' :
                command = self.view.displayText() + 'OPMODE=OFF'

            else :
                command = self.view.displayText() + 'OPMODE=ON'
                
        elif sub_comm == 'TRIG\nINT/EXT' :
            self.view.clearDisplay()
            if commRes('TRIGGER?') == 'INT' :
                command = self.view.displayText() +'TRIGGER=EXT'
            else :
                command = self.view.displayText() + 'TRIGGER=INT'
                
        elif sub_comm == 'MODE' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'MODE=' + self.modes[self.m]

        elif sub_comm == 'BREAK' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=OFF'

        elif sub_comm == 'REP\nRATE' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'REPRATE='
            
        elif sub_comm == 'COUNTS\nSEL' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'COUNTS='
            
        elif sub_comm == 'NEW\nFILL' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=NEW FILL'
        
        elif sub_comm == 'MENU\nSEL' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'MENU=' + str(self.menus)
            
        elif sub_comm == 'HV' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'HV='
            
        elif sub_comm == 'COUNTS\nRESET' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'COUNTS=0'
            
        elif sub_comm == 'FLUSH\nLINE' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=FLUSH ' + self.lines[self.l] + ' LINE'
            
        elif sub_comm == 'MENU\nRESET' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'MENU=RESET'
            
        elif sub_comm == 'EGY' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'EGY='
            
        elif sub_comm == 'EGY\nCAL' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=ENERGY CAL'
            
        elif sub_comm == 'PURGE\nLINE' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=PURGE ' + self.lines[self.l] + ' LINE'
            
        elif sub_comm == 'PURGE\n(Reservoir)' :
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=PURGE RESERVOIR'

        elif sub_comm == 'FILTER\nRESET' :
            """Resets the halogen filter capacity in percent(after the 
            halogen filter has been replaced)."""

            self.view.clearDisplay()
            command = self.view.displayText() + 'FILTER CONTAMINATION=RESET'

        elif sub_comm == 'F3' :
            """Fills laser reservoir w/ 100mb halogen and 1100mb
               Helium or gas connected to invert valve."""
            
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=PASSIVATION FILL'

        elif sub_comm == 'F4' :
            """Displays the capacity of the halogen filter in percent."""
            
            self.view.clearDisplay()
            command = self.view.displayText() + 'FILTER CONTAMINATION?'

        elif sub_comm == 'F5' :
            """Temp Control: Turns “on” or “off” a servo controlled 
            valve to regulate cooling water."""
            
            self.view.clearDisplay()
            if commRes('TEMP CONTROL?') == 'ON' :
                command = self.view.displayText() + 'TEMP CONTROL=OFF'
            else :
                command = self.view.displayText() + 'TEMP CONTROL=ON'  
            
        elif sub_comm == 'F6' :
            """Transport Fill => Fills laser reservoir to 1500mb Helium or gas connected
                to inert valve."""
            
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=TRANSPORT FILL'

        elif sub_comm == 'F7' :
            """Used w/ Halogen source (generator) or single gas
            mode. Performs a halogen injection. The partial pressure of halogen injected 
            depends on the value entered in the Gas Menu."""
            
            self.view.clearDisplay()
            command = self.view.displayText() + 'OPMODE=HI' 

        elif sub_comm == 'F8' :
            """GASMODE: Switches between premix and single gas operation."""
            
            self.view.clearDisplay()
            if commRes('GASMODE?') == 'PREMIX' :
                command = self.view.displayText() + 'GASMODE=SINGLE GASES'
            else :
                command = self.view.displayText() + 'GASMODE=PREMIX'  

        elif sub_comm == '->':
            if('PURGE' in self.view.displayText().split("\n")[1]):
                self.l +=1
                if(self.l>3) : self.l =0
                self.view.clearDisplay()
                command = self.view.displayText() + 'OPMODE=PURGE ' + self.lines[self.l] + ' LINE'
                
            elif('FLUSH' in self.view.displayText().split("\n")[1]):
                self.l +=1
                if(self.l>3) : self.l =0
                self.view.clearDisplay()
                command = self.view.displayText() + 'OPMODE=FLUSH ' + self.lines[self.l] + ' LINE'
                
            elif('MODE=' in self.view.displayText().split("\n")[1]):
                self.m +=1
                if(self.m>2) : self.m =0
                self.view.clearDisplay()
                command = self.view.displayText() + 'MODE=' + self.modes[self.m]
                
            elif('MENU' in self.view.displayText().split("\n")[1]):
                self.menus +=1
                if(self.menus>6) : self.menus =1
                self.view.clearDisplay()
                command = self.view.displayText() + 'MENU=' + str(self.menus)
                
            else :
                self.view.clearDisplay()
                command = self.view.displayText() + 'No menu selected'
                
        elif sub_comm == '<-':
            if('PURGE' in self.view.displayText().split("\n")[1]):
                self.l -=1
                if(self.l<0) : self.l =3
                self.view.clearDisplay()
                command = self.view.displayText() + 'OPMODE=PURGE ' + self.lines[self.l] + ' LINE'
                
            elif('FLUSH' in self.view.displayText().split("\n")[1]):
                self.l -=1
                if(self.l<0) : self.l =3
                self.view.clearDisplay()
                command = self.view.displayText() + 'OPMODE=FLUSH ' + self.lines[self.l] + ' LINE'
                
            elif('MODE=' in self.view.displayText().split("\n")[1]):
                self.m -=1
                if(self.m<0) : self.m =2
                self.view.clearDisplay()
                command = self.view.displayText() + 'MODE=' + self.modes[self.m]
                
            elif('MENU' in self.view.displayText().split("\n")[1]):
                self.menus -=1
                if(self.menus<1) : self.menus =6
                self.view.clearDisplay()
                command = self.view.displayText() + 'MENU=' + str(self.menus)
                
            else :
                self.view.clearDisplay()
                command = self.view.displayText() + 'No menu selected'
                
                  
        else :
            command = self.view.displayText() + sub_comm
            
        self.view.setDisplayText(command)
        
    def connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self.view.buttons.items():
            if btnText not in {'ENTER','EXE','CLEAR','BREAK', ['STOP\nEGY\nLOG']}:
                btn.clicked.connect(partial(self.buildCommand, btnText))   
            if btnText in {'F9','F10'}:
                btn.clicked.connect(self.view.clearDisplay)
                btn.clicked.connect(partial(self.buildCommand, f"{btnText} Button Not Configured"))
                
            
        self.view.buttons['ENTER'].clicked.connect(self.sendCommand)
        self.view.buttons['EXE'].clicked.connect(self.sendCommand)        
        self.view.buttons['CLEAR'].clicked.connect(self.view.clearDisplay)
        self.view.buttons['BREAK'].clicked.connect(self.laserbreak)
        self.view.buttons['STOP\nEGY\nLOG'].clicked.connect(self.stop_energy_logging)

    def laserbreak(self):
        """ Stops the laser and clears the display."""

        commRes('OPMODE=OFF')
        self.view.clearDisplay()
        self.view.displayText()+'Laser Stopped'

    def poll_laser_status(self):
        """Poll the laser system status every 1 second and update the display."""
        status = "MODE : {MODE}\t\t{REPRATE} Hz  {VOLTAGE} kV  {ENERGY} mJ  {PRESSURE} mbar  {GasMix} \n".format(
            MODE=commRes("MODE?"), 
            REPRATE=commRes("REPRATE?"), 
            VOLTAGE=commRes("HV?"), 
            ENERGY=commRes("EGY?"), 
            PRESSURE=commRes("PRESSURE?"), 
            GasMix=commRes("Menu?").split()[2]
        )
        self.view.setDisplayText(status)   
        
def commRes(command):
    try :
        res = laser_instr.query(command)
    except :
        #print("Error")
        res = 'Not a valid Command'
    else :
        return res   
    return res
        

def main():
    """Main function."""  
    #Set up pyvisa resource and port for communication
    global laser_instr
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    laser_instr = rm.open_resource('ASRL12::INSTR')
    laser_instr.write_termination = "\r"
    laser_instr.read_termination = "\r"
    laser_instr.timeout = 5000
    #print(commRes("OPMODE=ON"))
    
    
    #Test h5py import
    #h5py.run_tests()
    
    
    # Create an instance of QApplication
    lpx200 = QApplication(sys.argv)
    # Show the calculator's GUI
    view = View()
    view.show()
    model=commRes
    Control(view=view,model=model)
    sys.exit(lpx200.exec_())

if __name__ == '__main__':
    main()