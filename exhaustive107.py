from verify107 import *
import math
cases=[('literal_y',0,1,[(('Y',0,1),)]),('contradiction_y',0,1,[(('Y',0,1),),(('Y',0,0),)]),('existential_switch',1,1,[(('X',0,1),),(('Y',0,1),)])]
out=[]
for name,n,r,clauses in cases:
 start=time.time();g,B=build(n,r,clauses);options=[list(permutations(es)) for es in g.default()];players=[u for u in range(len(g.names)) if len(options[u])>1];radices=[len(options[u]) for u in players];strides=[];acc=1
 for d in reversed(radices):strides.insert(0,acc);acc*=d
 print(name,'profiles',acc,'vertices',len(g.names),flush=True)
 vals=[];profiles=[]
 for choices in product(*(range(d) for d in radices)):
  p=list(g.default())
  for u,ch in zip(players,choices):p[u]=options[u][ch]
  p=tuple(p);v=g.clear(p)[1];vals.append(tuple(v[u] for u in players));profiles.append(choices)
 pnes=[]
 for ix,choices in enumerate(profiles):
  if all(vals[ix+(alt-ch)*stride][j]<=vals[ix][j] for j,(ch,d,stride) in enumerate(zip(choices,radices,strides)) for alt in range(d)):
   pnes.append(ix)
   for u in g.gates:
    j=players.index(u);assert options[u][choices[j]]==g.default()[u]
 assert bool(pnes)==yes_qbf(n,r,clauses)
 row={'name':name,'formula':clauses,'expected_qbf':yes_qbf(n,r,clauses),'profiles':acc,'pne_count':len(pnes),'seconds':time.time()-start,'players':[g.names[u] for u in players],'radices':radices,'pne_profile_indices':pnes};out.append(row)
 print({k:v for k,v in row.items() if k not in ('pne_profile_indices','players','radices','formula')},flush=True)
 Path('exhaustive107_results.json').write_text(json.dumps(out,indent=2))
