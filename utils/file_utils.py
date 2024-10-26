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

# coursesディレクトリ内の全てのディレクトリ名を取得する(オフライン用につき未使用)
def get_all_courses():
    # coursesディレクトリのパスを取得
    courses_dir = base_dir() / "dist/static/courses"
    # coursesディレクトリ内のディレクトリ名を取得
    courses = [course.name for course in courses_dir.iterdir() if course.is_dir() and not course.name.startswith('.')]
    return courses

# 指定されたディレクトリ内のすべての課題jsonファイルを取得する(オフライン用につき未使用)
def get_all_assignments(course_name):
    # 指定されたディレクトリ内のjsonファイルを取得
    courses_dir = base_dir() / "dist/static/courses" / course_name
    assignments = []
    
    # ディレクトリ内のjsonファイルを読み込む
    for assignment in courses_dir.iterdir():
        if assignment.is_file() and assignment.suffix == ".json":
            with assignment.open('r', encoding='utf-8') as f:
                # jsonファイルの内容を読み込み、リストに追加
                try:
                    data = json.load(f)
                    assignments.append(data)
                except json.JSONDecodeError:
                    print(f"ファイルの読み込みに失敗しました: {assignment.name}")
                    
    return assignments
