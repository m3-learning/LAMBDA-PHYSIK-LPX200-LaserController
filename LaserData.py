#Import libraries
import pyvisa
import h5py
import time
import numpy as np
import datetime


def comm_res(commmand):
    try :
        res = laser_instr.query(command)
    except :
        #print("Error")
        res = 'Not a valid Command'
    else :
        return res   
    return res

def get_Data():
    opmode,trigger, reprate, voltage, energy, mode, pressure, menu = comm_res("opmode?"), comm_res("trigger?"), comm_res("reprate?"), comm_res("hv?"), comm_res("egy?"), comm_res("pressure?"), comm_res("mode?"), comm_res("menu?")
    gMenuNo, wvlth, gMix = menu.split()
    x=0
    while  comm_res(x<5) : #comm_res('opmode?') != 'NULL' :
        get_Data()
        l_data = append(l_data,[[opmode, trigger, reprate, voltage, energy, mode, pressure, gMenuNo, wvlth, gMix]],0)
        time.sleep(5)
        x=x+1
        #print(l_data)





def main():
    """Main function."""  
    current_time = datetime.datetime.now()
    str(current_time)
    yy = str(current_time.year)
    mm =  str(current_time.month)
    dd = str(current_time.day)
    h= str(current_time.hour)
    m= str( current_time.minute)
    s= str(current_time.second)

    dte = dd + '' + mm + '' + yy
    tme = h + ':' + m + ':' + s
    #print(current_time)
    #print(dte)
    #print(tme)

    #Test h5py import and check for available pyvisa resources
    #h5py.run_tests()
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    #Set up pyvisa resource and port for communication
    laser_instr = rm.open_resource('ASRL4::INSTR')
    laser_instr.write_termination = "\r"
    laser_instr.read_termination = "\r"

    # Declare variables and method for updating variables
    global opmode, time, trigger, reprate, voltage, energy, mode, pressure, menu, gMenuNo, wvlth, gMix
    dt = h5py.string_dtype(encoding='utf-8')
    l_data = np.array([['Operational Mode', 'Trigger', 'Reprate', 'Voltage', 'Energy', 'Mode', 'Pressure', 'Gas Menu Number', 'Wavelength', 'Gas Mixture']], dtype= dt)
    #print(l_data)
    get_Data()

    f = h5py.File(dte+'.hdf5','a')
    dset = f.create_dataset(tme, data=l_data, dtype=dt)
    f.close()
if __name__ == '__main__':
    main()
    