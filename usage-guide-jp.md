# はじめに
twitter-vrc-statusの使い方を説明します。分かりにくいところがあれば、修正PRをください！自分では気づかないものなので！
## このドキュメントで解説しないこと
- AWSの登録方法(→ネット上にたくさん情報がありますので)
- Twitterのtoken取得方法(同上、しかし昨年から承認プロセスが変わったので気をつけてください。少しグレーな裏技もあります(後述))
- contributionについて(→README.mdを見てください、お待ちしております！)

## 主に解説すること
- ツールの概要
- AWS lambdaとは何なのか
- AWS lambdaにどのような設定をすればよいのか

# 概要
このツールはTwitterのプロフィールにVRChatでのオンライン状況を反映させるツールで、柊 釘葉(Hiiragi Kugiha @hiiragi_kugiha)によって開発されました。
MITライセンスのもとで、ソースコードを自由に利用、改変することができます。(他の人にも役立つような変更はpull requestを送ってもらえると助かります！)  
このツールによって、
- VRChatのオンライン情報をTwitterの表示名に反映させること
- VRChatで今いるワールドをTwitterのlocationに反映させること
ができます。
[dy-dhffv4aaotod](https://user-images.githubusercontent.com/46911299/52549217-6b3f1d00-2e15-11e9-804f-6b2c20195801.jpg)

# 使い方(step-by-step)
これで分からなくても大丈夫です。次のセクションから一つずつ見ていきましょう。
1. Twitterのtokenを取得する
1. AWSに登録する
1. AWS lambdaのfunctionを作成する
1. GitHubにある最新releasのsrc.zipをAWS lambdaにアップロードする
1. AWS lambdaの環境変数に必要な情報(IDやパスワード)を入れる
1. CloudWatch Eventでfunctionを定期的(2分間隔くらい)に呼び出す

# Twitterのtoken
冒頭で詳しくは書かないといいましたが、この部分は少し難しいので調べる上で手がかりとなることを書きます。Twitterのプロフィールなどを操作するにはTwitter APIを利用しますが、
もちろん認証が必要で、その認証のために用いられるのがtokenです。詳しい人向けに言うと、OAuth2を使っているのです。そして、tokenを取得するためには、
事前にTwitter側にapplicationを登録する必要があります。そのtokenを使うのが誰なのかという情報が必要ということです。
以前は簡単に登録できたのですが、昨年の仕様変更でDeveloperアカウントの作成には承認が必要となり、時間と手間がかかるようになりました…。  
というわけで、ネット上で調べるときにはその仕様変更後のことを調べる必要があります。「apps.twitter.comにアクセスして…」などと書いてあるサイトは古いサイトです。
(仕様変更後はdeveloper.twitter.comになったので！)  
でも、やっぱり面倒ですよね…。ということで、少しグレーな裏技もあります。
グレーなので、ここで詳しくは話せませんが、ポイントとなるのは、applicationは何をもって自分を証明するのかということです。
そう、`consumer_key`と`consumer_secret`です！applicationの申請は、この2つの値を得るためのものなのです。
そして、その2つの値(正しくは`consumer_secret`のほうです)はwebアプリならサーバー側で持っておけばよいのですが、
ダウンロードして使うようなアプリは自分自身で持っておくほかありません。要するにそういうことなのです！  

# AWS lambda
## AWS lambdaとは
AWS自体については詳しく説明しませんが、簡単に言えばソフトウェアを動かすサーバーを借りられるサービスです。
このツールは非常に簡単な処理しか行わないので、料金はほとんどかかりません。まだ登録していない方は登録してください。  
## lambda functionの作成
AWSのコンソールからlambdaの画面を開きます
![image](https://user-images.githubusercontent.com/46911299/52549189-477bd700-2e15-11e9-8f4e-5af9796a60b4.png)  
---
この画面になるので、Create Function
![image](https://user-images.githubusercontent.com/46911299/52549266-a0e40600-2e15-11e9-9752-7b0a98371fef.png)  
---
名前などはお好きにどうぞ！ただし、runtimeはpython3.7です。
![image](https://user-images.githubusercontent.com/46911299/52549291-c3761f00-2e15-11e9-8d45-9816f8f6e61d.png)  
---
こんな感じの画面になりましたか？
![image](https://user-images.githubusercontent.com/46911299/52549316-e56fa180-2e15-11e9-872b-c7a8410d3fcf.png)  
---
functionとしてコードを直書きするのではなく、GitHubのreleasesから最新のsrc.zipをダウンロードしてアップロードします。
(ライブラリを使うにはzipの中にそれらを入れる必要があるので!)  
![image](https://user-images.githubusercontent.com/46911299/52549320-ed2f4600-2e15-11e9-886d-46c4858ec338.png)  
---
環境変数を設定しましょう。README.mdのConfigurationsにある環境変数を設定します！
`offline_location`と`private_location`は、それぞれオフラインのときとprivateなワールドにいるときのlocationの表示です。  
`name_template`は表示名なのですが、例としては、`{status}柊 釘葉`みたいな感じです！
`{status}`の部分が、VRChatでオンラインのときは`online_status`の中身になり、オフラインのときは`offline status`になります。
![image](https://user-images.githubusercontent.com/46911299/52549339-f7e9db00-2e15-11e9-8b5d-1839e0ecd155.png)  
ここまでできたら、SaveしてTestしてみましょう。引数は使っていないので、何を与えても大丈夫です！

## CloudWatch Eventの設定
あと少しです！前回までのステップで、手動でこのツールを動かすことに成功しました。
つまり、VRChatでワールド移動をするたびにこのツールを起動すれば、求めていた機能が実現します。
しかし、それは面倒なので自動で動かしてみましょう。
自動で動かすにはCloudWatch Eventというものを用います。AWS lambdaからtriggerとして追加しましょう。`rate(2 minutes)`くらいがおすすめです。
VRChat APIのルールとして、1分に1回までしかリクエストしてはいけないので、`rate(1 minute)`よりも頻繁に呼んではいけません。  

# 今後の予定
別のタスクも抱えていて時間が取れないのですが、次のようなことをやりたいと思います。
- 本ドキュメントの充実→まだ雑な部分があると思うので…
- 解説動画の作成(導入方法、コード解説)→柊釘葉 VTuberデビュー！？
- 本ドキュメントの英訳→README.mdが英語なのに、こっちは日本語しかないのは少しよくないので…
- 本ツールの宣伝→Twitterでの拡散ありがとうございました。まだ知らない人もいるみたいなので、もっと多くの人に知ってもらいたいです！

