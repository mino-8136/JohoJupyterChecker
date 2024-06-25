# joho-judge-system

学生が作成したJupyterNotebook内の課題を自動評価するためのプログラム

## 問題作成の仕様

- Markdownセルで「## 演習問題」というセル以降の課題が評価されるようになっている
- 課題のファイルは…を参照するようになっている


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
