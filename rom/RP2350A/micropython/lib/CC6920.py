import utime
from machine import I2C, Pin
import caldat
from caldat import current_offset
# I2C通信の初期化
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100_000)
#devices = i2c.scan()
#print("I2C devices found:", devices)
def twos_complement_to_signed(value, bit_length):
    """
    2の補数表現の値を符号付き整数に変換する

    :param value: 2の補数表現の値
    :param bit_length: ビット幅
    :return: 符号付き整数
    """
    if value >= 2 ** (bit_length - 1):
        value -= 2 ** bit_length
    return value

def get_current(adno, ch, capa):
    """
    I2C経由でADCから取得した電流値（mA）を返す

    :param adno: A/Dコンバータの番号。1の場合は0x48、2の場合は0x49を使用する
    :param ch: チャネル番号（1, 2, 3, 4）
    :param capa: 測定レンジ（20, 10, 5）
    :return: 計算された電流値（mA）
    """
    # I2C通信で使用するデバイスアドレスの設定（adnoが1の場合は0x48、2の場合は0x49）
    sad = 0x48 if adno == 1 else 0x49

    # チャネル番号に応じたMUX設定（チャネル1,3なら0x81、チャネル2,4なら0xB1）
    mux = 0x81 if ch in (1, 3) else 0xB1

    # capa値に応じた変換レートの設定
    rate_map = {20: 100, 10: 200, 5: 400}
    rate = rate_map.get(capa)
    if rate is None:
        raise ValueError(f"Invalid capa value: {capa}")

    # ADCの設定レジスタに書き込み
    i2c.writeto(sad, bytes([0x01, mux, 0x03]))
    utime.sleep(0.1)

    # ADCの変換結果レジスタを選択するため、レジスタポインタを0x00に設定
    i2c.writeto(sad, bytes([0x00]))
    utime.sleep(0.1)

    # 2バイトのデータを読み込む
    rxdata = i2c.readfrom(sad, 2)
    # print("Raw received data:", rxdata)

    # 受信した2バイトのデータを結合して16ビットの値にする
    ret = (rxdata[0] << 8) | rxdata[1]
    # OFFset補正
    ret = ret - current_offset[ch - 1]
    # 2の補数表現の値を符号付き整数に変換
    signed_val = twos_complement_to_signed(ret, 16)

    # ADCで読み取った値を電圧（mV）に変換する
    # 基準電圧6.144Vおよび差動入力（2分割）の影響を考慮
    voltage_mv = (signed_val * 6.144 * 1000) / (2 ** 15 * 2)

    # 電圧値を変換レートで割り、電流（mA）を算出する
    current_mA = (voltage_mv / rate)*1000
    # print(f"Calculated current: {current_mA:.2f} mA")
    return current_mA

def zero_cal(adno, ch, capa):
    """
    I2C経由でADCから取得した電流値（mA）を返す

    :param adno: A/Dコンバータの番号。1の場合は0x48、2の場合は0x49を使用する
    :param ch: チャネル番号（1, 2, 3, 4）
    :param capa: 測定レンジ（20, 10, 5）
    :return: 計算された電流値（mA）
    """
    # I2C通信で使用するデバイスアドレスの設定（adnoが1の場合は0x48、2の場合は0x49）
    sad = 0x48 if adno == 1 else 0x49

    # チャネル番号に応じたMUX設定（チャネル1,3なら0x81、チャネル2,4なら0xB1）
    mux = 0x81 if ch in (1, 3) else 0xB1

    # capa値に応じた変換レートの設定
    rate_map = {20: 100, 10: 200, 5: 400}
    rate = rate_map.get(capa)
    if rate is None:
        raise ValueError(f"Invalid capa value: {capa}")

    # ADCの設定レジスタに書き込み
    i2c.writeto(sad, bytes([0x01, mux, 0x03]))
    utime.sleep(0.1)

    # ADCの変換結果レジスタを選択するため、レジスタポインタを0x00に設定
    i2c.writeto(sad, bytes([0x00]))
    utime.sleep(0.1)

    # 2バイトのデータを読み込む
    rxdata = i2c.readfrom(sad, 2)
    # print("Raw received data:", rxdata)

    # 受信した2バイトのデータを結合して16ビットの値にする
    ret = (rxdata[0] << 8) | rxdata[1]
    return ret

def load_values():
    try:
        with open("caldata.txt", "r") as file:
            return file.read().split(",")  # 読み込んでリストに変換
    except FileNotFoundError:
        return None

# devices = i2c.scan()
# print("I2C devices found:", devices)

#offset = load_values

# 各チャネルの電流を計測（例としてチャネル1、2、4の値を取得）
get_current(1, 1, 20)   # チャネル1
get_current(1, 2, 10)   # チャネル2
get_current(2, 3, 10)   # チャネル3
get_current(2, 4, 5)    # チャネル4
