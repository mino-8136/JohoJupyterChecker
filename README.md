# JohoJupyterChecker

学生が作成したJupyterNotebook内の課題を自動評価するためのプログラム

## 問題作成と評価の仕様
- 実行時の時間制限は3秒となっている
- 評価の仕様として、全角と半角の区別を統一する、大文字と小文字を統一する、スペースはすべて除去する、日本語の句読点は無視する。
- 評価の仕様として、コードセルは空欄のものは無視されます。課題を提示する際は「# 課題4」のように何かコメントを書いておくことを推奨します。
- 1課題1コードセルでのみ対応可能です。

複数の入力については以下のような複数inputに対応しています。(input例:1\n2\n)
```
a = input() 
b = input()
```

### 課題の追加方法
- Markdownセルで「## 演習問題」というセル以降の課題が評価されるようになっているので、ipynbファイルにはその1行が必要です。
- 現行のオンライン版では、https://mino-8136.github.io/JohoJupyterChecker/course_list.json に登録されているコース情報を取得しています。
- (対応中)オフライン版では、実行exeと同階層のdocsフォルダが参照されます。
- 必ず解かせたい問題がある場合は、その問題の得点を"101"のように末尾を工夫すると判別しやすいです。

## 授業利用時の手順
- 公式サイトからPythonをインストールする。インストール時には「Use admin prilileges when installing py.exe」にチェックを入れる。
  - Microsoft Store版だとうまく動かない？
- 公式サイトからVisual Studio Codeをインストールする。初期設定のままでOK。
- Visual Studio Codeに以下の拡張機能をインストールする。
  - Japanese Language Pack for Visual Studio Code
  - Python
  - Jupyter
- ipynbファイルからPythonを実行するとき、ipykernelのインストールを求められるのでインストールする

### エラー対応
- プログラムが実行できない場合、ユーザー名に全角スペースが含まれるケースが多いです。
  - 別途ローカルアカウントの作成を行わせるか、コンピュータ室のPCから実行してください。
- 実行結果が全て「Python」になる場合、py.exeのインストールができていません。
  - Pythonのインストーラーから、「Modify」から「py launcher」で瞬時に追加できます。
- Windows Defenderに削除される場合、別途Windows セキュリティの削除対象から外す必要があります。
  - Windows セキュリティ → ウイルスと脅威の防止 → 現在の脅威 → 保護の履歴 → それらしい項目名の「操作」→ 「許可」
  - exe化に使っているpyinstallerが誤検知の対象となっている可能性が高いです。
 
## 教員向け
### 利用の制限
- ある程度パソコン操作に習熟してきた頃からの利用を推奨します。
- 学年組番号の入力欄では0000~9999の数値に制限しています。

### JohoJupyterCheckerのカスタマイズ
- オフライン版を使用する場合、「main.py」で「`is_offline = True`」にしてください。
  - アプリケーションと同階層にdocsフォルダを配置してください。
  - 各課題のurlは、「`"url": "python_basic_101/assignment01.json"`」のように、docsフォルダ以下のパスを記述してください。
- 提出されたJSONデータに不正が生じないように、「src -> components -> StudentScore.vue の `encryptionKey`」に暗号化キーを記述してください。
  - 課題タイトル・ID4桁・得点が暗号化されています。
- 上記の手順が完了したら、下記の「授業者向けのアプリ化手順」を全て実行してください。

## 開発者向け

### 開発要件
- Python 3.12
- Node.js 20.15.0
- npm install axios vue-axios crypto-js
- pip install flask flask-cors nbformat pywebview
- pip install pyinstaller
- 内部サーバーは http://localhost:5000 で融通

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

### 授業者向けのアプリ化手順
```sh
npm install
python -m venv .venv
.venv\Scripts\activate
pip install flask flask-cors nbformat pywebview pyinstaller
npm run build
pyinstaller main.py --onefile --distpath application --clean --add-data "dist;dist" -n JohoJupyterChecker
```
