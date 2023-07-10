# 基本となるイメージの指定
FROM postgres:latest

# 環境変数の設定
ENV POSTGRES_PASSWORD=Admin000!
ENV POSTGRES_USER=root
ENV POSTGRES_DB=joinsbotdb
ENV PGDATA=/var/lib/postgresql/data/pgdata

# 設定ファイルの変更(どこからでもアクセスできるように)
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf
RUN echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf

# タイムゾーンの設定
RUN echo "Asia/Tokyo" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# ポートの解放
EXPOSE 5432

# PostgreSQLの自動起動設定
CMD ["postgres"]



# docker build -t my_postgres_image .
# docker run -p 5432:5432 my_postgres_image


# GRANT ALL PRIVILEGES ON DATABASE joinsbotdb TO root;


# docker exec -it postgres_container psql -U root -d joinsbotdb

# docker exec -it postgres_container bash



# pgbectorインストール方法はhttps://github.com/pgvector/pgvector参照
# makeする前にapt updateとapt install build-essentialとapt-get install postgresql-server-dev-allをやる必要がある
# ivfflatインデックスを作成するには、まずpgvector拡張を有効にする必要があります。この拡張を有効にするには、PostgreSQLのコンソールに接続し、以下のコマンドを実行します：
# CREATE EXTENSION pgvector;　は中でやる必要あり。
# 次に、FAQテーブルにivfflatインデックスを追加します：
# CREATE INDEX faq_question_embedding_idx ON faq USING ivfflat(question_embedding);
