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

1. Install the package via pip::

```bash
   pip install lpx200
```

2. Make sure you have **PyQt5** and **PyVISA** installed, as they are required dependencies for this project::
```bash
   pip install PyQt5 pyvisa
```

Usage
-----

To run the GUI::

```bash
   python lpx200.py
```

The program will automatically detect the correct serial port that the laser is connected to and establish communication. Once started, you can interact with the laser via the buttons and commands provided in the interface.

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
