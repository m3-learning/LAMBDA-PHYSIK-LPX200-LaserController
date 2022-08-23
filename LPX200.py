#Lambda Physik LPX 200 Laser Controller

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
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
                   '4': (2, 0),'5': (2, 1),'6': (2, 2),'EGY': (2, 3),'EGY\nCAL': (2, 4),'PURGE\nLINE': (2, 5),'F3': (2, 7),'F8': (2, 8),
                   '1': (3, 0),'2': (3, 1),'3': (3, 2),'<-': (3, 3),'->': (3, 4),'PURGE\n(Reservoir)': (3, 5),'F4': (3, 7),'F9': (3, 8),
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
        self.connectSignals()
        
        
    def sendCommand(self):
        #print(self.view.displayText().split('\n')[1])
        resp = self.evaluate(self.view.displayText().split('\n')[1])
        self.view.setDisplayText(resp)
        
       
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
            if btnText not in {'ENTER','EXT','CLEAR','BREAK'} :
                btn.clicked.connect(partial(self.buildCommand, btnText))   
            if btnText in {'F10','F1','F2','F3','F4','F5','F6','F7','F8','F9'}:
                btn.clicked.connect(self.view.clearDisplay)
                btn.clicked.connect(partial(self.buildCommand, f"{btnText} Button Not Configured"))
                
            
        self.view.buttons['ENTER'].clicked.connect(self.sendCommand)
        self.view.buttons['EXE'].clicked.connect(self.sendCommand)        
        self.view.buttons['CLEAR'].clicked.connect(self.view.clearDisplay)
        self.view.buttons['BREAK'].clicked.connect(self.view.clearDisplay)
        
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
    laser_instr = rm.open_resource('ASRL4::INSTR')
    laser_instr.write_termination = "\r"
    laser_instr.read_termination = "\r"
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