import sys
import os
import json
from pathlib import Path

# 実行ファイルの基点ディレクトリを取得
def base_dir():
    if hasattr(sys, "_MEIPASS"):
        # 実行ファイルで起動した場合、展開先ディレクトリを基点とする。
        return Path(sys._MEIPASS)
    else:
        # python コマンドで起動した場合、プロジェクトディレクトリを基点とする。(開発時)
        return Path(".")

# 課題ファイルの基点ディレクトリを取得
def docs_dir():
    if hasattr(sys, "_MEIPASS"):
        # 実行ファイルで起動した場合、もとの実行ファイルのディレクトリを基点とする。
        return Path(sys.executable).parent 
    else:
        # python コマンドで起動した場合、プロジェクトディレクトリを基点とする。(開発時)
        return Path(".")

# ディレクトリ内のファイル構造を元にJSONを生成する関数
def generate_course_structure(base_path):
    # 辞書を作成
    structure = {"courses": {}}
    
    # ディレクトリを走査
    for course_name in os.listdir(base_path):
        course_path = os.path.join(base_path, course_name)
        if os.path.isdir(course_path):  # コースフォルダか確認
            checkers = []
            for file_name in os.listdir(course_path):
                file_path = os.path.join(course_path, file_name)
                # JSONファイルのみ処理
                if os.path.isfile(file_path) and file_name.endswith(".json"):
                    checkers.append(f"{course_name}/{file_name}")
            # コースとその課題を辞書に追加
            if checkers:  # 課題があれば追加
                structure["courses"][course_name] = {"checkerURLs": checkers}
    
    return structure