import urllib.request
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
import json
import os
import sys
import tempfile
import webbrowser
import webview
import threading
import urllib
import urllib.request

from utils.file_utils import base_dir, docs_dir
from utils.evaluation_utils import evaluate_submission

#--------------------------------------------------------------#
is_offline = False # オフラインモードの場合はTrueにする
#--------------------------------------------------------------#

app = Flask(
    __name__, 
    template_folder= base_dir() / "dist", 
    static_folder= base_dir() /  "dist/static", 
    static_url_path="/static"
)
CORS(app)

# コース一覧を取得するAPI
@app.route('/api/courses')
def api_get_all_courses():
    if is_offline:
        # オフラインモードの場合、ローカルからコース一覧ファイルを取得する
        url = docs_dir() / "docs" / "course_list.json"
        with url.open('r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data)
    else: 
        # オンラインモードの場合、指定されたURLからコース一覧ファイルを取得する
        url = "https://mino-8136.github.io/JohoJupyterChecker/course_list.json"
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
            return jsonify(data)
        except urllib.error.HTTPError as e:
            return jsonify({"error": f"HTTPError: {e.code}"}), 500


# 指定されたURL/パスから課題ファイルを1つ取得するAPI
@app.route('/api/assignments', methods=['POST'])
def api_get_all_assignments():
    if is_offline:
        # オフラインモードの場合、指定されたディレクトリ内のjsonファイルを取得
        url = docs_dir() / "docs" / request.json['url']
        with url.open('r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data)
    else:
        # オンラインモードの場合、指定されたURLから課題ファイルを取得する
        url = request.json['url']
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
            return jsonify(data)
        except urllib.error.HTTPError as e:
            return jsonify({"error": f"HTTPError: {e.code}"}), 500


# 提出された課題ファイルを正誤判定して返すAPI
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

def start_server():
    app.run(port=5000, debug=False)

if __name__ == '__main__':
    # WebBrowser版の場合
    #webbrowser.open("http://localhost:5000/", new=2, autoraise=True)
    #app.run(debug=True, port=5000)

    # Flaskサーバーをバックグラウンドで実行
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()

    # Pywebviewウィンドウを開く
    webview.create_window("JohoJupyterChecker", "http://localhost:5000/", width=600, height=800, min_size=(500, 300))
    webview.start()
    sys.exit()