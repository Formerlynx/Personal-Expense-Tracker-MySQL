# Deploy on Render with Aiven MySQL

## Aiven values

Set these Render environment variables:

```text
MYSQL_HOST=personal-expense-tracker-1-verghese-b728.c.aivencloud.com
MYSQL_PORT=22833
MYSQL_USER=avnadmin
MYSQL_DB=defaultdb
MYSQL_SSL_MODE=REQUIRED
MYSQL_SSL_CA=/etc/secrets/aiven-ca.pem
MYSQL_SSL_VERIFY_CERT=true
MYSQL_SSL_VERIFY_IDENTITY=true
```

Add the Aiven CA certificate in Render under **Secret Files** with the filename
`aiven-ca.pem`. Set `MYSQL_PASSWORD`, `FLASK_SECRET_KEY`, and `GOOGLE_API_KEY`
as secret environment variables. Never commit those values.

The Aiven password was shared in chat and must be rotated in Aiven before
deployment. Update `MYSQL_PASSWORD` with the new value afterward.

## Render service

The included `render.yaml` defines:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --bind 0.0.0.0:$PORT app:app`

Create the Render service from this repository, add the Aiven CA secret file,
and deploy. The app connects to Aiven's existing `defaultdb` database and
creates the `users` and `expenses` tables automatically.