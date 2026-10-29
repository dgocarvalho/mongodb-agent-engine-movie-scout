"""Opt-in native read-only source comparison; no dotenv, memory writes or raw errors.

Run from repository root with authorized Playground session IDs as arguments. Privately
consume only the dedicated movie URI from the running tool process. Compare independent
projected source facts, never call application normalization to establish expected facts.
"""

import json
import subprocess
import sys
import urllib.request


def native_process(code, payload):
    cid = subprocess.run([
        "docker", "ps", "-q", "--filter", "label=com.docker.compose.project=movie-scout",
        "--filter", "label=com.docker.compose.service=app",
    ], capture_output=True, text=True, check=True).stdout.strip()
    assert cid and "\n" not in cid
    launcher = r'''
from pathlib import Path
import subprocess,sys
matches=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  cmd=(p/'cmdline').read_bytes().split(b'\0')
  env=dict(x.split(b'=',1) for x in (p/'environ').read_bytes().split(b'\0') if b'=' in x)
  if env.get(b'RUNNER_MODE')==b'tool' and any(b'entrypoint.py' in x for x in cmd):
   matches.append((p,cmd,env))
 except (OSError,ValueError):pass
assert len(matches)==1
p,cmd,env=matches[0]
safe={k.decode():v.decode() for k,v in env.items()
      if k in (b'PATH',b'PYTHONPATH',b'VIRTUAL_ENV',b'MOVIES_MONGODB_URI')}
r=subprocess.run([cmd[0].decode(),'-c',sys.argv[1]],input=sys.stdin.read(),
 capture_output=True,text=True,cwd=str((p/'cwd').resolve()),env=safe,timeout=90)
print(r.stdout if r.returncode==0 else 'native_check FAILED sanitized')
if r.returncode:
 import re
 match=re.findall(r'^(\w+(?:Error|Exception)):',r.stderr,re.M)
 print('failure_category',match[-1] if match else 'unclassified')
sys.exit(r.returncode)
'''
    result = subprocess.run(["docker", "exec", "-i", cid, "python", "-c", launcher, code],
                            input=json.dumps(payload), capture_output=True, text=True, timeout=100)
    print(result.stdout)
    if result.returncode:
        print("native_check FAILED sanitized")
    assert result.returncode == 0


COMPARE = r'''
import json,sys,logging,math,os
from decimal import Decimal
from bson import ObjectId,Decimal128
from pymongo import MongoClient,timeout
logging.disable(logging.CRITICAL)
batches=json.loads(sys.stdin.read());client=None;total=0
try:
 client=MongoClient(os.environ['MOVIES_MONGODB_URI'],connect=False)
 for expected in batches:
  assert 0<len(expected)<=10
  with timeout(10):
   with timeout(5):
    ids=[ObjectId(x['source_id'].split(':',1)[1]) for x in expected]
    cursor=client.sample_mflix.movies.find({'_id':{'$in':ids}},
     {'_id':1,'title':1,'year':1,'genres':1,'imdb.rating':1,'plot':1}).max_time_ms(5000).limit(10)
    try:docs=list(cursor)
    finally:cursor.close()
   assert len(docs)==len(expected)==len(set(x['source_id'] for x in expected))
   for row in expected:
    d=next(x for x in docs if 'objectId:'+str(x['_id'])==row['source_id'])
    year=d.get('year')
    year=year if isinstance(year,int) and not isinstance(year,bool) and 1<=year<=9999 else None
    genres=d.get('genres')
    genres=genres if isinstance(genres,list) and genres and all(isinstance(x,str) and x.strip() for x in genres) else None
    rating=d.get('imdb',{}).get('rating')
    rating=rating.to_decimal() if isinstance(rating,Decimal128) else rating
    rating=float(rating) if isinstance(rating,(int,float,Decimal)) and not isinstance(rating,bool) else None
    rating=rating if rating is not None and math.isfinite(rating) and 0<=rating<=10 else None
    plot=d.get('plot');plot=plot if isinstance(plot,str) and plot.strip() else None
    missing=[k for k,v in [('year',year),('genres',genres),('imdb_rating',rating),('plot',plot)] if v is None]
    trunc=[k for k,v in [('title',len(d['title'])>300),
      ('genres',genres is not None and (len(genres)>10 or any(len(x)>80 for x in genres))),
      ('plot',plot is not None and len(plot)>500)] if v]
    actual={'source_id':'objectId:'+str(d['_id']),'title':d['title'][:300],'year':year,
     'genres':[x[:80] for x in genres[:10]] if genres else None,'imdb_rating':rating,
     'plot':plot[:500] if plot else None,'missing_fields':missing,'truncated_fields':trunc}
    assert actual==row
   total+=len(docs)
 print('independent_source PASS batches',len(batches),'records',total,'all_8_fields true distinct_ids true')
except Exception as error:
 print('comparison_category',type(error).__name__)
 import traceback
 print('comparison_lines',[x.lineno for x in traceback.extract_tb(error.__traceback__)])
 raise SystemExit(1) from None
finally:
 if client is not None:client.close()
'''


def compare_sessions(sessions):
    batches = []
    for session in sessions:
        with urllib.request.urlopen(
            "http://localhost:3000/api/v1/execution-logs?session_id=" + session, timeout=15
        ) as response:
            rows = json.load(response)["logs"]
        for row in rows:
            if row["tool"] == "search_movies" and row["status"] == "success":
                outcome = json.loads(row["output"])
                if outcome["movies"]:
                    batches.append(outcome["movies"])
    assert batches
    native_process(COMPARE, batches)


if __name__ == "__main__":
    try:
        compare_sessions(sys.argv[1:])
    except Exception as error:
        print("source_comparison FAILED", type(error).__name__)
        raise SystemExit(1) from None