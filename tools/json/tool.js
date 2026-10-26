'use strict';
const $=id=>document.getElementById(id),LIMIT=2*1024*1024;
function notify(message,error=false){$('message').textContent=message;$('message').classList.toggle('error',error);}
function update(){ $('input-size').textContent=`${$('source').value.length.toLocaleString()} 字元`;$('output-size').textContent=`${$('result').value.length.toLocaleString()} 字元`;}
function perform(mode){const input=$('source').value;if(!input.trim()){notify('請先輸入 JSON',true);return;}if(new Blob([input]).size>LIMIT){notify('輸入超過 2 MB 安全限制',true);return;}try{const data=JSON.parse(input);if(mode==='validate'){$('result').value='';notify('✓ JSON 格式正確（僅語法驗證，不代表符合業務 Schema）');}else{$('result').value=JSON.stringify(data,null,mode==='format'?2:0);notify(`✓ ${mode==='format'?'已格式化':'已壓縮'} · ${$('result').value.length} 字元`);}update();}catch(e){$('result').value='';notify(`✕ JSON 語法錯誤：${e.message}`,true);update();}}
$('source').addEventListener('input',update);
for(const mode of ['format','compact','validate'])$(mode).addEventListener('click',()=>perform(mode));
$('sample').addEventListener('click',()=>{$('source').value='{"project":"EveMissLab","status":"preview","features":["format","validate","compact"],"version":1}';$('result').value='';update();notify('已填入公開範例');});
$('clear').addEventListener('click',()=>{$('source').value='';$('result').value='';update();notify('內容已清除');});
$('copy').addEventListener('click',async()=>{if(!$('result').value){notify('目前沒有可複製的處理結果',true);return;}try{await navigator.clipboard.writeText($('result').value);notify('✓ 已複製結果');}catch{notify('瀏覽器不允許剪貼簿存取；請手動選取結果',true);}});
$('save').addEventListener('click',()=>{const t=$('result').value;if(!t){notify('請先產生處理結果',true);return;}const blob=new Blob([t+'\n'],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='evemisslab-json-result.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('✓ 已送出本機下載');});
$('file').addEventListener('change',async e=>{const file=e.target.files?.[0];if(!file)return;if(file.size>LIMIT){notify('檔案超過 2 MB 安全限制',true);e.target.value='';return;}try{$('source').value=await file.text();$('result').value='';update();notify(`✓ 已讀取本機檔案：${file.name}（尚未驗證 JSON）`);}catch{notify('讀取檔案失敗',true);}e.target.value='';});
update();
