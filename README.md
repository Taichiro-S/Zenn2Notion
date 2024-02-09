これは**Zennでいいねした投稿と読んでいる本をNotionデータベースに保存する**プログラムです

詳細は[こちらの記事]()をご一読ください

**認証情報を使うので取り扱いには注意してください。**

### 使い方

1. Notionの設定
   Notion Integrationを作成しSecretを控えておきます。
   以下のURLで公開されている2つのNotionのデータベースをそれぞれ自分のワークスペースに複製し、IDを控えておきます。複製したデータベースのコネクトに作成したIntegrationを追加します。
   - [いいねした投稿保存用](https://zealous-rosehip-7a8.notion.site/8d13f37a21914981840a995f70272d37?v=e498ea5550174a249f0dbae5af86b556&pvs=4)
   - [読んでいる本保存用](https://zealous-rosehip-7a8.notion.site/636574be4b7648349f217a735402b3ba?v=244e9c4d26b64af09889f84b10151689&pvs=4)
2. このリポジトリをクローンして以下を`.env`に書きます。
   - REMEMBER_USER_TOKEN：ブラウザでZennにログインした状態でChromeの検証画面のCookiesに入っているremember_user_tokenの値
   - NOTION_SECRET：Notion integrationのSecret
   - NOTION_DATABASE_ID_FOR_LIKES：いいねした投稿保存用のNotionのデータベースのID
   - NOTION_DATABASE_ID_FOR_BOOKS：読んでいる本保存用のNotionのデータベースのID
3. いいねした投稿の保存は`python3 save_zenn_likes.py`、読んでいる本の保存は`python3 save_zenn_reading_books.py`で実行します。

