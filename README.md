# BigQuery SQL Generator

BigQueryのSQLを生成するツールです。
対象のテーブルIDと作成したいSQLを指示で自然言語に入力するとSQLが自動で生成されて BigQueryに対して実行されます。

# Getting Started
OpenAI APIのtokenを用意してください

```
pipenv install
pipenv shell
export DEFAULT_API_KEY=<YOUR_API_KEY>
streamlist run main
```

# 認証について
現在のgcloudの認証状態に基づいて実行されます

# その他
- export DEFAULT_SA_PATH を設定するとsa_pathの入力がない場合のdefault値になります
- export DEFAULT_TABLE_KEY を設定するとtable_keyの入力がない場合のdefault値になります
- export DEFAULT_INSTRUCTION を設定するとinstructionの入力がない場合のdefault値になります

# Datasetについて
-  GCPが提供している `public-dataset` から利用することをお勧めします
- https://console.cloud.google.com/bigquery?p=bigquery-public-data
- https://console.cloud.google.com/marketplace/browse?filter=solution-type:dataset&_ga=2.148763127.1552394929.1684987172-724389206.1673507078&_gac=1.158082888.1685085860.CjwKCAjwscGjBhAXEiwAswQqNNknH286mD2IIjYtfGIjMHtlrl_sz0RXB4vAEGyODAQGsLdiu_F6MxoC680QAvD_BwE


