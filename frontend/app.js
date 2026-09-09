// 前端逻辑:进入项目 / 会话流 / SSE 事件分发 / 权限弹窗 / 草稿区渲染(§4.1/§4.2)。
// 原生 JS,无框架无构建(D-P1-1);注释一律中文,遵守简单优先。

// DOM 句柄
const eventsEl = document.getElementById('ai-events');
const pingBtn = document.getElementById('btn-ping');
const abortBtn = document.getElementById('btn-abort');
const pathInput = document.getElementById('project-path-input');
const routeSelect = document.getElementById('ai-route-select');
const panelHeader = document.getElementById('ai-panel-header');
const panelBody = document.getElementById('ai-panel-body');

// 会话相关句柄
const enterForm = document.getElementById('enter-form');
const enterPathInput = document.getElementById('enter-path-input');
const enterBtn = document.getElementById('btn-enter');
const stateBadge = document.getElementById('state-badge');
const draftView = document.getElementById('draft-view');
const draftContent = document.getElementById('draft-content');
const draftEmpty = document.getElementById('draft-empty');
const roundsPlaceholder = document.getElementById('rounds-placeholder');
const roundsHint = document.getElementById('rounds-hint');
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('btn-send');
const permissionModal = document.getElementById('permission-modal');
const permissionMessage = document.getElementById('permission-message');
const permissionAllowBtn = document.getElementById('btn-permission-allow');
const permissionDenyBtn = document.getElementById('btn-permission-deny');

// 发散与 G1 句柄(FLOW-06 / FLOW-03)
const divergenceEntry = document.getElementById('divergence-entry');
const divergenceBtn = document.getElementById('btn-divergence');
const brainstormView = document.getElementById('brainstorm-view');
const brainstormContent = document.getElementById('brainstorm-content');
const approveDraftBtn = document.getElementById('btn-approve-draft');
const approveHint = document.getElementById('approve-hint');

// 当前会话状态(前端侧;权威判定在后端 derive_state)
let currentProject = null;
let currentState = null;
let streamingBubble = null; // 流式中的 AI 气泡

// §7.4 状态中文名(derive_state 返回值 → 界面徽标)
const STATE_LABELS = {
  phase1_new: '新讨论(阶段 1)',
  phase12_in_progress: '阶段 1-2 讨论中',
  phase3: '轮次阶段(阶段 3)',
  phase4: '撰写中(阶段 4)',
  phase5_awaiting_tier: '待选自检档(阶段 5)',
  phase5_checking: '自检进行中(阶段 5)',
  mission_complete: '使命完成',
};

// ---------------------------------------------------------------------------
// markdown 渲染(XSS 安全:关闭 raw HTML,标签转义后渲染 —— T-idi03-02)
// ---------------------------------------------------------------------------

function renderMarkdown(text) {
  if (!window.marked) return document.createTextNode(text || '');
  // marked v12:配置禁用原始 HTML 注入(sanitize 双保险)
  marked.setOptions({ mangle: false, headerIds: false });
  const html = marked.parse(String(text || ''));
  // 解析后仍剥离 script/style/iframe/on* 属性(AI 内容不可信)
  const tpl = document.createElement('template');
  tpl.innerHTML = html;
  stripUnsafeNodes(tpl.content);
  const frag = document.createDocumentFragment();
  frag.appendChild(tpl.content.cloneNode(true));
  return frag;
}

function stripUnsafeNodes(root) {
  const banned = ['SCRIPT', 'STYLE', 'IFRAME', 'OBJECT', 'EMBED', 'LINK'];
  root.querySelectorAll(banned.join(',')).forEach((n) => n.remove());
  root.querySelectorAll('*').forEach((el) => {
    [...el.attributes].forEach((attr) => {
      // 事件处理器属性与 javascript: 链接一律剥离
      if (attr.name.startsWith('on') || (attr.name === 'href' && attr.value.trim().startsWith('javascript:'))) {
        el.removeAttribute(attr.name);
      }
    });
  });
}

// ---------------------------------------------------------------------------
// SSE 订阅:事件 → 会话气泡 / 工作面板 / 权限弹窗
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
    dispatchEvent_(event);
  };
}

function dispatchEvent_(event) {
  // 会话流侧:kind=say 流式进 AI 气泡;permission_request 弹确认框
  if (event.kind === 'say') {
    appendSayToChat(event.content || '');
  }
  if (event.kind === 'permission_request') {
    showPermissionModal(event);
  }
  // 工作面板:全部事件原样展示(透明优先,§4.3)
  renderEvent(event);
  // done:收尾会话气泡 + 拉新草稿
  if (event.kind === 'done' || event.kind === 'error') {
    if (streamingBubble) {
      streamingBubble = null;
    }
    refreshDraftAfterStream();
    pingBtn.disabled = false;
  }
}

// kind → 标签(与后端统一事件枚举一一对应)
const KIND_LABELS = {
  say: '说话', read: '读文件', write: '写文件',
  command: '执行', result: '结果', error: '错误', done: '结束',
  permission_request: '权限', permission_resolved: '权限',
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
    // AI 说话内容按 markdown 渲染(经 stripUnsafeNodes 防 XSS)
    content.appendChild(renderMarkdown(event.content || ''));
  } else {
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
// 会话流:消息气泡(用户右对齐、AI 左对齐、AI markdown 渲染)
// ---------------------------------------------------------------------------

function makeBubble(role) {
  const bubble = document.createElement('div');
  bubble.classList.add('chat-bubble', role === 'user' ? 'chat-user' : 'chat-ai');
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return bubble;
}

function appendChatMessage(role, content) {
  const bubble = makeBubble(role);
  if (role === 'ai' && window.marked) {
    bubble.appendChild(renderMarkdown(content));
  } else {
    bubble.textContent = content;
  }
  return bubble;
}

function appendSayToChat(text) {
  if (!streamingBubble) {
    streamingBubble = makeBubble('ai');
    streamingBubble.classList.add('streaming-ai');
  }
  const p = document.createElement('div');
  p.className = 'say-chunk';
  p.appendChild(renderMarkdown(text));
  streamingBubble.appendChild(p);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function renderTranscript(transcript) {
  chatMessages.innerHTML = '';
  (transcript || []).forEach((m) => appendChatMessage(m.role, m.content));
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ---------------------------------------------------------------------------
// 进入项目(FLOW-01)/ 发消息(FLOW-02)/ 权限(AI-04):fetch 封装
// ---------------------------------------------------------------------------

async function enterProject(path) {
  const resp = await fetch('/api/enter', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path }),
  });
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    renderEvent({ kind: 'error', content: `进入失败:${err.message || resp.status}`, raw: null });
    return null;
  }
  const data = await resp.json();
  currentProject = path;
  currentState = data.state;
  applySessionView(data);
  return data;
}

function applySessionView(data) {
  // 状态徽标 + 门控 + 文档渲染 + 会话流恢复(进入项目 / G1 定稿后整页重建视图)
  applySessionGates(data);
  renderTranscript(data.transcript);
}

function applySessionGates(data) {
  // 状态徽标(中文名,右上角)
  stateBadge.textContent = STATE_LABELS[data.state] || data.state;
  stateBadge.classList.remove('hidden');

  // 子视图切换:阶段 1-2 → draft-view;阶段 3+ → rounds-placeholder
  if (data.state === 'phase1_new' || data.state === 'phase12_in_progress') {
    draftView.classList.remove('hidden');
    roundsPlaceholder.classList.add('hidden');
  } else {
    draftView.classList.add('hidden');
    roundsPlaceholder.classList.remove('hidden');
    if (data.state === 'phase3' && data.current_round) {
      roundsHint.textContent = `已进入轮次阶段(本阶段占位)。当前轮:第 ${data.current_round} 轮。`;
    }
  }

  renderDraft(data.draft);
  renderBrainstorm(data.brainstorm);

  // 发散入口(§3.7:仅阶段 1-2 且雏形诞生前开放)
  if (
    (data.state === 'phase1_new' || data.state === 'phase12_in_progress') &&
    data.divergence_available
  ) {
    divergenceEntry.classList.remove('hidden');
  } else {
    divergenceEntry.classList.add('hidden');
  }

  // 「认可雏形」按钮(§4.4 常驻草稿区末尾):有雏形且未定稿才可点
  if (data.g1_available) {
    approveDraftBtn.disabled = false;
    approveDraftBtn.title = '点击即定稿为 discuss-round-1.md,进入轮次阶段(不可回退)';
    approveHint.textContent = '定稿后进入轮次阶段,不可退回阶段 1-2 会话;draft.md 保留。';
    approveHint.classList.remove('hidden');
  } else {
    approveDraftBtn.disabled = true;
    approveHint.classList.add('hidden');
    approveDraftBtn.title = data.draft
      ? '已定稿——项目已在轮次阶段'
      : '先要有雏形草稿才能认可';
  }
}

function renderDraft(draft) {
  if (draft == null || draft === '') {
    draftContent.innerHTML = '';
    draftEmpty.classList.remove('hidden');
  } else {
    draftContent.innerHTML = '';
    draftContent.appendChild(renderMarkdown(draft));
    draftEmpty.classList.add('hidden');
  }
}

function renderBrainstorm(brainstorm) {
  // 发散候选区:brainstorm.md 有内容才显示(流后拉新 GET /api/brainstorm 也走这里)
  if (brainstorm == null || brainstorm === '') {
    brainstormView.classList.add('hidden');
    brainstormContent.innerHTML = '';
  } else {
    brainstormContent.innerHTML = '';
    brainstormContent.appendChild(renderMarkdown(brainstorm));
    brainstormView.classList.remove('hidden');
  }
}

async function refreshDraftAfterStream() {
  // done 后拉新草稿(AI 可能在调用中写了 draft.md)
  if (currentProject == null) return;
  try {
    const resp = await fetch('/api/draft');
    const data = await resp.json();
    if (data.status === 'ok') renderDraft(data.draft);
  } catch { /* 拉不到保持现状 */ }
  // 发散结束后 brainstorm.md 就绪——同拍拉新(Wave 3:发散产物呈现)
  await refreshBrainstormAfterStream();
  // 拉新门控(G-idi01-7):门控全部由磁盘推导,流结束后视磁盘现状重判——
  // 草稿出来了「认可雏形」就地解禁、发散入口就地关闭,无需手动重进目录。
  await refreshGatesAfterStream();
}

async function refreshGatesAfterStream() {
  if (currentProject == null) return;
  try {
    const resp = await fetch('/api/session');
    if (!resp.ok) return;
    const data = await resp.json();
    if (data.status === 'ok') applySessionGates(data);
  } catch { /* 拉不到保持现状 */ }
}

async function refreshBrainstormAfterStream() {
  if (currentProject == null) return;
  try {
    const resp = await fetch('/api/brainstorm');
    const data = await resp.json();
    if (data.status === 'ok') renderBrainstorm(data.brainstorm);
  } catch { /* 拉不到保持现状 */ }
}

async function sendMessage(text) {
  if (!currentProject) {
    appendChatMessage('user', '(请先进入项目目录)');
    return;
  }
  const resp = await fetch('/api/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (resp.status === 202) return true;
  const err = await resp.json().catch(() => ({}));
  appendChatMessage('ai', `(发送被拒:${err.message || resp.status})`);
  return false;
}

function showPermissionModal(event) {
  permissionMessage.textContent = event.summary || `AI 请求使用工具 ${event.tool}`;
  permissionModal.classList.remove('hidden');
  const respond = async (approved) => {
    permissionModal.classList.add('hidden');
    await fetch('/api/permission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: event.id, approved }),
    }).catch(() => { /* 网络失败:后端 abort 时会强制释放 */ });
  };
  permissionAllowBtn.onclick = () => respond(true);
  permissionDenyBtn.onclick = () => respond(false);
}

// ---------------------------------------------------------------------------
// 绑定:进入 / 发送(含回车)/ 权限按钮
// ---------------------------------------------------------------------------

enterBtn.addEventListener('click', () => enterProject(enterPathInput.value.trim()));

enterPathInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') enterProject(enterPathInput.value.trim());
});

sendBtn.addEventListener('click', () => {
  const text = messageInput.value.trim();
  if (!text) return;
  messageInput.value = '';
  appendChatMessage('user', text);
  sendMessage(text);
});

messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const text = messageInput.value.trim();
    if (!text) return;
    messageInput.value = '';
    appendChatMessage('user', text);
    sendMessage(text);
  }
});

// ---------------------------------------------------------------------------
// 发散模式(FLOW-06 §3.7):「没想法」入口 → POST /api/divergence,过程走 SSE 直播
// ---------------------------------------------------------------------------

divergenceBtn.addEventListener('click', async () => {
  if (!currentProject) {
    renderEvent({ kind: 'error', content: '请先进入项目目录', raw: null });
    return;
  }
  divergenceBtn.disabled = true;
  renderEvent({
    kind: 'say',
    content: '已发起发散模式,多视角风暴进行中(事件照常直播)……',
    raw: null,
  });
  try {
    const resp = await fetch('/api/divergence', { method: 'POST' });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      renderEvent({
        kind: 'error',
        content: `发散发起失败:${err.message || resp.status}`,
        raw: null,
      });
    }
  } catch {
    renderEvent({ kind: 'error', content: '发散发起失败(网络)', raw: null });
  } finally {
    // 解禁在收到终止事件时进行(done/error 后);两拍防连点
    setTimeout(() => { divergenceBtn.disabled = false; }, 1500);
  }
});

// ---------------------------------------------------------------------------
// G1 认可雏形(FLOW-03 §4.4):direct-through 交互形态——点击即 POST /api/g1,零确认
// (前置决策门已定:DESIGN.md §4.4 字面 = 常驻按钮、点击即 G1 通过;不可回滚门由
//  后端幂等防护承担——已定稿时后端 409)
// ---------------------------------------------------------------------------

approveDraftBtn.addEventListener('click', async () => {
  if (approveDraftBtn.disabled) return;
  approveDraftBtn.disabled = true;
  try {
    const resp = await fetch('/api/g1', { method: 'POST' });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      renderEvent({
        kind: 'error',
        content: `定稿失败:${data.message || resp.status}`,
        raw: null,
      });
      // 已定稿(409 幂等防)以外的失败:按钮恢复,让用户处理后再点
      approveDraftBtn.disabled = data.message && data.message.includes('已定稿');
      return;
    }
    renderEvent({
      kind: 'say',
      content: '雏形已定稿为 discuss-round-1.md,进入轮次阶段。draft.md 已保留。',
      raw: null,
    });
    // 定稿成功:重进(POST /api/enter)刷新状态,切到轮次视图
    await enterProject(currentProject);
  } catch {
    renderEvent({ kind: 'error', content: '定稿请求失败(网络)', raw: null });
    approveDraftBtn.disabled = false;
  }
});

// ---------------------------------------------------------------------------
// 面板折叠(点击标题切换)
// ---------------------------------------------------------------------------

panelHeader.addEventListener('click', () => {
  const collapsed = panelBody.classList.toggle('collapsed');
  panelHeader.querySelector('.collapse-indicator').textContent = collapsed ? '▸' : '▾';
});

// ---------------------------------------------------------------------------
// 探针控制:路线切换(POST /api/config) / 发起测试调用 / 中止(Plan 01 保留)
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
