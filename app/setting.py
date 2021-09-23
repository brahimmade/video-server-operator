from os import environ

MYSQL_URL = f"mysql+pymysql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@" \
            f"{environ.get('DB_HOST')}/{environ.get('DB_NAME')}"
