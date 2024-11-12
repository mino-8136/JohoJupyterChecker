# JohoJupyterChecker

学生が作成したJupyterNotebook内の課題を自動評価するためのプログラム

## 問題作成と評価の仕様
- 実行時の時間制限は3秒となっている
- 評価の仕様として、全角と半角の区別を統一する、大文字と小文字を統一する、スペースはすべて除去する、日本語の句読点は無視する。

複数の入力については以下のような複数inputに対応しています。(input例:1\n2\n)
```
a = input() 
b = input()
```

### 課題の追加方法
- Markdownセルで「## 演習問題」というセル以降の課題が評価されるようになっているので、その1行が必要。
- docs/course_list.json に登録されているコース情報を取得しているので、課題追加時はそこも追記。
  - ローカルのオフラインモードでアプリケーションで実行する場合、実行exeと同階層のdocsフォルダが参照されます。

## 授業利用時の手順
- 公式サイトからPythonをインストールする。インストール時には「Use admin prilileges when installing py.exe」にチェックを入れる。
  - Microsoft Store版だとうまく動かない？
- 公式サイトからVisual Studioをインストールする。初期設定のままでOK。
- Visual Studio Codeに以下の拡張機能をインストールする。
  - Japanese Language Pack for Visual Studio Code
  - Python
  - Jupyter
- ipynbファイルからPythonを実行するとき、ipykernelのインストールを求められるのでインストールする

### エラー対応
- プログラムが実行できない場合、ユーザー名に全角スペースが含まれるケースが多い。
  - 別途ローカルアカウントの作成を行わせるか、コンピュータ室のPCから実行する
- 実行結果が全て「Python」になる場合、py.exeのインストールができていない。
  - Pythonのインストーラーから、「Modify」から「py launcher」で瞬時に追加できる

## 開発者向け

### 開発要件
- Python 3.12
- Node.js 20.15.0
- npm install axios vue-axios crypto-js
- pip install flask flask-cors nbformat pywebview
- pip install pyinstaller
- 内部サーバーは http://localhost:5000 で融通
- 
### Projectの初回起動
```sh
npm install
```

### 仮想環境の用意
```sh
python -m venv .venv
.venv\Scripts\activate
(上記のpipライブラリのインストール)
```

### Python経由での起動
```sh
npm run build
py main.py
```

### アプリケーションのビルド
```sh
.venv\Scripts\activate
npm run build
pyinstaller main.py --onefile --distpath application --clean --add-data "dist;dist" -n JohoJupyterChecker
```