import machine
import utime
from machine import Pin, I2C
import tmpOFFSET
from tmpOFFSET import offset
import CC6920

# 電流リード
print('ch1 Current:{:.2f}'.format(CC6920.get_current(1, 1, 20))+'mA')
print('ch2 Current:{:.2f}'.format(CC6920.get_current(1, 2, 10))+'mA')
print('ch3 Current:{:.2f}'.format(CC6920.get_current(2, 3, 10))+'mA')
print('ch4 Current:{:.2f}'.format(CC6920.get_current(2, 4, 5))+'mA')
