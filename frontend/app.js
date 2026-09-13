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
const roundTitle = document.getElementById('round-title');
const roundSwitcher = document.getElementById('round-switcher');
const roundDoc = document.getElementById('round-doc');
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

// 轮次批注流句柄(D-P2-20:阶段 3 侧栏切换为批注流)
const annotationsPanel = document.getElementById('annotations-panel');
const pendingCount = document.getElementById('pending-count');
const annotationList = document.getElementById('annotation-list');
const processRoundBtn = document.getElementById('btn-process-round');

// 划词小菜单句柄(D-P2-1)
const selectionMenu = document.getElementById('selection-menu');
const annotateBtn = document.getElementById('btn-annotate');
const plainAskBtn = document.getElementById('btn-plain-ask');

// 阶段 3/4/5 视图句柄(PLAN idi-03-04)
const authorizeRow = document.getElementById('authorize-row');
const authorizeBtn = document.getElementById('btn-authorize');
const authorizeHint = document.getElementById('authorize-hint');
const confirmationModal = document.getElementById('confirmation-modal');
const confirmWordInput = document.getElementById('confirm-word-input');
const confirmAuthorizeBtn = document.getElementById('btn-confirm-authorize');
const confirmCancelBtn = document.getElementById('btn-confirm-cancel');
const confirmError = document.getElementById('confirm-error');
const writingView = document.getElementById('writing-view');
const startWritingBtn = document.getElementById('btn-start-writing');
const writingHint = document.getElementById('writing-hint');
const tierModal = document.getElementById('tier-modal');
const tierLooseBtn = document.getElementById('btn-tier-loose');
const tierStrictBtn = document.getElementById('btn-tier-strict');
const checksPanel = document.getElementById('checks-panel');
const checkState = document.getElementById('check-state');
const checkSwitcher = document.getElementById('check-switcher');
const latestCheck = document.getElementById('latest-check');
const verdictCards = document.getElementById('verdict-cards');
const continueCheckBtn = document.getElementById('btn-continue-check');
const continueRepairBtn = document.getElementById('btn-continue-repair');

// 当前会话状态(前端侧;权威判定在后端 derive_state)
let currentProject = null;
let currentState = null;
let streamingBubble = null; // 流式中的 AI 气泡
let currentRoundNumber = null;   // phase3 当前轮号(点击「处理本轮批注」的目标)
let displayedRoundNumber = null; // 当前显示的轮号(切换器切历史轮时 < currentRoundNumber)
let processInFlight = false;     // 「处理本轮批注」在飞标记(SSE done 后拉新的判据)
let writingInFlight = false;     // 「撰写/继续撰写」在飞标记(done 后拉新的判据)
let checkInFlight = false;       // 「继续自检/继续修复」在飞标记(done 后拉新的判据)
let tierModalShown = false;      // 档位模态本会话是否已弹过(防重复弹,不落盘)

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
    // 处理本轮批注在飞时 done/error 都收尾:拉新轮次链(新当前轮+上轮冻结)+
    // 恢复按钮(refreshRoundsAfterStream 内 applySessionGates 会重算按钮态,
    // 这里补保险恢复文案)
    if (processInFlight) {
      processInFlight = false;
      processRoundBtn.textContent = '处理本轮批注';
      processRoundBtn.title = '仅阶段 3 当前轮可用';
      refreshRoundsAfterStream();
    }
    // 撰写在飞:done 后拉新链(session → phase5_awaiting_tier 档位视图,D-P3-27)
    if (writingInFlight) {
      writingInFlight = false;
      refreshRoundsAfterStream();
    }
    // 自检/修复在飞:done 后拉新链(session + checks 报告与 mode 控件)
    if (checkInFlight) {
      refreshChecksAfterStream();
    }
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

  // 只读归档防线复位(归档分支内再逐面隐藏;其余态恢复可用,D-P3-25)
  processRoundBtn.classList.remove('hidden');
  messageInput.disabled = false;
  sendBtn.disabled = false;

  // 子视图切换:阶段 1-2 → draft-view;阶段 3+ → rounds-placeholder
  if (data.state === 'phase1_new' || data.state === 'phase12_in_progress') {
    draftView.classList.remove('hidden');
    roundsPlaceholder.classList.add('hidden');
    annotationsPanel.classList.add('hidden'); // 阶段 1-2 侧栏是会话流(D-P2-2)
  } else {
    draftView.classList.add('hidden');
    roundsPlaceholder.classList.remove('hidden');
    if (data.state === 'phase3' && data.current_round) {
      // phase3:真轮次视图(文档渲染 + 批注流侧栏 + 计数);D-P2-20
      currentRoundNumber = data.current_round;
      pendingCount.textContent = `本轮批注未处理 ${data.pending_annotations}`;
      annotationsPanel.classList.remove('hidden');
      applyPhase3Extras(data);
      loadRoundsView(data.current_round);
    } else if (data.state === 'phase4') {
      // 阶段 4:撰写视图(按钮文案二态纯消费 snapshot.writing_tmp_exists,D-P3-10)
      annotationsPanel.classList.add('hidden');
      hidePhase3Extras();
      applyWritingView(data);
    } else if (data.state === 'phase5_awaiting_tier' || data.state === 'phase5_checking') {
      // 阶段 5:自检报告视图(awaiting_tier 额外弹档位模态/呈「开始自检」)
      annotationsPanel.classList.add('hidden');
      hidePhase3Extras();
      applyPhase5View(data);
    } else {
      // mission_complete:占位维持现状(本计划后续切片替换归档视图)
      annotationsPanel.classList.add('hidden');
      checksPanel.classList.add('hidden');
      hidePhase3Extras();
      roundsHint.textContent = `当前状态:${STATE_LABELS[data.state] || data.state}(视图在本计划后续切片呈现)。`;
      roundsHint.classList.remove('hidden');
      roundDoc.innerHTML = '';
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

// ---------------------------------------------------------------------------
// 阶段 3 G3 授权入口 + 阶段 4 撰写视图 + 阶段 5 报告视图 + 归档视图
// (PLAN idi-03-04;FLOW-05 / DATA-02 / DATA-03 / DATA-04)
// ---------------------------------------------------------------------------

// 非 phase3 态:隐藏 G3 授权行与撰写视图(两个容器都只在各自阶段呈现)
function hidePhase3Extras() {
  authorizeRow.classList.add('hidden');
  writingView.classList.add('hidden');
  checksPanel.classList.add('hidden');
  roundSwitcher.classList.remove('hidden');
}

// phase3:G3 授权行三态(照 g1_available 先例,D-P3-26 按钮点亮 = 四查全过)
function applyPhase3Extras(data) {
  writingView.classList.add('hidden');
  authorizeRow.classList.remove('hidden');
  if (data.g3_available) {
    authorizeBtn.disabled = false;
    authorizeBtn.title = '四处机械校验已全部通过——点击开始授权';
    authorizeHint.textContent = '点击后需输入确认词「确认授权」;不输入或不放行即视为拒绝(记为一条普通批注)。';
    authorizeHint.classList.remove('hidden');
  } else {
    authorizeBtn.disabled = true;
    authorizeBtn.title = '四处机械校验尚未全部通过:annotations/清单/维度表/授权标记';
    authorizeHint.textContent = '四处机械校验全部通过后按钮才会点亮(annotations 无待处理 + 未决清单清零 + 维度表全绿 + 授权标记为「是」)。';
    authorizeHint.classList.remove('hidden');
  }
}

// phase4:撰写视图(按钮文案二态纯消费 snapshot.writing_tmp_exists,D-P3-10 字面)
function applyWritingView(data) {
  roundsHint.classList.add('hidden');
  roundTitle.textContent = '撰写总设计文档';
  roundSwitcher.classList.add('hidden');
  roundDoc.innerHTML = '';
  writingView.classList.remove('hidden');
  if (data.writing_tmp_exists) {
    startWritingBtn.textContent = '继续撰写(检测到上次中断的半成品,重写覆盖)';
    writingHint.textContent = '残留的半份 tmp 将被整体覆盖重写(上次撰写中途崩溃,重跑即恢复,无需重新确认词)。';
  } else {
    startWritingBtn.textContent = '撰写总设计文档';
    writingHint.textContent = 'AI 将撰写总设计文档并整体落盘;过程在 AI 工作面板全程直播。';
  }
  writingHint.classList.remove('hidden');
}

// ---------------------------------------------------------------------------
// G3 确认词模态(FLOW-05 / D-P3-3):strip 后全等「确认授权」才放行;默认拒绝
// ---------------------------------------------------------------------------

const CONFIRM_WORD = '确认授权';

function openConfirmModal() {
  confirmWordInput.value = '';
  confirmAuthorizeBtn.disabled = true; // 初始 disabled(未输入即不可放行)
  confirmError.classList.add('hidden');
  confirmationModal.classList.remove('hidden');
  confirmWordInput.focus();
}

function closeConfirmModal() {
  confirmationModal.classList.add('hidden');
}

// 拒绝路径(D-P3-5):不 POST 授权,把拒绝原因作为一条普通批注转给下一轮
async function rejectAuthorization() {
  const reason = window.prompt('拒绝原因(将作为一条普通批注转给下一轮):', '授权被拒,继续完善');
  if (reason == null) return; // 取消:既不授权也不建批注(用户放弃本次操作)
  const note = reason.trim() || '授权被拒,继续完善';
  const n = currentRoundNumber;
  if (n == null) return;
  // quote 取当前轮文档首行标题文本(前端已知;空串由 append_item 语义兜底)
  const quote = firstLineOfRoundDoc() || '本轮讨论文档';
  const result = await roundApi.postAnnotations(n, { quote, before: '', note });
  if (result.ok) {
    renderEvent({ kind: 'say', content: '已记录拒绝,并作为一条普通批注转给下一轮。', raw: null });
    await loadRoundView(n);
    await refreshPendingCount();
  } else {
    renderEvent({
      kind: 'error',
      content: `拒绝批注落盘失败:${(result.data && result.data.message) || result.status}`,
      raw: null,
    });
  }
}

function firstLineOfRoundDoc() {
  const text = String(roundDoc.textContent || '');
  const line = text.split('\n').map((s) => s.trim()).find((s) => s);
  return line || '';
}

authorizeBtn.addEventListener('click', () => {
  if (authorizeBtn.disabled) return;
  openConfirmModal();
});

// 输入事件:strip 后全等才 enable(textContent 比较,不进渲染管线,D-P3-3)
confirmWordInput.addEventListener('input', () => {
  const ok = confirmWordInput.value.trim() === CONFIRM_WORD;
  confirmAuthorizeBtn.disabled = !ok;
});

confirmAuthorizeBtn.addEventListener('click', async () => {
  if (confirmAuthorizeBtn.disabled) return;
  confirmAuthorizeBtn.disabled = true;
  try {
    const resp = await fetch('/api/authorize', { method: 'POST' });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      confirmError.textContent = `授权失败:${data.message || resp.status}`;
      confirmError.classList.remove('hidden');
      confirmAuthorizeBtn.disabled = false;
      return;
    }
    closeConfirmModal();
    await refreshRoundsAfterStream(); // 拉新 /api/session → 进入 phase4 撰写视图
  } catch {
    confirmError.textContent = '授权请求失败(网络)';
    confirmError.classList.remove('hidden');
    confirmAuthorizeBtn.disabled = false;
  }
});

confirmCancelBtn.addEventListener('click', async () => {
  closeConfirmModal();
  await rejectAuthorization();
});

// 撰写按钮(phase4):POST /api/writing → 202 → SSE 直播 → done 拉新
startWritingBtn.addEventListener('click', async () => {
  if (startWritingBtn.disabled || writingInFlight) return;
  writingInFlight = true;
  startWritingBtn.disabled = true;
  const originalText = startWritingBtn.textContent;
  startWritingBtn.textContent = '撰写中…';
  renderEvent({
    kind: 'say',
    content: '已发起撰写总设计文档,过程在下方工作面板全程直播……',
    raw: null,
  });
  try {
    const resp = await fetch('/api/writing', { method: 'POST' });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      renderEvent({ kind: 'error', content: `撰写发起失败:${err.message || resp.status}`, raw: null });
      writingInFlight = false;
      startWritingBtn.disabled = false;
      startWritingBtn.textContent = originalText;
    }
  } catch {
    renderEvent({ kind: 'error', content: '撰写请求失败(网络)', raw: null });
    writingInFlight = false;
    startWritingBtn.disabled = false;
    startWritingBtn.textContent = originalText;
  }
});

// phase5:awaiting_tier 呈档位引导(模态 + 开始自检按钮);checking 呈报告视图
function applyPhase5View(data) {
  writingView.classList.add('hidden');
  roundsHint.classList.add('hidden');
  roundTitle.textContent = '自检报告';
  roundSwitcher.classList.add('hidden');
  roundDoc.innerHTML = '';
  checksPanel.classList.remove('hidden');
  loadChecksView(data);
}

// 拉取 GET /api/checks 渲染报告列表 + 最新报告 + 按 selfcheck.mode 切控件区
async function loadChecksView(sessionData) {
  const result = await roundApi.listChecks();
  if (!result.ok) {
    checkState.textContent = '报告拉取失败';
    return;
  }
  const data = result.data;
  const selfcheck = data.selfcheck || { tier: null, mode: 'running', questions: [] };
  const mode = selfcheck.mode;

  // 报告切换器(照 round-switcher 模式)
  checkSwitcher.innerHTML = '';
  (data.checks || []).forEach((n) => {
    const opt = document.createElement('option');
    opt.value = String(n);
    opt.textContent = `第 ${n} 次核查${n === data.current_check ? '(当前)' : ''}`;
    checkSwitcher.appendChild(opt);
  });
  if (data.current_check != null) checkSwitcher.value = String(data.current_check);
  checkState.textContent = `档位:${selfcheck.tier || '未选'} / ${mode}`;

  // 最新报告 markdown 渲染(XSS:renderMarkdown→stripUnsafeNodes,D-P3-28)
  latestCheck.innerHTML = '';
  if (data.latest) {
    latestCheck.appendChild(renderMarkdown(data.latest));
  } else {
    latestCheck.textContent = '(尚无核查报告)';
  }

  // 档位引导:awaiting_tier 且未选档 → 弹模态(会话内只弹一次);已选档 → 开始自检
  if (sessionData && sessionData.state === 'phase5_awaiting_tier') {
    continueCheckBtn.textContent = '开始自检';
    continueCheckBtn.classList.remove('hidden');
    continueRepairBtn.classList.add('hidden');
    verdictCards.innerHTML = '';
    if (!selfcheck.tier && !tierModalShown) {
      tierModalShown = true;
      tierModal.classList.remove('hidden');
    }
    return;
  }

  // checking:按 mode 切控件区(§8.2 锁定版清单,D-P3-20 互斥)
  verdictCards.innerHTML = '';
  if (mode === 'paused') {
    // 暂停态:隐藏继续自检与继续修复;呈现修复者抛问裁决卡({number, text})
    continueCheckBtn.classList.add('hidden');
    continueRepairBtn.classList.add('hidden');
    (selfcheck.questions || []).forEach((q) => {
      verdictCards.appendChild(renderVerdictCard(q, 'paused'));
    });
  } else if (mode === 'p2') {
    // 纯 P2 残余态:隐藏继续自检;呈现残余裁决卡({number, location, issue, suggestion})
    continueCheckBtn.classList.add('hidden');
    continueRepairBtn.classList.add('hidden');
    (selfcheck.questions || []).forEach((q) => {
      verdictCards.appendChild(renderVerdictCard(q, 'p2'));
    });
  } else if (mode === 'resumed') {
    // 裁决待续跑态:只呈现「继续修复」(D-P3-20 判定式②唯一放行)
    continueCheckBtn.classList.add('hidden');
    continueRepairBtn.classList.remove('hidden');
  } else {
    // running:呈现「继续自检」(意外中断恢复,D-P3-20/§7.3②)
    continueCheckBtn.textContent = '继续自检';
    continueCheckBtn.classList.remove('hidden');
    continueRepairBtn.classList.add('hidden');
  }
}

// 裁决卡(createElement/textContent,零 innerHTML 拼接用户内容,D-P3-28)
// 按 mode 取键:p2 → location/issue/suggestion 三行(D-P3-17);paused → text 单行
function renderVerdictCard(question, mode) {
  const card = document.createElement('div');
  card.className = 'verdict-card';
  card.dataset.number = String(question.number);

  if (mode === 'p2') {
    const loc = document.createElement('p');
    loc.className = 'verdict-location';
    loc.textContent = question.location || '(未标位置)';
    card.appendChild(loc);
    const issue = document.createElement('p');
    issue.className = 'verdict-issue';
    issue.textContent = question.issue || '';
    card.appendChild(issue);
    const sug = document.createElement('p');
    sug.className = 'verdict-suggestion';
    sug.textContent = `建议修法:${question.suggestion || '(无)'}`;
    card.appendChild(sug);
  } else {
    // paused:修复者抛问文本({number, text})
    const q = document.createElement('p');
    q.className = 'verdict-issue';
    q.textContent = question.text || '';
    card.appendChild(q);
  }

  const noteInput = document.createElement('input');
  noteInput.type = 'text';
  noteInput.className = 'verdict-note-input';
  noteInput.placeholder = '备注(可选)';
  card.appendChild(noteInput);

  const buttons = document.createElement('div');
  buttons.className = 'verdict-buttons';
  const fixBtn = document.createElement('button');
  fixBtn.textContent = '修';
  const keepBtn = document.createElement('button');
  keepBtn.textContent = '接受现状';
  buttons.appendChild(fixBtn);
  buttons.appendChild(keepBtn);
  card.appendChild(buttons);

  const submit = async (decision) => {
    fixBtn.disabled = true;
    keepBtn.disabled = true;
    const resp = await fetch('/api/checks/verdict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ number: question.number, decision, note: noteInput.value }),
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      renderEvent({
        kind: 'error',
        content: `裁决落盘失败:${data.message || resp.status}`,
        raw: null,
      });
      fixBtn.disabled = false;
      keepBtn.disabled = false;
      return;
    }
    renderEvent({ kind: 'say', content: `裁决 #${question.number} 已落盘(${decision})。`, raw: null });
    await refreshChecksAfterStream();
  };
  fixBtn.addEventListener('click', () => submit('修'));
  keepBtn.addEventListener('click', () => submit('接受现状'));
  return card;
}

// 「继续自检」/「开始自检」:POST /api/checks/start → 202 → SSE 直播 → done 拉新
continueCheckBtn.addEventListener('click', async () => {
  if (continueCheckBtn.disabled || checkInFlight) return;
  checkInFlight = true;
  continueCheckBtn.disabled = true;
  renderEvent({ kind: 'say', content: '已发起核查,过程在下方工作面板全程直播……', raw: null });
  try {
    const resp = await fetch('/api/checks/start', { method: 'POST' });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      renderEvent({ kind: 'error', content: `自检发起失败:${err.message || resp.status}`, raw: null });
      checkInFlight = false;
      continueCheckBtn.disabled = false;
    }
  } catch {
    renderEvent({ kind: 'error', content: '自检请求失败(网络)', raw: null });
    checkInFlight = false;
    continueCheckBtn.disabled = false;
  }
});

// 「继续修复」:POST /api/checks/repair → 202 → SSE 直播 → done 拉新
continueRepairBtn.addEventListener('click', async () => {
  if (continueRepairBtn.disabled || checkInFlight) return;
  checkInFlight = true;
  continueRepairBtn.disabled = true;
  renderEvent({ kind: 'say', content: '已发起修复,过程在下方工作面板全程直播……', raw: null });
  try {
    const resp = await fetch('/api/checks/repair', { method: 'POST' });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      renderEvent({ kind: 'error', content: `修复发起失败:${err.message || resp.status}`, raw: null });
      checkInFlight = false;
      continueRepairBtn.disabled = false;
    }
  } catch {
    renderEvent({ kind: 'error', content: '修复请求失败(网络)', raw: null });
    checkInFlight = false;
    continueRepairBtn.disabled = false;
  }
});

// 档位模态两按钮:POST /api/checks/tier → 关模态拉新
async function chooseTier(tier) {
  try {
    const resp = await fetch('/api/checks/tier', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tier }),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      renderEvent({ kind: 'error', content: `档位选择失败:${err.message || resp.status}`, raw: null });
      return;
    }
    tierModal.classList.add('hidden');
    renderEvent({ kind: 'say', content: `已选择「${tier}」档,点「开始自检」启动核查。`, raw: null });
    await refreshChecksAfterStream();
  } catch {
    renderEvent({ kind: 'error', content: '档位选择失败(网络)', raw: null });
  }
}

tierLooseBtn.addEventListener('click', () => chooseTier('宽松'));
tierStrictBtn.addEventListener('click', () => chooseTier('严格'));

// done 后拉新:session(状态徽标/门控)+ checks(报告与 mode 控件)
async function refreshChecksAfterStream() {
  if (currentProject == null) return;
  checkInFlight = false;
  continueCheckBtn.disabled = false;
  continueRepairBtn.disabled = false;
  await refreshRoundsAfterStream();
  await loadChecksView(null);
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

// ---------------------------------------------------------------------------
// 轮次视图(D-P2-20):切换器 + 文档渲染 + 批注流侧栏 + 未处理数;阶段 3 专属
// ---------------------------------------------------------------------------

// 轮次路由 fetch 封装(照 sendMessage 形态;异常统一返回 {ok, status}`)
const roundApi = {
  async list() {
    const resp = await fetch('/api/rounds');
    if (!resp.ok) return { ok: false, status: resp.status };
    return { ok: true, data: await resp.json() };
  },
  async get(n) {
    const resp = await fetch(`/api/rounds/${n}`);
    if (!resp.ok) return { ok: false, status: resp.status };
    return { ok: true, data: await resp.json() };
  },
  async postAnnotations(n, body) {
    const resp = await fetch(`/api/rounds/${n}/annotations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await resp.json().catch(() => ({}));
    return { ok: resp.ok, status: resp.status, data };
  },
  async postPlain(n, body) {
    const resp = await fetch(`/api/rounds/${n}/plain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await resp.json().catch(() => ({}));
    return { ok: resp.ok, status: resp.status, data };
  },
  async listChecks() {
    const resp = await fetch('/api/checks');
    if (!resp.ok) return { ok: false, status: resp.status };
    return { ok: true, data: await resp.json() };
  },
};

// 进入/拉新 phase3 视图:拉轮次列表 → 渲染切换器 → 渲染指定轮(默认当前轮)
async function loadRoundsView(roundN) {
  const result = await roundApi.list();
  if (!result.ok) {
    roundsHint.textContent = '轮次列表拉取失败(稍后操作会重试)。';
    return;
  }
  const { rounds, current_round } = result.data;
  roundsHint.classList.add('hidden');

  // 切换器:列出全部轮,目标轮默认选中(首次进当前轮;拉新时也回当前轮)
  const target = roundN || current_round;
  roundSwitcher.innerHTML = '';
  (rounds || []).forEach((n) => {
    const opt = document.createElement('option');
    opt.value = String(n);
    opt.textContent = `第 ${n} 轮${n === current_round ? '(当前)' : ' (历史·只读)'}`;
    roundSwitcher.appendChild(opt);
  });
  roundSwitcher.value = String(target);
  await loadRoundView(target, current_round);
  // 划词菜单一次性绑定(menu 单例;handler 内部动态读当前显示轮判定冻结,D-P2-21)
  initSelectionMenu();
}

// 渲染指定轮:标题 + 冻结判定 + 文档 markdown + 批注流条目
async function loadRoundView(n, currentRound) {
  const cr = currentRound || currentRoundNumber;
  const result = await roundApi.get(n);
  if (!result.ok) {
    roundDoc.innerHTML = '';
    annotationList.innerHTML = '';
    roundsHint.textContent = `第 ${n} 轮文档拉取失败(该轮不存在或不完整)。`;
    roundsHint.classList.remove('hidden');
    return;
  }
  displayedRoundNumber = n;
  const isCurrent = n === cr;

  roundTitle.textContent = `第 ${n} 轮${isCurrent ? '' : '(历史轮·只读)'}`;
  renderRoundDocument(result.data.document, result.data.annotations);

  // 冻结呈现(D-P2-21):仅「轮 < 当前轮」推导,无独立状态;服务端 409 是防线
  renderAnnotations(result.data.annotations, isCurrent);
  updateFrozenPresentation(isCurrent);
}

// 文档区 markdown 渲染(复用 Phase 1 XSS 管线,零 innerHTML 拼接)+ 本轮批注高亮
function renderRoundDocument(text, annotations) {
  roundDoc.innerHTML = ''; // 清旧渲染节点(不用 += 拼接)
  if (text) roundDoc.appendChild(renderMarkdown(text));
  if (annotations) highlightAnnotations(roundDoc, annotations);
}

// 高亮(§4.1「高亮 = 有批注」/D-P2-4/D-P2-23):渲染后 DOM 的文本节点中
// 定位 quote 精确匹配并包 <mark>。createElement/textNode 拆分包 mark,
// 零 innerHTML 拼接(T-idi02-12);quote 空或找不到 → 跳过该条不抛(防呆,
// T-idi02-16 定位错段不如不标)。定位语义与 backend.annotations.locate_quote
// 同思路:多处匹配时优先"匹配前文以 before 结尾"的那一处(D-P2-6 前后端共用)。
function highlightAnnotations(roundDocEl, annotations) {
  const items = (annotations && annotations.items) || [];
  items.forEach((item) => {
    const quote = String(item.quote || '');
    if (!quote) return;

    // 遍历段落类元素,在其文本内容中找 quote(实现取简:首个命中即可)
    const blocks = roundDocEl.querySelectorAll('p, li, td, h1, h2, h3, h4, blockquote');
    for (const block of blocks) {
      const textNode = firstTextNodeContaining(block, quote);
      if (!textNode) continue;

      // 定位:本节点内多处匹配时用 before 辅助(匹配点前文以 before 结尾优先)
      const data = String(textNode.data || '');
      const starts = findAllIndexes(data, quote);
      if (!starts.length) break; // 防御:textNodeContaining 已保证含 quote
      let target = starts[0];
      if (starts.length > 1) {
        const before = String(item.before || '');
        const hit = before
          ? starts.find((s) => data.slice(Math.max(0, s - before.length), s) === before)
          : undefined;
        if (hit !== undefined) target = hit;
      }

      // 拆分文本节点包 mark(纯 DOM 操作,无 innerHTML)
      const afterNode = textNode.splitText(target);
      afterNode.splitText(quote.length); // 截出 quote 段独立文本节点
      const mark = document.createElement('mark');
      mark.className = 'annotation-quote-mark';
      mark.textContent = quote; // textContent 赋值,零注入面
      afterNode.parentNode.replaceChild(mark, afterNode);
      break; // 每条 annotation 一个 mark(首个命中即可)
    }
  });
}

// 找出 block 内第一个包含 quote 的文本节点(TreeWalker 实现取简)
function firstTextNodeContaining(block, quote) {
  const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    if (String(node.data || '').includes(quote)) return node;
  }
  return null;
}

// 全部匹配起点(照 locate_quote 的多匹配枚举语义)
function findAllIndexes(text, quote) {
  const indexes = [];
  let pos = text.indexOf(quote);
  while (pos !== -1) {
    indexes.push(pos);
    pos = text.indexOf(quote, pos + 1);
  }
  return indexes;
}

// 批注流条目渲染:quote 摘录 + note/answer + 状态徽标;plain 灰斜体;answered 灰化不删
function renderAnnotations(annotations, isCurrentRound) {
  annotationList.innerHTML = '';
  const items = (annotations && annotations.items) || [];
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'hint';
    empty.textContent = '本轮暂无批注——在左侧文档划词即可批注。';
    annotationList.appendChild(empty);
    if (!isCurrentRound) empty.textContent = '该轮暂无批注。';
    return;
  }
  items.forEach((item) => {
    const li = document.createElement('div');
    li.className = 'annotation-item'
      + (item.type === 'plain' ? ' annotation-plain' : '')
      + (item.status === 'answered' ? ' annotation-answered' : ' annotation-pending-item');
    li.dataset.annotationId = item.id || '';

    // quote 摘录(textContent,前 60 字截断显示)
    const quote = document.createElement('p');
    quote.className = 'annotation-quote';
    const qt = String(item.quote || '');
    quote.textContent = `「${qt.length > 60 ? qt.slice(0, 60) + '…' : qt}」`;
    li.appendChild(quote);

    // note(用户批注 / plain 的提问)——markdown 渲染(经 stripUnsafeNodes)
    if (item.note != null && item.note !== '') {
      const noteEl = document.createElement('div');
      noteEl.className = 'annotation-note';
      noteEl.appendChild(renderMarkdown(item.note));
      li.appendChild(noteEl);
    }

    // answer(AI 回应附在旁边,§4.2):parsed 折叠展示;plain 直接灰斜体显示
    if (item.answer != null && item.answer !== '') {
      const ansEl = document.createElement('details');
      ansEl.className = 'annotation-answer';
      const summary = document.createElement('summary');
      summary.textContent = item.type === 'plain' ? '大白话回答' : 'AI 回应';
      ansEl.appendChild(summary);
      const body = document.createElement('div');
      body.className = 'annotation-answer-body';
      body.appendChild(renderMarkdown(item.answer));
      ansEl.appendChild(body);
      li.appendChild(ansEl);
      if (item.type === 'plain') ansEl.open = true; // plain 即时答案展开可见
    }

    // 状态徽标(中文;plain 恒 answered)
    const badge = document.createElement('span');
    badge.className = 'annotation-badge ' + (item.status === 'answered' ? 'badge-answered' : 'badge-pending');
    badge.textContent = item.status === 'answered' ? '已回应' : '待处理';
    li.appendChild(badge);

    annotationList.appendChild(li);
  });
}

// 冻结轮三面呈现(D-P2-21):容器灰化 + 计数徽标隐藏 + 处理按钮禁用
function updateFrozenPresentation(isCurrent) {
  if (isCurrent) {
    roundDoc.classList.remove('round-frozen');
    pendingCount.style.display = '';
    processRoundBtn.disabled = processInFlight;
  } else {
    roundDoc.classList.add('round-frozen');
    pendingCount.style.display = 'none'; // 历史轮不显示本轮计数(D-P2-21)
    processRoundBtn.disabled = true;
  }
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
// 轮次切换器:切到历史轮 → 只读重渲染(冻结呈现由 updateFrozenPresentation 判定)
// ---------------------------------------------------------------------------

roundSwitcher.addEventListener('change', () => {
  const n = parseInt(roundSwitcher.value, 10);
  if (!Number.isFinite(n)) return;
  loadRoundView(n);
});

// ---------------------------------------------------------------------------
// 划词交互(D-P2-1~3,§4.2/§9):mouseup 检测选区 → 原生小菜单两项
// 「批注」「用大白话讲这段」。仅绑 round-doc 容器——阶段 1-2 草稿区/会话流
// 无划词(D-P2-2);冻结轮(显示轮 < 当前轮)handler 直接返回(D-P2-21)。
// ---------------------------------------------------------------------------

// mouseup 时捕获的选区快照(菜单动作延迟读取会因选择被清除而丢)
let menuSelection = null;

// before 计算(D-P2-3):选区真正起点(方向无关)在其文本节点中的前文取末 40 字。
// 用 getRangeAt(0).startContainer/startOffset,不用 anchorNode——反向拖拽时
// anchor 是选区终点,locate_quote 的 before 二次定位会被反向起点败掉;
// Range 起点在两种拖拽方向下同为选区真正起点。startContainer 非文本节点
// (元素节点,如划过整段)时取空串——配对靠 quote 唯一性,合法降级。
function computeBefore(selection) {
  if (!selection || selection.rangeCount === 0) return '';
  const range = selection.getRangeAt(0);
  const { startContainer, startOffset } = range;
  if (startContainer.nodeType === Node.TEXT_NODE) {
    // 文本节点:起点前的字符切片取末 40(中文按字符计,§6.2「前 40 字」)
    return String(startContainer.data || '').slice(0, startOffset).slice(-40);
  }
  return ''; // 元素节点起点:无同文本节点前文可取,配对靠 quote 唯一性
}

// 选区是否落在 round-doc 容器内(menu 本就只在 round-doc mouseup 时弹出,
// 双保险:跨容器选区(从侧栏拖进文档)也要求锚定在 round-doc)
function selectionInRoundDoc(selection) {
  if (!selection || selection.rangeCount === 0) return false;
  const node = selection.anchorNode;
  if (!node) return false;
  const el = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
  return !!(el && roundDoc.contains(el));
}

// 隐藏菜单并清空选区快照
function hideSelectionMenu() {
  selectionMenu.classList.add('hidden');
  menuSelection = null;
}

// 显示菜单在选区附近(向右下偏移,不越视口——简单 clamp)
function showSelectionMenu(selection) {
  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();
  selectionMenu.classList.remove('hidden');
  const OFFSET = 8;
  let x = window.scrollX + rect.left + OFFSET;
  let y = window.scrollY + rect.bottom + OFFSET;
  // clamp:不越视口右/下边界(简单数学,不含菜单尺寸精确补偿)
  const menuRect = selectionMenu.getBoundingClientRect();
  const maxX = window.scrollX + document.documentElement.clientWidth - menuRect.width - 4;
  const maxY = window.scrollY + document.documentElement.clientHeight - menuRect.height - 4;
  if (x > maxX) x = maxX;
  if (y > maxY) y = maxY;
  if (x < 0) x = 0;
  if (y < 0) y = 0;
  selectionMenu.style.left = `${x}px`;
  selectionMenu.style.top = `${y}px`;
}

// 一次性绑定入口(menu 单例,handler 内部动态读当前显示轮判定冻结)
let selectionMenuBound = false;
function initSelectionMenu() {
  if (selectionMenuBound) return;
  selectionMenuBound = true;

  // 仅 round-doc 容器内 mouseup 触发(D-P2-2:draft-view / chat 区绝不绑此菜单)
  roundDoc.addEventListener('mouseup', () => {
    // 冻结轮禁用(D-P2-21:历史轮不可批注)——服务端 409 是防线,这里只是呈现
    if (currentRoundNumber != null && displayedRoundNumber != null
        && displayedRoundNumber < currentRoundNumber) return;
    if (currentState !== 'phase3') return;

    const selection = window.getSelection();
    if (!selection || selection.isCollapsed || !String(selection.toString()).trim()) {
      hideSelectionMenu();
      return;
    }
    if (!selectionInRoundDoc(selection)) {
      hideSelectionMenu();
      return;
    }
    menuSelection = selection;
    showSelectionMenu(selection);
  });

  // 点文档其他位置/滚动 → 菜单消失(菜单自身点击不冒泡关闭)
  document.addEventListener('mousedown', (e) => {
    if (selectionMenu.classList.contains('hidden')) return;
    if (selectionMenu.contains(e.target)) return;
    hideSelectionMenu();
  });
  window.addEventListener('scroll', hideSelectionMenu, true);

  // 菜单项 1:「批注」→ 原生 prompt 收 note → POST annotations(实现取简,零依赖)
  annotateBtn.addEventListener('click', async () => {
    const sel = menuSelection;
    hideSelectionMenu();
    if (!sel) return;
    const quote = String(sel.toString());
    const before = computeBefore(sel);
    const note = window.prompt('写批注(将绑定到划选原文)', '');
    if (note == null) return; // 取消:不建条目
    if (!note.trim()) {
      renderEvent({ kind: 'error', content: '批注内容不能为空', raw: null });
      return;
    }
    const n = displayedRoundNumber;
    const result = await roundApi.postAnnotations(n, { quote, before, note });
    if (result.ok) {
      // 成功:拉新侧栏(新条目 pending 徽标)+ 计数(G-idi01-7 同型拉新)
      await loadRoundView(n);
      await refreshPendingCount();
    } else if (result.status === 409) {
      renderEvent({ kind: 'error', content: '仅当前轮可批注', raw: null });
    } else {
      renderEvent({
        kind: 'error',
        content: `批注失败:${(result.data && result.data.message) || result.status}`,
        raw: null,
      });
    }
  });

  // 菜单项 2:「用大白话讲这段」→ 固定 question 直接 POST plain(实现取简)
  plainAskBtn.addEventListener('click', async () => {
    const sel = menuSelection;
    hideSelectionMenu();
    if (!sel) return;
    const quote = String(sel.toString());
    const before = computeBefore(sel);
    const n = displayedRoundNumber;
    renderEvent({ kind: 'say', content: '正在请 AI 用大白话解释这段(数秒内返回)…', raw: null });
    const result = await roundApi.postPlain(n, {
      quote,
      before,
      question: '用大白话讲讲这段',
    });
    if (result.ok) {
      // 即时答已落盘为 plain 条目:拉新侧栏(answer 灰斜体展示)
      await loadRoundView(n);
    } else if (result.status === 409) {
      renderEvent({ kind: 'error', content: '仅当前轮可用大白话(或有调用进行中)', raw: null });
    } else if (result.status === 502) {
      renderEvent({
        kind: 'error',
        content: `大白话调用失败:${(result.data && result.data.message) || 'AI 未返回结果'}`,
        raw: null,
      });
    } else {
      renderEvent({
        kind: 'error',
        content: `大白话请求失败:${(result.data && result.data.message) || result.status}`,
        raw: null,
      });
    }
  });
}

// 拉新未处理数(建批注后 / done 后共用)
async function refreshPendingCount() {
  if (currentProject == null) return;
  try {
    const resp = await fetch('/api/session');
    if (!resp.ok) return;
    const data = await resp.json();
    if (data.status === 'ok' && data.state === 'phase3') {
      pendingCount.textContent = `本轮批注未处理 ${data.pending_annotations}`;
    }
  } catch { /* 拉不到保持现状 */ }
}

// ---------------------------------------------------------------------------
// 处理本轮批注(FLOW-04 / §4.4 G2):点击 → POST process(202)→ SSE 直播
// → done 后拉新 refreshRoundsAfterStream → 新当前轮 + 上一轮自动冻结。
// 按钮:仅 phase3 且显示当前轮时可用;busy(process_in_flight)禁用防重复。
// ---------------------------------------------------------------------------

processRoundBtn.addEventListener('click', async () => {
  if (processRoundBtn.disabled || processInFlight) return; // busy 防重复
  if (currentState !== 'phase3') {
    renderEvent({ kind: 'error', content: '仅阶段 3 可处理本轮批注', raw: null });
    return;
  }
  processInFlight = true;
  processRoundBtn.disabled = true;
  const originalText = processRoundBtn.textContent;
  processRoundBtn.textContent = '处理中…';
  processRoundBtn.title = 'AI 正在批量回应批注,AI 工作面板可见全过程';
  renderEvent({
    kind: 'say',
    content: '已发起处理本轮批注,读文件/写文件过程在下方工作面板全程直播……',
    raw: null,
  });
  try {
    const resp = await fetch('/api/rounds/process', { method: 'POST' });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      renderEvent({
        kind: 'error',
        content: `处理发起失败:${err.message || resp.status}`,
        raw: null,
      });
      // 202 未受理(非 phase3/在飞):恢复按钮;done 链不会来
      processInFlight = false;
      processRoundBtn.disabled = false;
      processRoundBtn.textContent = originalText;
      return;
    }
    // 202 受理:保持处理中禁用态直至 SSE done(refreshRoundsAfterStream 收尾)
  } catch {
    renderEvent({ kind: 'error', content: '处理请求失败(网络)', raw: null });
    processInFlight = false;
    processRoundBtn.disabled = false;
    processRoundBtn.textContent = originalText;
  }
});

// done 后拉新链(G-idi01-7 先例扩展到双端点):串行 fetch /api/session →
// applySessionGates(新 current_round/rounds/pending_annotations)→ 其 phase3
// 分支内的 loadRoundsView 已拉新当前轮文档+annotations;上一轮冻结随
// n < current_round 的呈现自然成立。纯事件驱动一拉,无轮询。
async function refreshRoundsAfterStream() {
  if (currentProject == null) return;
  try {
    const resp = await fetch('/api/session');
    if (!resp.ok) return;
    const data = await resp.json();
    if (data.status === 'ok') applySessionGates(data);
  } catch { /* 拉不到保持现状 */ }
}

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
