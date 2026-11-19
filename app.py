import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DEADZONE: Nightmare", page_icon="🧟", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 50% 0%,#17251d,#070b09 65%);color:#eaffef}
[data-testid="stHeader"],footer,#MainMenu{visibility:hidden}
.block-container{padding-top:1rem;max-width:1100px}
.dz-title{text-align:center;font:800 clamp(32px,6vw,56px) Orbitron,sans-serif;letter-spacing:5px;color:#eaffef;text-shadow:0 0 12px #39ff83,0 0 32px #16874b}
.dz-sub{text-align:center;color:#86a995;letter-spacing:3px;font-size:11px;margin:0 0 12px}
</style>
<div class="dz-title">DEADZONE</div>
<div class="dz-sub">NIGHTMARE PROTOCOL • SURVIVE THE OUTBREAK</div>
""", unsafe_allow_html=True)

game = r"""
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}body{margin:0;background:transparent;color:#eaffef;font-family:Arial,sans-serif;overflow:hidden}
.hud{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin:8px 0}
.stat{background:#0b1710;border:1px solid #28603d;border-radius:9px;padding:7px 9px;text-align:center;min-width:0}
.lab{font-size:9px;letter-spacing:1.5px;color:#83ad91}.val{font-size:18px;font-weight:800;color:#dfffe8;text-shadow:0 0 8px #39ff83}
canvas{display:block;width:100%;height:auto;aspect-ratio:16/10;border:1px solid #34754a;border-radius:12px;background:#0a100d;touch-action:none;cursor:crosshair;box-shadow:0 0 22px #35ff8022}
.controls{display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin:9px 0}
button{padding:10px 13px;border-radius:8px;border:1px solid #32754b;background:#102b1b;color:#dfffea;font-weight:800;letter-spacing:.5px;cursor:pointer}
button.primary{background:linear-gradient(135deg,#39ed7e,#13864a);color:#03150a;border:0}
.help{text-align:center;color:#789b85;font-size:11px;line-height:1.7}
@media(max-width:600px){.hud{grid-template-columns:repeat(3,1fr)}.val{font-size:16px}button{padding:9px 10px;font-size:11px}}
</style></head><body>
<div class="hud">
 <div class="stat"><div class="lab">WAVE</div><div class="val" id="wave">0</div></div>
 <div class="stat"><div class="lab">KILLS</div><div class="val" id="kills">0</div></div>
 <div class="stat"><div class="lab">HEALTH</div><div class="val" id="hp">100</div></div>
 <div class="stat"><div class="lab">AMMO</div><div class="val" id="ammo">18/72</div></div>
 <div class="stat"><div class="lab">CREDITS</div><div class="val" id="cash">0</div></div>
 <div class="stat"><div class="lab">BEST KILLS</div><div class="val" id="best">0</div></div>
</div>
<canvas id="g" width="960" height="600" tabindex="0" aria-label="DEADZONE zombie survival game"></canvas>
<div class="controls">
 <button class="primary" id="start">START NIGHTMARE</button>
 <button id="reload">RELOAD [R]</button>
 <button id="dash">DASH [SHIFT]</button>
 <button id="shop">FIELD SHOP [E]</button>
 <button id="sound">SOUND: ON</button>
</div>
<div class="help">MOVE: WASD / ARROWS • AIM: MOUSE • FIRE: HOLD CLICK • RELOAD: R • DASH: SHIFT • SHOP: E<br>Defeat waves, earn credits, buy upgrades. An Alpha boss arrives every 5 waves. Best score is saved in this browser.</div>
<script>
(()=>{
const c=document.getElementById('g'),ctx=c.getContext('2d'),W=960,H=600,$=id=>document.getElementById(id);
let state='menu',keys={},mouse={x:650,y:300,down:false},p=null,z=[],bullets=[],particles=[],medkits=[];
let wave=0,kills=0,hp=100,maxHp=100,cash=0,ammo=18,mag=18,reserve=72,damage=38,fireDelay=11,lastShot=0;
let reloadT=0,dashT=0,dashCD=0,spawnLeft=0,spawnTimer=0,shop=false,sound=true,audio=null,frame=0,best=0;
try{best=+(localStorage.getItem('deadzoneNightmareBest')||0)}catch(e){}
$('best').textContent=best;
const rand=(a,b)=>Math.random()*(b-a)+a,dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
function beep(freq=250,dur=.06,type='square',vol=.025){
 if(!sound)return;
 try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();
 let o=audio.createOscillator(),g=audio.createGain();o.type=type;o.frequency.value=freq;g.gain.setValueAtTime(vol,audio.currentTime);g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+dur);o.connect(g);g.connect(audio.destination);o.start();o.stop(audio.currentTime+dur)}catch(e){}
}
function startRun(){
 p={x:W/2,y:H/2,r:14,speed:3.15,inv:0};z=[];bullets=[];particles=[];medkits=[];
 wave=0;kills=0;hp=maxHp=100;cash=0;ammo=mag=18;reserve=72;damage=38;fireDelay=11;
 reloadT=dashT=dashCD=0;shop=false;nextWave();beep(170,.16,'triangle');
}
function nextWave(){
 wave++;spawnLeft=7+wave*4;spawnTimer=30;state='play';
 if(wave%5===0)spawnLeft++;
}
function spawnZombie(boss=false){
 let side=Math.floor(rand(0,4));
 let x=side===0?-30:side===1?W+30:rand(0,W);
 let y=side===2?-30:side===3?H+30:rand(0,H);
 let h=boss?900:42+wave*11;
 z.push({x,y,r:boss?31:rand(13,18),hp:h,max:h,speed:boss?0.82:0.92+Math.min(wave*.035,.8),boss,hit:0,attack:0});
}
function shoot(){
 if(state!=='play'||shop||reloadT||frame-lastShot<fireDelay)return;
 if(ammo<=0){beep(85,.05);return}
 ammo--;lastShot=frame;
 let a=Math.atan2(mouse.y-p.y,mouse.x-p.x);
 bullets.push({x:p.x+Math.cos(a)*19,y:p.y+Math.sin(a)*19,vx:Math.cos(a)*12,vy:Math.sin(a)*12,life:70,damage});
 beep(115,.04,'square',.018);
 for(let i=0;i<3;i++)particles.push({x:p.x+Math.cos(a)*20,y:p.y+Math.sin(a)*20,vx:rand(-2,2),vy:rand(-2,2),life:10,color:'#ffd18a'});
}
function reload(){
 if(state!=='play'||reloadT||ammo===mag||reserve<=0)return;
 reloadT=82;beep(160,.1,'sine');
}
function dash(){
 if(state!=='play'||dashCD>0)return;
 dashT=11;dashCD=155;p.inv=19;beep(620,.08,'triangle');
}
function buy(type){
 const cost={heal:35,damage:65,ammo:25,mag:85,armor:90}[type];
 if(cash<cost)return;
 cash-=cost;
 if(type==='heal')hp=Math.min(maxHp,hp+45);
 if(type==='damage')damage+=14;
 if(type==='ammo')reserve+=54;
 if(type==='mag'){mag+=4;ammo=mag}
 if(type==='armor'){maxHp+=25;hp+=25}
 beep(520,.08,'sine');
}
function toggleShop(){if(state==='play')shop=!shop}
$('start').onclick=startRun;$('reload').onclick=reload;$('dash').onclick=dash;$('shop').onclick=toggleShop;
$('sound').onclick=()=>{sound=!sound;$('sound').textContent='SOUND: '+(sound?'ON':'OFF')};
window.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();keys[k]=true;
 if([' ','arrowup','arrowdown','arrowleft','arrowright'].includes(k))e.preventDefault();
 if(k==='r')reload();if(k==='shift')dash();if(k==='e')toggleShop();
 if(k==='escape')shop=false;
});
window.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect();mouse.x=(e.clientX-r.left)/r.width*W;mouse.y=(e.clientY-r.top)/r.height*H});
c.addEventListener('pointerdown',e=>{
 const r=c.getBoundingClientRect();mouse.x=(e.clientX-r.left)/r.width*W;mouse.y=(e.clientY-r.top)/r.height*H;
 if(shop){let idx=Math.floor((mouse.y-(H/2-108))/43);['heal','damage','ammo','mag','armor'].forEach((t,i)=>{if(i===idx)buy(t)});return}
 if(state==='menu'||state==='over'){startRun();return}
 mouse.down=true;c.setPointerCapture(e.pointerId);
});
c.addEventListener('pointerup',()=>mouse.down=false);c.addEventListener('pointercancel',()=>mouse.down=false);
function gameOver(){
 if(state!=='play')return;state='over';beep(65,.42,'sawtooth',.05);
 if(kills>best){best=kills;$('best').textContent=best;try{localStorage.setItem('deadzoneNightmareBest',String(best))}catch(e){}}
}
function update(){
 frame++;if(state!=='play')return;
 if(reloadT>0&&--reloadT===0){let n=Math.min(mag-ammo,reserve);ammo+=n;reserve-=n;beep(330,.08,'sine')}
 if(dashCD>0)dashCD--;if(dashT>0)dashT--;if(p.inv>0)p.inv--;
 let dx=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0);
 let dy=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0),m=Math.hypot(dx,dy)||1;
 let sp=dashT?10.5:p.speed;p.x=Math.max(16,Math.min(W-16,p.x+dx/m*sp));p.y=Math.max(16,Math.min(H-16,p.y+dy/m*sp));
 if(mouse.down)shoot();
 if(spawnLeft>0&&--spawnTimer<=0){spawnZombie(wave%5===0&&spawnLeft===1);spawnLeft--;spawnTimer=Math.max(12,49-wave*1.7)}
 bullets.forEach(b=>{
  b.x+=b.vx;b.y+=b.vy;b.life--;
  for(const e of z){if(!b.dead&&dist(b,e)<e.r+4){e.hp-=b.damage;e.hit=5;b.dead=true;
   for(let i=0;i<4;i++)particles.push({x:b.x,y:b.y,vx:rand(-2,2),vy:rand(-2,2),life:16,color:e.boss?'#ff5278':'#8dff9e'});
   if(e.hp<=0){e.dead=true;kills++;cash+=e.boss?150:12;if(Math.random()<.14)medkits.push({x:e.x,y:e.y,r:9})}
   break;
  }}
 });
 bullets=bullets.filter(b=>b.life>0&&!b.dead);
 for(const e of z){
  let a=Math.atan2(p.y-e.y,p.x-e.x);e.x+=Math.cos(a)*e.speed;e.y+=Math.sin(a)*e.speed;if(e.hit>0)e.hit--;
  if(dist(p,e)<p.r+e.r&&p.inv<=0){hp-=e.boss?1.15:.58;p.inv=6;if(hp<=0){hp=0;gameOver()}}
 }
 z=z.filter(e=>!e.dead);
 for(const m of medkits){if(dist(p,m)<p.r+m.r){hp=Math.min(maxHp,hp+24);m.dead=true;beep(720,.08,'sine')}}
 medkits=medkits.filter(m=>!m.dead);
 particles.forEach(a=>{a.x+=a.vx;a.y+=a.vy;a.life--});particles=particles.filter(a=>a.life>0);
 if(spawnLeft===0&&z.length===0){state='between';setTimeout(()=>{if(state==='between')nextWave()},1700)}
 $('wave').textContent=wave;$('kills').textContent=kills;$('hp').textContent=Math.ceil(hp);
 $('ammo').textContent=reloadT?'RELOAD':ammo+'/'+reserve;$('cash').textContent=cash;
}
function text(t,y,size,color){ctx.textAlign='center';ctx.font='800 '+size+'px Orbitron,Arial';ctx.fillStyle=color;ctx.shadowColor=color;ctx.shadowBlur=14;ctx.fillText(t,W/2,y);ctx.shadowBlur=0}
function draw(){
 ctx.fillStyle='#0a100d';ctx.fillRect(0,0,W,H);
 ctx.strokeStyle='rgba(75,135,88,.13)';ctx.lineWidth=1;
 for(let x=0;x<W;x+=40){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}
 for(let y=0;y<H;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}
 for(let i=0;i<20;i++){let x=(i*173+40)%W,y=(i*97+30)%H;ctx.fillStyle='rgba(100,30,35,.17)';ctx.beginPath();ctx.arc(x,y,5+i%4*2,0,7);ctx.fill()}
 medkits.forEach(m=>{ctx.fillStyle='#55ff91';ctx.shadowColor='#55ff91';ctx.shadowBlur=15;ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,7);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#06200e';ctx.font='bold 13px Arial';ctx.textAlign='center';ctx.fillText('+',m.x,m.y+4)});
 bullets.forEach(b=>{ctx.fillStyle='#ffe4a5';ctx.shadowColor='#ffb347';ctx.shadowBlur=12;ctx.beginPath();ctx.arc(b.x,b.y,4,0,7);ctx.fill();ctx.shadowBlur=0});
 z.forEach(e=>{
  ctx.save();ctx.translate(e.x,e.y);ctx.fillStyle=e.hit?'#fff':e.boss?'#a51d48':'#397b49';ctx.shadowColor=e.boss?'#ff225f':'#55ff77';ctx.shadowBlur=e.boss?22:9;ctx.beginPath();ctx.arc(0,0,e.r,0,7);ctx.fill();ctx.shadowBlur=0;
  ctx.fillStyle='#101510';ctx.beginPath();ctx.arc(-5,-3,2.7,0,7);ctx.arc(5,-3,2.7,0,7);ctx.fill();
  ctx.fillStyle='#14251a';ctx.fillRect(-e.r,-e.r-10,e.r*2,5);ctx.fillStyle='#ff426b';ctx.fillRect(-e.r,-e.r-10,e.r*2*Math.max(0,e.hp/e.max),5);
  if(e.boss){ctx.fillStyle='#ffb7c7';ctx.font='bold 11px Arial';ctx.textAlign='center';ctx.fillText('ALPHA',0,-e.r-17)}ctx.restore();
 });
 particles.forEach(a=>{ctx.globalAlpha=Math.max(0,a.life/16);ctx.fillStyle=a.color;ctx.fillRect(a.x,a.y,3,3)});ctx.globalAlpha=1;
 if(p){
  let a=Math.atan2(mouse.y-p.y,mouse.x-p.x);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a);ctx.fillStyle='#c6d9ca';ctx.fillRect(0,-4,27,8);ctx.restore();
  ctx.fillStyle=p.inv%4<2?'#d9ffe3':'#42e982';ctx.shadowColor='#3cff8b';ctx.shadowBlur=15;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,7);ctx.fill();ctx.shadowBlur=0;
 }
 ctx.strokeStyle='#d2ffdf';ctx.lineWidth=1.4;ctx.beginPath();ctx.arc(mouse.x,mouse.y,9,0,7);ctx.moveTo(mouse.x-14,mouse.y);ctx.lineTo(mouse.x-5,mouse.y);ctx.moveTo(mouse.x+5,mouse.y);ctx.lineTo(mouse.x+14,mouse.y);ctx.moveTo(mouse.x,mouse.y-14);ctx.lineTo(mouse.x,mouse.y-5);ctx.moveTo(mouse.x,mouse.y+5);ctx.lineTo(mouse.x,mouse.y+14);ctx.stroke();
 if(state==='menu'||state==='over'||state==='between'||shop){
  ctx.fillStyle='rgba(2,7,5,.82)';ctx.fillRect(0,0,W,H);
  if(state==='menu'){text('DEADZONE',H/2-65,48,'#baffcb');text('NIGHTMARE PROTOCOL',H/2-18,20,'#ff6682');text('CLICK START NIGHTMARE',H/2+48,16,'#d4f8dc');text('WASD MOVE • MOUSE AIM • HOLD CLICK TO FIRE',H/2+82,13,'#91b89d');text('ALPHA BOSS EVERY 5 WAVES',H/2+118,13,'#ffb1bd')}
  if(state==='over'){text('YOU DIED',H/2-55,48,'#ff5575');text('KILLS '+kills+'  •  WAVE '+wave,H/2+2,23,'#e4ffe9');text('BEST KILLS '+best,H/2+42,16,'#f4d48d');text('CLICK RESTART TO ENTER AGAIN',H/2+87,14,'#a9efbb')}
  if(state==='between'){text('WAVE CLEARED',H/2-10,34,'#8effac');text('THE NEXT HORDE IS COMING',H/2+30,15,'#b4d8bf')}
  if(shop){
   text('FIELD UPGRADES',H/2-133,28,'#baffcb');
   const opts=[['MEDKIT +45 HP','heal',35],['DAMAGE +14','damage',65],['AMMO +54','ammo',25],['MAGAZINE +4','mag',85],['MAX HEALTH +25','armor',90]];
   opts.forEach((o,i)=>{let y=H/2-95+i*43;ctx.fillStyle='#102a1c';ctx.fillRect(W/2-205,y-23,410,35);ctx.fillStyle='#d6ffe0';ctx.font='bold 15px Arial';ctx.textAlign='center';ctx.fillText(o[0]+'  •  $'+o[2],W/2,y)});
   text('CLICK AN UPGRADE • PRESS E TO CLOSE',H/2+145,12,'#8fb69c');
  }
 }
}
function loop(){update();draw();requestAnimationFrame(loop)}loop();
})();
</script></body></html>
"""
components.html(game, height=760, scrolling=False)
st.markdown('<div style="text-align:center;color:#789b85;font-size:11px;letter-spacing:1px">DEADZONE • NIGHTMARE PROTOCOL • PYTHON + HTML5 CANVAS</div>', unsafe_allow_html=True)
