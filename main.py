from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
import json
import os
import sys
import tempfile
import webbrowser

from utils.file_utils import base_dir, get_all_assignments
from utils.evaluation_utils import compare_output, evaluate_submission

app = Flask(
    __name__, 
    static_folder= base_dir() /  "dist/static", 
    template_folder= base_dir() / "dist", 
    static_url_path="/static"
)
CORS(app)

# ファイル一覧を取得するAPI
@app.route('/api/assignments')
def api_get_all_assignments():
    return jsonify(get_all_assignments())

# 課題データを返すAPI
@app.route('/api/submit', methods=['POST'])
def submit_assignment():

    # 提出されたJupyterNotebookファイルの読み込み
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    
    # 一時ファイルとしてJupyterNotebookファイルを保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ipynb') as tmp:
        file.save(tmp.name)
        notebook_path = tmp.name
        
    # 渡された課題JSONデータから問題を抽出する
    assignments = json.loads(request.form['assignments'])
    problems = assignments['problems']
    # print(problems)

    # JupyterNotebookファイルと課題データを実行して評価
    try:
        results = evaluate_submission(notebook_path, problems)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # 一時ファイルを削除
        os.remove(notebook_path)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # TODO:開発中はコメントアウト
    # webbrowser.open("http://localhost:5000/", new=2, autoraise=True)
    app.run(debug=True, port=5000)