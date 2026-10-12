import urllib.request,urllib.parse,json,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parent
urls={
'openalex_work':'https://api.openalex.org/works/https://doi.org/10.1287/moor.2022.0355',
'openalex_citing':'https://api.openalex.org/works?filter=cites:W4391111008&per-page=100',
'semantic_citing':'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1287/moor.2022.0355/citations?fields=title,year,url,externalIds&limit=100',
'author_hoefer':'https://algo.rwth-aachen.de/team/hoefer/index.en.shtml',
'problem107':'https://raw.githubusercontent.com/ai-in-math-or/open-problems-in-or/main/data/llm_math_export/problems/W4391111008_p0.json',
'github_code_search':'https://api.github.com/search/code?q='+urllib.parse.quote('"edge-ranking" "Nash"')
}
def work(kv):
 k,url=kv
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchAudit/1.0'}),timeout=20) as r:b=r.read()
  try:
   x=json.loads(b);ext='json'
   if k=='openalex_work':v={a:x.get(a) for a in ('id','display_name','cited_by_count','updated_date')}
   elif k=='openalex_citing':v={'count':x.get('meta',{}).get('count'),'results':[{'title':a.get('display_name'),'year':a.get('publication_year'),'doi':a.get('doi')} for a in x.get('results',[])]}
   elif k=='semantic_citing':v=x
   elif k=='problem107':v={'keys':list(x)}
   else:v={'total_count':x.get('total_count')}
  except Exception:ext='html';v={'bytes':len(b)}
  P.joinpath(k+'.'+ext).write_bytes(b);return k,v
 except Exception as e:return k,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 out=dict(pool.map(work,urls.items()));P.joinpath('citation_lookup_summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
