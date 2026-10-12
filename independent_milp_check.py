"""Different clearing algorithm for auditing: a disjunctive MILP.
The MILP maximizes total edge flow over fixed points of greedy payments.
No calls to Game.clear are used inside the MILP. Integer rounding is accepted
only after checking all fixed-point equations exactly. This is supplementary
numerical optimization evidence, not a formal MILP optimality certificate.
"""
import sys,json,random,time
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
# The shared graph generator is imported from this code directory.
from verify107 import Game,build,add_alarm,signal

def solve(g,p):
 E=len(g.edges);N=len(g.names);D=2*E+N
 # variables: continuous edge flows; binary positive-flow enablers; binary full-output flags.
 lo=np.zeros(D);hi=np.ones(D);hi[:E]=[c for _,_,c in g.edges]
 c=np.zeros(D);c[:E]=-1
 integ=np.ones(D);integ[:E]=0
 rows=[];lower=[];upper=[]
 def con(terms,l=-np.inf,u=np.inf):
  a=np.zeros(D)
  for j,x in terms:a[j]+=x
  rows.append(a);lower.append(l);upper.append(u)
 for v,es in enumerate(p):
  inc=[i for i,(_,w,_) in enumerate(g.edges) if w==v]
  delta=[(i,1) for i in es]+[(i,-1) for i in inc]
  # total out <= supply + incoming
  con(delta,u=g.b[v])
  # if not all outgoing edges full, all available inflow must be spent
  U=g.b[v]+sum(g.edges[i][2] for i in inc)
  con(delta+[(2*E+v,U)],l=g.b[v])
  cap=sum(g.edges[i][2] for i in es)
  con([(i,1) for i in es]+[(2*E+v,-cap)],l=0)
  for j,i in enumerate(es):
   con([(i,1),(E+i,-g.edges[i][2])],u=0)
   if j:
    prev=es[j-1]
    con([(prev,1),(E+i,-g.edges[prev][2])],l=0)
 res=milp(c,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(np.array(rows),lower,upper),options={'time_limit':20,'mip_rel_gap':0})
 assert res.success,res.message
 f=tuple(int(round(x)) for x in res.x[:E]);assert max(abs(f[i]-res.x[i]) for i in range(E))<1e-6
 # Exact independently stated fixed-point condition: cap clipping of remaining prefix input.
 for v,es in enumerate(p):
  a=g.b[v]+sum(f[i] for i,(_,w,_) in enumerate(g.edges) if w==v)
  prefix=0
  for i in es:
   assert f[i]==min(g.edges[i][2],max(a-prefix,0))
   prefix+=g.edges[i][2]
 assert abs(sum(f)+res.fun)<1e-6
 return f,tuple(sum(f[i] for i in es) for es in p)

def main():
 start=time.time();rng=random.Random(20261012);checks=[]
 # Feedback changes external input from 0 to T when owner reverses its order.
 # This demonstrates why a local fixed-input comparison is insufficient.
 for M in (2,3,4):
  g=Game();g.edge('v','w',M+1);g.edge('w','v',M);g.edge('v','z',4);g.edge('z','v',3)
  p=g.default();u=g.pos['v'];good=solve(g,p);bad=solve(g,g.dev(p,u,reversed(p[u])))
  assert good[1][u]==M and bad[1][u]==3
  checks.append({'kind':'feedback_sharpness','M':M,'T':3,'good':good[1][u],'bad':bad[1][u]})
 # Crosscheck every alarm profile through a distinct optimization formulation.
 from itertools import product
 for inp in (0,2):
  g=Game();g.node('a2',inp);g.node('a3',inp);add_alarm(g);p=g.default()
  for bits in product((0,1),repeat=3):
   q=p
   for name,bit in zip(('a1','a2','a3'),bits):
    if bit:q=g.dev(q,g.pos[name],reversed(q[g.pos[name]]))
   f,us=solve(g,q);old=g.clear(q)
   assert f==old[0] and us==old[1]
   checks.append({'kind':'alarm','input':inp,'bits':bits,'utilities':us})
 # Wild and normalized full instances, including empty clauses and tautologies.
 cases=[(0,1,[[]]),(0,1,[[('Y',0,0),('Y',0,1)]]),(1,2,[[('X',0,1),('Y',0,0)],[('Y',0,1),('Y',1,1)]]),(1,1,[[('X',0,0)],[('X',0,1)]]),(0,2,[[('Y',0,1)],[('Y',1,0)]])]
 for idx,(n,r,clauses) in enumerate(cases):
  g,B=build(n,r,clauses);p=g.default()
  for rep in range(6):
   norm=(rep%2==0)
   q=tuple(es if norm and u in g.gates else tuple(rng.sample(es,len(es))) for u,es in enumerate(p))
   f,us=solve(g,q);old=g.clear(q)
   assert f==old[0] and us==old[1]
   if norm:assert us[g.pos['d']]==r*B+signal(g,q,n,r,clauses,B)
   checks.append({'kind':'full_graph','case':idx,'normalized':norm,'flow_sum':sum(f),'tester_utility':us[g.pos['d']]})
 out={'method':'Disjunctive MILP maximizing total flow, separate from downward iteration','floating_optimization_caveat':'MILP solver uses floating arithmetic; rounded fixed-point equations checked exactly; no formal optimality certificate claimed','checks':checks,'count':len(checks),'seconds':time.time()-start}
 Path('independent_milp_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
