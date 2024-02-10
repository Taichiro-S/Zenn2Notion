**Zennでいいねした投稿と読んでいる本をNotionデータベースに保存する**プログラムです

詳細は[こちらの記事](https://zenn.dev/xcter/articles/05db4018cfdc71)をご一読ください

## 筆者の環境

- macOS Sonoma 14.3
- python 3.11.1

## 必要なもの

- [Notion](https://www.notion.so/)のアカウント
- python実行環境

## 使い方

1. このリポジトリをクローンし、以下コマンドでvenvを使用して実行環境を作成してください。
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. [ここ](https://www.notion.so/my-integrations)からNotion Integrationを作成しSecretを控えておきます。
3. 以下のURLで公開されている2つのNotionのデータベースをそれぞれ自分のワークスペースに複製し、IDを控えておきます。
   - [いいねした投稿保存用](https://zealous-rosehip-7a8.notion.site/8d13f37a21914981840a995f70272d37?v=e498ea5550174a249f0dbae5af86b556&pvs=4)
   - [読んでいる本保存用](https://zealous-rosehip-7a8.notion.site/636574be4b7648349f217a735402b3ba?v=244e9c4d26b64af09889f84b10151689&pvs=4)
4. 複製したデータベースのコネクトに、作成したIntegrationを追加します。

5. 以下の値を`.env`に書きます。
   **tokenとsecretの取り扱いには注意してください**
   - REMEMBER_USER_TOKEN：ブラウザでZennにログインした状態でChromeの検証画面のCookiesに入っているremember_user_tokenの値
   - NOTION_SECRET：Notion integrationのSecret
   - NOTION_DATABASE_ID_FOR_LIKES：いいねした投稿保存用のNotionのデータベースのID
   - NOTION_DATABASE_ID_FOR_BOOKS：読んでいる本保存用のNotionのデータベースのID
6. いいねした投稿の保存は`python3 save_zenn_likes.py`、読んでいる本の保存は`python3 save_zenn_reading_books.py`で実行します。

