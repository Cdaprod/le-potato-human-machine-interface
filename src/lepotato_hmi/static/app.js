const $ = id => document.getElementById(id);
const eyes = $('eyes');
const storedToken = sessionStorage.getItem('hmi_token') || '';
const authHeaders = () => storedToken ? {Authorization: `Bearer ${storedToken}`} : {};

function glance(){
  const x = Math.round((Math.random()-.5)*28), y = Math.round((Math.random()-.5)*17);
  document.querySelectorAll('.eye i').forEach(p=>p.style.transform=`translate(${x}px,${y}px)`);
}
setInterval(glance,2100);
setInterval(()=>{eyes.classList.add('blink');setTimeout(()=>eyes.classList.remove('blink'),150)},4300);
function setMood(value){
  $('mood').textContent=value;
  const size=value.startsWith('happy')?'90px':value.startsWith('concerned')?'105px':'115px';
  document.querySelectorAll('.eye').forEach(el=>el.style.height=size);
}
async function api(path, options={}){
  const response=await fetch(path,{...options,headers:{...authHeaders(),...(options.headers||{})}});
  if(response.status===401){sessionStorage.removeItem('hmi_token');window.location.replace('/');throw Error('Authentication required')}
  if(!response.ok)throw Error(`${response.status} ${await response.text()}`);
  return response.json();
}
async function refresh(){
  try{
    const [status,devices,events]=await Promise.all([
      api('/api/status'),api('/api/devices'),api('/api/events')
    ]);
    $('status').textContent=JSON.stringify(status,null,2);
    $('devices').textContent=devices.length?JSON.stringify(devices,null,2):'No USB serial devices found';
    $('events').textContent=events.slice(0,30)
      .map(e=>`${e.timestamp} ${e.kind} ${JSON.stringify(e.payload)}`).join('\n')||'No events';
    setMood(`${status.expression.mood} · ${status.expression.detail}`);
  }catch(error){$('feedback').textContent=error.message}
}
$('test').onsubmit=async event=>{
  event.preventDefault();
  const form=new FormData(event.target);
  try{
    await api('/api/test-event',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(Object.fromEntries(form))});
    await refresh();
  }catch(error){$('feedback').textContent=error.message}
};
$('publish').onsubmit=async event=>{
  event.preventDefault();
  const form=new FormData(event.target);
  let payload=form.get('payload');
  try{payload=JSON.parse(payload)}catch{}
  try{
    await api('/api/mqtt/publish',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({topic:form.get('topic'),payload})});
    $('feedback').textContent='Queued for MQTT publication';
  }catch(error){$('feedback').textContent=error.message}
};
refresh();setInterval(refresh,3000);
