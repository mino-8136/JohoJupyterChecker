import sys
from pathlib import Path
import json

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
        # 実行ファイルで起動した場合、展開先ディレクトリを基点とする。
        return Path(sys.executable).parent 
    else:
        # python コマンドで起動した場合、プロジェクトディレクトリを基点とする。(開発時)
        return Path(".")