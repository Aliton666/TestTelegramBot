from os import getenv
from dotenv import load_dotenv
load_dotenv()

TOKEN = getenv("TOKEN")
ADMIN_USERID = getenv("ADMIN_USERID")

PGHOST = getenv("PGHOST")
PGDATABASE = getenv("PGDATABASE")
PGUSER = getenv("PGUSER")
PGPASSWORD = getenv("PGPASSWORD")
PGPORT = getenv("PGPORT")
