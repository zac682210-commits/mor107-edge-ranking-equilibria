from itertools import permutations,product
import json,random,time
from pathlib import Path
class Game:
 def __init__(s):s.names=[];s.pos={};s.b=[];s.edges=[];s.out=[];s.gates=[];s.fanouts=[]
 def node(s,name,b=0):
  if name not in s.pos:s.pos[name]=len(s.names);s.names.append(name);s.b.append(b);s.out.append([])
  return s.pos[name]
 def edge(s,a,b,c):
  assert c>0
  u=s.node(a);v=s.node(b);i=len(s.edges);s.edges.append((u,v,c));s.out[u].append(i);return i
 def threshold(s,name,targets,H,T):
  r=T+1;fan=name+'_fan';priv=name+'_private';s.edge(name,priv,r+H);s.edge(priv,name,r);s.edge(name,fan,T+1)
  for target,c in targets:s.edge(fan,target,c)
  s.gates.append(s.pos[name]);s.fanouts.append(s.pos[fan])
 def default(s):return tuple(tuple(es) for es in s.out)
 def clear(s,p):
  f=[e[2] for e in s.edges]
  for it in range(sum(f)+1):
   total=s.b.copy()
   for x,(_,v,_) in zip(f,s.edges):total[v]+=x
   g=[0]*len(f)
   for u,es in enumerate(p):
    rem=total[u]
    for e in es:z=min(rem,s.edges[e][2]);g[e]=z;rem-=z
   if g==f:return tuple(f),tuple(sum(f[e] for e in es) for es in p),it
   assert all(y<=x for x,y in zip(f,g));f=g
  raise RuntimeError('descending integer bound exceeded')
 def dev(s,p,u,order):return p[:u]+(tuple(order),)+p[u+1:]
 def pne(s,p,base=None):
  if base is None:base=s.clear(p)[1]
  for u,es in enumerate(p):
   for order in permutations(es):
    if order!=es:
     val=s.clear(s.dev(p,u,order))[1][u]
     if val>base[u]:return False,(u,order,val,base[u])
  return True,None

def add_alarm(g):
 for a,b,c in [(5,2,1),(2,5,6),(2,1,6),(4,2,2),(1,4,4),(1,6,4),(6,3,2),(3,1,6),(7,3,1),(3,7,6)]:g.edge('a'+str(a),'a'+str(b),c)
def build(n,r,clauses):
 assert r>=1 and clauses
 g=Game();m=len(clauses);R=5;B=R*(m+1)+1;K=m+r
 for i in range(n):
  g.node('x'+str(i),B)
  for bit in (0,1):g.edge('x'+str(i),f'X{i}_{bit}',B)
 g.node('d',r*B)
 for i in range(r):
  for bit in (0,1):g.edge('d',f'Y{i}_{bit}',B)
 g.edge('d','bonus_sink',B)
 for typ,num in [('X',n),('Y',r)]:
  for i in range(num):
   for bit in (0,1):
    targets=[('q'+str(i),R)] if typ=='Y' else []
    targets += [('c'+str(j),R) for j,c in enumerate(clauses) if (typ,i,bit) in c]
    H=B-R*len(targets);assert H>=1;g.threshold(f'{typ}{i}_{bit}',targets,H,B)
 for j in range(m):g.edge('c'+str(j),'g',R)
 for i in range(r):g.edge('q'+str(i),'g',R)
 g.threshold('g',[('a2',2),('a3',2),('d',1)],R*(K-1),R*K);add_alarm(g)
 return g,B

def truth(clauses,x,y):return all(any((x[i] if t=='X' else y[i])==b for t,i,b in c) for c in clauses)
def yes_qbf(n,r,c):return any(all(not truth(c,x,y) for y in product((0,1),repeat=r)) for x in product((0,1),repeat=n))
def signal(g,p,n,r,c,B):
 x=tuple(int(g.names[g.edges[p[g.pos['x'+str(i)]][0]][1]].split('_')[1]) for i in range(n))
 sel=[g.names[g.edges[e][1]] for e in p[g.pos['d']][:r]]
 if 'bonus_sink' in sel:return 0
 y={}
 for v in sel:
  a,b=v[1:].split('_');i=int(a)
  if i in y:return 0
  y[i]=int(b)
 return int(len(y)==r and truth(c,x,tuple(y[i] for i in range(r))))
def alarm_checks():
 result={}
 for incoming in (0,2):
  g=Game();g.node('a2',incoming);g.node('a3',incoming);add_alarm(g);p=g.default();us=[g.pos['a'+str(i)] for i in (1,2,3)];rows=[]
  for bits in product((0,1),repeat=3):
   q=p
   for u,b in zip(us,bits):
    if b:q=g.dev(q,u,reversed(q[u]))
   f,v,it=g.clear(q);ok,w=g.pne(q,v);rows.append({'bits':bits,'utilities':[v[u] for u in us],'pne':ok})
  assert any(x['pne'] for x in rows)==(incoming==0);result[str(incoming)]=rows
 return result

def gate_checks():
 count=0
 for T in range(1,9):
  for H in range(T+1):
   for t in range(T+1):
    g=Game();g.node('v',t);g.threshold('v',[('sink',T+1)],H,T);p=g.default();f,v,it=g.clear(p);u=g.pos['v'];e=p[u][1]
    assert f[e]==max(t-H,0) and v[u]==t+T+1
    vv=g.clear(g.dev(p,u,reversed(p[u])))[1];assert vv[u]==t and v[u]>vv[u];count+=1
 return count

def random_reductions(count=300,seed=107):
 rng=random.Random(seed);cases=[];profiles=0;gatedevs=0;pnechecks=0
 for z in range(count):
  n=rng.randint(0,3);r=rng.randint(1,3);m=rng.randint(1,6);literals=[(t,i,b) for t,num in [('X',n),('Y',r)] for i in range(num) for b in (0,1)]
  c=[tuple(rng.sample(literals,min(3,len(literals)))) for _ in range(m)];g,B=build(n,r,c);p=g.default()
  for rep in range(12):
   q=tuple(tuple(rng.sample(list(es),len(es))) if u not in g.gates else es for u,es in enumerate(p));f,v,it=g.clear(q)
   assert v[g.pos['d']]==r*B+signal(g,q,n,r,c,B)
   for u in g.gates:
    vb=g.clear(g.dev(q,u,reversed(q[u])))[1];assert vb[u]<v[u];gatedevs+=1
   wild=tuple(tuple(rng.sample(list(es),len(es))) for es in p)
   for u in g.gates:
    good=g.dev(wild,u,p[u]);bad=g.dev(wild,u,reversed(p[u]));assert g.clear(good)[1][u]>g.clear(bad)[1][u];gatedevs+=1
   for u in g.fanouts:assert g.clear(g.dev(q,u,reversed(q[u])))[1][u]==v[u]
   profiles+=1
  for x in product((0,1),repeat=n):
   if all(not truth(c,x,y) for y in product((0,1),repeat=r)):
    q=p
    for i,b in enumerate(x):
     if b:q=g.dev(q,g.pos['x'+str(i)],reversed(q[g.pos['x'+str(i)]]))
    for name,target in [('a1','a4'),('a2','a1'),('a3','a7')]:
     u=g.pos[name];q=g.dev(q,u,sorted(q[u],key=lambda e:g.names[g.edges[e][1]]!=target))
    if r<=2:
     ok,w=g.pne(q);assert ok,(n,r,c,w);pnechecks+=1
    break
  cases.append({'n':n,'r':r,'clauses':c,'yes_qbf':yes_qbf(n,r,c),'vertices':len(g.names),'edges':len(g.edges)})
 return {'cases':cases,'normalized_profiles':profiles,'gate_deviation_comparisons':gatedevs,'full_pne_checks':pnechecks}
if __name__=='__main__':
 start=time.time();out={'alarm':alarm_checks(),'isolated_gate_cases':gate_checks(),'random_reductions':random_reductions()};out['seconds']=time.time()-start
 Path('verification107.json').write_text(json.dumps(out,indent=2));print('isolated_gate_cases',out['isolated_gate_cases'],'seconds',out['seconds']);print({k:v for k,v in out['random_reductions'].items() if k!='cases'})
