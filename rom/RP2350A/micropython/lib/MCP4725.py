import time
from machine import I2C, Pin

# I2Cバスの初期化（バス1、SCL: GPIO3, SDA: GPIO2, 周波数: 100kHz）
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100_000)

# 接続されているI2Cデバイスをスキャン
devices = i2c.scan()
print("I2Cデバイス検出:", devices)

# デバイスが見つからない場合はエラー
if not devices:
    raise RuntimeError("I2Cデバイスが見つかりません。配線や電源を確認してください。")

# MCP4725のI2Cアドレス（スキャン結果から確認）
DAC_ADDR = 0x60

# MCP4725が接続されていなければエラー
if DAC_ADDR not in devices:
    raise RuntimeError(f"MCP4725がアドレス 0x{DAC_ADDR:02X} に見つかりません。")

# -------------------------------
# 出力電圧の設定と送信処理
# -------------------------------

VREF = 5.0       # 基準電圧（MCP4725のVccに依存）
VOUT = 1.5       # 出力したい電圧（0〜VREFの範囲で指定）

# 出力電圧を12ビットDACのデジタル値に変換
code12 = int(VOUT / VREF * 4095 + 0.5)

# デジタル値をMSB/LSBに分割（Fast Mode：0x40）
msb = code12 >> 4
lsb = (code12 & 0x0F) << 4
frame = bytes([0x40, msb, lsb])  # コマンド+データ

# MCP4725に出力値を送信
i2c.writeto(DAC_ADDR, frame)

print(f"MCP4725に {VOUT:.2f} V（コード {code12}）を設定しました（アドレス: 0x{DAC_ADDR:02X}）")
