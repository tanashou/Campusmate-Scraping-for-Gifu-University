# Gifu University Scraper

岐阜大学の学務情報システムに登録されている講義予定などをスクレイピングし，Google Calendar に追加します。

# Requirements

-   [rye](https://rye-up.com)
- macOSでのみ動作確認済みです。他の OS でも同様に動作するはずです。
# Installation

    git clone https://github.com/tanashou/Campusmate-Scraping.git

# Setup

-   [ryeをインストール](https://rye-up.com/guide/installation/)してください。 その後、次のコマンドを実行してください。

          rye sync

-   google calendar api を使用できるようにします。[こちら](https://developers.google.com/calendar/api/quickstart/python)から Set up your environment を行なってください。その後，0Auth クライアントをダウンロードし, `credentials.json`として本プロジェクトのルートディレクトリに保存してください。

-   大学のログインに必要なユーザー名やパスワード，予定を追加したい Google カレンダーの ID を環境変数として登録してください。それぞれの環境変数名は次のようにしてください。
    | 変数名 | 値 |
    | ------------ | ---------------- |
    | GIFU_UNI_SCRAPER_USERNAME | ユーザー名 |
    | GIFU_UNI_SCRAPER_PASSWORD | パスワード |
    | GIFU_UNI_SCRAPER_CAL_ID | Google カレンダー ID |

# Usage

    rye run main

# License

MIT
