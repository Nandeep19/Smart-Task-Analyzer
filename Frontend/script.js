const tasks = [];
function renderTasks(){
  const el = document.getElementById('task-list');
  el.innerHTML = '';
  tasks.forEach(t=>{
    const li = document.createElement('li');
    li.className='task-item';
    li.textContent = `${t.id} — ${t.title} (imp:${t.importance} est:${t.estimated_hours} deps:${t.dependencies.join(',')})`;
    el.appendChild(li);
  });
}
document.getElementById('task-form').addEventListener('submit', (e)=>{
  e.preventDefault();
  const t = {
    id: document.getElementById('id').value.trim(),
    title: document.getElementById('title').value.trim(),
    due_date: document.getElementById('due_date').value.trim() || null,
    estimated_hours: Number(document.getElementById('estimated_hours').value) || undefined,
    importance: Number(document.getElementById('importance').value) || undefined,
    dependencies: document.getElementById('dependencies').value.split(',').map(s=>s.trim()).filter(Boolean)
  };
  tasks.push(t);
  renderTasks();
});
document.getElementById('analyze').addEventListener('click', async ()=>{
  const bulk = document.getElementById('bulk').value.trim();
  let payloadTasks = tasks.slice();
  if(bulk){
    try{
      const parsed = JSON.parse(bulk);
      if(Array.isArray(parsed)) payloadTasks = parsed;
    }catch(e){
      alert('Invalid JSON in bulk input');
      return;
    }
  }
  if(payloadTasks.length===0){ alert('No tasks to analyze'); return; }
  const strategy = document.getElementById('strategy').value;
  try{
    const res = await fetch('/api/tasks/analyze/', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({tasks: payloadTasks, strategy})
    });
    const data = await res.json();
    if(res.status !== 200){ alert('Error: '+(data.error || JSON.stringify(data))); return; }
    renderResult(data.results);
  }catch(e){
    alert('Request failed: '+e.message);
  }
});
function renderResult(results){
  const out = document.getElementById('result');
  out.innerHTML='';
  results.forEach(r=>{
    const div = document.createElement('div');
    const level = r.score >= 0.6 ? 'high' : (r.score >= 0.35 ? 'medium' : 'low');
    div.className = level;
    div.style.padding='8px'; div.style.margin='6px 0';
    div.innerHTML = `<strong>${r.title}</strong> — score: ${r.score}<br/><em>${r.explanation}</em><br/><small>${JSON.stringify(r.details)}</small>`;
    out.appendChild(div);
  });
}
