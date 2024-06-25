from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
import json
import nbformat
import os
import subprocess
import sys
import tempfile
import webbrowser


# 実行ファイルの基点ディレクトリを取得
def base_dir():
    if hasattr(sys, "_MEIPASS"):
        # 実行ファイルで起動した場合、展開先ディレクトリを基点とする。
        return Path(sys._MEIPASS)
    else:
        # python コマンドで起動した場合、プロジェクトディレクトリを基点とする。
        return Path(".")

app = Flask(
    __name__, 
    static_folder= base_dir() /  "dist/static", 
    template_folder= base_dir() / "dist", 
    static_url_path="/static"
    )
CORS(app)


# スクリプトを抽出する
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



# 課題データを返すAPI
@app.route('/api/submit', methods=['POST'])
def submit_assignment():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file provided"}), 400
    
    # 一時ファイルとしてJupyterNotebook全体を保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ipynb') as tmp:
        file.save(tmp.name)
        notebook_path = tmp.name

    try:
        # Notebookファイルをjsonとして読み込み、各スクリプトを取得
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        results = []
        code_cells = extract_scripts(notebook_path)
        
        #print(code_cells)

        # 各スクリプトを実行し、結果を収集
        for code in code_cells:

            # 一時ファイルとしてスクリプトを保存 (名前に空白があるとつらい)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as script_file:
                script_file.write(code.encode('utf-8'))
                script_path = script_file.name
                #print(script_path)
            
            try:
                result = subprocess.run(('python', script_path), capture_output=True, text=True, timeout=5)
                output = result.stdout + result.stderr
               
            except subprocess.TimeoutExpired:
                output = "Execution timed out."
            except subprocess.CalledProcessError as e:
                output = e.output
            except Exception as e:
                output = str(e)
            
            results.append({
                "code": code,
                "output": output
            })

            os.remove(script_path)
        
        # 出力結果をjsonファイルでreturnする
        print(results)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # 一時ファイルを削除
        os.remove(notebook_path)

@app.route("/")
def index():
    """フロントエンド側のページを表示する。

    Returns:
        str: HTML
    """
    return render_template("index.html")

if __name__ == '__main__':
    webbrowser.open("http://localhost:5000/", new=2, autoraise=True)
    app.run(debug=False, port=5000)