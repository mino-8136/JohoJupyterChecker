# joho-judge-system

学生が作成したJupyterNotebook内の課題を自動評価するためのプログラム

## 問題作成と評価の仕様

- Markdownセルで「## 演習問題」というセル以降の課題が評価されるようになっている
- 課題のファイルは(!未定)を参照するようになっている
- 実行時の時間制限は3秒となっている
- 評価の仕様として、全角と半角の区別を統一する、大文字と小文字を統一する、スペースはすべて除去する


複数の入力については以下のような複数inputを想定しており、自動入力も改行で区切ります。(例:1\n2\n)
```
a = input() 
b = input()
```

以下のようなスペース区切りには現在対応していません。(例:1 2)
```
a, b = input()
```

## 授業利用時のメモ
- プログラム動作時にpythonを叩くので、cmdから「python」が実行できるようにPATHを通す必要がある
- プログラムが実行できない場合、パスの日本語状態が問題になっている可能性があるのでローカルアカウントの作成をする
- pip install flask flask-cors noformat pywebview を実行しないと実行評価ができない？

## 開発要件
- Python 3.12
- Node.js 20.15.0
- npm install axios vue-axios crypto-js
- pip install flask flask-cors nbformat pywebview
- pip install pyinstaller
- 内部サーバーは http://localhost:5000 で融通


## 諸々の操作

### Projectの初回起動

```sh
npm install
```

### 内部サーバーの起動

```sh
npm run dev
```

### 仮想環境の用意
```sh
python -m venv .venv
.venv\Scripts\activate
(いろいろなライブラリのインストール)
```

### Python経由での起動
```
npm run build
python main.py
```

### アプリケーションのビルド
```
npm run build
.venv\Scripts\activate
pyinstaller main.py --onefile --distpath application --clean --add-data "dist;dist" -n JohoJudgeSystem
```

- コンソールはあったほうが生徒の質問対応がしやすいかも

### その他
- git fetch -p
- git branch -d 削除ブランチ名 
- git branch -D 強制削除ブランチ名