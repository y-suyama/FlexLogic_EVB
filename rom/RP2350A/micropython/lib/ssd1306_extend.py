import machine
import ssd1306
import framebuf
import math
from machine import Pin, I2C

# --- 内蔵フォントをfractional scaleで拡大して描く関数 ---
def draw_scaled_text(oled, text, x, y, scale=1.0):
    """
    内蔵フォントでテキストをフレームバッファに描画後、
    拡大してOLEDに描画します。
    """
    x, y = int(x), int(y)
    width, height = len(text) * 8, 8
    buf = bytearray(width * height)
    fb = framebuf.FrameBuffer(buf, width, height, framebuf.MONO_HLSB)
    fb.fill(0)
    fb.text(text, 0, 0, 1)

    dest_width, dest_height = int(width * scale), int(height * scale)
    
    # 最近傍補間でピクセルを拡大描画
    for j in range(dest_height):
        src_y = min(int(j / scale), height - 1)
        for i in range(dest_width):
            src_x = min(int(i / scale), width - 1)
            if fb.pixel(src_x, src_y):
                oled.pixel(x + i, y + j, 1)

# --- 数値を丸めて分割する関数 ---
def round_and_split(number):
    """
    数値を小数点以下2桁に丸め、整数部と小数部を返します。
    """
    rounded = round(number, 2)
    integer_part = int(rounded)
    decimal_part = int((rounded - integer_part) * 100)
    return integer_part, decimal_part

# --- チャンネルごとに表示するテキストを生成 ---
def prepare_text(channels):
    """
    各チャネルの値を処理し、大きいテキストと小さいテキストを作成します。
    """
    big_text, small_text = [], []
    for ch in channels:
        if ch > 1000:
            big_text.append("----")
            small_text.append("")
        else:
            big, small = map(str, round_and_split(ch))
            big_text.append(big)
            small_text.append('.'+small)
    return big_text, small_text

# --- OLEDの設定および描画関数 ---
def oled_setting(ch1, ch2, ch3, ch4):
    """
    4つのチャネル値をOLEDディスプレイに表示します。
    """
    # I2Cの初期化
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)

    # チャネルデータとテキスト生成
    channels = [ch1, ch2, ch3, ch4]
    big_text, small_text = prepare_text(channels)

    # テキストの描画位置とサイズ計算
    big_scale = 1.7
    big_char_w, big_char_h = 8 * big_scale, 8 * big_scale
    small_char_w, small_char_h = 8, 8
    left_margin, gap = 1, 1

    x_small_offset = [left_margin + len(big) * big_char_w + gap for big in big_text]
    offset_big_y = 32 - big_char_h
    offset_small_y = offset_big_y + (big_char_h - small_char_h)

    # 画面を四分割する領域の定義
    quadrants = [(0, 0), (64, 0), (0, 32), (64, 32)]

    # 各領域にテキストを描画
    for i, (base_x, base_y) in enumerate(quadrants):
        draw_scaled_text(oled, big_text[i], base_x + left_margin, base_y + offset_big_y, big_scale)
        oled.text(small_text[i], int(base_x + x_small_offset[i]), int(base_y + offset_small_y), 1)

    # 画面を四分割する線の描画
    oled.hline(0, 32, 128, 1)   # 横線
    oled.vline(64, 0, 64, 1)    # 縦線

    # 左上にラベルを描画
    for i, label in enumerate(["ch1", "ch2", "ch3", "ch4"]):
        x, y = quadrants[i][0] + 2, quadrants[i][1] + 2
        oled.text(label, x, y, 1)

    oled.show()  # 描画を反映
