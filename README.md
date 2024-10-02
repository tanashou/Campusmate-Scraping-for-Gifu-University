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
    | TACT_USERNAME | ユーザー名 |
    | TACT_PASSWORD | パスワード |
    | GIFU_UNI_SCRAPER_CAL_ID | Google カレンダー ID |

**(任意)** ワンタイムパスワードの自動生成を行いたい場合は、以下の環境変数を設定してください。

    | 変数名       | 値                                  |
    | ------------ | ----------------------------------- |
    | TACT_OTP_URI | TACT のワンタイムパスワード生成 URI |

    URI を設定しなかった場合はプログラム実行時にワンタイムパスワードの入力が求められます。

# Usage

1. プロジェクトのディレクトリに移動した後に次のコマンドを実行してください。

    ```
    rye run main
    ```

1. ワンタイムパスワードの生成 URI を設定していない場合は、ログイン時にワンタイムパスワードを求められるので入力してください。

    **注意** Microsoft Authenticator のアプリを使用して二段階認証を行っている方はプログラム実行時にアプリから認証が求められますが、無視してください。(ワンタイムパスワードの入力画面に遷移する際にどうしても通知が入ってしまいます。)

1. 授業情報などが収集され、Google カレンダーに追加されます。

# License

MIT
