import machine
import utime
from machine import Pin, SPI
import k_thermo

def two_complement_to_signed_int(value, bit_length):
    """
    指定されたビット長の二の補数表現を符号付き整数に変換する。

    :param value: 二の補数形式の整数値
    :param bit_length: 値のビット長（例：16, 14）
    :return: 符号付き整数
    """
    if value >= 1 << (bit_length - 1):
        value -= 1 << bit_length
    return value

def setup_spi_and_cs(no):
    """
    SPIバスと対応するチップセレクトピンを初期化する。

    :param no: 使用するSPIスレーブ番号（1または2）
    :return: spiオブジェクト、csピンオブジェクト
    """
    spi = SPI(1, baudrate=4000000, polarity=0, phase=1,
              sck=Pin(10), mosi=Pin(11), miso=Pin(8))
    cs_pin = Pin(4 if no == 1 else 24, Pin.OUT, value=1)
    return spi, cs_pin

def spi_transfer(spi, cs_pin, txdata):
    """
    SPI経由でデータを送信し、応答を受信する。

    :param spi: SPIオブジェクト
    :param cs_pin: チップセレクトピン
    :param txdata: 送信データ（bytearray）
    :return: 受信データ（bytearray）
    """
    rxdata = bytearray(len(txdata))
    utime.sleep(0.07)
    cs_pin(0)
    try:
        spi.write(txdata)
        utime.sleep(0.1)
    finally:
        cs_pin(1)

    utime.sleep(0.07)
    cs_pin(0)
    try:
        spi.write_readinto(txdata, rxdata)
        utime.sleep(0.1)
    finally:
        cs_pin(1)

    return rxdata

def inttmp(no):
    """
    内部温度センサの生データを取得する。

    :param no: 使用するデバイス番号（1または2）
    :return: 14ビット精度の温度センサ出力（整数）
    """
    txdata = bytearray([0xBD, 0x1B])
    spi, cs_pin = setup_spi_and_cs(no)
    rxdata = spi_transfer(spi, cs_pin, txdata)

    raw = (rxdata[0] << 6) | (rxdata[1] >> 2)
    return two_complement_to_signed_int(raw, 14)

def conv(no, ch, offset):
    """
    K型熱電対からの測定値を℃に変換する。

    :param no: 使用するデバイス番号（1または2）
    :param ch: 測定対象のチャネル（1〜4）
    :param offset: オフセット補正値
    :return: 補正済みの温度（℃）
    """
    txdata = bytearray(2)
    txdata[1] = 0x0B  # ADCのConfigレジスタ設定

    # 測定チャネルの選択
    txdata[0] = 0x8D if ch in (1, 3) else 0xBD

    spi, cs_pin = setup_spi_and_cs(no)
    rxdata = spi_transfer(spi, cs_pin, txdata)

    raw = (rxdata[0] << 8) | rxdata[1]
    voltage_mv = two_complement_to_signed_int(raw, 16) * 0.256 * 1000 / 32768  # 2^15 = 32768

    # 内部温度センサの補正電圧を加算
    cold_junction_temp = inttmp(no) * 0.03125
    voltage_mv += k_thermo.linear_interpolation_t_to_v(cold_junction_temp)

    # 熱電対電圧から温度へ変換
    temp_c = k_thermo.linear_interpolation_v_to_t(voltage_mv)
    return temp_c + offset
