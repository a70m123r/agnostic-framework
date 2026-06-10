/* review_layer.js v2 — radial marking-menu + permanent comment pins + frame replay.
   Injected by review_server.py into any .html it serves. Self-contained, no deps.

   INTERACTION
   - LONG-PRESS anywhere (450ms, <6px movement) -> progress ring -> radial menu around the cursor.
     Keep holding and release over a segment (marking-menu style), or release and click a segment.
     Right-click also opens the radial. Esc / click-outside closes.
   - Radial: tools (comment pin / pen / arrow / box / mark / text) + SAVE / DISCARD / use-viewer.
   - SAVE posts {state, annotations, png, pin} -> server; the session becomes ONE permanent GOLD pin.
   - Permanent pins persist (server registry), re-render on every load, and on click open a popup:
     the comment, the old capture thumbnail, and "go to frame" which REPLAYS the saved page state
     (specimen / toggles / sliders) so old feedback can be compared against the current iteration. */
(function(){
  if (window.__reviewLayerLoaded) return; window.__reviewLayerLoaded = true;
  var NS='http://www.w3.org/2000/svg';
  var tool='off', color='#ff5a3c', anns=[], idc=0, cur=null, dragStart=null, hidden=false;
  var COLORS=['#ff5a3c','#ffd23c','#3cc8ff','#5dffa0','#ff7ad9','#ffffff'];
  var permPins=[], lastRadialPos=null;

  function ready(fn){ if(document.body) fn(); else addEventListener('DOMContentLoaded',fn); }

  // ================= overlay svg (session drawings) =================
  var svg=document.createElementNS(NS,'svg');
  svg.id='__rv_svg';
  svg.setAttribute('style','position:fixed;inset:0;width:100vw;height:100vh;z-index:2147482000;pointer-events:none;');
  var defs=document.createElementNS(NS,'defs');
  var mk1=document.createElementNS(NS,'marker');
  mk1.setAttribute('id','__rv_arrow'); mk1.setAttribute('markerWidth','10'); mk1.setAttribute('markerHeight','10');
  mk1.setAttribute('refX','7'); mk1.setAttribute('refY','3'); mk1.setAttribute('orient','auto');
  var mp=document.createElementNS(NS,'path'); mp.setAttribute('d','M0,0 L7,3 L0,6 Z'); mp.setAttribute('fill','context-stroke');
  mk1.appendChild(mp); defs.appendChild(mk1); svg.appendChild(defs);
  function resize(){ svg.setAttribute('width',innerWidth); svg.setAttribute('height',innerHeight); placePins(); }
  addEventListener('resize',resize);

  // ================= permanent pins layer (clickable in ANY mode) =================
  var pinsDiv=document.createElement('div');
  pinsDiv.id='__rv_pins';
  pinsDiv.setAttribute('style','position:fixed;inset:0;z-index:2147482400;pointer-events:none;');
  function renderPins(){
    pinsDiv.innerHTML='';
    permPins.forEach(function(p,i){
      var b=document.createElement('button');
      b.className='__rv_pin';
      b.title=(p.comment||'').slice(0,120);
      b.textContent=String(i+1);
      b.setAttribute('style','position:absolute;width:24px;height:24px;border-radius:50% 50% 50% 4px;background:#f0b75e;color:#1a1206;border:2px solid #0c0f16;font:700 12px "Segoe UI";cursor:pointer;pointer-events:auto;transform:translate(-12px,-12px) rotate(0deg);box-shadow:0 2px 8px rgba(0,0,0,.5);');
      b.onclick=function(ev){ ev.stopPropagation(); openPermPopup(p,i); };
      pinsDiv.appendChild(b);
    });
    placePins();
  }
  function placePins(){
    var kids=pinsDiv.children;
    for(var i=0;i<kids.length;i++){ var p=permPins[i]; if(!p) continue;
      kids[i].style.left=Math.round((p.nx!=null?p.nx*innerWidth:p.x))+'px';
      kids[i].style.top =Math.round((p.ny!=null?p.ny*innerHeight:p.y))+'px'; }
  }
  function loadPins(){
    fetch(location.origin+'/pins?page='+encodeURIComponent(location.pathname))
      .then(function(r){ return r.ok?r.json():{pins:[]}; })
      .then(function(j){ permPins=j.pins||[]; renderPins(); })
      .catch(function(){});
  }

  // ================= toolbar (kept as secondary surface) =================
  var bar=document.createElement('div');
  bar.id='__rv_bar';
  bar.setAttribute('style','position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:2147483000;display:flex;gap:4px;align-items:center;background:rgba(16,20,29,.96);border:1px solid #2a3142;border-radius:10px;padding:6px 8px;font:12px/1 "Segoe UI",system-ui,sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.5);user-select:none;');
  var TOOLS=[['off','◳ use viewer'],['pin','◉ comment'],['pen','✎ pen'],['arrow','↗ arrow'],['rect','▭ box'],['hi','▤ mark'],['text','T text']];
  var btns={};
  TOOLS.forEach(function(t){ var b=mkBtn(t[1]); b.onclick=function(){ setTool(t[0]); }; btns[t[0]]=b; bar.appendChild(b); });
  bar.appendChild(sep());
  COLORS.forEach(function(c){ var s=document.createElement('button'); s.title=c; s.setAttribute('style',swStyle(c,c===color)); s.dataset.c=c; s.onclick=function(){ color=c; paintSwatches(); }; bar.appendChild(s); });
  bar.appendChild(sep());
  var bUndo=mkBtn('⏪ undo'); bUndo.onclick=undo; bar.appendChild(bUndo);
  var bHide=mkBtn('⤳ hide'); bHide.onclick=toggleHide; bar.appendChild(bHide);
  var bDisc=mkBtn('✕ discard'); bDisc.onclick=discard; bar.appendChild(bDisc);
  var bSave=mkBtn('⤓ save'); bSave.style.cssText+=';background:#16324a;border-color:#2f6a9a;color:#cfe6ff;'; bSave.onclick=save; bar.appendChild(bSave);
  var hint=document.createElement('span'); hint.textContent='long-press = radial'; hint.setAttribute('style','color:#5a6275;font-size:11px;margin-left:4px;'); bar.appendChild(hint);

  function mkBtn(label){ var b=document.createElement('button'); b.textContent=label; b.setAttribute('style','background:transparent;color:#e8edf6;border:1px solid #2a3142;border-radius:7px;padding:5px 9px;font:12px "Segoe UI";cursor:pointer;white-space:nowrap;'); return b; }
  function sep(){ var s=document.createElement('span'); s.setAttribute('style','width:1px;height:18px;background:#2a3142;margin:0 3px;'); return s; }
  function swStyle(c,on){ return 'width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid '+(on?'#fff':'transparent')+';cursor:pointer;padding:0;'; }
  function paintSwatches(){ bar.querySelectorAll('button[data-c]').forEach(function(s){ s.setAttribute('style',swStyle(s.dataset.c, s.dataset.c===color)); }); }
  function setTool(t){ tool=t; Object.keys(btns).forEach(function(k){ btns[k].style.background=(k===t?'#16324a':'transparent'); btns[k].style.borderColor=(k===t?'#2f6a9a':'#2a3142'); btns[k].style.color=(k===t?'#cfe6ff':'#e8edf6'); }); svg.style.pointerEvents=(t==='off'?'none':'auto'); svg.style.cursor=(t==='text'||t==='pin'?'text':'crosshair'); }

  function toggleHide(){ hidden=!hidden; svg.style.display=hidden?'none':'block'; pinsDiv.style.display=hidden?'none':'block'; bHide.textContent=hidden?'⤢ show':'⤳ hide'; }
  addEventListener('keydown',function(e){ if(e.key==='h'&&!/input|textarea/i.test((e.target.tagName||''))) toggleHide(); if(e.key==='Escape'){ closeRadial(); if(cur){ anns.pop(); cur=null; render(); } } });

  // ================= long-press -> radial marking menu =================
  var lp={timer:null,x:0,y:0,fired:false,holding:false};
  var ring=null;
  function ringShow(x,y){
    ringHide();
    ring=document.createElement('div');
    ring.setAttribute('style','position:fixed;left:'+(x-16)+'px;top:'+(y-16)+'px;width:32px;height:32px;border-radius:50%;z-index:2147483400;pointer-events:none;');
    var rs=document.createElementNS(NS,'svg'); rs.setAttribute('width','32'); rs.setAttribute('height','32');
    var c=document.createElementNS(NS,'circle');
    c.setAttribute('cx','16'); c.setAttribute('cy','16'); c.setAttribute('r','13');
    c.setAttribute('fill','none'); c.setAttribute('stroke','#f0b75e'); c.setAttribute('stroke-width','3');
    var circ=2*Math.PI*13; c.setAttribute('stroke-dasharray',circ); c.setAttribute('stroke-dashoffset',circ);
    c.setAttribute('transform','rotate(-90 16 16)');
    rs.appendChild(c); ring.appendChild(rs); document.body.appendChild(ring);
    var t0=performance.now();
    (function anim(){ if(!ring) return; var k=Math.min(1,(performance.now()-t0)/450); c.setAttribute('stroke-dashoffset',circ*(1-k)); if(k<1) requestAnimationFrame(anim); })();
  }
  function ringHide(){ if(ring){ ring.remove(); ring=null; } }

  addEventListener('pointerdown',function(e){
    if(e.button===2) return;
    if(isOurs(e.target)) return;
    lp.x=e.clientX; lp.y=e.clientY; lp.fired=false;
    ringShow(lp.x,lp.y);
    lp.timer=setTimeout(function(){ lp.fired=true; lp.holding=true; ringHide();
      if(cur){ anns.pop(); cur=null; dragStart=null; render(); }   // abort a just-started degenerate shape
      openRadial(lp.x,lp.y,true);
    },450);
  },true);
  addEventListener('pointermove',function(e){
    if(lp.timer&&(Math.abs(e.clientX-lp.x)>6||Math.abs(e.clientY-lp.y)>6)){ clearTimeout(lp.timer); lp.timer=null; ringHide(); }
    if(radial&&lp.holding) radialHover(e.clientX,e.clientY);
  },true);
  addEventListener('pointerup',function(e){
    if(lp.timer){ clearTimeout(lp.timer); lp.timer=null; ringHide(); }
    if(radial&&lp.holding){ lp.holding=false; var seg=radialHit(e.clientX,e.clientY); if(seg!=null){ radialPick(seg); } }
  },true);
  addEventListener('contextmenu',function(e){ if(isOurs(e.target)) return; e.preventDefault(); openRadial(e.clientX,e.clientY,false); },true);
  function isOurs(t){ if(!t||!t.closest) return false; return !!t.closest('#__rv_bar,#__rv_radial,#__rv_pop,.__rv_pin'); }

  // ---- radial geometry ----
  var radial=null, radialItems=[
    {k:'pin',   g:'◉', label:'comment'},
    {k:'pen',   g:'✎', label:'pen'},
    {k:'arrow', g:'↗', label:'arrow'},
    {k:'rect',  g:'▭', label:'box'},
    {k:'hi',    g:'▤', label:'mark'},
    {k:'text',  g:'T',      label:'text'},
    {k:'save',  g:'⤓', label:'save'},
    {k:'discard',g:'✕',label:'discard'},
    {k:'off',   g:'◳', label:'viewer'}
  ];
  function openRadial(x,y,holding){
    closeRadial();
    lastRadialPos={x:x,y:y,nx:x/innerWidth,ny:y/innerHeight};
    var R=92, r0=30, size=R*2+8, n=radialItems.length;
    x=Math.max(R+6,Math.min(innerWidth-R-6,x)); y=Math.max(R+6,Math.min(innerHeight-R-6,y));
    radial=document.createElement('div');
    radial.id='__rv_radial'; radial._cx=x; radial._cy=y; radial._R=R; radial._r0=r0;
    radial.setAttribute('style','position:fixed;left:'+(x-R-4)+'px;top:'+(y-R-4)+'px;width:'+size+'px;height:'+size+'px;z-index:2147483500;');
    var s=document.createElementNS(NS,'svg'); s.setAttribute('width',size); s.setAttribute('height',size);
    var cx=R+4, cy=R+4;
    radial._segs=[];
    for(var i=0;i<n;i++){
      var a0=(i/n)*Math.PI*2-Math.PI/2, a1=((i+1)/n)*Math.PI*2-Math.PI/2, am=(a0+a1)/2;
      var p=segPath(cx,cy,r0,R,a0,a1);
      var g=document.createElementNS(NS,'g'); g.style.cursor='pointer';
      var path=document.createElementNS(NS,'path');
      path.setAttribute('d',p);
      var isAct=radialItems[i].k===tool;
      path.setAttribute('fill',isAct?'#16324a':'rgba(16,20,29,.96)');
      path.setAttribute('stroke',isAct?'#2f6a9a':'#2a3142');
      path.setAttribute('stroke-width','1');
      var tx=document.createElementNS(NS,'text');
      tx.setAttribute('x',cx+Math.cos(am)*(r0+R)/2); tx.setAttribute('y',cy+Math.sin(am)*(r0+R)/2-2);
      tx.setAttribute('text-anchor','middle'); tx.setAttribute('fill','#e8edf6');
      tx.setAttribute('font-size','14'); tx.setAttribute('font-family','Segoe UI');
      tx.textContent=radialItems[i].g;
      var tl=document.createElementNS(NS,'text');
      tl.setAttribute('x',cx+Math.cos(am)*(r0+R)/2); tl.setAttribute('y',cy+Math.sin(am)*(r0+R)/2+11);
      tl.setAttribute('text-anchor','middle'); tl.setAttribute('fill','#8e98ad');
      tl.setAttribute('font-size','9'); tl.setAttribute('font-family','Segoe UI');
      tl.textContent=radialItems[i].label;
      g.appendChild(path); g.appendChild(tx); g.appendChild(tl);
      (function(idx){ g.addEventListener('click',function(ev){ ev.stopPropagation(); radialPick(idx); }); })(i);
      s.appendChild(g); radial._segs.push(path);
    }
    var cc=document.createElementNS(NS,'circle');
    cc.setAttribute('cx',cx); cc.setAttribute('cy',cy); cc.setAttribute('r',r0-4);
    cc.setAttribute('fill','rgba(12,15,22,.97)'); cc.setAttribute('stroke','#2a3142');
    var ct=document.createElementNS(NS,'text');
    ct.setAttribute('x',cx); ct.setAttribute('y',cy+4); ct.setAttribute('text-anchor','middle');
    ct.setAttribute('fill','#8e98ad'); ct.setAttribute('font-size','9'); ct.setAttribute('font-family','Segoe UI');
    ct.textContent=anns.length? anns.length+' notes' : tool;
    s.appendChild(cc); s.appendChild(ct);
    radial.appendChild(s);
    document.body.appendChild(radial);
    setTimeout(function(){ addEventListener('pointerdown',outsideClose,true); },0);
  }
  function segPath(cx,cy,r0,r1,a0,a1){
    var x0=cx+Math.cos(a0)*r0,y0=cy+Math.sin(a0)*r0,x1=cx+Math.cos(a0)*r1,y1=cy+Math.sin(a0)*r1;
    var x2=cx+Math.cos(a1)*r1,y2=cy+Math.sin(a1)*r1,x3=cx+Math.cos(a1)*r0,y3=cy+Math.sin(a1)*r0;
    return 'M'+x0+','+y0+' L'+x1+','+y1+' A'+r1+','+r1+' 0 0 1 '+x2+','+y2+' L'+x3+','+y3+' A'+r0+','+r0+' 0 0 0 '+x0+','+y0+' Z';
  }
  function radialHit(px,py){
    if(!radial) return null;
    var dx=px-radial._cx, dy=py-radial._cy, d=Math.sqrt(dx*dx+dy*dy);
    if(d<radial._r0||d>radial._R+10) return null;
    var ang=Math.atan2(dy,dx)+Math.PI/2; if(ang<0) ang+=Math.PI*2;
    return Math.floor(ang/(Math.PI*2)*radialItems.length)%radialItems.length;
  }
  function radialHover(px,py){
    if(!radial) return; var hit=radialHit(px,py);
    radial._segs.forEach(function(p,i){ var isAct=radialItems[i].k===tool;
      p.setAttribute('fill', i===hit?'#1d4a6e':(isAct?'#16324a':'rgba(16,20,29,.96)'));
      p.setAttribute('stroke', i===hit?'#5ba3d9':(isAct?'#2f6a9a':'#2a3142')); });
  }
  function radialPick(i){
    var k=radialItems[i].k; closeRadial();
    if(k==='save') return save();
    if(k==='discard') return discard();
    setTool(k);
    if(k==='pin'&&lastRadialPos){ var a=newAnn('pin',{x:lastRadialPos.x,y:lastRadialPos.y,n:pinCount()+1,text:''}); render(); openComment(a); }
  }
  function outsideClose(e){ if(radial&&!radial.contains(e.target)) closeRadial(); }
  function closeRadial(){ if(radial){ radial.remove(); radial=null; removeEventListener('pointerdown',outsideClose,true);} lp.holding=false; }

  // ================= drawing =================
  function pt(e){ return { x:e.clientX, y:e.clientY }; }
  function pinCount(){ return anns.filter(function(z){return z.type==='pin';}).length; }
  svg.addEventListener('pointerdown',function(e){
    if(tool==='off') return;
    e.preventDefault(); svg.setPointerCapture(e.pointerId);
    var p=pt(e);
    if(tool==='pin'){ var a=newAnn('pin',{x:p.x,y:p.y,n:pinCount()+1,text:''}); render(); openComment(a); return; }
    if(tool==='text'){ var t=newAnn('text',{x:p.x,y:p.y,text:''}); render(); openText(t); return; }
    if(tool==='pen'){ cur=newAnn('pen',{pts:[p]}); }
    else if(tool==='arrow'){ cur=newAnn('arrow',{x1:p.x,y1:p.y,x2:p.x,y2:p.y}); }
    else if(tool==='rect'||tool==='hi'){ cur=newAnn(tool,{x:p.x,y:p.y,w:0,h:0}); dragStart=p; }
    render();
  });
  svg.addEventListener('pointermove',function(e){
    if(!cur) return; var p=pt(e);
    if(cur.type==='pen') cur.pts.push(p);
    else if(cur.type==='arrow'){ cur.x2=p.x; cur.y2=p.y; }
    else { cur.x=Math.min(dragStart.x,p.x); cur.y=Math.min(dragStart.y,p.y); cur.w=Math.abs(p.x-dragStart.x); cur.h=Math.abs(p.y-dragStart.y); }
    render();
  });
  svg.addEventListener('pointerup',function(){
    if(cur){ if((cur.type==='rect'||cur.type==='hi')&&cur.w<3&&cur.h<3) anns.pop();
      else if(cur.type==='pen'&&cur.pts.length<2) anns.pop();
      cur=null; dragStart=null; render(); }
  });

  function newAnn(type,props){
    var ax=props.x!=null?props.x:(props.pts?props.pts[0].x:props.x1);
    var ay=props.y!=null?props.y:(props.pts?props.pts[0].y:props.y1);
    var a={ id:++idc, type:type, color:color, t:Date.now(), context:hitContext(ax,ay) };
    for(var k in props) a[k]=props[k];
    anns.push(a); return a;
  }
  function undo(){ anns.pop(); render(); }
  function discard(){ if(anns.length&&!confirm('Discard '+anns.length+' unsaved notes?')) return; anns=[]; cur=null; setTool('off'); render(); }

  function hitContext(x,y){
    if(x==null||y==null) return null;
    var pe=svg.style.pointerEvents; svg.style.pointerEvents='none';
    var el=document.elementFromPoint(x,y);
    svg.style.pointerEvents=pe;
    if(!el) return null;
    var node=null;
    if(typeof window.__reviewHitTest==='function'){ try{ node=window.__reviewHitTest(x,y); }catch(e){} }
    return { tag:el.tagName.toLowerCase(), id:el.id||null,
      cls:(el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||null,
      text:(el.textContent||'').trim().slice(0,80)||null, node:node,
      nx:+(x/innerWidth).toFixed(4), ny:+(y/innerHeight).toFixed(4) };
  }

  // ================= render session annotations =================
  function render(){
    while(svg.childNodes.length>1) svg.removeChild(svg.lastChild);
    anns.forEach(function(a){
      if(a.type==='pen'){ var pl=el('polyline',{points:a.pts.map(function(p){return p.x+','+p.y;}).join(' '),fill:'none',stroke:a.color,'stroke-width':3,'stroke-linecap':'round','stroke-linejoin':'round'}); svg.appendChild(pl); }
      else if(a.type==='arrow'){ svg.appendChild(el('line',{x1:a.x1,y1:a.y1,x2:a.x2,y2:a.y2,stroke:a.color,'stroke-width':3,'marker-end':'url(#__rv_arrow)'})); }
      else if(a.type==='rect'){ svg.appendChild(el('rect',{x:a.x,y:a.y,width:a.w,height:a.h,fill:'none',stroke:a.color,'stroke-width':2.5,rx:4})); }
      else if(a.type==='hi'){ svg.appendChild(el('rect',{x:a.x,y:a.y,width:a.w,height:a.h,fill:a.color,'fill-opacity':0.25,stroke:'none'})); }
      else if(a.type==='text'){ var tx=el('text',{x:a.x,y:a.y,fill:a.color,'font-size':16,'font-family':'Segoe UI, sans-serif','font-weight':500}); tx.textContent=a.text||'…'; tx.style.cursor='pointer'; tx.onclick=function(ev){ if(tool==='off'){ev.stopPropagation(); openText(a);} }; svg.appendChild(tx); }
      else if(a.type==='pin'){ var g=el('g',{}); g.style.cursor='pointer';
        g.appendChild(el('circle',{cx:a.x,cy:a.y,r:10,fill:a.color,stroke:'#0c0f16','stroke-width':2}));
        var n=el('text',{x:a.x,y:a.y+4,fill:'#0c0f16','font-size':12,'font-weight':700,'text-anchor':'middle','font-family':'Segoe UI'});
        n.textContent=a.n; g.appendChild(n);
        if(a.text){ var lab=el('text',{x:a.x+14,y:a.y+4,fill:a.color,'font-size':12,'font-family':'Segoe UI'}); lab.textContent=a.text.length>32?a.text.slice(0,32)+'…':a.text; g.appendChild(lab); }
        g.onclick=function(ev){ ev.stopPropagation(); openComment(a); };
        svg.appendChild(g); }
    });
  }
  function el(tag,attrs){ var e=document.createElementNS(NS,tag); for(var k in attrs) e.setAttribute(k,attrs[k]); return e; }

  // ================= popups =================
  function popup(x,y,w){
    closePopup();
    var d=document.createElement('div');
    d.id='__rv_pop';
    d.setAttribute('style','position:fixed;left:'+Math.min(x,innerWidth-(w||260)-12)+'px;top:'+Math.min(y,innerHeight-170)+'px;z-index:2147483600;background:#10141d;border:1px solid #2f6a9a;border-radius:8px;padding:8px;box-shadow:0 6px 24px rgba(0,0,0,.6);max-width:'+((w||260))+'px;');
    document.body.appendChild(d); return d;
  }
  function closePopup(){ var p=document.getElementById('__rv_pop'); if(p) p.remove(); }
  function openComment(a){
    var d=popup(a.x+16,a.y);
    var ta=document.createElement('textarea'); ta.value=a.text||''; ta.placeholder='comment on pin #'+a.n+'…';
    ta.setAttribute('style','width:230px;height:64px;background:#0c0f16;color:#e8edf6;border:1px solid #2a3142;border-radius:6px;padding:6px;font:13px "Segoe UI";resize:vertical;');
    d.appendChild(ta); ta.focus();
    var row=document.createElement('div'); row.style.cssText='display:flex;gap:6px;margin-top:6px;justify-content:flex-end;';
    var del=mkBtn('\u{1F5D1} delete'); del.onclick=function(){ anns=anns.filter(function(z){return z!==a;}); renumber(); closePopup(); render(); };
    var ok=mkBtn('✓ keep'); ok.onclick=function(){ a.text=ta.value.trim(); closePopup(); render(); };
    row.appendChild(del); row.appendChild(ok); d.appendChild(row);
    ta.addEventListener('keydown',function(e){ if(e.key==='Enter'&&(e.metaKey||e.ctrlKey)) ok.onclick(); });
  }
  function openText(a){
    var d=popup(a.x,a.y-40);
    var inp=document.createElement('input'); inp.value=a.text||''; inp.placeholder='type label…';
    inp.setAttribute('style','width:220px;background:#0c0f16;color:#e8edf6;border:1px solid #2a3142;border-radius:6px;padding:6px;font:14px "Segoe UI";');
    d.appendChild(inp); inp.focus();
    function commit(){ a.text=inp.value.trim(); if(!a.text) anns=anns.filter(function(z){return z!==a;}); closePopup(); render(); }
    inp.addEventListener('keydown',function(e){ if(e.key==='Enter') commit(); if(e.key==='Escape'){ if(!a.text) anns=anns.filter(function(z){return z!==a;}); closePopup(); render(); } });
    inp.addEventListener('blur',commit);
  }
  function renumber(){ var k=0; anns.forEach(function(a){ if(a.type==='pin') a.n=++k; }); }

  function openPermPopup(p,i){
    var x=(p.nx!=null?p.nx*innerWidth:p.x), y=(p.ny!=null?p.ny*innerHeight:p.y);
    var d=popup(x+18,y-10,300);
    var h=document.createElement('div'); h.style.cssText='font:600 13px "Segoe UI";color:#f0b75e;margin-bottom:4px;';
    h.textContent='◉ pin '+(i+1)+' — '+new Date(p.savedAt||Date.now()).toLocaleString();
    d.appendChild(h);
    var c=document.createElement('div'); c.style.cssText='font:13px "Segoe UI";color:#e8edf6;white-space:pre-wrap;margin-bottom:6px;max-height:120px;overflow:auto;';
    c.textContent=p.comment||'(no comment)';
    d.appendChild(c);
    if(p.png){ var img=document.createElement('img'); img.src='/reviews/'+p.png; img.loading='lazy';
      img.setAttribute('style','width:280px;border:1px solid #2a3142;border-radius:6px;cursor:zoom-in;display:block;margin-bottom:6px;');
      img.title='the capture as it looked when the feedback was left — compare with the live view behind';
      img.onclick=function(){ window.open('/reviews/'+p.png,'_blank'); };
      d.appendChild(img); }
    var row=document.createElement('div'); row.style.cssText='display:flex;gap:6px;justify-content:flex-end;';
    var go=mkBtn('↦ go to frame'); go.style.cssText+=';background:#16324a;border-color:#2f6a9a;color:#cfe6ff;';
    go.onclick=function(){
      go.textContent='↦ replaying…';
      fetch('/reviews/'+p.review).then(function(r){return r.json();}).then(function(j){
        applyState(j.state||{},function(rep){ go.textContent='↦ go to frame'; toast('frame replayed — '+rep.length+' settings applied · compare with the thumbnail'); });
      }).catch(function(){ toast('could not load saved state'); go.textContent='↦ go to frame'; });
    };
    var cl=mkBtn('✕ close'); cl.onclick=closePopup;
    row.appendChild(go); row.appendChild(cl); d.appendChild(row);
  }

  // ================= state scrape + replay =================
  function scrapeState(){
    var s={ url:location.href, path:location.pathname, title:document.title, ts:new Date().toISOString(),
      viewport:{w:innerWidth,h:innerHeight,dpr:window.devicePixelRatio} };
    if(typeof window.__getReviewState==='function'){ try{ s.viewer=window.__getReviewState(); }catch(e){ s.viewerError=String(e); } }
    s.inputs={}; document.querySelectorAll('input,select').forEach(function(elm,i){ var k=elm.id||elm.name||(elm.tagName.toLowerCase()+i); s.inputs[k]={value:elm.value, type:elm.type||elm.tagName.toLowerCase()}; });
    s.activeControls=[]; document.querySelectorAll('button,.chip,[role=tab]').forEach(function(b){ if(/(^|\s)(on|active|selected)(\s|$)/.test(b.className||'')) s.activeControls.push((b.textContent||'').trim()); });
    return s;
  }
  function applyState(st,done){
    var report=[];
    try{
      if(st.viewer&&typeof window.__applyReviewState==='function'){ try{ window.__applyReviewState(st.viewer); report.push('viewer hook'); }catch(e){} }
      var acts=st.activeControls||[];
      var all=Array.prototype.slice.call(document.querySelectorAll('button,.chip,[role=tab]')).filter(function(b){ return !isOurs(b); });
      function isActive(b){ return /(^|\s)(on|active|selected)(\s|$)/.test(b.className||''); }
      acts.forEach(function(txt){ var t=(txt||'').trim(); if(!t) return;
        for(var i=0;i<all.length;i++){ if((all[i].textContent||'').trim()===t){ if(!isActive(all[i])){ all[i].click(); report.push(t); } return; } } });
      setTimeout(function(){
        var inp=st.inputs||{};
        Object.keys(inp).forEach(function(k){
          var elm=document.getElementById(k)||document.getElementsByName(k)[0];
          if(elm&&('value' in elm)&&!isOurs(elm)){ elm.value=inp[k].value;
            elm.dispatchEvent(new Event('input',{bubbles:true})); elm.dispatchEvent(new Event('change',{bubbles:true}));
            report.push(k+'='+inp[k].value); } });
        if(done) done(report);
      },380);
    }catch(e){ if(done) done(['error: '+e.message]); }
  }

  // ================= composite png =================
  function composite(cb){
    try{
      var W=innerWidth,H=innerHeight,out=document.createElement('canvas'); out.width=W; out.height=H;
      var o=out.getContext('2d');
      o.fillStyle=getComputedStyle(document.body).backgroundColor||'#0c0f16'; o.fillRect(0,0,W,H);
      document.querySelectorAll('canvas').forEach(function(c){ if(c.closest&&isOurs(c)) return; var r=c.getBoundingClientRect(); if(r.width<2||r.height<2) return; try{ o.drawImage(c,r.left,r.top,r.width,r.height); }catch(e){} });
      var xml=new XMLSerializer().serializeToString(svg);
      var img=new Image();
      img.onload=function(){ try{ o.drawImage(img,0,0,W,H); }catch(e){} done(); };
      img.onerror=done;
      function done(){ try{ cb(out.toDataURL('image/png')); }catch(e){ cb(null); } }
      img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(xml)));
    }catch(e){ cb(null); }
  }

  // ================= save =================
  function save(){
    if(!anns.length){ toast('nothing to save — long-press for the radial, leave a note first'); return; }
    var firstPin=null;
    for(var i=0;i<anns.length;i++){ if(anns[i].type==='pin'&&anns[i].text){ firstPin=anns[i]; break; } }
    if(!firstPin){ for(i=0;i<anns.length;i++){ if(anns[i].type==='pin'){ firstPin=anns[i]; break; } } }
    var comment=firstPin&&firstPin.text?firstPin.text:(prompt('Comment for this review pin:','')||'');
    var px,py;
    if(firstPin){ px=firstPin.x; py=firstPin.y; }
    else if(lastRadialPos){ px=lastRadialPos.x; py=lastRadialPos.y; }
    else { var sx=0,sy=0,sn=0; anns.forEach(function(a){ var ax=a.x!=null?a.x:(a.pts?a.pts[0].x:a.x1); var ay=a.y!=null?a.y:(a.pts?a.pts[0].y:a.y1); if(ax!=null){sx+=ax;sy+=ay;sn++;} }); px=sn?sx/sn:innerWidth/2; py=sn?sy/sn:innerHeight/2; }
    composite(function(png){
      var payload={ meta:{ name:slug(comment)||'review', tool:'review_layer v2', savedAt:new Date().toISOString(),
          pin:{ x:px, y:py, nx:+(px/innerWidth).toFixed(4), ny:+(py/innerHeight).toFixed(4), comment:comment } },
        state:scrapeState(), annotations:anns.map(stripFns), png:png };
      fetch(location.origin+'/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
        .then(function(r){ return r.ok?r.json():Promise.reject(r.status); })
        .then(function(j){
          if(j.pin){ permPins.push(j.pin); renderPins(); }
          anns=[]; cur=null; setTool('off'); render();
          toast('saved → '+j.path+' · pin #'+permPins.length+' placed');
        })
        .catch(function(){
          var stamp=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19);
          var fn=stamp+'-'+(slug(comment)||'review');
          blobDL(JSON.stringify(payload,null,2),fn+'.review.json','application/json');
          if(png) blobDL(png,fn+'.png',null,true);
          toast('no save-server — downloaded '+fn+'.review.json (move into reviews/)');
        });
    });
  }
  function slug(s){ return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,40); }
  function stripFns(a){ var o={}; for(var k in a) if(typeof a[k]!=='function') o[k]=a[k]; return o; }
  function blobDL(data,fn,mime,isDataUrl){ var a=document.createElement('a'); if(isDataUrl){ a.href=data; } else { a.href=URL.createObjectURL(new Blob([data],{type:mime||'text/plain'})); } a.download=fn; document.body.appendChild(a); a.click(); a.remove(); }
  function toast(msg){ var t=document.createElement('div'); t.textContent=msg; t.setAttribute('style','position:fixed;left:50%;bottom:60px;transform:translateX(-50%);z-index:2147483700;background:#16324a;color:#cfe6ff;border:1px solid #2f6a9a;border-radius:8px;padding:8px 14px;font:13px "Segoe UI";box-shadow:0 4px 16px rgba(0,0,0,.5);max-width:70vw;'); document.body.appendChild(t); setTimeout(function(){ t.style.transition='opacity .5s'; t.style.opacity='0'; setTimeout(function(){t.remove();},500); },3600); }

  // ================= boot =================
  ready(function(){
    document.body.appendChild(svg);
    document.body.appendChild(pinsDiv);
    document.body.appendChild(bar);
    resize(); setTool('off'); paintSwatches(); render(); loadPins();
  });
  window.__review={ get annotations(){return anns;}, get pins(){return permPins;}, state:scrapeState, apply:applyState,
    save:save, openRadial:openRadial, setTool:setTool, add:function(a){ anns.push(a); render(); } };
})();
