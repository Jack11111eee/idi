// 前端最小逻辑:EventSource 订阅 SSE、事件渲染进工作面板、探针控制(§4.1)。
// 原生 JS,无框架无构建(D-P1-1);注释一律中文,遵守简单优先。

// DOM 句柄
const eventsEl = document.getElementById('ai-events');
const pingBtn = document.getElementById('btn-ping');
const abortBtn = document.getElementById('btn-abort');
const pathInput = document.getElementById('project-path-input');
const routeSelect = document.getElementById('ai-route-select');
const panelHeader = document.getElementById('ai-panel-header');
const panelBody = document.getElementById('ai-panel-body');

// ---------------------------------------------------------------------------
// SSE 订阅:事件 → 工作面板条目
// ---------------------------------------------------------------------------

function initEventSource() {
  const source = new EventSource('/api/events');
  source.onmessage = (msg) => {
    let event;
    try {
      event = JSON.parse(msg.data);
    } catch {
      renderEvent({ kind: 'error', content: '事件解析失败', raw: msg.data });
      return;
    }
    renderEvent(event);
  };
}

// kind → 标签(与后端统一事件枚举一一对应)
const KIND_LABELS = {
  say: '说话', read: '读文件', write: '写文件',
  command: '执行', result: '结果', error: '错误', done: '结束',
};

// 渲染一条事件到工作面板
function renderEvent(event) {
  const item = document.createElement('div');
  item.className = `event-item kind-${event.kind}`;

  const label = document.createElement('span');
  label.className = 'event-kind';
  label.textContent = KIND_LABELS[event.kind] || event.kind;
  item.appendChild(label);

  const content = document.createElement('div');
  content.className = 'event-content';
  if (event.kind === 'say' && window.marked) {
    // AI 说话内容按 markdown 渲染
    content.innerHTML = window.marked.parse(event.content || '');
  } else {
    // 工具事件显示目标路径/命令;结果与错误折行展示
    content.textContent = event.content || '';
  }
  item.appendChild(content);

  eventsEl.appendChild(item);
  eventsEl.scrollTop = eventsEl.scrollHeight; // 保持最新可见

  // 终止事件:解除「发起」按钮禁用(流结束能再次发起)
  if (event.kind === 'done' || event.kind === 'error') {
    pingBtn.disabled = false;
    eventsEl.classList.remove('streaming');
  }
}

// ---------------------------------------------------------------------------
// 面板折叠(点击标题切换)
// ---------------------------------------------------------------------------

panelHeader.addEventListener('click', () => {
  const collapsed = panelBody.classList.toggle('collapsed');
  panelHeader.querySelector('.collapse-indicator').textContent = collapsed ? '▸' : '▾';
});

// ---------------------------------------------------------------------------
// 探针控制:路线切换(POST /api/config) / 发起测试调用 / 中止
// ---------------------------------------------------------------------------

// 路线下拉:切换即写回 config.json 的 ai_caller 键(运行时换线,不重进程)
routeSelect.addEventListener('change', async () => {
  const resp = await fetch('/api/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ai_caller: routeSelect.value }),
  });
  if (!resp.ok) {
    renderEvent({ kind: 'error', content: '路线切换失败', raw: null });
  }
});

// 页面加载时把下拉同步为当前后端配置
(async () => {
  try {
    const resp = await fetch('/api/config');
    const data = await resp.json();
    if (data.config && data.config.ai_caller) {
      routeSelect.value = data.config.ai_caller;
    }
  } catch { /* 后端不可达时保留默认 */ }
})();

pingBtn.addEventListener('click', async () => {
  const project_path = pathInput.value.trim();
  if (!project_path) {
    renderEvent({ kind: 'error', content: '请先输入项目目录', raw: null });
    return;
  }
  pingBtn.disabled = true;      // 进行中禁止重复发起
  eventsEl.classList.remove('streaming');
  eventsEl.innerHTML = ''; // 新调用清空旧直播
  renderEvent({ kind: 'say', content: `已发起调用(${routeSelect.value} 路线),等待事件…`, raw: null });
  eventsEl.classList.add('streaming'); // 流式中的面板标记(中止时用于切换为「已中止」)
  await fetch('/api/dev/ping', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      project_path,
      prompt: '读取本目录下任意一个文件并向我说明它的内容',
    }),
  });
  // 后台线程实际执行;按钮解禁在收到终止事件时进行(见 renderEvent)
});

abortBtn.addEventListener('click', async () => {
  await fetch('/api/abort', { method: 'POST' });
  if (eventsEl.classList.contains('streaming')) {
    eventsEl.classList.remove('streaming');
    eventsEl.classList.add('aborted'); // 正在流式中的面板 → 「已中止」
    setTimeout(() => eventsEl.classList.remove('aborted'), 3000);
  }
  renderEvent({ kind: 'error', content: '已中止(用户切断当前调用)', raw: null });
  pingBtn.disabled = false;
});

// 绑定后即启动订阅
initEventSource();

// ---------------------------------------------------------------------------
// claude CLI 自检浮层(§7.1:只挡第一次;后端不缓存失败,重检即再调)
// ---------------------------------------------------------------------------
const overlay = document.getElementById('cli-check-overlay');
const overlayMsg = document.getElementById('cli-check-message');
const recheckBtn = document.getElementById('cli-recheck-btn');

async function runCliCheck() {
  try {
    const resp = await fetch('/api/cli-check');
    const r = await resp.json();
    if (r.ok) {
      overlay.classList.add('hidden'); // 通过:放行,不再挡
    } else {
      overlayMsg.textContent = r.guidance; // 中文指引文案
      overlay.classList.remove('hidden');
    }
  } catch {
    // 自检端点不可达不挡界面(骨架原则:不崩溃)
  }
}

recheckBtn.addEventListener('click', runCliCheck);
runCliCheck();
