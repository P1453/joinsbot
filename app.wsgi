import sys
import os

# アプリケーションのディレクトリをパスに追加
sys.path.insert(0, '/path/to/your/app/directory')

# 環境変数を設定
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'production'

from app import app as application


# このスクリプトはWSGIサーバ（例えばApache mod_wsgiやuWSGIなど）からアプリケーションを起動するためのものです。WSGIサーバはこのファイルを使ってFlaskアプリケーションを起動し、クライアントからのリクエストを適切にルーティングします。

# このファイルの'/path/to/your/app/directory'はあなたの環境に合わせて適切なパスに変更してください。

# また、本番環境用にFLASK_ENV環境変数をproductionに設定していますが、開発環境ではdevelopmentに設定することを推奨します。これはFlaskの動作を変更し、例えばデバッグモードを有効にしたり、自動リロードを有効にしたりします。ただし、公開されている本番環境ではセキュリティ上、これらの機能は無効化されるべきです。