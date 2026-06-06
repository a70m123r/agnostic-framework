#!/usr/bin/env python3
"""Procedural build for the Adversarial-Function Atlas (v2).

Reads adversarial_examples_dataset.json (enriched) and emits a self-contained
interactive HTML with three coordinated views:
  1. Timeline      - rung x time, t_phenomenon <-> t_observed toggle, fuzzy-as-gradient,
                     detection-lag mode, colour overlays, scrubber, + the C1.3 rate inset.
  2. Evolution     - force-directed lineage graph: evolved-from / transposed-from (cross-plane) / related.
  3. Outcomes      - examples grouped by attack<->counter outcome (equilibrium / new-action-space +/-/ ...),
                     with counter-measures.
Data inlined => opens offline. Re-run after editing the dataset or EQ defaults.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.loads(open(os.path.join(HERE, "adversarial_examples_dataset.json"), encoding="utf-8").read())
data_js = json.dumps(rows, ensure_ascii=False)
EQ = {"density_mid": 2005, "cost_floor": 0.03, "year_min": 1990, "year_max": 2026}
eq_js = json.dumps(EQ)

TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adversarial-Function Atlas v2</title>
<style>
 :root{--bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--mut:#8b949e;--line:#30363d;--acc:#58a6ff;}
 *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}
 header{padding:9px 14px;border-bottom:1px solid var(--line)}h1{font-size:15px;margin:0}.sub{color:var(--mut);font-size:11px}
 .tabs{display:flex;gap:6px;padding:7px 12px;border-bottom:1px solid var(--line)}
 .tab{background:#21262d;border:1px solid var(--line);border-radius:6px;padding:5px 12px;cursor:pointer}.tab.on{background:var(--acc);color:#06101f;font-weight:600;border-color:var(--acc)}
 .bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:7px 12px;border-bottom:1px solid var(--line)}
 .bar label{color:var(--mut)} button,select{background:#21262d;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 8px;cursor:pointer;font-size:12px}
 button.on{background:var(--acc);color:#06101f;border-color:var(--acc);font-weight:600}
 .grp{display:none;gap:6px;align-items:center;flex-wrap:wrap}.grp.on{display:flex}
 .wrap{display:flex;height:calc(100vh - 130px)}.left{flex:1;min-width:0;display:flex;flex-direction:column}
 .right{width:350px;border-left:1px solid var(--line);overflow:auto;padding:10px 12px}
 svg#plot{flex:1;width:100%}
 .node{cursor:pointer}.rungband:nth-child(even){fill:#ffffff05}.rungband{fill:#ffffff02}
 .axis{stroke:var(--line)}.axt{fill:var(--mut);font-size:10px}.runglab{fill:var(--mut);font-size:10px}
 .playhead{stroke:var(--acc);stroke-width:1.4;stroke-dasharray:4 3}
 .edge{fill:none}.edge.evolved{stroke:#6e7681;stroke-width:1}.edge.transposed{stroke:#f0883e;stroke-width:1.6;stroke-dasharray:5 3}.edge.related{stroke:#30363d;stroke-width:.7}
 .lag{stroke:#d29922;stroke-width:1.1;opacity:.55}
 .leg{display:flex;flex-wrap:wrap;gap:8px;font-size:10px;color:var(--mut);padding:4px 12px;border-bottom:1px solid var(--line)}
 .sw{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:3px;vertical-align:middle}
 .row{margin:3px 0}.k{color:var(--mut)}.pill{display:inline-block;padding:1px 6px;border-radius:10px;font-size:10px;border:1px solid var(--line);margin:1px 3px 1px 0}
 .chain{display:flex;flex-direction:column;gap:3px;margin:5px 0}.lvl{background:#21262d;border:1px solid var(--line);border-left:3px solid #f0883e;border-radius:5px;padding:4px 7px;font-size:12px}.lvl .ar{color:#f0883e;font-weight:700}
 .cm{border-left:3px solid #3fb950;background:#13241a;border-radius:4px;padding:3px 6px;margin:2px 0;font-size:11.5px}
 .cite{font-size:11px;color:var(--mut);word-break:break-word}a{color:var(--acc)}
 #rate{width:100%;height:108px}.eqbox{padding:6px 12px;border-top:1px solid var(--line)}.eqbox .g{display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:11px;color:var(--mut)}
 .obadge{font-weight:700;padding:1px 6px;border-radius:5px;color:#06101f}
</style></head><body>
<header><h1>Adversarial-Function Atlas <span class="sub">v2 · {N} documented examples · viroid → cosmic + latent · Tier-3 exploratory, not canon</span></h1></header>
<div class="tabs">
 <button class="tab on" data-v="timeline">① Timeline</button>
 <button class="tab" data-v="tree">② Evolution / connection tree</button>
 <button class="tab" data-v="outcomes">③ Counter-measures &amp; outcomes</button>
</div>
<div class="bar">
 <!-- timeline controls -->
 <span class="grp on" id="g-timeline">
  <label>time:</label><button id="tm-phenom" class="on">t_phenomenon (when it operated)</button><button id="tm-obs">t_observed (when named)</button>
  <button id="tm-lag">detection-lag</button>
  <span style="width:8px"></span><label>scrub:</label><input id="scrub" type="range" min="0" max="1000" value="1000" style="width:170px"><button id="play">▶</button>
  <span style="width:8px"></span><label>colour:</label>
  <button class="ov on" data-ov="rung">rung</button><button class="ov" data-ov="latent">latent/phys</button><button class="ov" data-ov="register">register</button><button class="ov" data-ov="outcome">outcome</button>
  <button id="f-nested">nested-pawn</button>
 </span>
 <!-- tree controls -->
 <span class="grp" id="g-tree">
  <label>edges:</label><button id="e-evolved" class="on">evolved-from</button><button id="e-transposed" class="on">transposed (cross-plane)</button><button id="e-related">related</button>
  <span class="sub">drag a node to pin; nodes banded by rung (molecular bottom → cosmic top)</span>
 </span>
 <!-- outcomes controls -->
 <span class="grp" id="g-outcomes"><span class="sub">columns = what the attack↔counter dynamic produced · chip colour = rung · click for counter-measures</span></span>
</div>
<div class="leg" id="legend"></div>
<div class="wrap"><div class="left"><svg id="plot"></svg>
 <div class="eqbox" id="eqbox"><div class="g"><b style="color:var(--ink)">C1.3 dynamic:</b> rate ≈ density(t) × catalysis(t).
  density-k<input id="kd" type="range" min="5" max="40" value="18" style="width:70px"> cost-drop-k<input id="kc" type="range" min="5" max="40" value="16" style="width:70px">
  <button id="rq">Red-Queen cycling: off</button></div><svg id="rate"></svg></div>
</div><div class="right" id="detail"><div class="mut">Click any node for full classification, counter-measures, outcome, and the lineage / nested-pawn chain.</div></div></div>
<svg width="0" height="0"><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#f0883e"/></marker></defs></svg>
<script>
const DATA=/*DATA*/, EQ=/*EQ*/;
const RUNGS=["molecular","cellular","organismal","cognitive","social-institutional","latent-algorithmic","cosmic"];
const RI=Object.fromEntries(RUNGS.map((r,i)=>[r,i]));
const COL={
 rung:["#6e7681","#79c0ff","#3fb950","#d29922","#f0883e","#db61a2","#a371f7"],
 latent:{latent:"#a371f7",physical:"#3fb950",both:"#58a6ff"},
 register:{fact:"#58a6ff",time:"#f0883e",sequence:"#db61a2",none:"#6e7681"},
 outcome:{"equilibrium":"#58a6ff","new-action-space-positive":"#3fb950","new-action-space-negative":"#f85149","escalating-arms-race":"#f0883e","ongoing-no-equilibrium":"#8b949e","attacker-collapse":"#a371f7","defender-collapse":"#db61a2","n/a":"#484f58"}
};
const NS="http://www.w3.org/2000/svg";
const byId=Object.fromEntries(DATA.map(d=>[d.id,d]));
let S={view:"timeline",tmode:"phenom",lag:false,ov:"rung",nested:false,scrub:1000,rq:false,kd:18,kc:16,sel:null,
       edges:{evolved:true,transposed:true,related:false}};
const plot=document.getElementById("plot");let W,H;
function size(){W=plot.clientWidth;H=plot.clientHeight;}
function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function hash(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return h;}
function ybpOf(d){const v=S.tmode==="obs"?d.t_obs_ybp:(S.tmode==="phenom"?d.t_phenom_ybp:d.t_ybp);return (v===undefined?null:v);}
function isFuzzy(d){const t=S.tmode==="obs"?d.t_observed:d.t_phenomenon;return t&&t.fuzzy;}
function isNeutral(d){return (d.beneficiary_boundary_check||"").toUpperCase().includes("NEUTRAL");}
const FIN=DATA.map(ybpOf).filter(v=>typeof v==="number"&&v>0);
const UMAX=Math.max.apply(null,DATA.map(d=>{const v=(d.t_phenom_ybp||d.t_ybp||1);return Math.log10((typeof v==="number"&&v>0?v:1)+1);}));
let MT={l:118,r:120,t:12,b:26};
function Xu(u){return MT.l+(1-u/UMAX)*(W-MT.l-MT.r);}
function Xybp(v){ if(v===null||v===undefined) return MT.l-70; if(v===-1) return W-MT.r+58; if(v<=0) return W-MT.r+30; return Xu(Math.log10(v+1)); }
function Yband(i){const h=(H-MT.t-MT.b)/RUNGS.length;return MT.t+(RUNGS.length-1-i)*h+h/2;}
function colour(d){if(S.ov==="rung")return COL.rung[RI[d.rung]];if(S.ov==="latent")return COL.latent[d.latent_or_physical]||"#888";if(S.ov==="register")return COL.register[d.deceivability_register]||"#888";if(S.ov==="outcome")return COL.outcome[(d.outcome||{}).type]||"#888";return "#888";}
function scrubU(){return UMAX*(1-S.scrub/1000);}

// ---------- VIEW 1: TIMELINE ----------
function renderTimeline(){
 size();plot.innerHTML="";const h=(H-MT.t-MT.b)/RUNGS.length;
 RUNGS.forEach((r,i)=>{el("rect",{class:"rungband",x:0,y:MT.t+i*h,width:W,height:h},plot);el("text",{class:"runglab",x:6,y:MT.t+i*h+h/2+3},plot).textContent=RUNGS[RUNGS.length-1-i];});
 [[3.5e9,"3.5 Gya"],[5.4e8,"Cambrian"],[1e6,"1 Mya"],[1e3,"1 kya"],[120,"1900s"],[16,"2010s"]].forEach(([y,l])=>{const x=Xybp(y);el("line",{class:"axis",x1:x,y1:MT.t,x2:x,y2:H-MT.b},plot);el("text",{class:"axt",x:x+2,y:H-MT.b+12},plot).textContent=l;});
 el("text",{class:"axt",x:MT.l-70,y:H-MT.b+12},plot).textContent="undated";
 el("text",{class:"axt",x:W-MT.r+30,y:H-MT.b+12},plot).textContent="future";
 const px=Xu(scrubU());el("line",{class:"playhead",x1:px,y1:MT.t,x2:px,y2:H-MT.b},plot);
 // detection-lag connectors
 if(S.lag){DATA.forEach(d=>{const a=d.t_phenom_ybp,b=d.t_obs_ybp;if(typeof a==="number"&&a>0&&typeof b==="number"&&b>0){const y=Yband(RI[d.rung])+(hash(d.id)%16-8);el("line",{class:"lag",x1:Xybp(a),y1:y,x2:Xybp(b),y2:y},plot);}});}
 // selected edge to target
 if(S.sel){const d=S.sel,v=ybpOf(d),x=Xybp(v),y=Yband(RI[d.rung])+(hash(d.id)%16-8);const tx=Math.min(W-MT.r+50,x+60);el("path",{class:"edge transposed",d:`M${x},${y} C ${x+30},${y-24} ${tx-20},${y-24} ${tx},${y-24}`,"marker-end":"url(#arr)"},plot);el("text",{class:"axt",x:tx,y:y-28,"text-anchor":"end"},plot).textContent="target: "+(d.target||"").slice(0,44);}
 DATA.forEach(d=>{
  if(S.nested&&!((d.nested_pawn||{}).is_nested))return;
  const v=ybpOf(d),x=Xybp(v),y=Yband(RI[d.rung])+(hash(d.id)%16-8);
  const u=(typeof v==="number"&&v>0)?Math.log10(v+1):UMAX;const revealed=(v===null||v===-1)?true:(u>=scrubU()-1e-9);
  const sel=S.sel&&S.sel.id===d.id,nested=(d.nested_pawn||{}).is_nested,c=colour(d),op=revealed?0.92:0.07;
  if(isFuzzy(d)){ // fuzzy date -> horizontal gradient smear instead of a crisp dot
   const g=el("ellipse",{class:"node",cx:x,cy:y,rx:16,ry:4.5,fill:c,"fill-opacity":op*0.32,stroke:"none"},plot);
   el("circle",{class:"node",cx:x,cy:y,r:sel?6:3,fill:c,"fill-opacity":op,stroke:sel?"#fff":(nested?"#f0883e":"none"),"stroke-width":nested?1:0},plot).addEventListener("click",()=>sel_(d));
   g.addEventListener("click",()=>sel_(d));
  }else{
   el("circle",{class:"node",cx:x,cy:y,r:sel?7:(nested?5:4),fill:c,"fill-opacity":op,stroke:sel?"#fff":(nested?"#f0883e":"#0d1117"),"stroke-width":sel?1.6:(nested?1.1:.5)},plot).addEventListener("click",()=>sel_(d));
  }
 });
 document.getElementById("eqbox").style.display="";
 legend();
}
function sel_(d){S.sel=d;routerRender();detail(d);}

// ---------- VIEW 2: EVOLUTION TREE (force-directed, rung-banded) ----------
let P={};
function initForce(){P={};DATA.forEach(d=>{P[d.id]={x:Xybp(d.t_phenom_ybp||d.t_ybp||1)||W/2,y:Yband(RI[d.rung])+(hash(d.id)%40-20),vx:0,vy:0,pin:false};});
 for(let t=0;t<320;t++)forceTick();}
function edgesList(){const L=[];DATA.forEach(d=>{(d.lineage_edges||[]).forEach(e=>{if(e.to_id&&byId[e.to_id]&&S.edges[e.type])L.push({a:d.id,b:e.to_id,type:e.type});});});return L;}
function forceTick(){
 const ids=DATA.map(d=>d.id),h=(H-MT.t-MT.b)/RUNGS.length;
 for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){const A=P[ids[i]],B=P[ids[j]];let dx=A.x-B.x,dy=A.y-B.y,d2=dx*dx+dy*dy+0.01,f=320/d2,d=Math.sqrt(d2);dx/=d;dy/=d;A.vx+=dx*f;A.vy+=dy*f;B.vx-=dx*f;B.vy-=dy*f;}
 edgesList().forEach(e=>{const A=P[e.a],B=P[e.b];let dx=B.x-A.x,dy=B.y-A.y,d=Math.sqrt(dx*dx+dy*dy)+0.01,f=(d-70)*0.02;dx/=d;dy/=d;A.vx+=dx*f;A.vy+=dy*f;B.vx-=dx*f;B.vy-=dy*f;});
 DATA.forEach(d=>{const p=P[d.id];if(p.pin)return;const ty=Yband(RI[d.rung]);p.vy+=(ty-p.y)*0.06;p.vx+=((W/2)-p.x)*0.002;p.vx*=0.82;p.vy*=0.82;p.x+=Math.max(-12,Math.min(12,p.vx));p.y+=Math.max(-12,Math.min(12,p.vy));p.x=Math.max(MT.l,Math.min(W-MT.r,p.x));p.y=Math.max(MT.t+4,Math.min(H-MT.b-4,p.y));});
}
let dragId=null;
function renderTree(){
 size();if(!Object.keys(P).length)initForce();plot.innerHTML="";const h=(H-MT.t-MT.b)/RUNGS.length;
 RUNGS.forEach((r,i)=>{el("rect",{class:"rungband",x:0,y:MT.t+i*h,width:W,height:h},plot);el("text",{class:"runglab",x:6,y:MT.t+i*h+12},plot).textContent=RUNGS[RUNGS.length-1-i];});
 edgesList().forEach(e=>{const A=P[e.a],B=P[e.b];el("path",{class:"edge "+e.type,d:`M${A.x},${A.y} Q ${(A.x+B.x)/2},${(A.y+B.y)/2-18} ${B.x},${B.y}`},plot);});
 DATA.forEach(d=>{const p=P[d.id],sel=S.sel&&S.sel.id===d.id,nested=(d.nested_pawn||{}).is_nested;
  const c=el("circle",{class:"node",cx:p.x,cy:p.y,r:sel?7:4.5,fill:COL.rung[RI[d.rung]],stroke:sel?"#fff":(nested?"#f0883e":"#0d1117"),"stroke-width":sel?1.6:(nested?1.1:.5)},plot);
  c.addEventListener("mousedown",ev=>{dragId=d.id;P[d.id].pin=true;ev.preventDefault();});
  c.addEventListener("click",()=>sel_(d));});
 document.getElementById("eqbox").style.display="none";legend();
}
plot.addEventListener("mousemove",ev=>{if(dragId&&S.view==="tree"){const r=plot.getBoundingClientRect();P[dragId].x=ev.clientX-r.left;P[dragId].y=ev.clientY-r.top;renderTree();}});
window.addEventListener("mouseup",()=>{dragId=null;});

// ---------- VIEW 3: OUTCOMES ----------
const OUT_ORDER=["new-action-space-positive","equilibrium","escalating-arms-race","ongoing-no-equilibrium","new-action-space-negative","attacker-collapse","defender-collapse","n/a"];
function renderOutcomes(){
 size();plot.innerHTML="";document.getElementById("eqbox").style.display="none";
 const cols=OUT_ORDER.filter(o=>DATA.some(d=>(d.outcome||{}).type===o));
 const cw=(W-20)/cols.length;
 cols.forEach((o,ci)=>{
  const x0=10+ci*cw;el("rect",{x:x0,y:MT.t,width:cw-6,height:H-MT.t-6,fill:"#ffffff04",rx:6},plot);
  const items=DATA.filter(d=>(d.outcome||{}).type===o);
  el("rect",{x:x0,y:MT.t,width:cw-6,height:22,fill:COL.outcome[o],rx:6},plot);
  el("text",{x:x0+6,y:MT.t+15,style:"font-size:11px;font-weight:700;fill:#06101f"},plot).textContent=o+" ("+items.length+")";
  items.forEach((d,k)=>{const cols2=Math.floor((cw-16)/26)||1;const cx=x0+14+(k%cols2)*26,cy=MT.t+44+Math.floor(k/cols2)*26;
   const sel=S.sel&&S.sel.id===d.id;
   el("circle",{class:"node",cx:cx,cy:cy,r:sel?9:7,fill:COL.rung[RI[d.rung]],stroke:sel?"#fff":"#0d1117","stroke-width":sel?1.6:.6},plot).addEventListener("click",()=>sel_(d));
  });
 });
 legend();
}

// ---------- shared ----------
function legend(){const L=document.getElementById("legend");L.innerHTML="";
 if(S.view==="outcomes"||S.ov==="rung"||S.view==="tree"){RUNGS.forEach((r,i)=>{const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+COL.rung[i]+'"></span>'+r;L.appendChild(s);});}
 else{let m=S.ov==="latent"?COL.latent:S.ov==="register"?COL.register:COL.outcome;for(const k in m){const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+m[k]+'"></span>'+k;L.appendChild(s);}}
 if(S.view==="tree"){const e=document.createElement("span");e.innerHTML='&nbsp; edges: <span style="color:#6e7681">— evolved</span> <span style="color:#f0883e">- - transposed (cross-plane)</span>';L.appendChild(e);}
}
function chainHTML(ch){if(!ch)return"";const p=ch.split(/\s*(?:->|→|⇒)\s*/).filter(x=>x.trim());if(p.length<2)return '<div class="lvl">'+esc(ch)+'</div>';return '<div class="chain">'+p.map((x,i)=>'<div class="lvl">'+(i?'<span class="ar">▼ </span>':'')+esc(x)+'</div>').join("")+'</div>';}
function detail(d){const D=document.getElementById("detail"),np=d.nested_pawn||{},oc=d.outcome||{},li=d.lineage||{},tp=d.t_phenomenon||{},to=d.t_observed||{};
 const cm=(d.counter_measures||[]).map(c=>'<div class="cm"><b>'+esc(c.name)+'</b> <span class="k">'+esc(c.approx_time)+'</span><br>'+esc(c.note)+'</div>').join("");
 D.innerHTML='<div style="font-weight:700;font-size:14px">'+esc(d.name)+'</div>'+
 '<div class="row"><span class="pill">'+esc(d.rung)+'</span><span class="pill">'+esc(d.sub_primitive)+'</span><span class="pill">'+esc(d.latent_or_physical)+'</span><span class="pill">reg:'+esc(d.deceivability_register)+'</span></div>'+
 '<div class="row"><span class="k">operated (t_phenomenon):</span> '+esc(tp.label||d.t_label||"?")+(tp.fuzzy?' <span class="pill">fuzzy</span>':'')+'</div>'+
 '<div class="row"><span class="k">named (t_observed):</span> '+esc(to.label||"?")+(to.fuzzy?' <span class="pill">fuzzy</span>':'')+'</div>'+
 (oc.type?'<div class="row"><span class="obadge" style="background:'+(COL.outcome[oc.type]||"#888")+'">'+esc(oc.type)+'</span> '+esc(oc.note)+'</div>':'')+
 (np.is_nested?'<div class="row"><b style="color:#f0883e">nested pawn — duped up the chain:</b>'+chainHTML(np.chain)+'</div>':'')+
 '<div class="row"><span class="k">beneficiary →</span> '+esc(d.beneficiary)+'</div>'+
 '<div class="row"><span class="k">target →</span> '+esc(d.target)+'</div>'+
 '<div class="row"><span class="k">externalized cost →</span> '+esc(d.externalized_cost)+'</div>'+
 (cm?'<div class="row"><b style="color:#3fb950">counter-measures:</b>'+cm+'</div>':'<div class="row k">counter-measures: none documented</div>')+
 ((li.evolved_from||li.transposed_from||(li.related||[]).length||(li.evolution_steps||[]).length)?'<div class="row"><b>lineage:</b>'+
   (li.evolved_from?'<div>evolved from: '+esc(li.evolved_from)+'</div>':'')+
   (li.transposed_from?'<div style="color:#f0883e">transposed from (another plane): '+esc(li.transposed_from)+'</div>':'')+
   ((li.related||[]).length?'<div class="k">related: '+esc((li.related||[]).join("; "))+'</div>':'')+
   ((li.evolution_steps||[]).length?'<div class="k">evolution: '+esc((li.evolution_steps||[]).join("  →  "))+'</div>':'')+'</div>':'')+
 '<div class="row"><span class="k">C0.2 →</span> '+esc(d.beneficiary_boundary_check)+'</div>'+
 '<div class="row cite"><span class="k">sources →</span> '+esc(d.citation)+(d.enrich_citation?' · '+esc(d.enrich_citation):'')+'</div>';
}

// rate inset (timeline only)
function density(y){return 1/(1+Math.exp(-(S.kd/100)*(y-EQ.density_mid)));}
function cost(y){return EQ.cost_floor+(1-EQ.cost_floor)*Math.exp(-(S.kc/100)*(y-EQ.year_min));}
function rate(y){return density(y)/Math.max(cost(y),0.02);}
function renderRate(){const s=document.getElementById("rate");s.innerHTML="";const w=s.clientWidth||600,h=108,m={l:30,r:8,t:6,b:14};const ys=[];for(let y=EQ.year_min;y<=EQ.year_max;y++)ys.push(y);const mx=Math.max.apply(null,ys.map(rate));const X=y=>m.l+(y-EQ.year_min)/(EQ.year_max-EQ.year_min)*(w-m.l-m.r),Y=v=>h-m.b-(v/mx)*(h-m.t-m.b);
 el("line",{class:"axis",x1:m.l,y1:h-m.b,x2:w-m.r,y2:h-m.b},s);[1990,2005,2013,2026].forEach(y=>el("text",{class:"axt",x:X(y)-10,y:h-2},s).textContent=y);
 el("path",{d:"M"+ys.map(y=>X(y)+","+Y(rate(y))).join(" L"),fill:"none",stroke:"#58a6ff","stroke-width":2},s);
 if(S.rq)el("path",{d:"M"+ys.map(y=>X(y)+","+Y(rate(y)*(1+0.1*Math.sin((y-EQ.year_min)*1.3)))).join(" L"),fill:"none",stroke:"#db61a2","stroke-width":1,"stroke-dasharray":"3 2"},s);
 DATA.filter(d=>d.t_year&&d.t_year>=EQ.year_min&&d.rung==="latent-algorithmic").forEach(d=>el("circle",{cx:X(d.t_year),cy:Y(rate(d.t_year)),r:3,fill:"#f0883e",stroke:"#0d1117"},s).addEventListener("click",()=>sel_(d)));
}
function routerRender(){if(S.view==="timeline")renderTimeline();else if(S.view==="tree")renderTree();else renderOutcomes();}

// wiring
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));b.classList.add("on");S.view=b.dataset.v;
 document.querySelectorAll(".grp").forEach(g=>g.classList.remove("on"));document.getElementById("g-"+S.view).classList.add("on");routerRender();if(S.view==="timeline")renderRate();}));
document.getElementById("tm-phenom").addEventListener("click",function(){S.tmode="phenom";S.lag=false;this.classList.add("on");document.getElementById("tm-obs").classList.remove("on");document.getElementById("tm-lag").classList.remove("on");renderTimeline();});
document.getElementById("tm-obs").addEventListener("click",function(){S.tmode="obs";S.lag=false;this.classList.add("on");document.getElementById("tm-phenom").classList.remove("on");document.getElementById("tm-lag").classList.remove("on");renderTimeline();});
document.getElementById("tm-lag").addEventListener("click",function(){S.lag=!S.lag;this.classList.toggle("on",S.lag);renderTimeline();});
document.querySelectorAll(".ov").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".ov").forEach(x=>x.classList.remove("on"));b.classList.add("on");S.ov=b.dataset.ov;renderTimeline();}));
document.getElementById("f-nested").addEventListener("click",function(){S.nested=!S.nested;this.classList.toggle("on",S.nested);renderTimeline();});
const sc=document.getElementById("scrub");sc.addEventListener("input",()=>{S.scrub=+sc.value;renderTimeline();});
let tmr=null;document.getElementById("play").addEventListener("click",function(){if(tmr){clearInterval(tmr);tmr=null;this.textContent="▶";return;}this.textContent="⏸";if(S.scrub>=1000)S.scrub=0;tmr=setInterval(()=>{S.scrub+=8;if(S.scrub>=1000){S.scrub=1000;clearInterval(tmr);tmr=null;document.getElementById("play").textContent="▶";}sc.value=S.scrub;renderTimeline();},60);});
["evolved","transposed","related"].forEach(t=>document.getElementById("e-"+t).addEventListener("click",function(){S.edges[t]=!S.edges[t];this.classList.toggle("on",S.edges[t]);renderTree();}));
document.getElementById("kd").addEventListener("input",function(){S.kd=+this.value;renderRate();});
document.getElementById("kc").addEventListener("input",function(){S.kc=+this.value;renderRate();});
document.getElementById("rq").addEventListener("click",function(){S.rq=!S.rq;this.textContent="Red-Queen cycling: "+(S.rq?"on":"off");renderRate();});
window.addEventListener("resize",()=>{routerRender();if(S.view==="timeline")renderRate();});
routerRender();renderRate();
</script></body></html>"""

html = TEMPLATE.replace("/*DATA*/", data_js).replace("/*EQ*/", eq_js).replace("{N}", str(len(rows)))
open(os.path.join(HERE, "adversarial_atlas.html"), "w", encoding="utf-8").write(html)
print("wrote adversarial_atlas.html (", len(html), "chars,", len(rows), "examples )")
