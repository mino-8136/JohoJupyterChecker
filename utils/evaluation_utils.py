import subprocess
import os
import tempfile
import nbformat

# TODO:outputの正規化を行なう関数を実装する

# outputと実行結果を比較する関数
def compare_output(output, output_example):
    if output == output_example:
        return True
    else:
        return False
    

# スクリプトを抽出する関数
def extract_scripts(notebook_path, start_keyword="## 演習問題"):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    code_cells = []
    exercise_started = False

    for cell in nb['cells']:
        #Markdownセルの処理
        if cell['cell_type'] == 'markdown':
            if start_keyword in cell['source']:
                exercise_started = True
        elif cell['cell_type'] == 'code' and exercise_started:
            code_cells.append(cell['source'])

    return code_cells


# 提出されたノートブックを評価する関数
def evaluate_submission(notebook_path, problems):
    total_results = []
    code_cells = extract_scripts(notebook_path)

    # 各提出コードに対してテストを実施する
    for idx, code in enumerate(code_cells):

        # 各コードを一時ファイルに保存する
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as script_file:
            script_file.write(code.encode('utf-8'))
            script_path = script_file.name

        # 問題データから入出力例を取得
        if idx < len(problems):
            problem = problems[idx]
            examples = problem["examples"]
        else:
            examples = []
        # print(examples)

       # 各入出力例に対するテスト結果を格納するリスト
        unit_results = {
            "problem": problem.get("name", f"Problem {idx + 1}"),
            "results": []
        }

        # 各入出力例を用いてテストを実施
        for example in examples:
            input_example = example["input"]
            output_example = example["output"]

            # コードを実行して評価
            try:
                result = subprocess.run(
                    ('python', script_path),
                    input=input_example,
                    capture_output=True, text=True, timeout=3)
                output = result.stdout + result.stderr
                status = compare_output(output, output_example)
            
            # エラー処理
            except subprocess.TimeoutExpired:
                output = "Execution timed out."
                status = False
            except subprocess.CalledProcessError as e:
                output = e.output
                status = False
            except Exception as e:
                output = str(e)
                status = False
            
            # 結果の追加
            unit_results["results"].append({
                "input": input_example,
                "expected_output": output_example,
                "received_output": output,
                "status": status
            })

        os.remove(script_path)
        total_results.append(unit_results)

    print(total_results)
    return total_results