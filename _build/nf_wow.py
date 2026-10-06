# -*- coding: utf-8 -*-
DAY = '''
<section class="nf-day" id="dia-solar" data-day>
  <div class="nf-day-stage">
    <svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
      <defs>
        <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop id="sk1" offset="0" stop-color="#0A192F"/><stop id="sk2" offset="1" stop-color="#E9905B"/></linearGradient>
        <radialGradient id="sunG"><stop offset="0" stop-color="#FFE7A8"/><stop offset=".55" stop-color="#FFC861"/><stop offset="1" stop-color="#FFC861" stop-opacity="0"/></radialGradient>
        <linearGradient id="pnG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1B4D6B"/><stop offset="1" stop-color="#0F2E45"/></linearGradient>
        <linearGradient id="glG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#FFE7A8" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      </defs>
      <rect width="1600" height="900" fill="url(#skyG)"/>
      <g id="stars" fill="#fff">
        <circle cx="120" cy="90" r="2"/><circle cx="300" cy="160" r="1.5"/><circle cx="520" cy="70" r="2"/><circle cx="760" cy="130" r="1.4"/><circle cx="980" cy="60" r="2"/>
        <circle cx="1180" cy="150" r="1.6"/><circle cx="1400" cy="90" r="2"/><circle cx="1520" cy="200" r="1.4"/><circle cx="660" cy="230" r="1.2"/><circle cx="1300" cy="250" r="1.2"/>
      </g>
      <path id="sunPath" d="M 150 700 Q 800 -170 1450 700" fill="none"/>
      <g id="sun"><circle r="150" fill="url(#sunG)" opacity=".55"/><circle r="58" fill="#FFD983"/></g>
      <!-- Andes -->
      <path d="M0 640 L180 560 L300 600 L430 520 L560 590 L700 540 L820 600 L980 500 L1120 585 L1260 530 L1400 590 L1600 545 L1600 900 L0 900 Z" fill="#2B3E6E" opacity=".75"/>
      <path d="M0 700 L240 610 L380 650 L520 560 L590 548 L660 560 L800 640 L960 600 L1100 650 L1300 590 L1450 640 L1600 610 L1600 900 L0 900 Z" fill="#1F2F55"/>
      <path d="M520 560 L590 548 L660 560 L630 575 L605 566 L578 578 L552 570 Z" fill="#E8EDF5" opacity=".85"/>
      <rect y="742" width="1600" height="158" fill="#121D36"/>
      <g id="panels">
        <g transform="translate(330 760)"><polygon points="0,60 70,0 250,0 180,60" fill="url(#pnG)" stroke="#10B981" stroke-width="2"/><rect x="120" y="60" width="8" height="40" fill="#0C1528"/><polygon class="gl" points="0,60 70,0 250,0 180,60" fill="url(#glG)" opacity="0"/></g>
        <g transform="translate(610 760)"><polygon points="0,60 70,0 250,0 180,60" fill="url(#pnG)" stroke="#10B981" stroke-width="2"/><rect x="120" y="60" width="8" height="40" fill="#0C1528"/><polygon class="gl" points="0,60 70,0 250,0 180,60" fill="url(#glG)" opacity="0"/></g>
        <g transform="translate(890 760)"><polygon points="0,60 70,0 250,0 180,60" fill="url(#pnG)" stroke="#10B981" stroke-width="2"/><rect x="120" y="60" width="8" height="40" fill="#0C1528"/><polygon class="gl" points="0,60 70,0 250,0 180,60" fill="url(#glG)" opacity="0"/></g>
        <g transform="translate(1170 760)"><polygon points="0,60 70,0 250,0 180,60" fill="url(#pnG)" stroke="#10B981" stroke-width="2"/><rect x="120" y="60" width="8" height="40" fill="#0C1528"/><polygon class="gl" points="0,60 70,0 250,0 180,60" fill="url(#glG)" opacity="0"/></g>
        <g transform="translate(50 760)"><polygon points="0,60 70,0 250,0 180,60" fill="url(#pnG)" stroke="#10B981" stroke-width="2"/><rect x="120" y="60" width="8" height="40" fill="#0C1528"/><polygon class="gl" points="0,60 70,0 250,0 180,60" fill="url(#glG)" opacity="0"/></g>
      </g>
      <!-- curva de producción -->
      <path d="M 150 880 C 450 880, 600 790, 800 790 S 1150 880, 1450 880" fill="none" stroke="rgba(16,185,129,.25)" stroke-width="3" stroke-dasharray="6 8"/>
      <path id="prodLine" d="M 150 880 C 450 880, 600 790, 800 790 S 1150 880, 1450 880" fill="none" stroke="#10B981" stroke-width="4" stroke-linecap="round"/>
    </svg>
    <div class="nf-day-hud">
      <p class="x-eyebrow">Simulación en vivo</p>
      <h2>Un día con <b>energía solar</b> en Ecuador</h2>
      <p class="nf-day-cap" id="dayCap">Baja para ver cómo trabaja una planta solar desde que sale el sol.</p>
    </div>
    <div class="nf-day-stats">
      <div class="clock"><small>Hora</small><b id="dClock">06:00</b></div>
      <div><small>Produciendo ahora</small><b><span id="dKw">0</span> kW</b></div>
      <div><small>Energía generada hoy</small><b><span id="dKwh">0</span> kWh</b></div>
      <div><small>Ahorro de hoy</small><b>$<span id="dUsd">0</span></b></div>
    </div>
    <p class="nf-day-note">Simulación referencial de una planta de 100 kWp en Quito, con tarifa de $0.10 por kWh.</p>
  </div>
</section>
'''

CALC = '''
<section class="x-sec" id="calculadora">
  <div class="x-wrap">
    <div class="x-head x-rv"><p class="x-eyebrow" style="text-align:center">Calculadora solar</p><h2 class="x-h2">¿Cuánto ahorraría tu empresa con energía solar?</h2><p class="x-lead">Mueve los valores y mira el resultado al instante. En 10 segundos sabrás si vale la pena hablar con nosotros.</p></div>
    <div class="nf-calc x-rv" data-scalc>
      <div class="nf-calc-in">
        <h3>Tu consumo eléctrico</h3><p>Usa el valor aproximado de tu planilla de luz.</p>
        <div class="nf-f"><label for="sc-bill">Factura mensual de luz <output id="o-bill">$1,500</output></label>
          <input type="range" id="sc-bill" min="100" max="20000" step="50" value="1500"><div class="hint"><span>$100</span><span>$20,000</span></div></div>
        <div class="nf-f"><label>Tarifa aproximada por kWh</label>
          <div class="nf-seg" id="sc-tar"><button type="button" data-t="0.08">$0.08 · Industrial</button><button type="button" data-t="0.10" class="on">$0.10 · Comercial</button><button type="button" data-t="0.12">$0.12</button></div></div>
        <div class="nf-f"><label for="sc-cov">Consumo que quieres cubrir con sol <output id="o-cov">80%</output></label>
          <input type="range" id="sc-cov" min="30" max="100" step="5" value="80"><div class="hint"><span>30%</span><span>100%</span></div></div>
      </div>
      <div class="nf-calc-out">
        <div class="nf-big"><small>Ahorro estimado al año</small><b id="r-year">$0</b></div>
        <div class="nf-kpis">
          <div><small>Ahorro al mes</small><b id="r-month">$0</b></div>
          <div><small>Recuperas la inversión en</small><b id="r-pay">–</b></div>
          <div><small>Tamaño de la planta</small><b id="r-kwp">0 kWp</b></div>
          <div><small>Área de techo aprox.</small><b id="r-area">0 m²</b></div>
          <div><small>CO₂ evitado al año</small><b id="r-co2">0 t</b></div>
          <div><small>Paneles de 550 W</small><b id="r-pan">0</b></div>
        </div>
        <div class="nf-panels" id="r-viz" aria-hidden="true"></div>
        <div class="x-btns"><a href="#" class="x-btn x-btn-g" id="r-wa" target="_blank" rel="noopener">Quiero mi estudio solar</a><a href="#contacto" class="x-btn nf-btn-w" id="r-form">Llenar formulario</a></div>
      </div>
    </div>
    <p class="nf-calc-note">Estimación referencial: rendimiento de 120 kWh por kWp al mes, inversión de $900 a $1,200 por kWp instalado y factor de emisión de 0.4 kg CO₂ por kWh. El valor real depende del estudio técnico de tu sitio.</p>
  </div>
</section>
'''

JS = r'''
<script>
(function(){
  const $=s=>document.querySelector(s);
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* ---------- Un día con energía solar ---------- */
  const day=$('[data-day]');
  if(day){
    const path=$('#sunPath'),sun=$('#sun'),L=path.getTotalLength(),stars=$('#stars'),gls=[...document.querySelectorAll('#panels .gl')];
    const prod=$('#prodLine'),PL=prod.getTotalLength();prod.style.strokeDasharray=PL;prod.style.strokeDashoffset=PL;
    const sk1=$('#sk1'),sk2=$('#sk2'),cap=$('#dayCap');
    const K=[[0,'#141F3A','#C9745A'],[.14,'#41639E','#F4B887'],[.5,'#3B78C2','#A8D3F2'],[.84,'#2E4374','#EE9457'],[1,'#07111F','#3A3F6B']];
    const hx=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)),mix=(a,b,k)=>'#'+hx(a).map((v,i)=>Math.round(v+(hx(b)[i]-v)*k).toString(16).padStart(2,'0')).join('');
    const sky=t=>{for(let i=0;i<K.length-1;i++){if(t<=K[i+1][0]){const k=(t-K[i][0])/(K[i+1][0]-K[i][0]);return[mix(K[i][1],K[i+1][1],k),mix(K[i][2],K[i+1][2],k)];}}return[K[4][1],K[4][2]];};
    const caps=[[.1,'Amanecer: los paneles empiezan a despertar.'],[.36,'Media mañana: la planta ya cubre buena parte del consumo.'],[.64,'Mediodía en la línea ecuatorial: máxima producción.'],[.9,'Tarde: sigue generando mientras tu equipo trabaja.']];
    const fmt=n=>Math.round(n).toLocaleString('en-US');
    function render(t){
      const u=Math.min(1,Math.max(0,(t-.04)/.92)),p=Math.max(0,Math.sin(Math.PI*u))*(t>.04&&t<.96?1:0);
      const pt=path.getPointAtLength(L*Math.min(1,Math.max(0,t)));sun.setAttribute('transform','translate('+pt.x+' '+pt.y+')');
      const c=sky(t);sk1.setAttribute('stop-color',c[0]);sk2.setAttribute('stop-color',c[1]);
      stars.setAttribute('opacity',Math.max(0,1-t*8,(t-.9)*8).toFixed(2));
      gls.forEach(g=>g.setAttribute('opacity',(p*.8).toFixed(2)));
      prod.style.strokeDashoffset=PL*(1-u);
      const E=420*(1-Math.cos(Math.PI*u))/2,mins=360+t*750;
      $('#dClock').textContent=String(Math.floor(mins/60)).padStart(2,'0')+':'+String(Math.floor(mins%60)).padStart(2,'0');
      $('#dKw').textContent=fmt(p*85);$('#dKwh').textContent=fmt(E);$('#dUsd').textContent=fmt(E*.10);
      let txt='Atardecer: hoy esta planta ahorró $'+fmt(E*.10)+' con energía del sol.';
      for(const [lim,s] of caps){if(t<lim){txt=s;break;}}
      if(t<.02)txt='Baja para ver cómo trabaja una planta solar desde que sale el sol.';
      if(cap.textContent!==txt)cap.textContent=txt;
    }
    render(0);
    if(window.gsap&&window.ScrollTrigger&&!reduce){
      ScrollTrigger.create({trigger:day,start:'top top',end:'+=260%',pin:'.nf-day-stage',scrub:.6,onUpdate:s=>render(s.progress)});
      ScrollTrigger.refresh();
    }else render(.7);
  }

  /* ---------- Calculadora solar ---------- */
  const box=$('[data-scalc]');
  if(box){
    const bill=$('#sc-bill'),cov=$('#sc-cov');let tar=.10,last=-1;
    const usd=n=>'$'+Math.round(n).toLocaleString('en-US');
    const anim=(el,to,f)=>{const from=+(el.dataset.v||0);el.dataset.v=to;
      if(window.gsap&&!reduce){const o={v:from};gsap.to(o,{v:to,duration:.5,ease:'power2.out',onUpdate:()=>el.textContent=f(o.v)});}else el.textContent=f(to);};
    function calc(){
      const b=+bill.value,c=+cov.value/100,kwh=b/tar,target=kwh*c,kwp=target/120,pan=Math.ceil(kwp*1000/550),area=pan*2.6,
            sm=target*tar,sy=sm*12,lo=kwp*900/sy,hi=kwp*1200/sy,co2=target*12*.4/1000;
      $('#o-bill').textContent=usd(b);$('#o-cov').textContent=Math.round(c*100)+'%';
      anim($('#r-year'),sy,usd);anim($('#r-month'),sm,usd);
      anim($('#r-kwp'),kwp,v=>v.toFixed(1)+' kWp');anim($('#r-area'),area,v=>Math.round(v).toLocaleString('en-US')+' m²');
      anim($('#r-co2'),co2,v=>v.toFixed(1)+' t');anim($('#r-pan'),pan,v=>Math.round(v).toLocaleString('en-US'));
      $('#r-pay').textContent=lo.toFixed(1)+' a '+hi.toFixed(1)+' años';
      if(pan!==last){const viz=$('#r-viz'),n=Math.min(pan,60);
        viz.innerHTML=Array.from({length:n},(_,i)=>'<i style="animation-delay:'+(i*12)+'ms"></i>').join('')+(pan>60?'<em>+'+(pan-60).toLocaleString('en-US')+' paneles</em>':'');last=pan;}
      const msg='Hola Nasfeco, quiero un estudio de energía solar para mi empresa. Mi factura de luz es de '+usd(b)+' al mes y quiero cubrir el '+Math.round(c*100)+'% con sol. La calculadora estima una planta de '+kwp.toFixed(1)+' kWp y un ahorro de '+usd(sy)+' al año.';
      $('#r-wa').href='https://wa.me/593997312362?text='+encodeURIComponent(msg);
      $('#r-form').onclick=()=>{const d=$('#n_details'),s=$('#n_service');if(d)d.value=msg.replace('Hola Nasfeco, quiero','Quiero');if(s)s.value='Energía solar';};
    }
    bill.addEventListener('input',calc);cov.addEventListener('input',calc);
    document.querySelectorAll('#sc-tar button').forEach(b=>b.addEventListener('click',()=>{tar=+b.dataset.t;document.querySelectorAll('#sc-tar button').forEach(x=>x.classList.toggle('on',x===b));calc();}));
    calc();
  }
})();
</script>
'''
