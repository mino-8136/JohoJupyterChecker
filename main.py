from flask import Flask, request, jsonify
from flask_cors import CORS
import nbformat
from nbconvert import PythonExporter
import subprocess
import os
import tempfile

app = Flask(__name__)
CORS(app)

# 課題データを読み込む
import json

with open('problems/week1.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

@app.route('/api/submit', methods=['POST'])
def submit_assignment():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file provided"}), 400

    # 一時ファイルとして保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ipynb') as tmp:
        file.save(tmp.name)
        notebook_path = tmp.name

    try:
        # NotebookファイルをPythonスクリプトに変換
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        exporter = PythonExporter()
        source, _ = exporter.from_notebook_node(nb)

        # Pythonスクリプトとして一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
            script_path = tmp.name
            with open(script_path, 'w', encoding='utf-8') as script_file:
                script_file.write(source)

        # スクリプトを実行し、結果を収集
        result = subprocess.run(['python', script_path], capture_output=True, text=True, timeout=10)
        
        # 出力結果を比較
        output = result.stdout.strip()
        results = []
        for problem in problems['assignments']:
            expected_output = problem['expected_output'].strip()
            result_status = (output == expected_output)
            results.append({
                'name': problem['name'],
                'status': result_status
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # 一時ファイルを削除
        os.remove(notebook_path)
        os.remove(script_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
