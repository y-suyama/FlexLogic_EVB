import machine
import utime
import time
from machine import Pin, SPI, I2C, Timer
import tmpOFFSET
import ssd1306

# Initialize I2C and OLED display
#i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
#display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Main
# メインスレッドで実行する関数

# CPLD Interface SPI0
#spi0 = SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,sck=Pin(22), mosi=Pin(23), miso=Pin(20), cs=Pin(21)
def setup_spi():
    """
    SPIバスを初期化する。
    """
    spi = SPI(0, baudrate=4000000, polarity=0, phase=1)
    
    # GPIOの設定
    sck = Pin(22)
    mosi = Pin(23)
    miso = Pin(20)
    cs = Pin(21, Pin.OUT, value=1)

def main():
    setup_spi()
    print('The main function stops with CTRL + C.')
    while True:
        try:
            with open('/lib/tempmon_oled.py', 'r') as file:
                exec(file.read())
            time.sleep(1)
        except KeyboardInterrupt:
            display.fill(0)  # Clear the display
            display.show()   # Update the display to show the changes
            break

# main関数を呼び出して実行
if __name__ == "__main__":
    main()
