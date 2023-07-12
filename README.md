# Document_Checking_Tools

## pythonのライブラリーのインストール

```
$ pip install flask 
$ pip install pyrebase4
```

## textlintのインストール
```
$ npm install textlint --save-dev
```

## textlintのルールファイルを作成
```
$ npx textlint --init
```

## textlintのルールのインストール

```
$ npm install textlint-rule-preset-ja-technical-writing
$ npm install textlint-plugin-html
```

## pdftotextのインストール
```
$ apt-get install -y poppler-util
```

## textlintrc.json
```json
{
  "rules": {
    "preset-ja-technical-writing": {
      "sentence-length": {
        "max": 100
      },
      "max-comma": {
        "max": 4
      },
      "max-ten": {
        "max": 4
      },
      "max-kanji-continuous-len": {
        "max": 7,
        "allow": []
      },
      "arabic-kanji-numbers": true,
      "no-mix-dearu-desumasu": {
        "preferInHeader": "",
        "preferInBody": "である",
        "preferInList": "である",
        "strict": true
      },
      "ja-no-mixed-period": {
        "periodMark": "．"
      },
      "no-double-negative-ja": true,
      "no-dropping-the-ra": true,
      "no-doubled-conjunctive-particle-ga": true,
      "no-doubled-conjunction": true,
      "no-doubled-joshi": {
        "min_interval": 1
      },
      "no-invalid-control-character": true,
      "no-zero-width-spaces": true,
      "no-exclamation-question-mark": true,
      "no-hankaku-kana": true,
      "ja-no-weak-phrase": true,
      "ja-no-successive-word": true,
      "ja-no-abusage": true,
      "ja-no-redundant-expression": true,
      "ja-unnatural-alphabet": true,
      "no-unmatched-pair": true
    }
   },
  "filters": {
    "comments": true
  }
}
```

## firebaseの設定
* ./static/json/firebase.jsonに以下の情報を記載する
```json
{
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}
```

## Run textlint
```
$ npx textlint target.md
```

## Run pdftotext
```
$ pdftotext target.pdf target.md
```

## Run App
```
$ python3 web_app.py
```
