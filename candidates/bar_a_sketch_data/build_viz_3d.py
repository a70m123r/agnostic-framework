#!/usr/bin/env python3
"""3D explorer for the Adversarial-Function Atlas.

Objective (Pav): compress the data by putting THREE framework axes on X/Y/Z
structurally, in one rotatable object. Self-contained canvas (no CDN, opens offline).
Four layouts, each with three meaningful axes:
  cube    : X=scale/rung (C2)  Y=time (C1)  Z=deceivability register (C2.2)
  valence : X=beneficiary  Y=target  Z=third-party  (the observer-agnostic octants)
  horn    : angle=rung  height=time  radius=detection-lag  (the lag-collapse cone)
  kind    : X=deceivability  Y=symmetry  Z=structural-outcome  (the move phase-space)
Drag = rotate, wheel = zoom, click = pick. Re-run after editing the dataset.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.loads(open(os.path.join(HERE, "adversarial_examples_dataset.json"), encoding="utf-8").read())
data_js = json.dumps(rows, ensure_ascii=False)

TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adversarial-Function Atlas — 3D</title>
<style>
 :root{--bg:#0d1117;--ink:#e6edf3;--mut:#8b949e;--line:#30363d;--acc:#58a6ff;}
 *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 -apple-system,Segoe UI,Roboto,sans-serif;overflow:hidden}
 header{padding:8px 14px;border-bottom:1px solid var(--line)}h1{font-size:15px;margin:0}.sub{color:var(--mut);font-size:11px}
 .bar{display:flex;gap:8px;align-items:center;padding:7px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
 .bar label{color:var(--mut)} button,select{background:#21262d;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 8px;cursor:pointer;font-size:12px}
 button.on{background:var(--acc);color:#06101f;border-color:var(--acc);font-weight:600}
 .wrap{display:flex;height:calc(100vh - 92px)}#cv{flex:1;display:block;cursor:grab}#cv:active{cursor:grabbing}
 .right{width:340px;border-left:1px solid var(--line);overflow:auto;padding:10px 12px}
 .leg{display:flex;flex-wrap:wrap;gap:8px;font-size:10px;color:var(--mut);padding:4px 12px;border-bottom:1px solid var(--line)}
 .sw{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:3px;vertical-align:middle}
 .row{margin:3px 0}.k{color:var(--mut)}.pill{display:inline-block;padding:1px 6px;border-radius:10px;font-size:10px;border:1px solid var(--line);margin:1px 3px 1px 0}
 .vbadge{font-weight:700;padding:1px 6px;border-radius:5px;color:#06101f}.cite{font-size:11px;color:var(--mut);word-break:break-word}
</style></head><body>
<header><h1>Adversarial-Function Atlas — 3D <span class="sub">{N} examples · three framework axes per layout · drag to rotate · wheel to zoom · click a point</span></h1></header>
<div class="bar">
 <label>layout:</label>
 <button class="lo on" data-l="cube">scale × time × deceivability</button>
 <button class="lo" data-l="valence">beneficiary × target × third</button>
 <button class="lo" data-l="horn">lag horn (rung·time·lag)</button>
 <button class="lo" data-l="kind">deceivability × symmetry × outcome</button>
 <span style="width:10px"></span><label>colour:</label>
 <button class="ov on" data-ov="rung">rung</button><button class="ov" data-ov="register">register</button><button class="ov" data-ov="structural">structural</button><button class="ov" data-ov="benvalence">beneficiary valence</button>
 <span style="width:10px"></span><button id="spin">spin: off</button><button id="reset">reset view</button>
</div>
<div class="leg" id="legend"></div>
<div class="wrap"><canvas id="cv"></canvas><div class="right" id="detail"><div class="mut">Drag to rotate the cloud. Each layout puts three framework axes on X/Y/Z. Click any point for its classification.</div></div></div>
<script>
const DATA=/*DATA*/;
const RUNGS=["molecular","cellular","organismal","cognitive","social-institutional","latent-algorithmic","cosmic"];
const RI=Object.fromEntries(RUNGS.map((r,i)=>[r,i]));
const REG=["none","fact","time","sequence","existence"];const RGI=Object.fromEntries(REG.map((r,i)=>[r,i]));
const STR=["collapse-defender","collapse-attacker","ongoing-no-equilibrium","escalating-arms-race","equilibrium","new-action-space","n/a"];const STI=Object.fromEntries(STR.map((s,i)=>[s,i]));
const COL={rung:["#6e7681","#79c0ff","#3fb950","#d29922","#f0883e","#db61a2","#a371f7"],
 reg:{none:"#6e7681",fact:"#58a6ff",time:"#f0883e",sequence:"#db61a2",existence:"#a371f7"},
 val:{positive:"#3fb950",negative:"#f85149",mixed:"#d29922",neutral:"#8b949e"},
 struct:{"new-action-space":"#3fb950","equilibrium":"#58a6ff","escalating-arms-race":"#f0883e","ongoing-no-equilibrium":"#8b949e","collapse-attacker":"#a371f7","collapse-defender":"#db61a2","n/a":"#484f58"}};
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let W,H,DPR=window.devicePixelRatio||1;
function sz(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);}
let S={layout:"cube",ov:"rung",yaw:0.7,pitch:-0.45,scale:1,sel:null,spin:false};
const UMAX=Math.max.apply(null,DATA.map(d=>{const v=(d.t_phenom_ybp||d.t_ybp||1);return Math.log10((typeof v==="number"&&v>0?v:1)+1);}));
let LAGMAX=1;DATA.forEach(d=>{if(d.t_phenom_ybp>0&&d.t_obs_ybp>0){const l=Math.log10(d.t_phenom_ybp+1)-Math.log10(d.t_obs_ybp+1);if(l>LAGMAX)LAGMAX=l;}});
function tnorm(d){const v=(d.t_phenom_ybp||d.t_ybp);if(v===-1)return 1;if(v==null)return -1;const u=Math.log10(v+1)/UMAX;return (1-u)*2-1;}
function valn(v){return v==="positive"?1:v==="negative"?-1:v==="mixed"?0.25:0;}
function lagn(d){if(d.t_phenom_ybp>0&&d.t_obs_ybp>0)return (Math.log10(d.t_phenom_ybp+1)-Math.log10(d.t_obs_ybp+1))/LAGMAX;return 0;}
function xyz(d){const o=d.outcome||{},v=o.valence||{};
 if(S.layout==="cube")return [RI[d.rung]/6*2-1, tnorm(d), (RGI[d.deceivability_register]||0)/4*2-1];
 if(S.layout==="valence"){const t=(o.named_third_parties||[])[0];return [valn(v.beneficiary), valn(v.target), valn(t?t.valence:null)];}
 if(S.layout==="horn"){const r=0.25+lagn(d)*0.95,th=RI[d.rung]/7*2*Math.PI;return [r*Math.cos(th), tnorm(d), r*Math.sin(th)];}
 return [(RGI[d.deceivability_register]||0)/4*2-1, o.symmetric?0.9:-0.9, (STI[o.structural]||0)/6*2-1];}
function col(d){if(S.ov==="rung")return COL.rung[RI[d.rung]];if(S.ov==="register")return COL.reg[d.deceivability_register]||"#888";if(S.ov==="structural")return COL.struct[(d.outcome||{}).structural]||"#888";if(S.ov==="benvalence")return COL.val[((d.outcome||{}).valence||{}).beneficiary]||"#888";return "#888";}
function rot(x,y,z){const cy=Math.cos(S.yaw),sy=Math.sin(S.yaw);let x1=x*cy+z*sy,z1=-x*sy+z*cy,y1=y;const cx=Math.cos(S.pitch),sx=Math.sin(S.pitch);let y2=y1*cx-z1*sx,z2=y1*sx+z1*cx;return [x1,y2,z2];}
function proj(p){const R=Math.min(W,H)/2.6*S.scale;const r=rot(p[0],p[1],p[2]);return [W/2+r[0]*R, H/2-r[1]*R, r[2]];}
const AX={cube:["scale →","← time (deep→now)","deceivability ↑"],valence:["beneficiary +→","target +→","third-party +↑"],horn:["rung","← time","rung"],kind:["deceivability →","symmetric ↑","outcome →"]};
function draw(){sz();ctx.clearRect(0,0,W,H);
 // axes triad
 const O=proj([0,0,0]);const ax=[[1.15,0,0],[0,1.15,0],[0,0,1.15]];const labs=AX[S.layout];const axc=["#f0883e","#3fb950","#58a6ff"];
 ax.forEach((a,i)=>{const e=proj(a);ctx.strokeStyle=axc[i];ctx.globalAlpha=.5;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(O[0],O[1]);ctx.lineTo(e[0],e[1]);ctx.stroke();ctx.globalAlpha=.85;ctx.fillStyle=axc[i];ctx.font="11px sans-serif";ctx.fillText(labs[i],e[0]+3,e[1]);});
 ctx.globalAlpha=1;
 // points, depth-sorted
 const pts=DATA.map(d=>{const p=proj(xyz(d));return {d,sx:p[0],sy:p[1],z:p[2]};}).sort((a,b)=>a.z-b.z);
 pts.forEach(pt=>{const zn=(pt.z+1.4)/2.8,sel=S.sel&&S.sel.id===pt.d.id;
  ctx.globalAlpha=sel?1:(0.35+0.6*zn);ctx.fillStyle=col(pt.d);
  ctx.beginPath();ctx.arc(pt.sx,pt.sy,sel?7:(2.5+3.5*zn),0,6.2832);ctx.fill();
  if(sel){ctx.strokeStyle="#fff";ctx.lineWidth=1.5;ctx.stroke();}});
 ctx.globalAlpha=1;pt2=pts;
}
let pt2=[];
function pick(mx,my){let best=null,bd=14;pt2.forEach(pt=>{const dx=pt.sx-mx,dy=pt.sy-my,dd=Math.sqrt(dx*dx+dy*dy);if(dd<bd){bd=dd;best=pt.d;}});return best;}
function vchip(v){return v?'<span class="vbadge" style="background:'+(COL.val[v]||"#888")+'">'+v+'</span>':'<span class="k">n/a</span>';}
function esc(s){return (s==null?"":""+s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function detail(d){const o=d.outcome||{},v=o.valence||{},D=document.getElementById("detail");
 D.innerHTML='<div style="font-weight:700;font-size:14px">'+esc(d.name)+'</div>'+
 '<div class="row"><span class="pill">'+esc(d.rung)+'</span><span class="pill">'+esc(d.sub_primitive)+'</span><span class="pill">reg:'+esc(d.deceivability_register)+'</span></div>'+
 '<div class="row"><b>outcome:</b> <span class="pill" style="border-color:'+(COL.struct[o.structural]||"#888")+'">'+esc(o.structural)+'</span>'+(o.symmetric?' <span class="pill" style="border-color:#58a6ff">symmetric</span>':'')+'</div>'+
 '<div class="row"><span class="k">beneficiary</span> '+vchip(v.beneficiary)+' &nbsp; <span class="k">target</span> '+vchip(v.target)+'</div>'+
 '<div class="row"><span class="k">operated:</span> '+esc((d.t_phenomenon||{}).label||d.t_label||"?")+'</div>'+
 '<div class="row"><span class="k">beneficiary →</span> '+esc(d.beneficiary)+'</div><div class="row"><span class="k">target →</span> '+esc(d.target)+'</div>'+
 '<div class="row"><span class="k">externalized cost →</span> '+esc(d.externalized_cost)+'</div>'+
 '<div class="row cite"><span class="k">sources →</span> '+esc(d.citation)+'</div>';}
function legend(){const L=document.getElementById("legend");L.innerHTML="";let m=null;
 if(S.ov==="rung"){RUNGS.forEach((r,i)=>{const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+COL.rung[i]+'"></span>'+r;L.appendChild(s);});}
 else{m=S.ov==="register"?COL.reg:S.ov==="structural"?COL.struct:COL.val;for(const k in m){const s=document.createElement("span");s.innerHTML='<span class="sw" style="background:'+m[k]+'"></span>'+k;L.appendChild(s);}}}
// interaction
let drag=false,lx,ly;
cv.addEventListener("mousedown",e=>{drag=true;lx=e.offsetX;ly=e.offsetY;});
window.addEventListener("mouseup",()=>{drag=false;});
cv.addEventListener("mousemove",e=>{if(!drag)return;S.yaw+=(e.offsetX-lx)*0.01;S.pitch+=(e.offsetY-ly)*0.01;S.pitch=Math.max(-1.55,Math.min(1.55,S.pitch));lx=e.offsetX;ly=e.offsetY;draw();});
cv.addEventListener("wheel",e=>{e.preventDefault();S.scale*=(e.deltaY<0?1.1:0.9);S.scale=Math.max(0.4,Math.min(4,S.scale));draw();},{passive:false});
let moved=false;cv.addEventListener("mousedown",()=>moved=false);cv.addEventListener("mousemove",()=>{if(drag)moved=true;});
cv.addEventListener("click",e=>{if(moved)return;const d=pick(e.offsetX,e.offsetY);if(d){S.sel=d;detail(d);draw();}});
document.querySelectorAll(".lo").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".lo").forEach(x=>x.classList.remove("on"));b.classList.add("on");S.layout=b.dataset.l;draw();}));
document.querySelectorAll(".ov").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".ov").forEach(x=>x.classList.remove("on"));b.classList.add("on");S.ov=b.dataset.ov;legend();draw();}));
document.getElementById("reset").addEventListener("click",()=>{S.yaw=0.7;S.pitch=-0.45;S.scale=1;draw();});
let spinT=null;document.getElementById("spin").addEventListener("click",function(){S.spin=!S.spin;this.textContent="spin: "+(S.spin?"on":"off");this.classList.toggle("on",S.spin);if(S.spin){spinT=setInterval(()=>{S.yaw+=0.01;draw();},40);}else clearInterval(spinT);});
window.addEventListener("resize",draw);
legend();draw();
</script></body></html>"""

html = TEMPLATE.replace("/*DATA*/", data_js).replace("{N}", str(len(rows)))
open(os.path.join(HERE, "adversarial_atlas_3d.html"), "w", encoding="utf-8").write(html)
print("wrote adversarial_atlas_3d.html (", len(html), "chars,", len(rows), "examples )")
