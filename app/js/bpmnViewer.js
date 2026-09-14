/**
 * STATSFIRM CO. - CAMUNDA BPMN & FORM RENDERER ENGINE
 * Dynamically loads and renders official Camunda Form Schema JSON files
 */

const BpmnViewer = {
  currentFormKey: null,
  currentSchema: null,

  async init() {
    await this.loadFormList();
    await this.loadWorkflowLog();
  },

  async loadFormList() {
    try {
      const res = await fetch('/api/bpmn/forms');
      const data = await res.json();
      if (!data.success) return;

      const container = document.getElementById('bpmnFormPills');
      if (!container) return;

      container.innerHTML = '';
      data.forms.forEach((f, idx) => {
        const pill = document.createElement('button');
        pill.className = `form-pill ${idx === 0 ? 'active' : ''}`;
        pill.textContent = f.filename.replace('.form', '').replace(/_/g, ' ').toUpperCase();
        pill.title = f.title;
        pill.onclick = () => {
          document.querySelectorAll('.form-pill').forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          this.loadFormSchema(f.filename);
        };
        container.appendChild(pill);
      });

      if (data.forms.length > 0) {
        this.loadFormSchema(data.forms[0].filename);
      }
    } catch (err) {
      console.error('Error cargando lista de formularios Camunda:', err);
    }
  },

  async loadFormSchema(filename) {
    try {
      this.currentFormKey = filename;
      const res = await fetch(`/api/bpmn/forms/${filename}`);
      const data = await res.json();
      if (!data.success) return;

      this.currentSchema = data.schema;
      this.renderForm(data.schema);
    } catch (err) {
      console.error('Error cargando esquema de formulario:', err);
    }
  },

  renderForm(schema) {
    const container = document.getElementById('camundaFormContainer');
    if (!container) return;

    let html = `<form id="activeCamundaForm" onsubmit="BpmnViewer.submitActiveForm(event)">`;

    schema.components.forEach(comp => {
      if (comp.type === 'text') {
        const cleanText = comp.text.replace(/# /g, '').replace(/\n/g, '<br>');
        html += `<div class="form-text-header" style="margin-bottom: 20px; padding: 14px 18px; background: rgba(34,211,238,0.06); border-left: 3px solid var(--electric-cyan); border-radius: 6px;">
          <h3 style="font-family: var(--font-display); font-size: 16px; color: var(--electric-cyan); margin-bottom: 6px;">${cleanText.split('<br>')[0]}</h3>
          <p style="font-size: 13px; color: var(--titanium-light); margin: 0;">${cleanText.split('<br>')[1] || ''}</p>
        </div>`;
      } else if (comp.type === 'textfield') {
        const isRequired = comp.validate && comp.validate.required ? 'required' : '';
        const isDisabled = comp.disabled ? 'disabled' : '';
        const defaultVal = comp.disabled ? 'Global Fintech Corp.' : '';
        html += `
          <div class="form-group">
            <label class="form-label">${comp.label} ${isRequired ? '<span style="color:var(--code-green)">*</span>' : ''}</label>
            <input type="text" class="form-control" name="${comp.key}" value="${defaultVal}" ${isRequired} ${isDisabled} placeholder="Ingrese ${comp.label}...">
          </div>
        `;
      } else if (comp.type === 'number') {
        const isRequired = comp.validate && comp.validate.required ? 'required' : '';
        const min = comp.validate && comp.validate.min !== undefined ? `min="${comp.validate.min}"` : '';
        const max = comp.validate && comp.validate.max !== undefined ? `max="${comp.validate.max}"` : '';
        html += `
          <div class="form-group">
            <label class="form-label">${comp.label} ${isRequired ? '<span style="color:var(--code-green)">*</span>' : ''}</label>
            <input type="number" class="form-control" name="${comp.key}" ${min} ${max} ${isRequired} placeholder="Valor numérico...">
          </div>
        `;
      } else if (comp.type === 'textarea') {
        const isRequired = comp.validate && comp.validate.required ? 'required' : '';
        html += `
          <div class="form-group">
            <label class="form-label">${comp.label} ${isRequired ? '<span style="color:var(--code-green)">*</span>' : ''}</label>
            <textarea class="form-control" name="${comp.key}" rows="3" ${isRequired} placeholder="Detalle la información requerida..."></textarea>
          </div>
        `;
      } else if (comp.type === 'select') {
        const isRequired = comp.validate && comp.validate.required ? 'required' : '';
        let optionsHtml = `<option value="">-- Seleccione una opción --</option>`;
        if (comp.values) {
          comp.values.forEach(v => {
            optionsHtml += `<option value="${v.value}">${v.label}</option>`;
          });
        }
        html += `
          <div class="form-group">
            <label class="form-label">${comp.label} ${isRequired ? '<span style="color:var(--code-green)">*</span>' : ''}</label>
            <select class="form-control" name="${comp.key}" ${isRequired}>${optionsHtml}</select>
          </div>
        `;
      } else if (comp.type === 'checkbox') {
        const isRequired = comp.validate && comp.validate.required ? 'required' : '';
        html += `
          <div class="form-group" style="display: flex; align-items: center; gap: 10px; padding: 10px 0;">
            <input type="checkbox" id="${comp.id}" name="${comp.key}" value="true" ${isRequired} style="width: 18px; height: 18px; accent-color: var(--code-green);">
            <label for="${comp.id}" style="font-size: 14px; cursor: pointer; color: var(--pure-white);">${comp.label}</label>
          </div>
        `;
      } else if (comp.type === 'checklist') {
        html += `<div class="form-group"><label class="form-label">${comp.label}</label><div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">`;
        if (comp.values) {
          comp.values.forEach(v => {
            html += `
              <label style="display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--titanium-light); cursor: pointer;">
                <input type="checkbox" name="${comp.key}" value="${v.value}" style="width: 16px; height: 16px; accent-color: var(--electric-cyan);">
                ${v.label}
              </label>
            `;
          });
        }
        html += `</div></div>`;
      }
    });

    html += `
      <div style="margin-top: 24px; display: flex; gap: 14px; justify-content: flex-end;">
        <button type="button" class="btn btn-secondary" onclick="document.getElementById('activeCamundaForm').reset()">Limpiar Formulario</button>
        <button type="submit" class="btn btn-primary">
          <span>⚡ Enviar Tarea a Motor Camunda</span>
        </button>
      </div>
    </form>`;

    container.innerHTML = html;
  },

  async submitActiveForm(event) {
    event.preventDefault();
    const form = event.target;
    const formDataObj = {};
    const formData = new FormData(form);

    for (let [key, val] of formData.entries()) {
      if (formDataObj[key]) {
        if (!Array.isArray(formDataObj[key])) formDataObj[key] = [formDataObj[key]];
        formDataObj[key].push(val);
      } else {
        formDataObj[key] = val;
      }
    }

    try {
      const res = await fetch('/api/bpmn/tasks/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          formKey: this.currentFormKey,
          formData: formDataObj,
          submittedBy: 'Ing. Alejandro Morales (Cliente)'
        })
      });

      const result = await res.json();
      if (result.success) {
        showToast(result.message, 'success');
        form.reset();
        await this.loadWorkflowLog();
      } else {
        showToast(result.error || 'Error al procesar formulario', 'error');
      }
    } catch (err) {
      console.error('Error enviando formulario:', err);
      showToast('Error de conexión con el motor Camunda', 'error');
    }
  },

  async loadWorkflowLog() {
    try {
      const res = await fetch('/api/bpmn/instances');
      const data = await res.json();
      if (!data.success) return;

      const container = document.getElementById('workflowLogList');
      if (!container) return;

      container.innerHTML = '';
      data.log.forEach(item => {
        const div = document.createElement('div');
        div.style = 'padding: 12px 16px; background: rgba(15,23,42,0.6); border: 1px solid var(--card-border); border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;';
        div.innerHTML = `
          <div>
            <div style="font-weight: 600; font-size: 13px; color: var(--pure-white);">${item.process || item.formKey}</div>
            <div style="font-family: var(--font-mono); font-size: 11px; color: var(--titanium-light);">${item.taskName || item.taskId} • ${item.candidateGroup || 'Ejecutado'}</div>
          </div>
          <div style="text-align: right;">
            <span class="status-chip" style="font-size: 10px;">${item.status}</span>
            <div style="font-size: 10px; color: var(--titanium-gray); margin-top: 4px;">${item.timestamp || item.submittedAt}</div>
          </div>
        `;
        container.appendChild(div);
      });
    } catch (err) {
      console.error('Error cargando historial de workflow:', err);
    }
  }
};

window.BpmnViewer = BpmnViewer;
