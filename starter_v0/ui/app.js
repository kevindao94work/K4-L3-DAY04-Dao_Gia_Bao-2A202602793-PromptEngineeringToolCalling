let state=null,busy=false;
const $=id=>document.getElementById(id);
function el(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function pretty(value){return JSON.stringify(value,null,2);}
function replyText(text){try{const x=JSON.parse(text);return x.reply||text;}catch{return text;}}
function render(){
 $('version').textContent=`${state.version} · ${state.runtime_version}\n${state.provider} / ${state.model}\n${state.artifact_version}`;
 $('export').disabled=!state.turns.length;
 if(state.turns.length){$('messages').replaceChildren();for(const turn of state.turns){
  const article=el('article',undefined,'turn');article.append(el('div',`LƯỢT ${turn.turn_index} · ${turn.status}`,'turn-meta'),el('p',turn.user,'user'),el('p',replyText(turn.assistant_text||''),'assistant'));
  if(turn.invalidated_pending_ticket)article.append(el('p','Bản xác nhận cũ đã hết hiệu lực.','small'));
  for(const event of turn.tool_events||[]){const error=event.result?.error;const details=el('details',undefined,error?'tool error':'tool');details.open=true;
   details.append(el('summary',`${event.tool} · ${error?'LỖI: '+error:event.executed?'Đã thực thi':'Chưa thực thi'}`),el('h4','Đầu vào'),el('pre',pretty(event.args)),el('h4','Kết quả thực tế'),el('pre',pretty(event.result)));article.append(details);}
  if(!(turn.tool_events||[]).length)article.append(el('p','Không gọi công cụ.','small'));
  $('messages').append(article);
 }}else{$('messages').replaceChildren(el('h2','Bắt đầu với một yêu cầu'),el('p','Bạn có thể bổ sung thông tin, sửa ý hoặc hủy ở lượt sau.'));}
 $('pending').hidden=!state.pending_ticket;if(state.pending_ticket)$('payload').textContent=pretty(state.pending_ticket.payload);
 $('messages').lastElementChild?.scrollIntoView({behavior:'smooth',block:'nearest'});
}
async function api(path,body={}){
 busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);$('status').textContent='Đang xử lý…';
 try{const res=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-Helpdesk-UI':'1'},body:JSON.stringify({session_id:state?.transcript_id,...body})});const data=await res.json();if(!res.ok)throw new Error(data.error||res.status);state=data;render();$('status').textContent='Đã lưu hội thoại cục bộ.';}
 catch(e){$('status').textContent='Không hoàn thành: '+e.message;}
 finally{busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);$('export').disabled=!state?.turns.length;}
}
$('composer').addEventListener('submit',e=>{e.preventDefault();if(busy||!$('message').value.trim())return;const text=$('message').value;$('message').value='';api('send',{message:text});});
$('new').onclick=()=>api('new');$('confirm').onclick=()=>api('confirm',{confirmation_id:state.pending_ticket?.confirmation_id});$('cancel').onclick=()=>api('cancel');
for(const b of document.querySelectorAll('.example'))b.onclick=()=>{$('message').value=b.textContent;$('message').focus();};
$('export').onclick=()=>{const a=el('a');a.href=URL.createObjectURL(new Blob([pretty(state)],{type:'application/json'}));a.download=state.transcript_id+'.transcript.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
api('new');
