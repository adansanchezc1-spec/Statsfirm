/**
 * STATSFIRM CO. - CLIENT OPERATING ECOSYSTEM & SPA CONTROLLER
 * Orchestrates navigation, real-time API integrations, digital signatures,
 * chat simulator, and SLA countdown timers.
 */

// Global State
let currentTab = 'telemetry';
let telemetryData = null;
let slaCountdownInterval = null;

// Toast Notification Helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
  toast.innerHTML = `<span>${icon}</span> <div>${message}</div>`;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Navigation Controller
function switchTab(tabId) {
  currentTab = tabId;

  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.tab === tabId);
  });

  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.toggle('active', pane.id === `tab-${tabId}`);
  });

  const titles = {
    telemetry: 'Consola de Telemetría & Salud de Sprints',
    diagnostico: 'Diagnóstico Express & Readiness Index',
    squad: 'Directorio del Squad & Comunicación Directa',
    bpmn: 'Orquestador BPMN 2.0 Camunda & Formularios',
    vault: 'Bóveda Documental Criptográfica',
    dashboards: 'Consolas Analíticas & KPIs de Negocio (Capa 3)',
    approvals: 'Aprobación de Entregables con Firma Electrónica',
    support: 'Centro de Soporte 24/7 & Gestión de Incidentes'
  };
  document.getElementById('headerPageTitle').textContent = titles[tabId] || 'Consola del Cliente';

  // Specific tab initializers
  if (tabId === 'telemetry') {
    renderTelemetryCharts();
  } else if (tabId === 'bpmn') {
    if (window.BpmnViewer) window.BpmnViewer.init();
  } else if (tabId === 'approvals') {
    loadApprovalsData();
  } else if (tabId === 'vault') {
    loadVaultData();
  } else if (tabId === 'squad') {
    loadSquadData();
    loadChatMessages();
  } else if (tabId === 'support') {
    loadIncidentsData();
  }
}

// Fetch & Load Telemetry
async function loadTelemetry() {
  try {
    const res = await fetch('/api/telemetry');
    const data = await res.json();
    if (!data.success) return;

    telemetryData = data.data;
    renderTelemetryStats();
    renderTelemetryCharts();
  } catch (err) {
    console.error('Error cargando telemetría:', err);
  }
}

function renderTelemetryStats() {
  if (!telemetryData) return;
  const { sprints, pipelineHealth } = telemetryData;

  document.getElementById('activeSprintLabel').textContent = `Sprint 0${sprints.activeSprintNum}`;
  document.getElementById('sprintPointsBadge').textContent = `${sprints.storyPointsCompleted} / ${sprints.storyPointsCommitted} SP`;
  document.getElementById('daysRemainingBadge').textContent = `${sprints.daysRemaining} días restantes`;

  document.getElementById('c1Throughput').textContent = pipelineHealth.capa1Bronze.throughput;
  document.getElementById('c1Records').textContent = pipelineHealth.capa1Bronze.recordsProcessedToday;
  document.getElementById('c2Quality').textContent = `${pipelineHealth.capa2Silver.dbtTestPassRatePct}%`;
  document.getElementById('c3Latency').textContent = `${pipelineHealth.capa3Gold.latencyP99Ms} ms`;
}

function renderTelemetryCharts() {
  if (!telemetryData || !window.TelemetryEngine) return;
  window.TelemetryEngine.renderGantt('ganttChartContainer', telemetryData.sprints.gantt);
  window.TelemetryEngine.renderBurndown('burndownChartContainer', telemetryData.sprints.burndown);
}

// Squad & Chat Module
async function loadSquadData() {
  try {
    const res = await fetch('/api/squad');
    const data = await res.json();
    if (!data.success) return;

    const container = document.getElementById('squadGridContainer');
    if (!container) return;

    container.innerHTML = '';
    data.data.forEach(member => {
      const card = document.createElement('div');
      card.className = 'glass-card';
      card.style = 'padding: 18px;';
      card.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
          <div class="avatar-circle" style="width: 44px; height: 44px; font-size: 16px;">${member.name.charAt(0)}</div>
          <div>
            <h4 style="font-size: 15px; font-weight: 700; color: var(--pure-white);">${member.name}</h4>
            <div style="font-size: 12px; color: var(--code-green); font-weight: 500;">${member.role}</div>
          </div>
        </div>
        <p style="font-size: 12px; color: var(--titanium-light); margin-bottom: 12px;">${member.bio}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: var(--font-mono);">
          <span style="color: var(--electric-cyan);">${member.chapter}</span>
          <span class="status-chip" style="font-size: 9px; padding: 2px 6px;">${member.status}</span>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error('Error cargando miembros del squad:', err);
  }
}

async function loadChatMessages() {
  try {
    const res = await fetch('/api/messages');
    const data = await res.json();
    if (!data.success) return;

    const chatBox = document.getElementById('chatMessagesBox');
    if (!chatBox) return;

    chatBox.innerHTML = '';
    data.data.forEach(msg => {
      const isUser = msg.sender.includes('Cliente');
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${isUser ? 'user' : 'squad'}`;
      bubble.innerHTML = `
        <div class="chat-sender">${msg.sender} • <span style="color:var(--titanium-gray)">${msg.timestamp}</span></div>
        <div>${msg.text}</div>
      `;
      chatBox.appendChild(bubble);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (err) {
    console.error('Error cargando mensajes:', err);
  }
}

async function sendChatMessage(e) {
  e.preventDefault();
  const input = document.getElementById('chatInputText');
  const text = input.value.trim();
  if (!text) return;

  try {
    const res = await fetch('/api/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (data.success) {
      input.value = '';
      await loadChatMessages();
      setTimeout(loadChatMessages, 1200); // Wait for automated squad response
    }
  } catch (err) {
    console.error('Error enviando mensaje:', err);
  }
}

// Readiness Index & Diagnostic Calculator
async function calculateDiagnostic(e) {
  e.preventDefault();
  const form = e.target;
  const services = Array.from(form.querySelectorAll('input[name="services"]:checked')).map(cb => cb.value);

  const payload = {
    dataMaturity: form.dataMaturity.value,
    processMaturity: form.processMaturity.value,
    volumeTb: form.volumeTb.value,
    systemsCount: form.systemsCount.value,
    servicesSelected: services,
    urgency: form.urgency.value
  };

  try {
    const res = await fetch('/api/diagnostico/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();

    if (result.success) {
      const d = result.data;
      document.getElementById('diagResultBox').style.display = 'block';
      document.getElementById('readinessScoreVal').textContent = `${d.readinessScore} / 100`;
      document.getElementById('readinessLevelLabel').textContent = d.maturityLabel;
      document.getElementById('estCapexVal').textContent = `$${d.estimatedCapexUsd.toLocaleString()} USD`;
      document.getElementById('estOpexVal').textContent = `$${d.estimatedMonthlyOpexUsd.toLocaleString()} USD / mes`;

      showToast('Diagnóstico calculado exitosamente según marco STF', 'success');
      document.getElementById('diagResultBox').scrollIntoView({ behavior: 'smooth' });
    }
  } catch (err) {
    console.error('Error calculando diagnóstico:', err);
    showToast('Error al procesar cálculo', 'error');
  }
}

// Document Vault
async function loadVaultData() {
  try {
    const res = await fetch('/api/vault');
    const data = await res.json();
    if (!data.success) return;

    const tbody = document.getElementById('vaultTableBody');
    if (!tbody) return;

    tbody.innerHTML = '';
    data.data.forEach(doc => {
      const tr = document.createElement('tr');
      tr.style = 'border-bottom: 1px solid rgba(255,255,255,0.06);';
      tr.innerHTML = `
        <td style="padding: 14px 16px; font-weight: 600; color: var(--pure-white);">${doc.title}</td>
        <td style="padding: 14px 16px; font-family: var(--font-mono); font-size: 11px; color: var(--electric-cyan);">${doc.type}</td>
        <td style="padding: 14px 16px; font-family: var(--font-mono); font-size: 11px; color: var(--titanium-gray);">${doc.hashSha256.substring(0, 16)}...</td>
        <td style="padding: 14px 16px; font-size: 12px; color: var(--titanium-light);">${doc.size}</td>
        <td style="padding: 14px 16px;"><span class="status-chip" style="font-size:10px;">${doc.status}</span></td>
        <td style="padding: 14px 16px; text-align: right;">
          <a href="${doc.downloadUrl}" class="btn btn-secondary" style="padding: 4px 12px; font-size: 12px;">Descargar</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Error cargando bóveda documental:', err);
  }
}

// Deliverables & Digital Signatures
async function loadApprovalsData() {
  try {
    const res = await fetch('/api/approvals');
    const data = await res.json();
    if (!data.success) return;

    const pendingBox = document.getElementById('pendingApprovalsContainer');
    if (!pendingBox) return;

    pendingBox.innerHTML = '';
    if (data.pending.length === 0) {
      pendingBox.innerHTML = `
        <div style="padding: 24px; text-align: center; color: var(--code-green);">
          ✓ No hay entregables pendientes de firma. Todos los hitos están autorizados.
        </div>
      `;
    } else {
      data.pending.forEach(app => {
        const div = document.createElement('div');
        div.className = 'glass-card';
        div.style = 'margin-bottom: 20px; border-color: var(--code-green);';
        
        let dodItems = '';
        app.dodChecklist.forEach(chk => {
          dodItems += `
            <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #E2E8F0; margin-bottom: 6px;">
              <span style="color: var(--code-green); font-weight: bold;">✓</span> ${chk.item}
            </div>
          `;
        });

        div.innerHTML = `
          <div class="card-header">
            <div>
              <span class="card-badge">${app.sprint}</span>
              <h3 style="font-family: var(--font-display); font-size: 17px; margin-top: 6px; color: var(--pure-white);">${app.title}</h3>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 11px; color: var(--titanium-light)">MONTO DE FACTURACIÓN:</div>
              <div style="font-family: var(--font-mono); font-size: 20px; color: var(--code-green); font-weight: bold;">$${app.amountToInvoiceUsd.toLocaleString()} USD</div>
            </div>
          </div>
          
          <div style="margin: 16px 0; padding: 14px; background: rgba(15,23,42,0.6); border-radius: 8px;">
            <div style="font-size: 12px; font-weight: 700; color: var(--electric-cyan); margin-bottom: 8px;">EVIDENCIAS DE DEFINITION OF DONE (DoD):</div>
            ${dodItems}
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 18px;">
            <button class="btn btn-primary" onclick="openSignatureModal('${app.id}', '${app.title}', ${app.amountToInvoiceUsd})">
              ✍️ Firmar Aprobación con Certificado Avanzado
            </button>
          </div>
        `;
        pendingBox.appendChild(div);
      });
    }

    // Signed history
    const historyBox = document.getElementById('signedHistoryContainer');
    if (historyBox && data.history.length > 0) {
      historyBox.innerHTML = '';
      data.history.forEach(h => {
        const div = document.createElement('div');
        div.style = 'padding: 14px; background: rgba(15,23,42,0.5); border: 1px solid rgba(0,255,102,0.2); border-radius: 8px; margin-bottom: 10px;';
        div.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-weight: 700; color: var(--pure-white); font-size: 14px;">${h.title}</div>
              <div style="font-size: 11px; color: var(--titanium-gray); font-family: var(--font-mono);">Certificado SHA-256: ${h.signatureHash.substring(0, 24)}... • Factura ERP: ${h.invoiceNumber}</div>
            </div>
            <span class="status-chip" style="font-size: 10px;">FIRMADO Y FACTURADO</span>
          </div>
        `;
        historyBox.appendChild(div);
      });
    }
  } catch (err) {
    console.error('Error cargando aprobaciones:', err);
  }
}

function openSignatureModal(id, title, amount) {
  document.getElementById('signApprovalId').value = id;
  document.getElementById('modalApprovalTitle').textContent = title;
  document.getElementById('modalApprovalAmount').textContent = `$${amount.toLocaleString()} USD`;
  document.getElementById('signatureModal').classList.add('active');
}

function closeSignatureModal() {
  document.getElementById('signatureModal').classList.remove('active');
}

async function submitDigitalSignature(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    approvalId: form.approvalId.value,
    signerName: form.signerName.value,
    signerRole: form.signerRole.value,
    signatureType: form.signatureType.value,
    npsScore: parseInt(form.npsScore.value) || 10,
    feedback: form.feedback.value
  };

  try {
    const res = await fetch('/api/approvals/sign', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      closeSignatureModal();
      showToast('Aprobación formalizada. Factura electrónica enviada al ERP.', 'success');
      loadApprovalsData();
    }
  } catch (err) {
    console.error('Error al firmar:', err);
    showToast('Error procesando la firma digital', 'error');
  }
}

// Incidents & Support 24/7
async function loadIncidentsData() {
  try {
    const res = await fetch('/api/incidents');
    const data = await res.json();
    if (!data.success) return;

    const list = document.getElementById('incidentsListContainer');
    if (!list) return;

    list.innerHTML = '';
    data.data.forEach(inc => {
      const card = document.createElement('div');
      card.className = 'glass-card';
      card.style = 'margin-bottom: 16px; padding: 16px;';
      const isSev1 = inc.severity === 'Sev 1';

      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div>
            <span style="display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; font-family: var(--font-mono); background: ${isSev1 ? 'rgba(239,68,68,0.2)' : 'rgba(245,158,11,0.2)'}; color: ${isSev1 ? 'var(--danger-red)' : 'var(--warning-amber)'}; border: 1px solid currentColor;">${inc.severity}</span>
            <span style="font-weight: 700; color: var(--pure-white); margin-left: 8px; font-size: 14px;">${inc.title}</span>
          </div>
          <span class="status-chip" style="font-size: 10px;">${inc.status}</span>
        </div>
        <div style="font-size: 12px; color: var(--titanium-light); margin-bottom: 6px;">
          Componente: <strong>${inc.component}</strong> • Asignado: <strong>${inc.sreOnCallAssigned || 'SRE On-Call'}</strong>
        </div>
        ${inc.rca ? `<div style="font-size: 12px; color: #E2E8F0; padding: 8px; background: rgba(15,23,42,0.6); border-radius: 6px; margin-top: 8px;"><strong>RCA Post-Mortem:</strong> ${inc.rca}</div>` : ''}
        ${isSev1 && inc.status === 'ACTIVE_TRIAGE' ? `<div id="slaCountdownBox" style="font-family: var(--font-mono); color: var(--danger-red); font-weight: bold; font-size: 13px; margin-top: 8px;">⏳ SLA de Respuesta Inicial: <span id="slaTimerVal">14:52</span> restantes</div>` : ''}
      `;
      list.appendChild(card);
    });

    startSlaTimer();
  } catch (err) {
    console.error('Error cargando incidentes:', err);
  }
}

function startSlaTimer() {
  if (slaCountdownInterval) clearInterval(slaCountdownInterval);
  let secondsRemaining = 14 * 60 + 52;

  slaCountdownInterval = setInterval(() => {
    const el = document.getElementById('slaTimerVal');
    if (!el) {
      clearInterval(slaCountdownInterval);
      return;
    }
    if (secondsRemaining <= 0) {
      el.textContent = '00:00 (ESCALADO AL BOARD)';
      clearInterval(slaCountdownInterval);
      return;
    }
    secondsRemaining--;
    const mins = Math.floor(secondsRemaining / 60);
    const secs = secondsRemaining % 60;
    el.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }, 1000);
}

async function reportIncident(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    title: form.title.value,
    severity: form.severity.value,
    component: form.component.value,
    description: form.description.value
  };

  try {
    const res = await fetch('/api/incidents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      form.reset();
      showToast('Incidente reportado. El equipo SRE On-Call ha sido alertado vía PagerDuty.', 'info');
      loadIncidentsData();
    }
  } catch (err) {
    console.error('Error reportando incidente:', err);
  }
}

// Window Initialization
window.addEventListener('DOMContentLoaded', () => {
  loadTelemetry();
});
