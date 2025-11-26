import utime
from machine import Pin, I2C
import tmpADC
from tmpOFFSET import offset
import ssd1306_extend

# 無限ループで定期的に温度情報を取得・表示
while True:
    # --- ADC1（SPI1_CS0）からの読み取り ---
    # 熱電対チャネル1と2、および内蔵温度センサ
    ch1 = tmpADC.conv(1, 1, offset[0])  # 熱電対チャネル1
    ch2 = tmpADC.conv(1, 2, offset[1])  # 熱電対チャネル2
    tmp1 = tmpADC.inttmp(1)            # 内蔵温度センサ（ADC1）

    # --- ADC2（SPI1_CS1）からの読み取り ---
    # 熱電対チャネル3と4、および内蔵温度センサ
    ch3 = tmpADC.conv(2, 3, offset[2])  # 熱電対チャネル3
    ch4 = tmpADC.conv(2, 4, offset[3])  # 熱電対チャネル4
    tmp2 = tmpADC.inttmp(2)            # 内蔵温度センサ（ADC2）

    # --- OLEDに温度データを表示 ---
    ssd1306_extend.oled_setting(ch1, ch2, ch3, ch4)

    # 更新間隔のウェイト（例：1秒ごと）
    utime.sleep(1)
