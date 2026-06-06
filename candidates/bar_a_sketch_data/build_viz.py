#!/usr/bin/env python3
"""Procedural build for the Adversarial-Function Atlas.

Reads adversarial_examples_dataset.json and emits a self-contained interactive
HTML (data inlined; opens offline). Re-run after editing the dataset OR the
dynamic-equation defaults below to regenerate.

  python build_viz.py
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "adversarial_examples_dataset.json")
OUT = os.path.join(HERE, "adversarial_atlas.html")

rows = json.loads(open(DATA, encoding="utf-8").read())
data_js = json.dumps(rows, ensure_ascii=False)

# Dynamic-equation defaults (C1.3: rate of W_C formation ~= density(t) x catalysis(t)).
# Editable here; the page also exposes them as live sliders.
EQ = {
    "density_k": 0.18,      # logistic growth rate of observer density (per year)
    "density_mid": 2005,    # inflection year of internet adoption
    "cost_k": 0.16,         # exponential decay rate of cost-to-attempt (catalysis)
    "cost_floor": 0.03,     # asymptotic marginal cost (~0)
    "year_min": 1990,
    "year_max": 2026,
}
eq_js = json.dumps(EQ)

TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adversarial-Function Atlas (Stage-1 sketch)</title>
<style>
  :root{--bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--mut:#8b949e;--line:#30363d;--acc:#58a6ff;}
  *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}
  header{padding:10px 14px;border-bottom:1px solid var(--line)} h1{font-size:15px;margin:0 0 2px} .sub{color:var(--mut);font-size:11px}
  .wrap{display:flex;gap:0;height:calc(100vh - 58px)} .left{flex:1;min-width:0;display:flex;flex-direction:column}
  .right{width:340px;border-left:1px solid var(--line);overflow:auto;padding:10px 12px}
  .bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line)}
  .bar label{color:var(--mut)} button,select{background:#21262d;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 8px;cursor:pointer;font-size:12px}
  button.on{background:var(--acc);color:#06101f;border-color:var(--acc);font-weight:600}
  input[type=range]{vertical-align:middle} #plot{flex:1;width:100%}
  .node{cursor:pointer;stroke:#0d1117;stroke-width:.6}
  .rungband{fill:#ffffff03} .rungband:nth-child(even){fill:#ffffff06}
  .axis{stroke:var(--line)} .axt{fill:var(--mut);font-size:10px} .runglab{fill:var(--mut);font-size:10px}
  .playhead{stroke:var(--acc);stroke-width:1.5;stroke-dasharray:4 3}
  .edge{stroke:#f0883e;stroke-width:1.3;fill:none;marker-end:url(#arr)}
  .chain{display:flex;flex-direction:column;gap:4px;margin:6px 0}
  .lvl{background:#21262d;border:1px solid var(--line);border-left:3px solid #f0883e;border-radius:5px;padding:5px 7px;font-size:12px}
  .lvl .ar{color:#f0883e;font-weight:700}
  .k{color:var(--mut)} .v{color:var(--ink)} .row{margin:3px 0}
  .pill{display:inline-block;padding:1px 6px;border-radius:10px;font-size:10px;border:1px solid var(--line);margin-right:4px}
  .leg{display:flex;flex-wrap:wrap;gap:8px;font-size:10px;color:var(--mut);padding:4px 12px;border-bottom:1px solid var(--line)}
  .sw{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:3px;vertical-align:middle}
  #rate{width:100%;height:120px} .eqbox{padding:8px 12px;border-top:1px solid var(--line)} .eqbox .g{display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:11px;color:var(--mut)}
  .muted{color:var(--mut)} .cite{font-size:11px;color:var(--mut);word-break:break-word} a{color:var(--acc)}
</style></head>
<body>
<header>
  <h1>Adversarial-Function Atlas <span class="sub">— Stage-1 sketch · {N} documented examples · viroid → cosmic + latent · Tier-3 exploratory, not canon</span></h1>
  <div class="sub">Time scrubber sweeps deep-time → present; the function climbs the rungs. Click a node for detail + the nested-pawn chain. Colour overlay + filters below.</div>
</header>
<div class="bar">
  <label>scrub time:</label><input id="scrub" type="range" min="0" max="1000" value="1000" style="width:240px">
  <span id="scrublab" class="muted"></span>
  <button id="play">▶ play</button>
  <span style="width:14px"></span>
  <label>colour:</label>
  <button class="ov on" data-ov="rung">rung</button>
  <button class="ov" data-ov="latent">latent/physical</button>
  <button class="ov" data-ov="register">register</button>
  <button class="ov" data-ov="conf">confidence</button>
  <span style="width:14px"></span>
  <label>filter:</label>
  <button id="f-nested">nested-pawn only</button>
  <button id="f-neutral">neutral (fails C0.2)</button>
  <button id="reset">reset</button>
</div>
<div class="leg" id="legend"></div>
<div class="wrap">
  <div class="left">
    <svg id="plot"></svg>
    <div class="eqbox">
      <div class="g"><b style="color:var(--ink)">Underlying dynamic (C1.3):</b> rate of W_C-formation ≈ density(t) × catalysis(t) — the internet-era backdrop.
        density-growth k<input id="kd" type="range" min="5" max="40" value="18" style="width:80px"> ·
        cost-drop k<input id="kc" type="range" min="5" max="40" value="16" style="width:80px"> ·
        <button id="rq">Red-Queen cycling: off</button></div>
      <svg id="rate"></svg>
    </div>
  </div>
  <div class="right" id="detail"><div class="muted">Click any node for its full classification, the beneficiary→target edge, and (where present) the "thinks-they-gain → actually-instrument-to" chain.</div></div>
</div>
<svg width="0" height="0"><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#f0883e"/></marker></defs></svg>
<script>
const DATA = /*DATA*/;
const EQ = /*EQ*/;
const RUNGS = ["molecular","cellular","organismal","cognitive","social-institutional","latent-algorithmic","cosmic"];
const RUNG_I = Object.fromEntries(RUNGS.map((r,i)=>[r,i]));
const COL = {
  latent:{latent:"#a371f7",physical:"#3fb950",both:"#58a6ff"},
  register:{fact:"#58a6ff",time:"#f0883e",sequence:"#db61a2",none:"#6e7681"},
  conf:{"web-verified":"#3fb950","training-knowledge":"#d29922","speculative":"#8b949e"},
  rung:["#6e7681","#79c0ff","#3fb950","#d29922","#f0883e","#db61a2","#a371f7"]
};
const NS="http://www.w3.org/2000/svg";
let state={ov:"rung",nested:false,neutral:false,scrub:1000,rq:false,kd:18,kc:16,sel:null};

// time axis: u = log10(ybp+1); present (small ybp) at RIGHT
const UMAX = Math.max.apply(null, DATA.map(d=>Math.log10((d.t_ybp||1)+1)));
function ux(d){return Math.log10((d.t_ybp||1)+1);}
const plot=document.getElementById("plot");
let W=0,H=0,M={l:120,r:18,t:14,b:28};
function size(){W=plot.clientWidth;H=plot.clientHeight;}

function X(u){return M.l + (1 - u/UMAX)*(W-M.l-M.r);}      // present right, deep-time left
function Yband(i){const h=(H-M.t-M.b)/RUNGS.length;return M.t + (RUNGS.length-1-i)*h + h/2;} // molecular bottom, cosmic top
function colour(d){
  if(state.ov==="rung")return COL.rung[RUNG_I[d.rung]]||"#888";
  if(state.ov==="latent")return COL.latent[d.latent_or_physical]||"#888";
  if(state.ov==="register")return COL.register[d.deceivability_register]||"#888";
  if(state.ov==="conf")return COL.conf[d.confidence]||"#888";
  return "#888";
}
function isNeutral(d){return (d.beneficiary_boundary_check||"").toUpperCase().includes("NEUTRAL");}
function visible(d){
  if(state.nested && !(d.nested_pawn&&d.nested_pawn.is_nested))return false;
  if(state.neutral && !isNeutral(d))return false;
  return true;
}
function scrubU(){ // slider 0..1000 -> u threshold (1000=present shows all)
  return UMAX*(1 - state.scrub/1000);
}
function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;}

// jitter so same (rung,time) nodes don't fully overlap (deterministic by id hash)
function hash(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return h;}
function render(){
  size(); plot.innerHTML="";
  const h=(H-M.t-M.b)/RUNGS.length;
  RUNGS.forEach((r,i)=>{
    el("rect",{class:"rungband",x:0,y:M.t+i*h,width:W,height:h},plot);
    el("text",{class:"runglab",x:6,y:M.t+i*h+h/2+3},plot).textContent=RUNGS[RUNGS.length-1-i];
  });
  // x ticks (representative times)
  const ticks=[[3.5e9,"3.5 Gya"],[5.4e8,"Cambrian"],[1e6,"1 Mya"],[1e3,"1000 ya"],[120,"1900s"],[20,"2000s"]];
  ticks.forEach(([y,lab])=>{const x=X(Math.log10(y+1));el("line",{class:"axis",x1:x,y1:M.t,x2:x,y2:H-M.b},plot);el("text",{class:"axt",x:x+2,y:H-M.b+12},plot).textContent=lab;});
  // playhead
  const px=X(scrubU());el("line",{class:"playhead",x1:px,y1:M.t,x2:px,y2:H-M.b},plot);
  // edge layer (drawn under nodes when a node is selected)
  if(state.sel){const d=state.sel;const x=X(ux(d)),y=Yband(RUNG_I[d.rung])+ (hash(d.id)%18-9);
    const tx=Math.min(W-M.r-4,x+70);el("path",{class:"edge",d:`M${x},${y} C ${x+40},${y-26} ${tx-30},${y-26} ${tx},${y-26}`},plot);
    el("text",{class:"axt",x:tx,y:y-30,"text-anchor":"end"},plot).textContent="→ target: "+(d.target||"").slice(0,46);}
  // nodes
  DATA.forEach(d=>{
    if(!visible(d))return;
    const u=ux(d),x=X(u),y=Yband(RUNG_I[d.rung])+(hash(d.id)%18-9);
    const revealed = u >= scrubU()-1e-9;          // left of / at playhead
    const sel = state.sel && state.sel.id===d.id;
    const nested = d.nested_pawn && d.nested_pawn.is_nested;
    const c=el("circle",{class:"node",cx:x,cy:y,r:sel?7:(nested?5.2:4),fill:colour(d),
      "fill-opacity":revealed?0.92:0.07,"stroke":sel?"#fff":(nested?"#f0883e":"#0d1117"),"stroke-width":sel?1.6:(nested?1.1:0.6)},plot);
    c.addEventListener("click",()=>{state.sel=d;render();detail(d);});
    c.addEventListener("mouseenter",()=>{c.setAttribute("r",sel?7:6);});
    c.addEventListener("mouseleave",()=>{c.setAttribute("r",sel?7:(nested?5.2:4));});
  });
  document.getElementById("scrublab").textContent = state.scrub>=1000?"all of time":("revealing to ≈ "+fmtYbp(scrubU()));
  legend();
}
function fmtYbp(u){const y=Math.pow(10,u)-1;if(y>1e8)return (y/1e9).toFixed(1)+" Gya";if(y>1e5)return (y/1e6).toFixed(0)+" Mya";if(y>500)return Math.round(2026-y)>0?(2026-Math.round(y)):"";if(y<60)return (2026-Math.round(y))+"";return Math.round(y)+" ya";}
function legend(){
  const L=document.getElementById("legend");L.innerHTML="";
  let m={};
  if(state.ov==="rung")m=Object.fromEntries(RUNGS.map((r,i)=>[r,COL.rung[i]]));
  else if(state.ov==="latent")m=COL.latent; else if(state.ov==="register")m=COL.register; else m=COL.conf;
  for(const k in m){const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+m[k]+'"></span>'+k;L.appendChild(s);}
  const n=document.createElement("span");n.innerHTML='<span class="sw" style="background:#0d1117;border:1px solid #f0883e"></span>nested-pawn (orange ring)';L.appendChild(n);
}
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function chainHTML(ch){
  if(!ch)return"";
  const parts=ch.split(/\s*(?:->|→|⇒)\s*/).filter(x=>x.trim());
  if(parts.length<2)return '<div class="lvl">'+esc(ch)+'</div>';
  return '<div class="chain">'+parts.map((p,i)=>'<div class="lvl">'+(i?'<span class="ar">▼ </span>':'')+esc(p)+'</div>').join("")+'</div>';
}
function detail(d){
  const D=document.getElementById("detail");
  const np=d.nested_pawn||{};
  D.innerHTML =
   '<div style="font-weight:700;font-size:14px">'+esc(d.name)+'</div>'+
   '<div class="row"><span class="pill">'+esc(d.rung)+'</span><span class="pill">'+esc(d.sub_primitive)+'</span>'+
     '<span class="pill">'+esc(d.latent_or_physical)+'</span><span class="pill">reg: '+esc(d.deceivability_register)+'</span>'+
     '<span class="pill">'+esc(d.t_label||"")+'</span><span class="pill">'+esc(d.confidence)+'</span></div>'+
   (np.is_nested?'<div class="row"><b style="color:#f0883e">Nested pawn — duped up the chain:</b>'+chainHTML(np.chain)+'</div>':"")+
   '<div class="row"><span class="k">beneficiary →</span> <span class="v">'+esc(d.beneficiary)+'</span></div>'+
   '<div class="row"><span class="k">target →</span> <span class="v">'+esc(d.target)+'</span></div>'+
   '<div class="row"><span class="k">externalized cost →</span> <span class="v">'+esc(d.externalized_cost)+'</span></div>'+
   (d.indirect_actors&&d.indirect_actors.toLowerCase()!=="none"?'<div class="row"><span class="k">indirect actors (adjacent planes) →</span> <span class="v">'+esc(d.indirect_actors)+'</span></div>':"")+
   '<div class="row"><span class="k">C0.2 →</span> <span class="v">'+esc(d.beneficiary_boundary_check)+'</span></div>'+
   '<div class="row cite"><span class="k">source →</span> '+esc(d.citation)+'</div>';
}

// ---- dynamic-equation inset (C1.3 concentration x catalysis) ----
function density(yr){const k=state.kd/100;return 1/(1+Math.exp(-k*(yr-EQ.density_mid)));}
function catalysis(yr){const k=state.kc/100;return EQ.cost_floor + (1-EQ.cost_floor)*Math.exp(-k*(yr-EQ.year_min));} // cost(t)
function rate(yr){return density(yr)/Math.max(catalysis(yr),0.02);} // density / cost
function renderRate(){
  const s=document.getElementById("rate");s.innerHTML="";const w=s.clientWidth||600,h=120,m={l:34,r:8,t:8,b:16};
  const ys=[];for(let y=EQ.year_min;y<=EQ.year_max;y++)ys.push(y);
  const vals=ys.map(rate);const mx=Math.max.apply(null,vals);
  const X=y=>m.l+(y-EQ.year_min)/(EQ.year_max-EQ.year_min)*(w-m.l-m.r);
  const Y=v=>h-m.b-(v/mx)*(h-m.t-m.b);
  el("line",{class:"axis",x1:m.l,y1:h-m.b,x2:w-m.r,y2:h-m.b},s);
  el("text",{class:"axt",x:2,y:h-m.b},s).textContent="rate";
  [EQ.year_min,2000,2013,EQ.year_max].forEach(y=>el("text",{class:"axt",x:X(y)-12,y:h-3},s).textContent=y);
  let path="M"+ys.map(y=>X(y)+","+Y(rate(y))).join(" L");
  el("path",{d:path,fill:"none",stroke:"#58a6ff","stroke-width":2},s);
  if(state.rq){ // Red-Queen cycling overlay (perpetual, non-accelerating jitter on the rate)
    let rqp="M"+ys.map(y=>X(y)+","+Y(rate(y)*(1+0.10*Math.sin((y-EQ.year_min)*1.3)))).join(" L");
    el("path",{d:rqp,fill:"none",stroke:"#db61a2","stroke-width":1,"stroke-dasharray":"3 2"},s);
  }
  // plot latent-algorithmic examples on the curve at their year
  DATA.filter(d=>d.t_year&&d.t_year>=EQ.year_min&&d.rung==="latent-algorithmic").forEach(d=>{
    el("circle",{cx:X(d.t_year),cy:Y(rate(d.t_year)),r:3,fill:"#f0883e","stroke":"#0d1117"},s).addEventListener("click",()=>{state.sel=d;render();detail(d);});
  });
}

// ---- wiring ----
document.querySelectorAll(".ov").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".ov").forEach(x=>x.classList.remove("on"));b.classList.add("on");state.ov=b.dataset.ov;render();}));
document.getElementById("f-nested").addEventListener("click",function(){state.nested=!state.nested;this.classList.toggle("on",state.nested);render();});
document.getElementById("f-neutral").addEventListener("click",function(){state.neutral=!state.neutral;this.classList.toggle("on",state.neutral);render();});
document.getElementById("reset").addEventListener("click",()=>{state={ov:"rung",nested:false,neutral:false,scrub:1000,rq:false,kd:18,kc:16,sel:null};document.querySelectorAll(".ov").forEach(x=>x.classList.toggle("on",x.dataset.ov==="rung"));document.getElementById("f-nested").classList.remove("on");document.getElementById("f-neutral").classList.remove("on");document.getElementById("scrub").value=1000;document.getElementById("detail").innerHTML='<div class="muted">Click any node…</div>';render();renderRate();});
const sc=document.getElementById("scrub");sc.addEventListener("input",()=>{state.scrub=+sc.value;render();});
let timer=null;document.getElementById("play").addEventListener("click",function(){
  if(timer){clearInterval(timer);timer=null;this.textContent="▶ play";return;}
  this.textContent="⏸ pause";if(state.scrub>=1000)state.scrub=0;
  timer=setInterval(()=>{state.scrub+=8;if(state.scrub>=1000){state.scrub=1000;clearInterval(timer);timer=null;document.getElementById("play").textContent="▶ play";}sc.value=state.scrub;render();},60);
});
document.getElementById("kd").addEventListener("input",function(){state.kd=+this.value;renderRate();});
document.getElementById("kc").addEventListener("input",function(){state.kc=+this.value;renderRate();});
document.getElementById("rq").addEventListener("click",function(){state.rq=!state.rq;this.textContent="Red-Queen cycling: "+(state.rq?"on":"off");renderRate();});
window.addEventListener("resize",()=>{render();renderRate();});
render();renderRate();
</script></body></html>"""

html = (TEMPLATE
        .replace("/*DATA*/", data_js)
        .replace("/*EQ*/", eq_js)
        .replace("{N}", str(len(rows))))
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, "(", len(html), "chars,", len(rows), "examples )")
