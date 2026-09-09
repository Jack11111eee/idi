// 前端最小逻辑:EventSource 订阅 SSE、事件渲染进工作面板、探针控制(§4.1)。
// 原生 JS,无框架无构建(D-P1-1);注释一律中文,遵守简单优先。

// DOM 句柄
const eventsEl = document.getElementById('ai-events');
const pingBtn = document.getElementById('btn-ping');
const abortBtn = document.getElementById('btn-abort');
const pathInput = document.getElementById('project-path-input');
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
}

// ---------------------------------------------------------------------------
// 面板折叠(点击标题切换)
// ---------------------------------------------------------------------------

panelHeader.addEventListener('click', () => {
  const collapsed = panelBody.classList.toggle('collapsed');
  panelHeader.querySelector('.collapse-indicator').textContent = collapsed ? '▸' : '▾';
});

// ---------------------------------------------------------------------------
// 探针控制:发起测试调用 / 中止
// ---------------------------------------------------------------------------

pingBtn.addEventListener('click', async () => {
  const project_path = pathInput.value.trim();
  if (!project_path) {
    renderEvent({ kind: 'error', content: '请先输入项目目录', raw: null });
    return;
  }
  eventsEl.innerHTML = ''; // 新调用清空旧直播
  renderEvent({ kind: 'say', content: '已发起调用,等待事件…', raw: null });
  await fetch('/api/dev/ping', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      project_path,
      prompt: '读取本目录下任意一个文件并向我说明它的内容',
    }),
  });
});

abortBtn.addEventListener('click', async () => {
  await fetch('/api/abort', { method: 'POST' });
  renderEvent({ kind: 'error', content: '已中止(用户切断当前调用)', raw: null });
  eventsEl.classList.add('aborted');
  setTimeout(() => eventsEl.classList.remove('aborted'), 800);
});

// 绑定后即启动订阅
initEventSource();
