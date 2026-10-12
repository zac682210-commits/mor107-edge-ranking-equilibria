import urllib.request,urllib.parse,json,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parent
base='https://api.github.com/repos/ai-in-math-or/open-problems-in-or'
queries={'repo':base,'branches':base+'/branches?per_page=100','forks':base+'/forks?per_page=100','issues':base+'/issues?state=all&per_page=100','pulls':base+'/pulls?state=all&per_page=100','commits107':base+'/commits?path='+urllib.parse.quote('data/llm_math_export/solution_progress/W4391111008_p0')+'&per_page=100','repo_search': 'https://api.github.com/search/repositories?q='+urllib.parse.quote('"flow allocation games" in:readme')+'&per_page=100'}
def fetch(k,u):
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'MOR-Research-Audit'}),timeout=25).read();x=json.loads(b);P.joinpath(k+'.json').write_bytes(b)
  if isinstance(x,list):out=[{z:a.get(z) for z in ('name','full_name','sha','number','title') if z in a} for a in x]
  elif k=='repo':out={z:x.get(z) for z in ('default_branch','pushed_at','forks_count','open_issues_count')}
  else:out={'total_count':x.get('total_count'),'items':[a.get('full_name') for a in x.get('items',[])]}
  return k,out
 except Exception as e:return k,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as e:
 for k,x in e.map(lambda kv:fetch(*kv),queries.items()):print(k,json.dumps(x))
