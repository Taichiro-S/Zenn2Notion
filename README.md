### Zennのいいねした記事をNotionデータベースに保存するスクリプトです

**認証情報を使うので取り扱いには注意してください。**
**このスクリプトを使用して生じたいかなる損害についても私は責任を負いません。**

1. Notionの設定
   Notion Integrationを作成しSecretを控えておきます。
   データベースを作成し、Integrationをコネクトに追加します。
   データベースは、以下のようなプロパティを設定します。
   |プロパティ名|種類|何が入るか|
   |-|-|-|
   |title|タイトル|記事のタイトル|
   |topic|マルチセレクト|記事についているトピック|
   |author|テキスト|記事の著者|
   |link|URL|記事のリンク|
   |published_at|日付|記事の公開日|
2. リポジトリをクローンして以下の3つの値を`.env`に書きます。
   - REMEMBER_USER_TOKEN：ブラウザでZennにログインした状態でChromeの検証画面のCookiesに入っているremember_user_tokenの値
   - NOTION_SECRET：Notion integrationのSecret
   - NOTION_DATABASE_ID：NotionのデータベースのID
3. `python3 main.py`で実行します。
