// sidebar.js - minimal, non-invasive conversation list manager
(function(){
  const KEY = 'beatmind_convos_meta_v1';
  const listEl = document.getElementById('sb-convo-list');
  const newBtn = document.getElementById('sb-new-btn');
  const clearBtn = document.getElementById('sb-clear-btn');

  let convos = []; // { id, title, created, lastTs }

  function load() {
    try {
      convos = JSON.parse(localStorage.getItem(KEY) || '[]');
    } catch(e) { convos = []; console.error(e); }
  }
  function save() {
    localStorage.setItem(KEY, JSON.stringify(convos));
  }

  function idNow(){ return 'c_' + Date.now().toString(36); }
  function render() {
    if(!listEl) return;
    listEl.innerHTML = '';
    convos.forEach(c => {
      const el = document.createElement('div');
      el.className = 'convo-item';
      el.dataset.id = c.id;
      el.innerHTML = `<div style="font-weight:600">${escapeHtml(c.title || 'Untitled')}</div>
                      <div style="opacity:.6;font-size:.85rem">${new Date(c.lastTs||c.created).toLocaleString()}</div>`;
      el.addEventListener('click', ()=>select(c.id));
      listEl.appendChild(el);
    });
  }

  function createNew() {
    const c = { id: idNow(), title: 'New conversation', created: Date.now(), lastTs: Date.now() };
    convos.unshift(c);
    save();
    render();
    // notify app (other scripts can listen)
    dispatchSelect(c.id, c);
  }

  function select(id) {
    const c = convos.find(x=>x.id===id);
    if(!c) return;
    // update lastTs
    c.lastTs = Date.now();
    // move to front
    convos = [c].concat(convos.filter(x=>x.id!==id));
    save(); render();
    dispatchSelect(c.id, c);
  }

  function clearAll() {
    if(!confirm('Clear all conversations from local storage?')) return;
    convos = []; save(); render();
    // dispatch event to let other code know there's nothing active
    const ev = new CustomEvent('convo-cleared');
    window.dispatchEvent(ev);
  }

  function dispatchSelect(id, convo) {
    const ev = new CustomEvent('convo-selected', { detail: { id, convo }});
    window.dispatchEvent(ev);
  }

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, (c)=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
  }

  // init
  load();
  render();
  if(newBtn) newBtn.addEventListener('click', createNew);
  if(clearBtn) clearBtn.addEventListener('click', clearAll);

  // expose small API for other scripts
  window.BeatMindSidebar = {
    getConvos: () => convos,
    create: createNew,
    selectById: (id) => select(id),
    updateTitle: (id, title) => {
      const c = convos.find(x=>x.id===id);
      if(!c) return;
      c.title = title; c.lastTs = Date.now();
      save(); render();
    },
    remove: (id) => {
      convos = convos.filter(x=>x.id!==id); save(); render();
    }
  };

})();
