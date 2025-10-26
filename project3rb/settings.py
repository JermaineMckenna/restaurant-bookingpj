
# -------------------------------
# DATABASES
# -------------------------------
import os
import dj_database_url

DEFAULT_SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}


if os.environ.get('DYNO'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    
    url_db = dj_database_url.config(conn_max_age=0, ssl_require=False)
    DATABASES = {'default': url_db or DEFAULT_SQLITE}