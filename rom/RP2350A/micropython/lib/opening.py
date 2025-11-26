import time
import random
from machine import I2C, Pin
import ssd1306
import framebuf

# ========================================================
# SSD1306ディスプレイの設定（例：128×64）
# ========================================================
WIDTH = 128
HEIGHT = 64

# I2Cの初期化（scl=Pin(1), sda=Pin(0)）
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# ========================================================
# ① マトリックス風アニメーション（"SUYAMA" を使用、3秒間表示）
# ========================================================
def matrix_animation(duration=3):
    num_cols = WIDTH // 8      # 例: 128/8 = 16列
    num_rows = HEIGHT // 8     # 例: 64/8 = 8行
    charset = "SUYAMA"         # 使用する文字集合
    # 各カラムの降下開始位置にズレを持たせる（負の値で初期化）
    drops = [random.randint(-num_rows, 0) for _ in range(num_cols)]
    tail_length = 3            # 尻尾の長さ

    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < duration * 1000:
        display.fill(0)      # 画面全体クリア
        for col in range(num_cols):
            drop = drops[col]
            # ドロップの先頭部と尻尾部分を描画
            for t in range(tail_length):
                pos = drop - t
                if 0 <= pos < num_rows:
                    ch = random.choice(charset)
                    x = col * 8
                    y = pos * 8
                    display.text(ch, x, y, 1)
            # 各カラムの位置を1行分下へ移動
            drops[col] = drop + 1
            if drops[col] - tail_length > num_rows:
                drops[col] = random.randint(-num_rows, 0)
        display.show()
        time.sleep(0.05)

# ========================================================
# ② 各文字を大きく表示する関数
# ・内蔵8×8フォントをscale倍に拡大し、画面中央に描画
# ========================================================
def draw_large_letter(letter, scale=6):
    display.fill(0)  # 画面クリア
    # 8×8の一時バッファ作成
    buf = bytearray((8 * 8) // 8)
    fb = framebuf.FrameBuffer(buf, 8, 8, framebuf.MONO_HLSB)
    fb.fill(0)
    fb.text(letter, 0, 0, 1)
    
    text_width = 8 * scale
    text_height = 8 * scale
    x0 = (WIDTH - text_width) // 2
    y0 = (HEIGHT - text_height) // 2

    # バッファ内の各ピクセルをscale倍の矩形として描画
    for row in range(8):
        for col in range(8):
            if fb.pixel(col, row):
                display.fill_rect(x0 + col * scale, y0 + row * scale, scale, scale, 1)
    display.show()

# ========================================================
# ③ 文字列全体を大きく表示する関数（画面中央に配置）
# ========================================================
def draw_large_text(text, scale):
    display.fill(0)
    text_width = len(text) * 8 * scale
    text_height = 8 * scale
    x0 = (WIDTH - text_width) // 2
    y0 = (HEIGHT - text_height) // 2

    for i, letter in enumerate(text):
        buf = bytearray((8 * 8) // 8)
        fb = framebuf.FrameBuffer(buf, 8, 8, framebuf.MONO_HLSB)
        fb.fill(0)
        fb.text(letter, 0, 0, 1)
        x = x0 + i * 8 * scale
        for row in range(8):
            for col in range(8):
                if fb.pixel(col, row):
                    display.fill_rect(x + col * scale, y0 + row * scale, scale, scale, 1)
    display.show()

# ========================================================
# 白黒反転関数
# ・ディスプレイのバッファ内各バイトをXOR処理
# ========================================================
def invert_display():
    for i in range(len(display.buffer)):
        display.buffer[i] ^= 0xFF
    display.show()

# ========================================================
# メイン処理
# ========================================================
# ① マトリックス風アニメーションを3秒間表示
matrix_animation(3)

# ② 各文字（"S", "U", "Y", "A", "M", "A"）を拡大表示し、0.1秒ずつ順番に表示するシーケンスを3回反復
for cycle in range(3):
    for letter in "SUYAMA":
        draw_large_letter(letter, scale=6)
        time.sleep(0.1)

# ③ 最終表示：文字列全体 "SUYAMA" を画面中央に表示
final_text = "SUYAMA"
final_scale = min(WIDTH // (len(final_text) * 8), HEIGHT // 8)
draw_large_text(final_text, final_scale)

# ④ 最終表示を0.02秒ごとに白黒反転5回
for _ in range(5):
    invert_display()
    time.sleep(0.02)