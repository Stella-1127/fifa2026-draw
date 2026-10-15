/* Adapted from Jeffrey S. Rosenthal / Gareth O. Roberts, March 2022:
 * https://probability.ca/fdraw/drawnew.js
 * Original randassign/isvalid array-based rejection structure retained below,
 * renamed variables; 12 groups, three fixed hosts, full confed masks and seeds.
 * Original unmodified files in original/. Skip extension uses engine.js.
 * Multiple-balls method is not implemented in this 2026 adaptation.
 */
let candidate=[],random2026=Math.random;
function randint(n){return Math.floor(random2026()*n);}
function randassign(){candidate=initial();for(let pot=1;pot<=4;pot++){let taken=Array(12).fill(false);for(let i=0;i<48;i++)if(TEAMS[i].pot===pot&&candidate[i]>=0)taken[candidate[i]]=true;for(let i=0;i<48;i++)if(TEAMS[i].pot===pot&&candidate[i]<0){let g;do{g=randint(12);}while(taken[g]);candidate[i]=g;taken[g]=true;}}return candidate;}
function isvalid(){return valid(candidate);}
function uniformDraw(seed,maxAttempts=2000000){random2026=random(seed);for(let attempt=1;attempt<=maxAttempts;attempt++){randassign();if(isvalid())return{seed,a:candidate.slice(),steps:[],attempts:attempt,mechanism:'uniform'};}return{budgetExceeded:true,attempts:maxAttempts};}
function swapDraw(a,seed,count){random2026=random(seed);let accepted=0;for(let k=0;k<count;k++){let pot=randint(4)+1,ids=TEAMS.map((t,i)=>i).filter(i=>TEAMS[i].pot===pot&&!['MEX','CAN','USA'].includes(TEAMS[i].team_id));let i=ids[randint(ids.length)],j=ids[randint(ids.length)],b=a.slice();[b[i],b[j]]=[b[j],b[i]];candidate=b;if(isvalid()){a=b;accepted++;}}return{a,accepted};}
