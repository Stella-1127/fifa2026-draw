"""2026 Skip simulation based on arXiv:2602.21029 Section 3.4.
Independent implementation, not original author code.
pip install gurobipy ; requires a valid Gurobi license.
python gurobi_simulator.py --draws 10 --seed 2026 --output draws.csv
Run alongside teams_2026.csv and sequence_2026.csv (download from this page).
"""
import argparse,csv,random
from pathlib import Path
import gurobipy as gp
from gurobipy import GRB
GROUPS=list('ABCDEFGHIJKL')
QUARTERS=[set('EFI'),set('DGH'),set('ACL'),set('BJK')]
TOP=['ESP','ARG','FRA','ENG']
HOSTS={'MEX':'A','CAN':'B','USA':'D'}

def load(path):
    rows=list(csv.DictReader(open(path,encoding='utf-8-sig')))
    for r in rows:
        r['pot']=int(r['pot']);r['cs']=set(r['confederation_set'].replace('|',';').replace(',',';').split(';'))
    assert len(rows)==48 and len({r['team_id'] for r in rows})==48
    assert all(sum(r['pot']==p for r in rows)==12 for p in range(1,5))
    return rows

def model_for(rows):
    m=gp.Model('fifa2026');m.Params.OutputFlag=0
    ids=[r['team_id'] for r in rows];x=m.addVars(ids,GROUPS,vtype=GRB.BINARY,name='x')
    for i in ids:m.addConstr(gp.quicksum(x[i,g] for g in GROUPS)==1)
    for g in GROUPS:
        for p in range(1,5):m.addConstr(gp.quicksum(x[r['team_id'],g] for r in rows if r['pot']==p)==1)
        for c in ['AFC','CAF','CONCACAF','CONMEBOL','OFC']:
            m.addConstr(gp.quicksum(x[r['team_id'],g] for r in rows if c in r['cs'])<=1)
        eu=gp.quicksum(x[r['team_id'],g] for r in rows if 'UEFA' in r['cs'])
        m.addConstr(eu>=1);m.addConstr(eu<=2)
    for q in QUARTERS:m.addConstr(gp.quicksum(x[i,g] for i in TOP for g in q)<=1)
    for i,j in [('ESP','ARG'),('FRA','ENG')]:
        for half in [QUARTERS[0]|QUARTERS[1],QUARTERS[2]|QUARTERS[3]]:
            m.addConstr(gp.quicksum(x[i,g]+x[j,g] for g in half)<=1)
    for i,g in HOSTS.items():x[i,g].LB=1
    m.setObjective(0);m.update()
    return m,x

def simulate(rows,rng,sequence=None):
    m,x=model_for(rows);fixed=dict(HOSTS)
    if sequence is None:
        sequence=[]
        for p in range(1,5):
            ids=[r['team_id'] for r in rows if r['pot']==p and r['team_id'] not in HOSTS]
            rng.shuffle(ids);sequence.extend(ids)
    for i in sequence:
        if i in fixed:raise ValueError('Repeated drawn object')
        accepted=False
        for g in GROUPS:
            x[i,g].LB=1;m.optimize()
            if m.SolCount>0:
                fixed[i]=g;accepted=True;break
            if m.Status!=GRB.INFEASIBLE:
                raise RuntimeError(f'Unknown solver status {m.Status}; do not treat as infeasible')
            x[i,g].LB=0
        if not accepted:raise RuntimeError('No feasible placement')
    if len(fixed)!=48:raise ValueError('Incomplete draw')
    m.dispose();return fixed

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--draws',type=int,default=10);ap.add_argument('--seed',type=int,default=2026)
    ap.add_argument('--output',default='draws.csv');ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    root=Path(__file__).resolve().parent;rows=load(root/'teams_2026.csv');rng=random.Random(args.seed)
    seq=list(csv.DictReader(open(root/'sequence_2026.csv',encoding='utf-8-sig'))) if args.replay else None
    with open(args.output,'w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f);writer.writerow(['draw_id','seed','team_id','pot','group'])
        for b in range(1 if args.replay else args.draws):
            d=simulate(rows,rng,[r['team_id'] for r in seq if r['draw_method']=='random_ball'] if seq else None)
            if seq:assert all(d[r['team_id']]==r['allocated_group'] for r in seq)
            for r in rows:writer.writerow([b+1,args.seed,r['team_id'],r['pot'],d[r['team_id']]])
            print('completed',b+1)
