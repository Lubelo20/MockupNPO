(function(){
  var $=function(i){return document.getElementById(i)};
  document.documentElement.classList.remove('no-js');
  // animations that start hidden only switch on once this script is running
  if('IntersectionObserver' in window)document.documentElement.classList.add('anim-ready');

  // current page in nav
  var here=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.links a').forEach(function(a){
    if(a.getAttribute('href')===here)a.setAttribute('aria-current','page');
  });

  // header: solid once the page scrolls (it floats over the hero until then)
  var head=document.querySelector('.site-head');
  function paint(){if(head)head.classList.toggle('solid',window.scrollY>40)}
  window.addEventListener('scroll',paint,{passive:true});paint();

  // mobile menu: full-screen panel; Esc, a link, or the empty panel closes it
  var b=$('menu-btn'),l=$('links'),root=document.documentElement;
  function setMenu(o){
    l.classList.toggle('open',o);root.classList.toggle('menu-open',o);
    b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Close menu':'Open menu');
  }
  if(b&&l){
    b.addEventListener('click',function(){setMenu(!l.classList.contains('open'))});
    l.addEventListener('click',function(e){if(e.target===l||e.target.closest('a'))setMenu(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&l.classList.contains('open')){setMenu(false);b.focus()}});
    window.addEventListener('resize',function(){if(window.innerWidth>980&&l.classList.contains('open'))setMenu(false)});
  }

  var yr=$('yr');if(yr)yr.textContent=new Date().getFullYear();

  // reveal on scroll
  var els=document.querySelectorAll('.reveal,[data-anim]');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(el){io.observe(el)});
  }else els.forEach(function(el){el.classList.add('in')});

  // photo slider: arrows move one frame; disabled at the ends
  document.querySelectorAll('[data-slider]').forEach(function(sl){
    var track=sl.querySelector('.slides'),btns=sl.querySelectorAll('.sl-btn');
    function step(){var f=track.querySelector('figure');return f?f.getBoundingClientRect().width+16:300}
    function update(){
      var max=track.scrollWidth-track.clientWidth-2;
      btns[0].disabled=track.scrollLeft<=2;btns[1].disabled=track.scrollLeft>=max;
    }
    var target=null,idle;
    btns.forEach(function(b){b.addEventListener('click',function(){
      var max=track.scrollWidth-track.clientWidth,from=target===null?track.scrollLeft:target;
      target=Math.max(0,Math.min(max,(Math.round(from/step())+Number(b.dataset.dir))*step()));
      track.scrollTo({left:target,behavior:'smooth'});
    })});
    track.addEventListener('scroll',function(){update();clearTimeout(idle);idle=setTimeout(function(){target=null},150)},{passive:true});
    window.addEventListener('resize',update);
    update();
  });

  // gallery: category filters + full-size viewer; without JS each photo just links to its big file
  var gal=document.querySelector('[data-gallery]');
  if(gal){
    var items=[].slice.call(gal.querySelectorAll('.gi')),bar=document.querySelector('.g-filters');
    if(bar){
      bar.hidden=false;
      bar.addEventListener('click',function(e){
        var c=e.target.closest('[data-filter]');if(!c)return;
        bar.querySelectorAll('[data-filter]').forEach(function(x){x.setAttribute('aria-pressed',String(x===c))});
        items.forEach(function(it){it.hidden=c.dataset.filter!=='all'&&it.dataset.cat!==c.dataset.filter});
      });
    }
    var lb=document.querySelector('dialog.lb');
    if(lb&&typeof lb.showModal==='function'){
      var big=lb.querySelector('img'),cap=lb.querySelector('figcaption'),cur=0,last;
      function shown(){return items.filter(function(it){return !it.hidden})}
      function show(i){
        var v=shown();cur=(i+v.length)%v.length;var it=v[cur],im=it.querySelector('img');
        big.src=it.querySelector('a').getAttribute('href').replace(/\.jpg$/,'.webp');  // browsers with <dialog> all read WebP
        big.alt=im.alt;
        big.width=im.getAttribute('width')*2;big.height=im.getAttribute('height')*2;
        cap.textContent=it.querySelector('figcaption').textContent;
      }
      gal.addEventListener('click',function(e){
        var a=e.target.closest('.gi a');if(!a)return;
        e.preventDefault();last=a;show(shown().indexOf(a.parentNode));lb.showModal();
      });
      lb.querySelector('.lb-close').addEventListener('click',function(){lb.close()});
      lb.querySelector('.lb-prev').addEventListener('click',function(){show(cur-1)});
      lb.querySelector('.lb-next').addEventListener('click',function(){show(cur+1)});
      lb.addEventListener('click',function(e){if(e.target===lb||e.target.tagName==='FIGURE')lb.close()});
      lb.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
      lb.addEventListener('close',function(){if(last)last.focus()});
    }
  }

  // contact form: ?topic= preselects, submit opens WhatsApp
  var f=document.querySelector('form[data-wa]');
  if(!f)return;
  var sel=$('topic');
  var t=new URLSearchParams(location.search).get('topic');
  t=(t||'').toLowerCase().replace(/[^a-z-]/g,'');
  if(t&&sel.querySelector('option[value="'+t+'"]'))sel.value=t;
  var note=$('f-note');
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var name=$('f-name').value.trim();
    if(!name){note.textContent='Add your name so the team knows who to reply to.';$('f-name').focus();return}
    var org=$('f-org').value.trim(),msg=$('f-msg').value.trim();
    var want=sel.options[sel.selectedIndex].text;
    var text='Hi NCF, my name is '+name+(org?' from '+org:'')+'. I would like to: '+want+'.'+(msg?' '+msg:'');
    var url='https://wa.me/'+f.dataset.wa+'?text='+encodeURIComponent(text);
    // no 'noopener' feature: with it, window.open always returns null and the fallback fired too
    var w=window.open(url,'_blank');
    if(w)w.opener=null;else location.href=url;
    note.textContent='Your message is ready in WhatsApp. If it did not open, message 081 516 1673 directly.';
  });
})();
