# Campusmate Scraping for Gifu University

岐阜大学の学務情報システムに登録されている講義などの予定をスクレイピングし，Google Calendarに追加します。

# Requirements
* python 3.9+

# Installation
    git clone https://github.com/tanashou/Campusmate-Scraping.git
　

    pip install selenium
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

* [こちら](https://developers.google.com/calendar/api/quickstart/python)からSet up your environment を行なってください。その後，0Authクライアントをダウンロードし, `credentials.json`としてクローンしたディレクトリ内に保存してください。

* 大学のログインに必要なユーザー名やパスワード，予定を追加したいGoogleカレンダーのIDを環境変数として登録してください。それぞれの環境変数名は次のようにしてください。
    | 変数名        | 値                |
    | ------------ | ---------------- |
    | UNI_USER     | ユーザー名         |
    | UNI_PASS     | パスワード         |
    | UNI_CALENDAR | GoogleカレンダーID |

# Usage
    python main.py

# License
MIT
