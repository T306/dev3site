import os
import requests
from requests.auth import HTTPBasicAuth

##############################
SURREALDB_URL = os.environ['db_addr']
SURREALDB_NAMESPACE = "prod"
SURREALDB_DATABASE_NAME = "projects"
SURREALDB_USER_NAME = os.environ['db_user']
SURREALDB_USER_PASSWORD = os.environ['db_pass']


##############################
def db(query):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'ns': SURREALDB_NAMESPACE,
               'db': SURREALDB_DATABASE_NAME}
    r = requests.post(SURREALDB_URL,
                      data=query,
                      headers=headers,
                      auth=HTTPBasicAuth(SURREALDB_USER_NAME, SURREALDB_USER_PASSWORD))
    if "code" in r.json():
        raise Exception(r.json())
    return r.json()
