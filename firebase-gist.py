from firebase import firebase
import os
import datetime
import json
import logging
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from github3 import login

firebase_url = os.environ['FIREBASE_DB']
firebase_secret = os.environ['FIREBASE_SECRET']
firebase_path = os.environ['FIREBASE_PATH']
firebase_username = os.environ['FIREBASE_USERNAME'] # not checked ATM

gh_token = os.environ['GH_TOKEN']
gh_gist = os.environ['GH_GIST']
gh_fname = os.environ['GH_FNAME']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_firebase():
  f = firebase.FirebaseApplication(firebase_url, None)
  f.authentication = firebase.FirebaseAuthentication(firebase_secret, firebase_username, admin=True)
  return f

logger.info('==================================')
logger.info('Fetching firebase data')
f = connect_firebase()
data = f.get(firebase_path, None)
new_content = json.dumps(data, ensure_ascii=False, indent=2)

logger.info('Reading existing gist')
gh = login(token=gh_token)

gist = gh.gist(gh_gist)

old_content = ""
for f in gist.iter_files():
  if f.filename == gh_fname:
    old_content = f.content
    break

if old_content == new_content:
  logger.info('No changes detected')
else:
  logger.info('Updating gist with new content')
  gist.edit(files={
    gh_fname: {
      "content": new_content
    }
  })

logger.info('Done.')