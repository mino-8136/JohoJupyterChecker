import sys
from pathlib import Path
import json

# 実行ファイルの基点ディレクトリを取得
def base_dir():
    if hasattr(sys, "_MEIPASS"):
        # 実行ファイルで起動した場合、展開先ディレクトリを基点とする。
        return Path(sys._MEIPASS)
    else:
        # python コマンドで起動した場合、プロジェクトディレクトリを基点とする。
        return Path(".")



# 課題jsonのすべてのパスを取得するAPI(未完成)
def get_all_assignments():
    # 課題jsonファイルを読み込む
    directory_path = 'public/static/assignments'
    json_files = Path(directory_path).glob('*.json')

    all_data = []
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_data.append(data)
    
    return all_data
