import subprocess
import shutil
import os
import tempfile
import nbformat
import unicodedata
import re
from enum import Enum

# TypeScriptのStatus列挙型に対応するPythonのStatus列挙型(Common.tsと同様の定義)
class Status(Enum):
    Correct = '正解'
    Incorrect = '不正解'
    Error = 'エラー'
    Unanswered = '未回答'

# outputの正規化を行なう関数
# 半角文字への統一、文字列中の空白の削除、改行コードの統一
def normalize_output(output):
    output = unicodedata.normalize('NFKC', output) # 全角文字を半角文字に変換
    output = re.sub(r'[。、]', '', output)  # 文末の句読点を除去
    output = re.sub(r'\s+', '', output) # 空白文字を削除
    output = output.replace('\r\n', '\n').replace('\r', '\n') # 改行コードを統一
    return output

# input() 関数のメッセージ部分を空にする
def remove_input_message(code):
    pattern = r'input\s*\(\s*(?P<quote>[\'"])(?:\\.|[^\\])*?(?P=quote)\s*\)'
    modified_code = re.sub(pattern, 'input()', code)
    return modified_code

# outputと実行結果を比較する関数
def compare_output(output_user, output_test):
    # outputの正規化を行う
    output_user = normalize_output(output_user)
    output_test = normalize_output(output_test)

    if output_user == output_test:
        return Status.Correct
    elif output_user == "" or output_user == "\n":
        return Status.Unanswered
    else:
        return Status.Incorrect

# 実行するpythonコマンドを決定する関数
def get_python_command():
    if shutil.which("py"):
        return "py"
    elif shutil.which("python"):
        return "python"
    else:
        return 

# スクリプトを抽出する関数
def extract_scripts(notebook_path, start_keyword="## 演習問題"):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    code_cells = []
    exercise_started = False

    for cell in nb['cells']:
        #「## 演習問題」のセルを見つける
        if cell['cell_type'] == 'markdown':
            if start_keyword in cell['source']:
                exercise_started = True
        #Codeセルを抽出する処理
        elif cell['cell_type'] == 'code' and exercise_started and cell['source'] != '' :
            code_cells.append(cell['source'])

    return code_cells


# 提出されたノートブックを評価する関数
def evaluate_submission(notebook_path, problems):
    total_results = []
    code_cells = extract_scripts(notebook_path)
    cmd_command = get_python_command()

    # コマンドが見つからない場合はエラーを返す
    if cmd_command is None:
        print("Pythonが見つかりませんでした。")
        return 

    # 各提出コードに対してテストを実施する
    for idx, code in enumerate(code_cells):

        # 各コードを一時ファイルに保存する
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as script_file:
            modified_code = remove_input_message(code) # input関数を置き換える
            script_file.write(modified_code.encode('utf-8'))
            script_path = script_file.name

        # 問題データから入出力例を取得
        if idx < len(problems):
            problem = problems[idx]
            test_cases = problem["testCases"]
        else:
            test_cases = []

        # 各入出力例に対するテスト結果を格納するリスト
        unit_results = {
            "problem": problem.get("name", f"Problem {idx + 1}"),
            "results": []
        }

        # 各入出力例を用いてテストを実施
        case_index = 1
        for test_case in test_cases:
            input = test_case["input"]
            output = test_case["output"]

            # コードを実行して評価
            try:
                result = subprocess.run(
                    (cmd_command, script_path),
                    input=input,
                    capture_output=True, text=True, timeout=3)
                output_user = result.stdout + result.stderr

                # エラーの取得と判定
                if result.returncode != 0:
                    status = Status.Error
                else:
                    status = compare_output(output_user, output)
            
            # エラー処理
            except subprocess.TimeoutExpired:
                output_user = "Execution timed out."
                status = Status.Error
            except subprocess.CalledProcessError as e:
                output_user = e.output
                status = Status.Error
            except Exception as e:
                output_user = str(e)
                status = Status.Error
            
            # 結果の追加
            unit_results["results"].append({
                "input": input,
                "output": output,
                "output_user": output_user,
                "status": status.value
            })

            # print(f"{problem.get('name', 'Problem {idx + 1}')} [case:{case_index}] -> {status.value}")
            case_index += 1

        os.remove(script_path)
        total_results.append(unit_results)

    return total_results