chimera_commander plugin
=======================

Emerson Control Techniques COMMANDER SK driver for the chimera observatory control system
https://github.com/astroufsc/chimera.

Usage
-----

This is a Modbus implementation for COMMANDER SK family of Programmable Logical Controllers (PLC) intended to be used
for remote controlling these devices using TCP/IP.

Installation
------------

To use chimera-commander, you need first install pymodbus, ( https://pypi.python.org/pypi/pymodbus ),
a fully featured modbus protocol stack in  python. After that, you can do:


::

   pip install -U chimera_commander

or

::

    pip install -U git+https://github.com/astroufsc/chimera-commander.git


Configuration Example
---------------------

Here goes an example of the configuration to be added on ``chimera.config`` file.

::

    instrument:
        name: Myplc
        type: Commander
        clp_host: 127.0.0.1 # Host IP
    	clp_port: 502 # Host port


Tested Hardware (for instruments)
---------------------------------

This plugin was tested on these hardware:

* Commander SK - SKBD200110	Version 01.09.00
* SM-Ethernet	Version 02.00.02

Contact
-------

For more information, contact us on chimera's discussion list:
https://groups.google.com/forum/#!forum/chimera-discuss

Bug reports and patches are welcome and can be sent over our GitHub page:
https://github.com/astroufsc/chimera-template/
