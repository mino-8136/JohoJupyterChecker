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

## 開発要件
- Python 3.12
- Node.js 20.15.0
- npm install axios vue-axios
- pip install flask flask-cors nbformat
- pip install jinja2==3.0.3  (バージョン指定必要？)
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

### アプリケーションのビルド

```sh
npm run build
```
### Python経由での起動
```
python main.py
```
