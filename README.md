# JohoJupyterChecker

学生が作成したJupyterNotebook内の課題を自動評価するためのソフトウェア

<img src="https://github.com/user-attachments/assets/fda1b0e8-23b8-495f-96e1-03703a6ef6c5" width="300" />

- assignment … 学生が編集するipynbファイルや、各課題のこと
- checker(チェッカー) … テストケースが記述されたjsonファイル(バックエンド側での呼び方)
- course(コース) … 各assignment/checkerがまとめられたフォルダ

## 問題評価の仕様

### 評価の制限事項

- 実行時の時間制限は3秒となっています。
- コードセルは空欄のものは無視されます。
- 評価時に出力は以下の形式に揃えられます。
  - 全角と半角の区別を統一する
  - 大文字と小文字を統一する
  - スペースはすべて除去する
  - 日本語の句読点は無視する

### 非対応の問題形式

- 1つの問題に対して複数のコードセルを使用する問題
- 1つの問題に対して複数の正解が考えられる問題
- 数値の誤差を加味する問題
- 乱数を用いた問題

## 教員向け

### 授業利用時の手順

1. 公式サイトからPythonをインストールします。
   - インストール時には「Use admin prilileges when installing py.exe」にチェックを入れてください。
   - Microsoft Store版だとうまく動かない可能性があります。
2. 公式サイトからVisual Studio Codeをインストールします。
   - インストールは初期設定のままでOKです。
   - Visual Studio Codeが起動しない場合、後述の「エラー対応」を参照してください。
3. Visual Studio Codeに以下の拡張機能をインストールします。
   - Japanese Language Pack for Visual Studio Code
   - Python
   - Jupyter
4. ipynbファイルからPythonを実行するとき、ipykernelのインストールを求められるのでインストールしてください

### エラー対応

- Visual Studio Codeが実行できない場合、ユーザー名に全角スペースが含まれるケースが多いです。
  - 別途ローカルアカウントの作成を行わせるか、コンピュータ室のPCから実行してください。
- 実行結果が全て「Python」になる場合、py.exeのインストールができていません。
  - Pythonのインストーラーから、「Modify」から「py launcher」で瞬時に追加できます。
- Windows Defenderに削除される場合、別途Windows セキュリティの削除対象から外す必要があります。
  - Windows セキュリティ → ウイルスと脅威の防止 → 現在の脅威 → 保護の履歴 → それらしい項目名の「操作」→ 「許可」
  - exe化に使っているpyinstallerが誤検知の対象となっている可能性が高いです。

### コピーされる結果の詳細

- 課題のタイトル、学生番号、得点のデータが平文でクリップボードにコピーされます。
- AESでの暗号化データとしては、上記のデータに加えて、チェッカーファイルをもとにしたhash値が入っています。
  - 暗号化/復号キーは「src -> components -> StudentScore.vue」で設定した`encryptionKey`の値です。
  - データを書き換えて提出した場合の不正は暗号化データと照合して検知できます。
  - 同梱のチェッカーファイルを書き換えて判定した場合はhash値が変わります。

### 利用の制限

- ある程度パソコン操作に習熟してきた頃からの利用を推奨します。
- 学年組番号の入力欄では0000~9999の数値に制限しています。
- 課題ファイルは「.ipynbファイルを採点する」ボタンの上に直接D&Dして判定できます。
- このソフトウェアおよび問題は、教育機関または個人での利用であれば制限はありません。それ以外については連絡をお願いします。

## 課題の追加方法

### 課題ファイルの追加方法(オフライン版)

- オフライン版では、アプリケーションと同階層にdocsフォルダを配置してください。

```
JohoJupyterChecker.exe
docs/
└── sample_course/ (名前自由)
│   ├── checker01.json (名前自由)
│   └── checker02.json
└── sample_course2/
    ├── checker_01.json
    └── checker_02.json

```

### 課題用のipynbファイルの形式

- Markdownセルで「## 演習問題」というセル以降の課題が評価されるようになっているので、ipynbファイルにはその1行が必要です。
  - 演習の説明を載せる場合は、「## 演習問題」のMarkdownセルより前に書いてください。
- 空欄のコードセルは無視されてしまうので、課題を提示する際は「# 課題4」のようにコメントを書いておくことを推奨します。

### チェッカー用のjsonファイルの形式
```
{
  "id": "①ここにコース内での番号を書きます",
  "title": "②アプリケーション上に表示されるタイトルを書きます",
  "description": "③ここに課題全体の簡単な説明文を書きます",
  "problems": [
    {
      "name": "④課題を識別する名前を書きます",
      "description": "⑤課題の要点を書きます"
      "points": ⑥得点を設定します,
      "testCases": [
        {
          "input": "⑦入力を書きます。\nで複数インプットに対応します。末尾に\nが必要です。",
          "output": "⑧その入力に対する想定解を書きます。末尾に\nが必要です。"
        },
        {
          "input": "入力例2,3,4...と増やすことができます。",
          "output": "入力例・出力例が1つで十分な場合は、testCasesの中身は1セットで構いません。"
        }
      ],
    }
  ]
}
```

## JohoJupyterChecker自体のカスタマイズ

- 自分でアプリケーションを変更して実行ファイル化するためには、下記の「開発要件」を参考に「Python」と「Node.js」のインストールしてください。
  - それらのインストールが終了後、当プロジェクト全体をダウンロードして編集を行ってください。
- オフライン版で作成するには、「main.py」で「`is_offline = True`」にしてください。(v1.5はデフォルトでオフライン版です。)
  - オンライン版で作成するには、「main.py」で「`is_offline = False`」にしてください。
- オンライン版で課題配信元を変更するには、「main.py」で「`online_course_list_url`」のパスを変更してください。
  - course_list.jsonの形式は、後述の注釈を参考にしてください。
- 提出されたJSONデータに不正が生じないように、「src -> components -> StudentScore.vue の `encryptionKey`」に暗号化キーを記述することを推奨します。
  - 課題タイトル・ID4桁・得点・チェッカーのハッシュ値が暗号化されています。
- 上記の手順が完了したら、下記の「授業者向けのアプリ化手順」を全て実行してください。

### course_list.jsonの形式(オンライン版のみ)

```
{
  "courses": {
    "ここにコース名を書きます。課題フォルダ名と一致させてください。": {
      "checkerURLs": [
        "オンライン版でのみ、ここに課題のjsonファイルへのURLを書きます。(オフライン版では不要です。)",
        "配信しているファイルのURLを次々と書き足すことができます。"
      ]
    },
    "python_basic_101(例)": {
      "checkerURLs": [
        "https://mino-8136.github.io/JohoJupyterChecker/python_basic_101/checker01.json",
        "https://mino-8136.github.io/JohoJupyterChecker/python_basic_101/checker02.json",
        "https://mino-8136.github.io/JohoJupyterChecker/python_basic_101/checker03.json"
      ]
    }
  }
}

```

## 開発者向け

### 開発要件

- Python 3.12
- Node.js 20.15.0
- npm install axios vue-axios crypto-js
- pip install flask flask-cors nbformat pywebview pyinstaller
- 内部サーバーは http://localhost:5000 で融通

### Projectの初回起動と仮想環境の用意

```sh
npm install
python -m venv .venv
.venv\Scripts\activate
pip install flask flask-cors nbformat pywebview pyinstaller
```

### Python経由でのテスト起動

```sh
npm run build
py main.py
```

※ このまま`npm run dev`でブラウザ上でチェック可能

### アプリケーションのビルド

```sh
.venv\Scripts\activate
npm run build
pyinstaller main.py --onefile --distpath application --clean --add-data "dist;dist" -n JohoJupyterChecker
```

### 授業者向けのアプリ化手順(初回のみ)

```sh
npm install
python -m venv .venv
.venv\Scripts\activate
pip install flask flask-cors nbformat pywebview pyinstaller
npm run build
pyinstaller main.py --onefile --distpath application --clean --add-data "dist;dist" -n JohoJupyterChecker
```

### 授業者向けのアプリ化手順(2回目以降)

```sh
.venv\Scripts\activate
npm run build
pyinstaller main.py --onefile --distpath application --clean --add-data "dist;dist" -n JohoJupyterChecker
```
