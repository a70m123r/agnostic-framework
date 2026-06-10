/* review_layer.js — annotation + page-state capture overlay.
   Injected by review_server.py into any .html it serves. Self-contained, no deps.
   Captures: freehand pen, arrows, boxes, highlights, typed text, and pin-comments,
   PLUS a snapshot of the page state (the viewer's own state if it exposes
   window.__getReviewState(), else a generic scrape) so each review is replayable in context.
   Save -> POST /save (the review server writes reviews/<stamp>.review.json + .png),
   with an automatic file-download fallback if no save server is listening. */
(function(){
  if (window.__reviewLayerLoaded) return; window.__reviewLayerLoaded = true;
  var NS='http://www.w3.org/2000/svg';
  var tool='off', color='#ff5a3c', anns=[], idc=0, cur=null, dragStart=null, hidden=false;
  var COLORS=['#ff5a3c','#ffd23c','#3cc8ff','#5dffa0','#ff7ad9','#ffffff'];

  // ---- overlay svg ----
  var svg=document.createElementNS(NS,'svg');
  svg.id='__rv_svg';
  svg.setAttribute('style','position:fixed;inset:0;width:100vw;height:100vh;z-index:2147482000;pointer-events:none;');
  var defs=document.createElementNS(NS,'defs');
  defs.innerHTML='<marker id="__rv_arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="context-stroke"></path></marker>';
  svg.appendChild(defs);
  function ready(fn){ if(document.body) fn(); else addEventListener('DOMContentLoaded',fn); }

  function resize(){ svg.setAttribute('width',innerWidth); svg.setAttribute('height',innerHeight); }
  addEventListener('resize',resize);

  // ---- toolbar ----
  var bar=document.createElement('div');
  bar.id='__rv_bar';
  bar.setAttribute('style','position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:2147483000;display:flex;gap:4px;align-items:center;background:rgba(16,20,29,.96);border:1px solid #2a3142;border-radius:10px;padding:6px 8px;font:12px/1 "Segoe UI",system-ui,sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.5);user-select:none;');
  var TOOLS=[['off','◳ use viewer'],['pin','◉ comment'],['pen','✎ pen'],['arrow','↗ arrow'],['rect','▭ box'],['hi','▤ mark'],['text','T text']];
  var btns={};
  TOOLS.forEach(function(t){ var b=mk(t[1]); b.onclick=function(){ setTool(t[0]); }; btns[t[0]]=b; bar.appendChild(b); });
  bar.appendChild(sep());
  COLORS.forEach(function(c){ var s=document.createElement('button'); s.title=c; s.setAttribute('style',swStyle(c,c===color)); s.dataset.c=c; s.onclick=function(){ color=c; paintSwatches(); }; bar.appendChild(s); });
  bar.appendChild(sep());
  var bUndo=mk('⤺ undo'); bUndo.onclick=undo; bar.appendChild(bUndo);
  var bClear=mk('✕ clear'); bClear.onclick=function(){ if(anns.length&&confirm('Clear all annotations?')){ anns=[]; render(); } }; bar.appendChild(bClear);
  var bHide=mk('⤫ hide'); bHide.onclick=toggleHide; bar.appendChild(bHide);
  var bSave=mk('⤓ save'); bSave.style.cssText+=';background:#16324a;border-color:#2f6a9a;color:#cfe6ff;'; bSave.onclick=save; bar.appendChild(bSave);

  function mk(label){ var b=document.createElement('button'); b.textContent=label; b.setAttribute('style','background:transparent;color:#e8edf6;border:1px solid #2a3142;border-radius:7px;padding:5px 9px;font:12px "Segoe UI";cursor:pointer;white-space:nowrap;'); return b; }
  function sep(){ var s=document.createElement('span'); s.setAttribute('style','width:1px;height:18px;background:#2a3142;margin:0 3px;'); return s; }
  function swStyle(c,on){ return 'width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid '+(on?'#fff':'transparent')+';cursor:pointer;padding:0;'; }
  function paintSwatches(){ bar.querySelectorAll('button[data-c]').forEach(function(s){ s.setAttribute('style',swStyle(s.dataset.c, s.dataset.c===color)); }); }
  function setTool(t){ tool=t; Object.keys(btns).forEach(function(k){ btns[k].style.background=(k===t?'#16324a':'transparent'); btns[k].style.borderColor=(k===t?'#2f6a9a':'#2a3142'); btns[k].style.color=(k===t?'#cfe6ff':'#e8edf6'); }); svg.style.pointerEvents=(t==='off'?'none':'auto'); svg.style.cursor=(t==='text'||t==='pin'?'text':'crosshair'); }
  setTool('off');

  function toggleHide(){ hidden=!hidden; svg.style.display=hidden?'none':'block'; bHide.textContent=hidden?'⤢ show':'⤫ hide'; }
  addEventListener('keydown',function(e){ if(e.key==='h'&&!/input|textarea/i.test((e.target.tagName||''))) toggleHide(); if(e.key==='Escape'&&cur){ anns.pop(); cur=null; render(); } });

  // ---- drawing ----
  function pt(e){ return { x: e.clientX, y: e.clientY }; }
  svg.addEventListener('pointerdown',function(e){
    if(tool==='off') return;
    e.preventDefault(); svg.setPointerCapture(e.pointerId);
    var p=pt(e);
    if(tool==='pin'){ var a=newAnn('pin',{x:p.x,y:p.y,n:anns.filter(function(z){return z.type==='pin';}).length+1,text:''}); render(); openComment(a); return; }
    if(tool==='text'){ var t=newAnn('text',{x:p.x,y:p.y,text:''}); render(); openText(t); return; }
    if(tool==='pen'){ cur=newAnn('pen',{pts:[p]}); }
    else if(tool==='arrow'){ cur=newAnn('arrow',{x1:p.x,y1:p.y,x2:p.x,y2:p.y}); }
    else if(tool==='rect'){ cur=newAnn('rect',{x:p.x,y:p.y,w:0,h:0}); dragStart=p; }
    else if(tool==='hi'){ cur=newAnn('hi',{x:p.x,y:p.y,w:0,h:0}); dragStart=p; }
    render();
  });
  svg.addEventListener('pointermove',function(e){
    if(!cur) return; var p=pt(e);
    if(cur.type==='pen') cur.pts.push(p);
    else if(cur.type==='arrow'){ cur.x2=p.x; cur.y2=p.y; }
    else if(cur.type==='rect'||cur.type==='hi'){ cur.x=Math.min(dragStart.x,p.x); cur.y=Math.min(dragStart.y,p.y); cur.w=Math.abs(p.x-dragStart.x); cur.h=Math.abs(p.y-dragStart.y); }
    render();
  });
  svg.addEventListener('pointerup',function(e){ if(cur){ if((cur.type==='rect'||cur.type==='hi')&&cur.w<3&&cur.h<3){ anns.pop(); } else if(cur.type==='pen'&&cur.pts.length<2){ anns.pop(); } cur=null; dragStart=null; render(); } });

  function newAnn(type,props){ var a={ id:++idc, type:type, color:color, t:Date.now(), context:hitContext(props.x||(props.pts&&props.pts[0].x)||props.x1, props.y||(props.pts&&props.pts[0].y)||props.y1) }; for(var k in props) a[k]=props[k]; anns.push(a); return a; }
  function undo(){ anns.pop(); render(); }

  // what's under the anchor (for context) — peek past the overlay
  function hitContext(x,y){ if(x==null||y==null) return null; var pe=svg.style.pointerEvents; svg.style.pointerEvents='none'; var el=document.elementFromPoint(x,y); svg.style.pointerEvents=pe; if(!el) return null; var node=null; if(typeof window.__reviewHitTest==='function'){ try{ node=window.__reviewHitTest(x,y); }catch(e){} } return { tag:el.tagName.toLowerCase(), id:el.id||null, cls:(el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||null, text:(el.textContent||'').trim().slice(0,80)||null, node:node, nx:+(x/innerWidth).toFixed(4), ny:+(y/innerHeight).toFixed(4) }; }

  // ---- render ----
  function render(){
    while(svg.childNodes.length>1) svg.removeChild(svg.lastChild);
    anns.forEach(function(a){
      if(a.type==='pen'){ var pl=el('polyline',{points:a.pts.map(function(p){return p.x+','+p.y;}).join(' '),fill:'none',stroke:a.color,'stroke-width':3,'stroke-linecap':'round','stroke-linejoin':'round'}); svg.appendChild(pl); }
      else if(a.type==='arrow'){ svg.appendChild(el('line',{x1:a.x1,y1:a.y1,x2:a.x2,y2:a.y2,stroke:a.color,'stroke-width':3,'marker-end':'url(#__rv_arrow)'})); }
      else if(a.type==='rect'){ svg.appendChild(el('rect',{x:a.x,y:a.y,width:a.w,height:a.h,fill:'none',stroke:a.color,'stroke-width':2.5,rx:4})); }
      else if(a.type==='hi'){ svg.appendChild(el('rect',{x:a.x,y:a.y,width:a.w,height:a.h,fill:a.color,'fill-opacity':0.25,stroke:'none'})); }
      else if(a.type==='text'){ var tx=el('text',{x:a.x,y:a.y,fill:a.color,'font-size':16,'font-family':'Segoe UI, sans-serif','font-weight':500}); tx.textContent=a.text||'…'; tx.style.cursor='pointer'; tx.onclick=function(ev){ if(tool==='off'){ev.stopPropagation(); openText(a);} }; svg.appendChild(tx); }
      else if(a.type==='pin'){ var g=el('g',{}); g.style.cursor='pointer'; var c=el('circle',{cx:a.x,cy:a.y,r:10,fill:a.color,stroke:'#0c0f16','stroke-width':2}); var n=el('text',{x:a.x,y:a.y+4,fill:'#0c0f16','font-size':12,'font-weight':700,'text-anchor':'middle','font-family':'Segoe UI'}); n.textContent=a.n; g.appendChild(c); g.appendChild(n);
        if(a.text){ var lab=el('text',{x:a.x+14,y:a.y+4,fill:a.color,'font-size':12,'font-family':'Segoe UI'}); lab.textContent=a.text.length>32?a.text.slice(0,32)+'…':a.text; g.appendChild(lab); }
        g.onclick=function(ev){ ev.stopPropagation(); openComment(a); }; svg.appendChild(g); }
    });
  }
  function el(tag,attrs){ var e=document.createElementNS(NS,tag); for(var k in attrs) e.setAttribute(k,attrs[k]); return e; }

  // ---- comment / text popups ----
  function popup(x,y){ var d=document.createElement('div'); d.setAttribute('style','position:fixed;left:'+Math.min(x,innerWidth-260)+'px;top:'+Math.min(y,innerHeight-130)+'px;z-index:2147483600;background:#10141d;border:1px solid #2f6a9a;border-radius:8px;padding:8px;box-shadow:0 6px 24px rgba(0,0,0,.6);'); document.body.appendChild(d); return d; }
  function openComment(a){ var d=popup(a.x+16,a.y); var ta=document.createElement('textarea'); ta.value=a.text||''; ta.placeholder='comment on pin #'+a.n+'…'; ta.setAttribute('style','width:230px;height:64px;background:#0c0f16;color:#e8edf6;border:1px solid #2a3142;border-radius:6px;padding:6px;font:13px "Segoe UI";resize:vertical;'); d.appendChild(ta); ta.focus();
    var row=document.createElement('div'); row.style.cssText='display:flex;gap:6px;margin-top:6px;justify-content:flex-end;';
    var ok=mk('✓ save'); ok.onclick=function(){ a.text=ta.value.trim(); d.remove(); render(); };
    var del=mk('🗑 delete'); del.onclick=function(){ anns=anns.filter(function(z){return z!==a;}); renumber(); d.remove(); render(); };
    row.appendChild(del); row.appendChild(ok); d.appendChild(row);
    ta.addEventListener('keydown',function(e){ if(e.key==='Enter'&&(e.metaKey||e.ctrlKey)) ok.onclick(); });
  }
  function openText(a){ var d=popup(a.x,a.y-40); var inp=document.createElement('input'); inp.value=a.text||''; inp.placeholder='type label…'; inp.setAttribute('style','width:220px;background:#0c0f16;color:#e8edf6;border:1px solid #2a3142;border-radius:6px;padding:6px;font:14px "Segoe UI";'); d.appendChild(inp); inp.focus();
    function commit(){ a.text=inp.value.trim(); if(!a.text) anns=anns.filter(function(z){return z!==a;}); d.remove(); render(); }
    inp.addEventListener('keydown',function(e){ if(e.key==='Enter') commit(); if(e.key==='Escape'){ if(!a.text) anns=anns.filter(function(z){return z!==a;}); d.remove(); render(); } });
    inp.addEventListener('blur',commit);
  }
  function renumber(){ var k=0; anns.forEach(function(a){ if(a.type==='pin') a.n=++k; }); }

  // ---- state scrape ----
  function scrapeState(){
    var s={ url:location.href, path:location.pathname, title:document.title, ts:new Date().toISOString(), viewport:{w:innerWidth,h:innerHeight,dpr:window.devicePixelRatio} };
    if(typeof window.__getReviewState==='function'){ try{ s.viewer=window.__getReviewState(); }catch(e){ s.viewerError=String(e); } }
    s.inputs={}; document.querySelectorAll('input,select').forEach(function(elm,i){ var k=elm.id||elm.name||(elm.tagName.toLowerCase()+i); s.inputs[k]={value:elm.value, type:elm.type||elm.tagName.toLowerCase()}; });
    s.activeControls=[]; document.querySelectorAll('button,.chip,[role=tab]').forEach(function(b){ if(/(^|\s)(on|active|selected)(\s|$)/.test(b.className||'')) s.activeControls.push((b.textContent||'').trim()); });
    return s;
  }

  // ---- composite png (viewer canvases + annotation layer); best-effort, offline-safe ----
  function composite(cb){
    try{
      var W=innerWidth,H=innerHeight,out=document.createElement('canvas'); out.width=W; out.height=H; var o=out.getContext('2d');
      o.fillStyle=getComputedStyle(document.body).backgroundColor||'#0c0f16'; o.fillRect(0,0,W,H);
      document.querySelectorAll('canvas').forEach(function(c){ var r=c.getBoundingClientRect(); if(r.width<2||r.height<2) return; try{ o.drawImage(c,r.left,r.top,r.width,r.height); }catch(e){} });
      var xml=new XMLSerializer().serializeToString(svg);
      var img=new Image();
      img.onload=function(){ try{ o.drawImage(img,0,0,W,H); }catch(e){} done(); };
      img.onerror=done;
      function done(){ try{ cb(out.toDataURL('image/png')); }catch(e){ cb(null); } }
      img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(xml)));
    }catch(e){ cb(null); }
  }

  // ---- save ----
  function save(){
    var name=prompt('Name this review (optional):','')||'';
    composite(function(png){
      var payload={ meta:{ name:name, tool:'review_layer v0', savedAt:new Date().toISOString() }, state:scrapeState(), annotations:anns.map(stripFns), png:png };
      fetch(location.origin+'/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
        .then(function(r){ return r.ok?r.json():Promise.reject(r.status); })
        .then(function(j){ toast('saved → '+j.path+'  ('+anns.length+' notes)'); })
        .catch(function(){ var dl=JSON.parse(JSON.stringify(payload)); download(name||'review'); function download(base){ var stamp=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19); var fn=stamp+'-'+base.replace(/[^a-z0-9_-]/gi,'').slice(0,40); blobDL(JSON.stringify(dl,null,2),fn+'.review.json','application/json'); if(png) blobDL(png,fn+'.png',null,true); toast('no save-server — downloaded '+fn+'.review.json (move into reviews/)'); } });
    });
  }
  function stripFns(a){ var o={}; for(var k in a) if(typeof a[k]!=='function') o[k]=a[k]; return o; }
  function blobDL(data,fn,mime,isDataUrl){ var a=document.createElement('a'); if(isDataUrl){ a.href=data; } else { a.href=URL.createObjectURL(new Blob([data],{type:mime||'text/plain'})); } a.download=fn; document.body.appendChild(a); a.click(); a.remove(); }
  function toast(msg){ var t=document.createElement('div'); t.textContent=msg; t.setAttribute('style','position:fixed;left:50%;bottom:60px;transform:translateX(-50%);z-index:2147483600;background:#16324a;color:#cfe6ff;border:1px solid #2f6a9a;border-radius:8px;padding:8px 14px;font:13px "Segoe UI";box-shadow:0 4px 16px rgba(0,0,0,.5);'); document.body.appendChild(t); setTimeout(function(){ t.style.transition='opacity .5s'; t.style.opacity='0'; setTimeout(function(){t.remove();},500); },3200); }

  ready(function(){ document.body.appendChild(svg); document.body.appendChild(bar); resize(); paintSwatches(); render(); });
  window.__review={ get annotations(){return anns;}, state:scrapeState, save:save, add:function(a){ anns.push(a); render(); } };
})();
