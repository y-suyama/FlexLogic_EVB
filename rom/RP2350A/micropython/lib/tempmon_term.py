import machine
import utime
from machine import Pin, I2C
import tmpOFFSET
from tmpOFFSET import offset
import tmpADC


# ADC温度センサリード
print('ADC1 Tmp:{:.2f}'.format(tmpADC.inttmp(1) * 0.03125)+'deg')
print('ADC2 Tmp:{:.2f}'.format(tmpADC.inttmp(2) * 0.03125)+'deg')
# ADC1熱電対リード
print('ch1 Tmp:{:.2f}'.format(tmpADC.conv(1,1,offset[0]))+'deg')
print('ch2 Tmp:{:.2f}'.format(tmpADC.conv(1,2,offset[1]))+'deg')
# ADC2熱電対リード
print('ch3 Tmp:{:.2f}'.format(tmpADC.conv(2,3,offset[2]))+'deg')
print('ch4 Tmp:{:.2f}'.format(tmpADC.conv(2,4,offset[3]))+'deg')
