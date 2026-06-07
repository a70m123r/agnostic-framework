#!/usr/bin/env python3
"""Procedural build for the Adversarial-Function Atlas (v3).

Reads adversarial_examples_dataset.json (enriched, observer-agnostic outcome model)
and emits a self-contained interactive HTML with SIX coordinated views:
  1. Timeline    - rung x time; t_phenomenon<->t_observed toggle; fuzzy-as-gradient;
                   detection-lag mode; colour overlays (rung/latent/register/structural); scrubber; C1.3 rate inset.
  2. Evolution   - force-directed lineage graph; edge types evolved / transposed / latent-transposition / related;
                   per-node evolution_steps spurs (the "how each hack evolved" chain).
  3. Outcomes    - columns by observer-INDEPENDENT structural outcome; chips RECOLOUR by the chosen
                   observer frame (beneficiary / target / third-party) with a symmetric flip — the agnostic view.
  4. Stratosphere- the rungs bent into concentric shells, human band emphasised, cosmic envelope.
  5. Knowledge   - concept<->example ontology graph (rungs / sub-primitives / registers as hubs).
  6. Radar       - per-rung profiles across the measurable axes (lag / counters / connectivity / nested / latent / existence / symmetric).
Data inlined => opens offline. Re-run after editing the dataset.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.loads(open(os.path.join(HERE, "adversarial_examples_dataset.json"), encoding="utf-8").read())
data_js = json.dumps(rows, ensure_ascii=False)
EQ = {"density_mid": 2005, "cost_floor": 0.03, "year_min": 1990, "year_max": 2026}
eq_js = json.dumps(EQ)

TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adversarial-Function Atlas v3</title>
<style>
 :root{--bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--mut:#8b949e;--line:#30363d;--acc:#58a6ff;}
 *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}
 header{padding:8px 14px;border-bottom:1px solid var(--line)}h1{font-size:15px;margin:0}.sub{color:var(--mut);font-size:11px}
 .tabs{display:flex;gap:5px;padding:7px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
 .tab{background:#21262d;border:1px solid var(--line);border-radius:6px;padding:5px 11px;cursor:pointer;font-size:12px}.tab.on{background:var(--acc);color:#06101f;font-weight:600;border-color:var(--acc)}
 .bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:7px 12px;border-bottom:1px solid var(--line);min-height:40px}
 .bar label{color:var(--mut)} button,select{background:#21262d;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 8px;cursor:pointer;font-size:12px}
 button.on{background:var(--acc);color:#06101f;border-color:var(--acc);font-weight:600}
 .grp{display:none;gap:6px;align-items:center;flex-wrap:wrap}.grp.on{display:flex}
 .wrap{display:flex;height:calc(100vh - 132px)}.left{flex:1;min-width:0;display:flex;flex-direction:column}
 .right{width:362px;border-left:1px solid var(--line);overflow:auto;padding:10px 12px}
 svg#plot{flex:1;width:100%}
 .rungband:nth-child(even){fill:#ffffff05}.rungband{fill:#ffffff02}
 .axis{stroke:var(--line)}.axt{fill:var(--mut);font-size:10px}.runglab{fill:var(--mut);font-size:10px}
 .playhead{stroke:var(--acc);stroke-width:1.4;stroke-dasharray:4 3}
 .edge{fill:none}.edge.evolved{stroke:#6e7681;stroke-width:1}.edge.transposed{stroke:#f0883e;stroke-width:1.5;stroke-dasharray:5 3}
 .edge.latent-transposition{stroke:#a371f7;stroke-width:1.6;stroke-dasharray:2 3}.edge.related{stroke:#30363d;stroke-width:.7}
 .lag{stroke:#d29922;stroke-width:1.1;opacity:.5}.spur{stroke:#d29922;stroke-width:.8;opacity:.5}
 .leg{display:flex;flex-wrap:wrap;gap:8px;font-size:10px;color:var(--mut);padding:4px 12px;border-bottom:1px solid var(--line)}
 .sw{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:3px;vertical-align:middle}
 .row{margin:3px 0}.k{color:var(--mut)}.pill{display:inline-block;padding:1px 6px;border-radius:10px;font-size:10px;border:1px solid var(--line);margin:1px 3px 1px 0}
 .chain{display:flex;flex-direction:column;gap:3px;margin:5px 0}.lvl{background:#21262d;border:1px solid var(--line);border-left:3px solid #f0883e;border-radius:5px;padding:4px 7px;font-size:12px}.lvl .ar{color:#f0883e;font-weight:700}
 .cm{border-left:3px solid #3fb950;background:#13241a;border-radius:4px;padding:3px 6px;margin:2px 0;font-size:11.5px}
 .tp{border-left:3px solid #58a6ff;background:#0d1f2d;border-radius:4px;padding:3px 6px;margin:2px 0;font-size:11.5px}
 .cite{font-size:11px;color:var(--mut);word-break:break-word}a{color:var(--acc)}
 #rate{width:100%;height:104px}.eqbox{padding:6px 12px;border-top:1px solid var(--line)}.eqbox .g{display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:11px;color:var(--mut)}
 .vbadge{font-weight:700;padding:1px 6px;border-radius:5px;color:#06101f}
</style></head><body>
<header><h1>Adversarial-Function Atlas <span class="sub">v3 · {N} documented examples · viroid → cosmic + latent · observer-agnostic · Tier-3 exploratory, not canon</span></h1></header>
<div class="tabs">
 <button class="tab on" data-v="timeline">① Timeline</button>
 <button class="tab" data-v="tree">② Evolution tree</button>
 <button class="tab" data-v="outcomes">③ Outcomes (observer frames)</button>
 <button class="tab" data-v="strato">④ Stratosphere</button>
 <button class="tab" data-v="know">⑤ Knowledge graph</button>
 <button class="tab" data-v="radar">⑥ Radar</button>
</div>
<div class="bar">
 <span class="grp on" id="g-timeline">
  <label>time:</label><button id="tm-phenom" class="on">t_phenomenon</button><button id="tm-obs">t_observed</button><button id="tm-lag">detection-lag</button>
  <span style="width:6px"></span><label>scrub:</label><input id="scrub" type="range" min="0" max="1000" value="1000" style="width:150px"><button id="play">▶</button>
  <span style="width:6px"></span><label>colour:</label>
  <button class="ov on" data-ov="rung">rung</button><button class="ov" data-ov="latent">latent/phys</button><button class="ov" data-ov="register">register</button><button class="ov" data-ov="structural">structural</button>
  <button id="f-nested">nested-pawn</button>
 </span>
 <span class="grp" id="g-tree">
  <label>edges:</label><button id="e-evolved" class="on">evolved</button><button id="e-transposed" class="on">transposed</button><button id="e-latent-transposition" class="on">latent-transp</button><button id="e-related">related</button>
  <button id="spurs">evolution spurs: off</button><span class="sub">node size = #evolution-steps · drag to pin · click = chain</span>
 </span>
 <span class="grp" id="g-outcomes">
  <label>observer frame:</label><button id="fr-ben" class="on">beneficiary</button><button id="fr-tar">target</button><button id="fr-third">third-party</button>
  <button id="flip">flip symmetric</button><span class="sub">columns = observer-independent structural outcome · chip colour = the chosen chair's valence</span>
 </span>
 <span class="grp" id="g-strato"><span class="sub">concentric shells: molecular core → organismal surface → <b style="color:#d29922">the human band</b> → social scale-up → latent shell → cosmic envelope · colour = rung</span></span>
 <span class="grp" id="g-know">
  <label>concept edges:</label><button id="k-rung" class="on">rung</button><button id="k-sub">sub-primitive</button><button id="k-reg">register</button>
  <span class="sub">big nodes = concepts · small = examples · click a concept to isolate its examples</span>
 </span>
 <span class="grp" id="g-radar"><label>rungs:</label><span id="radar-toggles"></span></span>
</div>
<div class="leg" id="legend"></div>
<div class="wrap"><div class="left"><svg id="plot"></svg>
 <div class="eqbox" id="eqbox"><div class="g"><b style="color:var(--ink)">C1.3 dynamic:</b> rate ≈ density(t) × catalysis(t).
  density-k<input id="kd" type="range" min="5" max="40" value="18" style="width:64px"> cost-drop-k<input id="kc" type="range" min="5" max="40" value="16" style="width:64px">
  <button id="rq">Red-Queen: off</button></div><svg id="rate"></svg></div>
</div><div class="right" id="detail"><div class="mut">Click any node for full classification, the observer frames, counter-measures, and lineage (incl. how it evolved).</div></div></div>
<svg width="0" height="0"><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#f0883e"/></marker></defs></svg>
<script>
const DATA=/*DATA*/, EQ=/*EQ*/;
const RUNGS=["molecular","cellular","organismal","cognitive","social-institutional","latent-algorithmic","cosmic"];
const RI=Object.fromEntries(RUNGS.map((r,i)=>[r,i]));
const COL={
 rung:["#6e7681","#79c0ff","#3fb950","#d29922","#f0883e","#db61a2","#a371f7"],
 latent:{latent:"#a371f7",physical:"#3fb950",both:"#58a6ff"},
 reg:{fact:"#58a6ff",time:"#f0883e",sequence:"#db61a2",existence:"#a371f7",none:"#6e7681"},
 val:{positive:"#3fb950",negative:"#f85149",mixed:"#d29922",neutral:"#8b949e"},
 struct:{"new-action-space":"#3fb950","equilibrium":"#58a6ff","escalating-arms-race":"#f0883e","ongoing-no-equilibrium":"#8b949e","collapse-attacker":"#a371f7","collapse-defender":"#db61a2","n/a":"#484f58"}
};
const NS="http://www.w3.org/2000/svg";
const byId=Object.fromEntries(DATA.map(d=>[d.id,d]));
let S={view:"timeline",tmode:"phenom",lag:false,ov:"rung",nested:false,scrub:1000,rq:false,kd:18,kc:16,sel:null,
       edges:{evolved:true,transposed:true,"latent-transposition":true,related:false},spurs:false,
       frame:"ben",flip:false,kedges:{rung:true,sub:false,reg:false},kfocus:null,radarOn:{}};
RUNGS.forEach(r=>S.radarOn[r]=(r==="molecular"||r==="cognitive"||r==="cosmic"||r==="latent-algorithmic"));
const plot=document.getElementById("plot");let W,H;
function size(){W=plot.clientWidth;H=plot.clientHeight;}
function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
function esc(s){return (s==null?"":""+s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function hash(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return h;}
function mean(a){return a.length?a.reduce((x,y)=>x+y,0)/a.length:0;}
function frac(a,f){return a.length?a.filter(f).length/a.length:0;}
function ybpOf(d){const v=S.tmode==="obs"?d.t_obs_ybp:(S.tmode==="phenom"?d.t_phenom_ybp:d.t_ybp);return (v===undefined?null:v);}
function isFuzzy(d){const t=S.tmode==="obs"?d.t_observed:d.t_phenomenon;return t&&t.fuzzy;}
const UMAX=Math.max.apply(null,DATA.map(d=>{const v=(d.t_phenom_ybp||d.t_ybp||1);return Math.log10((typeof v==="number"&&v>0?v:1)+1);}));
const MT={l:120,r:120,t:12,b:26};
function Xu(u){return MT.l+(1-u/UMAX)*(W-MT.l-MT.r);}
function Xybp(v){if(v===null||v===undefined)return MT.l-72;if(v===-1)return W-MT.r+58;if(v<=0)return W-MT.r+30;return Xu(Math.log10(v+1));}
function Yband(i){const h=(H-MT.t-MT.b)/RUNGS.length;return MT.t+(RUNGS.length-1-i)*h+h/2;}
function colour(d){if(S.ov==="rung")return COL.rung[RI[d.rung]];if(S.ov==="latent")return COL.latent[d.latent_or_physical]||"#888";if(S.ov==="register")return COL.reg[d.deceivability_register]||"#888";if(S.ov==="structural")return COL.struct[(d.outcome||{}).structural]||"#888";return "#888";}
function scrubU(){return UMAX*(1-S.scrub/1000);}
function isNested(d){return (d.nested_pawn||{}).is_nested;}

// ---------- 1 TIMELINE ----------
function renderTimeline(){
 size();plot.innerHTML="";const h=(H-MT.t-MT.b)/RUNGS.length;
 RUNGS.forEach((r,i)=>{el("rect",{class:"rungband",x:0,y:MT.t+i*h,width:W,height:h},plot);el("text",{class:"runglab",x:6,y:MT.t+i*h+h/2+3},plot).textContent=RUNGS[RUNGS.length-1-i];});
 [[3.5e9,"3.5 Gya"],[5.4e8,"Cambrian"],[1e6,"1 Mya"],[1e3,"1 kya"],[120,"1900s"],[16,"2010s"]].forEach(([y,l])=>{const x=Xybp(y);el("line",{class:"axis",x1:x,y1:MT.t,x2:x,y2:H-MT.b},plot);el("text",{class:"axt",x:x+2,y:H-MT.b+12},plot).textContent=l;});
 el("text",{class:"axt",x:MT.l-72,y:H-MT.b+12},plot).textContent="undated";el("text",{class:"axt",x:W-MT.r+30,y:H-MT.b+12},plot).textContent="future";
 const px=Xu(scrubU());el("line",{class:"playhead",x1:px,y1:MT.t,x2:px,y2:H-MT.b},plot);
 if(S.lag)DATA.forEach(d=>{const a=d.t_phenom_ybp,b=d.t_obs_ybp;if(typeof a==="number"&&a>0&&typeof b==="number"&&b>0){const y=Yband(RI[d.rung])+(hash(d.id)%16-8);el("line",{class:"lag",x1:Xybp(a),y1:y,x2:Xybp(b),y2:y},plot);}});
 DATA.forEach(d=>{
  if(S.nested&&!isNested(d))return;
  const v=ybpOf(d),x=Xybp(v),y=Yband(RI[d.rung])+(hash(d.id)%16-8);
  const u=(typeof v==="number"&&v>0)?Math.log10(v+1):UMAX;const revealed=(v===null||v===-1)?true:(u>=scrubU()-1e-9);
  const sel=S.sel&&S.sel.id===d.id,c=colour(d),op=revealed?0.92:0.07,nst=isNested(d);
  if(isFuzzy(d)){el("ellipse",{class:"node",cx:x,cy:y,rx:15,ry:4.5,fill:c,"fill-opacity":op*0.3},plot).addEventListener("click",()=>sel_(d));
   el("circle",{cx:x,cy:y,r:sel?6:3,fill:c,"fill-opacity":op,stroke:sel?"#fff":(nst?"#f0883e":"none"),"stroke-width":nst?1:0},plot).addEventListener("click",()=>sel_(d));}
  else el("circle",{class:"node",cx:x,cy:y,r:sel?7:(nst?5:4),fill:c,"fill-opacity":op,stroke:sel?"#fff":(nst?"#f0883e":"#0d1117"),"stroke-width":sel?1.6:(nst?1.1:.5)},plot).addEventListener("click",()=>sel_(d));
 });
 document.getElementById("eqbox").style.display="";legend();
}
function sel_(d){S.sel=d;route();detail(d);}

// ---------- 2 EVOLUTION TREE ----------
let P={};
function initForce(){P={};DATA.forEach(d=>{P[d.id]={x:Xybp(d.t_phenom_ybp||d.t_ybp||1)||W/2,y:Yband(RI[d.rung])+(hash(d.id)%40-20),vx:0,vy:0,pin:false};});for(let t=0;t<320;t++)tick();}
function elist(){const L=[];DATA.forEach(d=>{(d.lineage_edges||[]).forEach(e=>{if(e.to_id&&byId[e.to_id]&&S.edges[e.type])L.push({a:d.id,b:e.to_id,type:e.type});});});return L;}
function tick(){const ids=DATA.map(d=>d.id);
 for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){const A=P[ids[i]],B=P[ids[j]];let dx=A.x-B.x,dy=A.y-B.y,d2=dx*dx+dy*dy+0.01,f=300/d2,d=Math.sqrt(d2);dx/=d;dy/=d;A.vx+=dx*f;A.vy+=dy*f;B.vx-=dx*f;B.vy-=dy*f;}
 elist().forEach(e=>{const A=P[e.a],B=P[e.b];let dx=B.x-A.x,dy=B.y-A.y,d=Math.sqrt(dx*dx+dy*dy)+0.01,f=(d-70)*0.02;dx/=d;dy/=d;A.vx+=dx*f;A.vy+=dy*f;B.vx-=dx*f;B.vy-=dy*f;});
 DATA.forEach(d=>{const p=P[d.id];if(p.pin)return;const ty=Yband(RI[d.rung]);p.vy+=(ty-p.y)*0.06;p.vx+=((W/2)-p.x)*0.002;p.vx*=0.82;p.vy*=0.82;p.x+=Math.max(-12,Math.min(12,p.vx));p.y+=Math.max(-12,Math.min(12,p.vy));p.x=Math.max(MT.l,Math.min(W-MT.r,p.x));p.y=Math.max(MT.t+4,Math.min(H-MT.b-4,p.y));});}
let dragId=null;
function renderTree(){
 size();if(!Object.keys(P).length)initForce();plot.innerHTML="";const h=(H-MT.t-MT.b)/RUNGS.length;
 RUNGS.forEach((r,i)=>{el("rect",{class:"rungband",x:0,y:MT.t+i*h,width:W,height:h},plot);el("text",{class:"runglab",x:6,y:MT.t+i*h+12},plot).textContent=RUNGS[RUNGS.length-1-i];});
 elist().forEach(e=>{const A=P[e.a],B=P[e.b];el("path",{class:"edge "+e.type,d:"M"+A.x+","+A.y+" Q "+((A.x+B.x)/2)+","+(((A.y+B.y)/2)-18)+" "+B.x+","+B.y},plot);});
 DATA.forEach(d=>{const p=P[d.id],sel=S.sel&&S.sel.id===d.id,nst=isNested(d),steps=((d.lineage||{}).evolution_steps||[]).length;
  if((S.spurs||sel)&&steps){for(let k=0;k<steps;k++){const a=k*0.7-((steps-1)*0.35);el("line",{class:"spur",x1:p.x,y1:p.y,x2:p.x+Math.cos(a-1.57)*(10+k*5),y2:p.y+Math.sin(a-1.57)*(10+k*5)},plot);}}
  const c=el("circle",{class:"node",cx:p.x,cy:p.y,r:sel?8:(3.5+Math.min(steps,6)*0.6),fill:COL.rung[RI[d.rung]],stroke:sel?"#fff":(nst?"#f0883e":"#0d1117"),"stroke-width":sel?1.6:(nst?1.1:.5)},plot);
  c.addEventListener("mousedown",ev=>{dragId=d.id;P[d.id].pin=true;ev.preventDefault();});c.addEventListener("click",()=>sel_(d));});
 document.getElementById("eqbox").style.display="none";legend();
}
plot.addEventListener("mousemove",ev=>{if(dragId&&S.view==="tree"){const r=plot.getBoundingClientRect();P[dragId].x=ev.clientX-r.left;P[dragId].y=ev.clientY-r.top;renderTree();}});
window.addEventListener("mouseup",()=>{dragId=null;});

// ---------- 3 OUTCOMES (observer frames) ----------
const STRUCT=["new-action-space","equilibrium","escalating-arms-race","ongoing-no-equilibrium","collapse-attacker","collapse-defender","n/a"];
function frameVal(d){const o=d.outcome||{};let f=S.frame;
 if(f==="third"){const t=(o.named_third_parties||[])[0];return t?t.valence:null;}
 let key=f==="ben"?"beneficiary":"target";
 if(S.flip&&o.symmetric)key=key==="beneficiary"?"target":"beneficiary";
 return (o.valence||{})[key];}
function renderOutcomes(){
 size();plot.innerHTML="";document.getElementById("eqbox").style.display="none";
 const cols=STRUCT.filter(s=>DATA.some(d=>(d.outcome||{}).structural===s));const cw=(W-20)/cols.length;
 cols.forEach((s,ci)=>{const x0=10+ci*cw,items=DATA.filter(d=>(d.outcome||{}).structural===s);
  el("rect",{x:x0,y:MT.t,width:cw-6,height:H-MT.t-6,fill:"#ffffff04",rx:6},plot);
  el("rect",{x:x0,y:MT.t,width:cw-6,height:20,fill:COL.struct[s],rx:6},plot);
  el("text",{x:x0+6,y:MT.t+14,style:"font-size:10.5px;font-weight:700;fill:#06101f"},plot).textContent=s+" ("+items.length+")";
  const per=Math.max(1,Math.floor((cw-16)/22));
  items.forEach((d,k)=>{const cx=x0+13+(k%per)*22,cy=MT.t+40+Math.floor(k/per)*22,sel=S.sel&&S.sel.id===d.id;
   const v=frameVal(d),fill=v?COL.val[v]:"#21262d";
   el("circle",{class:"node",cx:cx,cy:cy,r:sel?8:6,fill:fill,stroke:sel?"#fff":((d.outcome||{}).symmetric?"#58a6ff":"#0d1117"),"stroke-width":sel?1.6:((d.outcome||{}).symmetric?1.2:.6)},plot).addEventListener("click",()=>sel_(d));});
 });legend();
}

// ---------- 4 STRATOSPHERE ----------
function renderStrato(){
 size();plot.innerHTML="";document.getElementById("eqbox").style.display="none";
 const cx=W/2,cy=H/2,maxR=Math.min(W,H)/2-26;
 RUNGS.forEach((r,i)=>{const rad=maxR*(i+1)/RUNGS.length,hum=(r==="cognitive");
  el("circle",{cx:cx,cy:cy,r:rad,fill:"none",stroke:hum?"#d29922":"#30363d","stroke-width":hum?2:1,"stroke-opacity":hum?0.9:0.5},plot);
  el("text",{x:cx+4,y:cy-rad+12,style:"font-size:10px;font-weight:"+(hum?700:400)+";fill:"+(hum?"#d29922":"#8b949e")},plot).textContent=r+(hum?"  ← the human band":"");});
 DATA.forEach(d=>{const i=RI[d.rung],r0=maxR*i/RUNGS.length,r1=maxR*(i+1)/RUNGS.length,rad=r0+(r1-r0)*(0.35+(hash(d.id)%50)/100*0.5);
  let ang=(hash(d.id+"a")%360)*Math.PI/180;
  const tier=d.social_tier;if(tier){const TI=["pair","group","tribe","religion","government","civilisation"];const ti=TI.findIndex(t=>(tier||"").toLowerCase().includes(t));if(ti>=0)ang=(ti/TI.length)*2*Math.PI-1.57;}
  const x=cx+Math.cos(ang)*rad,y=cy+Math.sin(ang)*rad,sel=S.sel&&S.sel.id===d.id;
  el("circle",{class:"node",cx:x,cy:y,r:sel?7:(d.rung==="cognitive"?4.5:3.5),fill:COL.rung[i],stroke:sel?"#fff":(isNested(d)?"#f0883e":"#0d1117"),"stroke-width":sel?1.6:.5},plot).addEventListener("click",()=>sel_(d));});
 el("text",{x:cx,y:cy+3,style:"font-size:9px;fill:#6e7681;text-anchor:middle"},plot).textContent="core";
 legend();
}

// ---------- 5 KNOWLEDGE GRAPH ----------
let KP={},KN=[],KE=[];
function kbuild(){KN=[];KE=[];const cset={};
 function concept(id,label,kind){if(!cset[id]){cset[id]={id,label,kind,concept:true};KN.push(cset[id]);}return cset[id];}
 RUNGS.forEach(r=>concept("rung:"+r,r,"rung"));
 DATA.forEach(d=>{KN.push({id:d.id,label:d.name,concept:false,d:d});
  concept("rung:"+d.rung,d.rung,"rung");
  if(d.sub_primitive)concept("sub:"+d.sub_primitive,d.sub_primitive,"sub");
  if(d.deceivability_register)concept("reg:"+d.deceivability_register,d.deceivability_register,"reg");});
 DATA.forEach(d=>{KE.push({a:d.id,b:"rung:"+d.rung,kind:"rung"});
  if(d.sub_primitive)KE.push({a:d.id,b:"sub:"+d.sub_primitive,kind:"sub"});
  if(d.deceivability_register)KE.push({a:d.id,b:"reg:"+d.deceivability_register,kind:"reg"});});
 KP={};KN.forEach(n=>{KP[n.id]={x:W/2+(hash(n.id)%200-100),y:H/2+(hash(n.id+"y")%200-100),vx:0,vy:0,pin:false};});
 for(let t=0;t<240;t++)ktick();}
function kEdgesActive(){return KE.filter(e=>S.kedges[e.kind]);}
function ktick(){const ids=KN.map(n=>n.id);
 for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){const A=KP[ids[i]],B=KP[ids[j]];let dx=A.x-B.x,dy=A.y-B.y,d2=dx*dx+dy*dy+0.01,f=240/d2,d=Math.sqrt(d2);dx/=d;dy/=d;A.vx+=dx*f;A.vy+=dy*f;B.vx-=dx*f;B.vy-=dy*f;}
 kEdgesActive().forEach(e=>{const A=KP[e.a],B=KP[e.b];if(!A||!B)return;let dx=B.x-A.x,dy=B.y-A.y,d=Math.sqrt(dx*dx+dy*dy)+0.01,f=(d-60)*0.015;dx/=d;dy/=d;A.vx+=dx*f;A.vy+=dy*f;B.vx-=dx*f;B.vy-=dy*f;});
 KN.forEach(n=>{const p=KP[n.id];if(p.pin)return;p.vx+=((W/2)-p.x)*0.004;p.vy+=((H/2)-p.y)*0.004;p.vx*=0.8;p.vy*=0.8;p.x+=Math.max(-14,Math.min(14,p.vx));p.y+=Math.max(-14,Math.min(14,p.vy));p.x=Math.max(20,Math.min(W-20,p.x));p.y=Math.max(20,Math.min(H-20,p.y));});}
function renderKnow(){
 size();if(!KN.length)kbuild();plot.innerHTML="";document.getElementById("eqbox").style.display="none";
 const KCOL={rung:"#58a6ff",sub:"#f0883e",reg:"#a371f7"};
 kEdgesActive().forEach(e=>{const A=KP[e.a],B=KP[e.b];if(!A||!B)return;let on=!S.kfocus||S.kfocus===e.b||S.kfocus===e.a;el("line",{x1:A.x,y1:A.y,x2:B.x,y2:B.y,stroke:"#30363d","stroke-width":.5,"stroke-opacity":on?.5:.05},plot);});
 KN.forEach(n=>{const p=KP[n.id];
  if(n.concept){el("circle",{class:"node",cx:p.x,cy:p.y,r:8,fill:KCOL[n.kind],stroke:"#0d1117","stroke-width":1},plot).addEventListener("click",()=>{S.kfocus=(S.kfocus===n.id?null:n.id);renderKnow();});
   el("text",{x:p.x+10,y:p.y+3,style:"font-size:10px;fill:#e6edf3"},plot).textContent=n.label;}
  else{let on=!S.kfocus||kEdgesActive().some(e=>e.a===n.id&&e.b===S.kfocus);const sel=S.sel&&S.sel.id===n.id;
   el("circle",{class:"node",cx:p.x,cy:p.y,r:sel?6:3,fill:COL.rung[RI[n.d.rung]],"fill-opacity":on?.95:.12,stroke:sel?"#fff":"none","stroke-width":sel?1.4:0},plot).addEventListener("click",()=>sel_(n.d));}});
 legend();
}

// ---------- 6 RADAR ----------
function rungStats(){const g={};RUNGS.forEach(r=>g[r]=[]);DATA.forEach(d=>{if(g[d.rung])g[d.rung].push(d);});
 const ax=[["det-lag","detection lag"],["counters","counter-measures"],["conn","lineage conn."],["nested","nested-pawn"],["latent","latent"],["exist","existence reg."],["sym","symmetric"]];
 const raw={};RUNGS.forEach(r=>{const es=g[r];if(!es.length){raw[r]=null;return;}
  const lag=es.filter(d=>d.t_phenom_ybp>0&&d.t_obs_ybp>0).map(d=>Math.log10(d.t_phenom_ybp+1)-Math.log10(d.t_obs_ybp+1));
  raw[r]={"det-lag":mean(lag),"counters":mean(es.map(d=>(d.counter_measures||[]).length)),"conn":mean(es.map(d=>(d.lineage_edges||[]).length)),
   "nested":frac(es,d=>isNested(d)),"latent":frac(es,d=>d.latent_or_physical==="latent"),"exist":frac(es,d=>d.deceivability_register==="existence"),"sym":frac(es,d=>(d.outcome||{}).symmetric)};});
 ax.forEach(([k])=>{const mx=Math.max.apply(null,RUNGS.map(r=>raw[r]?Math.abs(raw[r][k]):0).concat([1e-9]));RUNGS.forEach(r=>{if(raw[r])raw[r][k]=raw[r][k]/mx;});});
 return {raw,ax};}
function renderRadar(){
 size();plot.innerHTML="";document.getElementById("eqbox").style.display="none";
 const {raw,ax}=rungStats(),cx=W/2,cy=H/2,R=Math.min(W,H)/2-60,n=ax.length;
 [0.25,0.5,0.75,1].forEach(g=>{let dd="";for(let i=0;i<=n;i++){const a=(i%n)/n*2*Math.PI-1.57,x=cx+Math.cos(a)*R*g,y=cy+Math.sin(a)*R*g;dd+=(i?"L":"M")+x+","+y+" ";}el("path",{d:dd,fill:"none",stroke:"#30363d","stroke-width":.5},plot);});
 ax.forEach(([k,lab],i)=>{const a=i/n*2*Math.PI-1.57,x=cx+Math.cos(a)*R,y=cy+Math.sin(a)*R;el("line",{x1:cx,y1:cy,x2:x,y2:y,stroke:"#30363d","stroke-width":.5},plot);
  el("text",{x:cx+Math.cos(a)*(R+12),y:cy+Math.sin(a)*(R+12),style:"font-size:10px;fill:#8b949e;text-anchor:middle"},plot).textContent=lab;});
 RUNGS.forEach((r)=>{if(!S.radarOn[r]||!raw[r])return;const c=COL.rung[RI[r]];let dd="";
  ax.forEach(([k],i)=>{const val=Math.max(0,Math.min(1,raw[r][k])),a=i/n*2*Math.PI-1.57,x=cx+Math.cos(a)*R*val,y=cy+Math.sin(a)*R*val;dd+=(i?"L":"M")+x+","+y+" ";});dd+="Z";
  el("path",{d:dd,fill:c,"fill-opacity":.12,stroke:c,"stroke-width":1.6},plot);});
 legend();
}

// ---------- shared ----------
function legend(){const L=document.getElementById("legend");L.innerHTML="";let m=null,title="";
 if(S.view==="outcomes"){m=COL.val;title="valence ("+(S.frame==="ben"?"beneficiary":S.frame==="tar"?"target":"third-party")+"): ";}
 else if(S.view==="timeline"&&S.ov==="latent")m=COL.latent;
 else if(S.view==="timeline"&&S.ov==="register")m=COL.reg;
 else if(S.view==="timeline"&&S.ov==="structural")m=COL.struct;
 if(m){if(title){const t=document.createElement("span");t.textContent=title;t.style.color="#8b949e";L.appendChild(t);}for(const k in m){const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+m[k]+'"></span>'+k;L.appendChild(s);}}
 else{RUNGS.forEach((r,i)=>{const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+COL.rung[i]+'"></span>'+r;L.appendChild(s);});}
 if(S.view==="tree"){const e=document.createElement("span");e.innerHTML='&nbsp; <span style="color:#6e7681">—evolved</span> <span style="color:#f0883e">--transposed</span> <span style="color:#a371f7">··latent-transp</span>';L.appendChild(e);}
 if(S.view==="know"){const e=document.createElement("span");e.innerHTML='&nbsp; concepts: <span style="color:#58a6ff">●rung</span> <span style="color:#f0883e">●sub-primitive</span> <span style="color:#a371f7">●register</span>';L.appendChild(e);}
}
function chainHTML(ch){if(!ch)return"";const p=(""+ch).split(/\s*(?:->|→|⇒)\s*/).filter(x=>x.trim());if(p.length<2)return '<div class="lvl">'+esc(ch)+'</div>';return '<div class="chain">'+p.map((x,i)=>'<div class="lvl">'+(i?'<span class="ar">▼ </span>':'')+esc(x)+'</div>').join("")+'</div>';}
function vchip(v){return v?'<span class="vbadge" style="background:'+(COL.val[v]||"#888")+'">'+v+'</span>':'<span class="k">n/a</span>';}
function detail(d){const D=document.getElementById("detail"),o=d.outcome||{},val=o.valence||{},fn=o.frame_notes||{},np=d.nested_pawn||{},li=d.lineage||{},tp=d.t_phenomenon||{},to=d.t_observed||{};
 const tps=(o.named_third_parties||[]).map(t=>'<div class="tp"><b>'+esc(t.observer)+'</b> '+vchip(t.valence)+'<br><span class="k">rel. to:</span> '+esc(t.relative_to)+(t.note?'<br>'+esc(t.note):'')+'</div>').join("");
 const cm=(d.counter_measures||[]).map(c=>'<div class="cm"><b>'+esc(c.name)+'</b> <span class="k">'+esc(c.approx_time)+'</span><br>'+esc(c.note)+'</div>').join("");
 const ev=(li.evolution_steps||[]);
 D.innerHTML='<div style="font-weight:700;font-size:14px">'+esc(d.name)+'</div>'+
 '<div class="row"><span class="pill">'+esc(d.rung)+'</span><span class="pill">'+esc(d.sub_primitive)+'</span><span class="pill">'+esc(d.latent_or_physical)+'</span><span class="pill">reg:'+esc(d.deceivability_register)+'</span>'+(d.social_tier?'<span class="pill">tier:'+esc(d.social_tier)+'</span>':'')+'</div>'+
 '<div class="row"><span class="k">operated:</span> '+esc(tp.label||d.t_label||"?")+(tp.fuzzy?' <span class="pill">fuzzy</span>':'')+' &nbsp; <span class="k">named:</span> '+esc(to.label||"?")+(to.fuzzy?' <span class="pill">fuzzy</span>':'')+'</div>'+
 '<div class="row"><b>outcome:</b> <span class="pill" style="border-color:'+(COL.struct[o.structural]||"#888")+'">'+esc(o.structural)+'</span>'+(o.symmetric?' <span class="pill" style="border-color:#58a6ff">symmetric</span>':'')+'</div>'+
 '<div class="row"><span class="k">beneficiary</span> '+vchip(val.beneficiary)+' — '+esc(fn.beneficiary)+'</div>'+
 '<div class="row"><span class="k">target</span> '+vchip(val.target)+' — '+esc(fn.target)+'</div>'+
 (tps?'<div class="row"><b>named third parties:</b>'+tps+'</div>':'')+
 (np.is_nested?'<div class="row"><b style="color:#f0883e">nested pawn:</b>'+chainHTML(np.chain)+'</div>':'')+
 '<div class="row"><span class="k">beneficiary →</span> '+esc(d.beneficiary)+'</div><div class="row"><span class="k">target →</span> '+esc(d.target)+'</div>'+
 '<div class="row"><span class="k">externalized cost →</span> '+esc(d.externalized_cost)+'</div>'+
 (cm?'<div class="row"><b style="color:#3fb950">counter-measures:</b>'+cm+'</div>':'')+
 (ev.length?'<div class="row"><b style="color:#d29922">how it evolved:</b>'+chainHTML(ev.join(" → "))+'</div>':'')+
 ((li.evolved_from||li.transposed_from||(li.related||[]).length)?'<div class="row"><b>lineage:</b>'+(li.evolved_from?'<div>evolved from: '+esc(li.evolved_from)+'</div>':'')+(li.transposed_from?'<div style="color:#f0883e">transposed from: '+esc(li.transposed_from)+'</div>':'')+((li.related||[]).length?'<div class="k">related: '+esc((li.related||[]).join("; ").slice(0,400))+'</div>':'')+'</div>':'')+
 '<div class="row"><span class="k">C0.2 →</span> '+esc(d.beneficiary_boundary_check)+'</div>'+
 '<div class="row cite"><span class="k">sources →</span> '+esc(d.citation)+(d.enrich_citation?' · '+esc(d.enrich_citation):'')+'</div>';
}
function density(y){return 1/(1+Math.exp(-(S.kd/100)*(y-EQ.density_mid)));}
function cost(y){return EQ.cost_floor+(1-EQ.cost_floor)*Math.exp(-(S.kc/100)*(y-EQ.year_min));}
function rate(y){return density(y)/Math.max(cost(y),0.02);}
function renderRate(){const s=document.getElementById("rate");s.innerHTML="";const w=s.clientWidth||600,h=104,m={l:30,r:8,t:6,b:14};const ys=[];for(let y=EQ.year_min;y<=EQ.year_max;y++)ys.push(y);const mx=Math.max.apply(null,ys.map(rate));const X=y=>m.l+(y-EQ.year_min)/(EQ.year_max-EQ.year_min)*(w-m.l-m.r),Y=v=>h-m.b-(v/mx)*(h-m.t-m.b);
 el("line",{class:"axis",x1:m.l,y1:h-m.b,x2:w-m.r,y2:h-m.b},s);[1990,2005,2013,2026].forEach(y=>el("text",{class:"axt",x:X(y)-10,y:h-2},s).textContent=y);
 el("path",{d:"M"+ys.map(y=>X(y)+","+Y(rate(y))).join(" L"),fill:"none",stroke:"#58a6ff","stroke-width":2},s);
 if(S.rq)el("path",{d:"M"+ys.map(y=>X(y)+","+Y(rate(y)*(1+0.1*Math.sin((y-EQ.year_min)*1.3)))).join(" L"),fill:"none",stroke:"#db61a2","stroke-width":1,"stroke-dasharray":"3 2"},s);
 DATA.filter(d=>d.t_year&&d.t_year>=EQ.year_min&&d.rung==="latent-algorithmic").forEach(d=>el("circle",{cx:X(d.t_year),cy:Y(rate(d.t_year)),r:3,fill:"#f0883e",stroke:"#0d1117"},s).addEventListener("click",()=>sel_(d)));}
function route(){if(S.view==="timeline")renderTimeline();else if(S.view==="tree")renderTree();else if(S.view==="outcomes")renderOutcomes();else if(S.view==="strato")renderStrato();else if(S.view==="know")renderKnow();else renderRadar();}

// wiring
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));b.classList.add("on");S.view=b.dataset.v;
 document.querySelectorAll(".grp").forEach(g=>g.classList.remove("on"));document.getElementById("g-"+S.view).classList.add("on");route();if(S.view==="timeline")renderRate();}));
document.getElementById("tm-phenom").addEventListener("click",function(){S.tmode="phenom";S.lag=false;this.classList.add("on");document.getElementById("tm-obs").classList.remove("on");document.getElementById("tm-lag").classList.remove("on");renderTimeline();});
document.getElementById("tm-obs").addEventListener("click",function(){S.tmode="obs";S.lag=false;this.classList.add("on");document.getElementById("tm-phenom").classList.remove("on");document.getElementById("tm-lag").classList.remove("on");renderTimeline();});
document.getElementById("tm-lag").addEventListener("click",function(){S.lag=!S.lag;this.classList.toggle("on",S.lag);renderTimeline();});
document.querySelectorAll(".ov").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".ov").forEach(x=>x.classList.remove("on"));b.classList.add("on");S.ov=b.dataset.ov;renderTimeline();}));
document.getElementById("f-nested").addEventListener("click",function(){S.nested=!S.nested;this.classList.toggle("on",S.nested);renderTimeline();});
const sc=document.getElementById("scrub");sc.addEventListener("input",()=>{S.scrub=+sc.value;renderTimeline();});
let tmr=null;document.getElementById("play").addEventListener("click",function(){if(tmr){clearInterval(tmr);tmr=null;this.textContent="▶";return;}this.textContent="⏸";if(S.scrub>=1000)S.scrub=0;tmr=setInterval(()=>{S.scrub+=8;if(S.scrub>=1000){S.scrub=1000;clearInterval(tmr);tmr=null;document.getElementById("play").textContent="▶";}sc.value=S.scrub;renderTimeline();},60);});
["evolved","transposed","latent-transposition","related"].forEach(t=>document.getElementById("e-"+t).addEventListener("click",function(){S.edges[t]=!S.edges[t];this.classList.toggle("on",S.edges[t]);renderTree();}));
document.getElementById("spurs").addEventListener("click",function(){S.spurs=!S.spurs;this.textContent="evolution spurs: "+(S.spurs?"on":"off");this.classList.toggle("on",S.spurs);renderTree();});
document.getElementById("fr-ben").addEventListener("click",function(){S.frame="ben";document.querySelectorAll("#g-outcomes .on").forEach(x=>{if(x.id.startsWith("fr-"))x.classList.remove("on")});this.classList.add("on");renderOutcomes();});
document.getElementById("fr-tar").addEventListener("click",function(){S.frame="tar";document.querySelectorAll("#g-outcomes button").forEach(x=>{if(x.id.startsWith("fr-"))x.classList.remove("on")});this.classList.add("on");renderOutcomes();});
document.getElementById("fr-third").addEventListener("click",function(){S.frame="third";document.querySelectorAll("#g-outcomes button").forEach(x=>{if(x.id.startsWith("fr-"))x.classList.remove("on")});this.classList.add("on");renderOutcomes();});
document.getElementById("flip").addEventListener("click",function(){S.flip=!S.flip;this.classList.toggle("on",S.flip);renderOutcomes();});
document.getElementById("k-rung").addEventListener("click",function(){S.kedges.rung=!S.kedges.rung;this.classList.toggle("on",S.kedges.rung);renderKnow();});
document.getElementById("k-sub").addEventListener("click",function(){S.kedges.sub=!S.kedges.sub;this.classList.toggle("on",S.kedges.sub);renderKnow();});
document.getElementById("k-reg").addEventListener("click",function(){S.kedges.reg=!S.kedges.reg;this.classList.toggle("on",S.kedges.reg);renderKnow();});
const rt=document.getElementById("radar-toggles");RUNGS.forEach(r=>{const b=document.createElement("button");b.textContent=r;if(S.radarOn[r])b.classList.add("on");b.style.borderColor=COL.rung[RI[r]];b.addEventListener("click",()=>{S.radarOn[r]=!S.radarOn[r];b.classList.toggle("on",S.radarOn[r]);renderRadar();});rt.appendChild(b);});
document.getElementById("kd").addEventListener("input",function(){S.kd=+this.value;renderRate();});
document.getElementById("kc").addEventListener("input",function(){S.kc=+this.value;renderRate();});
document.getElementById("rq").addEventListener("click",function(){S.rq=!S.rq;this.textContent="Red-Queen: "+(S.rq?"on":"off");renderRate();});
window.addEventListener("resize",()=>{route();if(S.view==="timeline")renderRate();});
route();renderRate();
</script></body></html>"""

html = TEMPLATE.replace("/*DATA*/", data_js).replace("/*EQ*/", eq_js).replace("{N}", str(len(rows)))
open(os.path.join(HERE, "adversarial_atlas.html"), "w", encoding="utf-8").write(html)
print("wrote adversarial_atlas.html (", len(html), "chars,", len(rows), "examples )")
