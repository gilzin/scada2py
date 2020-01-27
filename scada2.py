from pymodbus.server.async import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
from gpiozero import LED
import time
import sys
import datetime
from time import sleep


Pump=LED (26)
Vent=LED (19)
Led1=LED(13)
Led2=LED(6)

Pump.on()
Vent.off()



store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)




def read_context(a):
     context  = a[0]
     register = 3
     slave_id = 0
     address  = 10
     value = context[slave_id].getValues(register,address,10)
     if value[0]==0:
		Pump.off()
		print "Port 26 is 0/LOW/False - LED Off"
		Led1.off()
		Led2.on()
		sleep(1)
		Led2.off()
     if value[0]==1:
		Pump.on()
		print "Port 26 is 1/HIGH/True - LED On"  
                Led1.on()
		Led2.off()
     if value[1]==0:
		Vent.off()
		print "Port 25 is 0/LOW/False - LED OFF"
#                Led2.off()
     if value[1]==1:
		Vent.on()
		print "Port 25 is 0/LOW/False - LED On"
#		Led2.on()
     print value[0]
     print value[1]

read = LoopingCall(f=read_context, a=(context,))
read.start(.2)


StartTcpServer(context)


