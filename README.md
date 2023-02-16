# dev/django

這個版本基於 django, 使用 celery.

[x] django-q. 不支援秒執行.

[x] apscheduler. 會導致任務重複執行.

[v] celery. perfect.

> 資料庫暫時使用 sqlite3, 若要使用 postgresql 請建立 .env 檔案至主目錄(與 manage.py 路徑相同)

# .env 內容

```dotenv
#.env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
REDIS_URL=
```