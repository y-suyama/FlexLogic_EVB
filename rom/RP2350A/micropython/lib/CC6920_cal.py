import CC6920

def save_values(a, b, c, d):
    with open("lib/caldat.py", "w", encoding="utf-8") as file:  # Pythonファイルとして保存
        file.write(f"current_offset = [{a}, {b}, {c}, {d}]")  # リストとして書き込み

def load_values():
    try:
        from lib.caldat import current_offset  # Pythonファイルをインポートしてリストを取得
        return 
    except (ImportError, ModuleNotFoundError):
        return None  # ファイルが存在しない場合は None を返す


ch1 = CC6920.zero_cal(1, 1, 20)   # チャネル1
ch2 = CC6920.zero_cal(1, 2, 10)   # チャネル2
ch3 = 0
#ch3 = CC6920.zero_cal(2, 3, 10)    # チャネル3
ch4 = CC6920.zero_cal(2, 4, 5)    # チャネル4

save_values(ch1, ch2, ch3, ch4)


