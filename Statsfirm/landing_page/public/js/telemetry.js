/**
 * STATSFIRM CO. - TELEMETRY & DATA VISUALIZATION ENGINE
 * Interactive SVG Gantt Chart, Burndown Chart, and Lakehouse Pipeline Health
 */

const TelemetryEngine = {
  renderGantt(containerId, tasks) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const width = container.clientWidth || 650;
    const rowHeight = 44;
    const headerHeight = 36;
    const totalHeight = headerHeight + (tasks.length * rowHeight);

    let rowsSvg = '';
    tasks.forEach((t, i) => {
      const y = headerHeight + (i * rowHeight);
      const barWidth = Math.max(20, (width - 240) * (t.progress / 100));
      const color = t.status === 'DONE' ? 'var(--code-green)' : 'var(--electric-cyan)';

      rowsSvg += `
        <g class="gantt-row" transform="translate(0, ${y})">
          <line x1="0" y1="${rowHeight}" x2="${width}" y2="${rowHeight}" stroke="rgba(255,255,255,0.06)" />
          <text x="10" y="26" fill="#FFFFFF" font-size="13" font-family="var(--font-body)">${t.task}</text>
          <text x="10" y="38" fill="var(--titanium-gray)" font-size="10" font-family="var(--font-mono)">${t.owner}</text>
          
          <rect x="220" y="10" width="${width - 240}" height="18" rx="6" fill="rgba(255,255,255,0.05)" />
          <rect x="220" y="10" width="${barWidth}" height="18" rx="6" fill="${color}" opacity="0.85">
            <animate attributeName="width" from="0" to="${barWidth}" dur="0.8s" fill="freeze" />
          </rect>
          <text x="${230 + barWidth}" y="23" fill="#FFFFFF" font-size="11" font-family="var(--font-mono)" font-weight="bold">${t.progress}%</text>
        </g>
      `;
    });

    container.innerHTML = `
      <svg width="100%" height="${totalHeight}" viewBox="0 0 ${width} ${totalHeight}" style="overflow: visible;">
        <rect x="0" y="0" width="${width}" height="${headerHeight}" fill="rgba(15, 23, 42, 0.6)" />
        <text x="10" y="22" fill="var(--titanium-light)" font-size="11" font-family="var(--font-mono)">ENTREGABLE / TAREA TÉCNICA</text>
        <text x="220" y="22" fill="var(--titanium-light)" font-size="11" font-family="var(--font-mono)">PROGRESO DE SPRINT (%)</text>
        ${rowsSvg}
      </svg>
    `;
  },

  renderBurndown(containerId, dataPoints) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const width = container.clientWidth || 550;
    const height = 240;
    const padding = 40;

    const maxPoints = 50;
    const stepX = (width - (padding * 2)) / (dataPoints.length - 1);

    let idealPath = '';
    let actualPath = '';
    let dotsSvg = '';

    dataPoints.forEach((d, i) => {
      const x = padding + (i * stepX);
      const yIdeal = height - padding - ((d.ideal / maxPoints) * (height - (padding * 2)));
      const yActual = height - padding - ((d.actual / maxPoints) * (height - (padding * 2)));

      if (i === 0) {
        idealPath += `M ${x} ${yIdeal}`;
        actualPath += `M ${x} ${yActual}`;
      } else {
        idealPath += ` L ${x} ${yIdeal}`;
        actualPath += ` L ${x} ${yActual}`;
      }

      dotsSvg += `
        <circle cx="${x}" cy="${yActual}" r="4" fill="var(--code-green)" stroke="var(--bg-dark-slate)" stroke-width="2" />
        <text x="${x}" y="${height - 15}" fill="var(--titanium-gray)" font-size="9" text-anchor="middle" font-family="var(--font-mono)">${d.day.split(' ')[0]}</text>
      `;
    });

    container.innerHTML = `
      <svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}">
        <!-- Grid lines -->
        <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="rgba(255,255,255,0.1)" />
        <line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height - padding}" stroke="rgba(255,255,255,0.1)" />
        
        <!-- Ideal Velocity Line -->
        <path d="${idealPath}" fill="none" stroke="var(--titanium-gray)" stroke-dasharray="4 4" stroke-width="2" />
        
        <!-- Actual Velocity Line -->
        <path d="${actualPath}" fill="none" stroke="var(--code-green)" stroke-width="3" />
        
        ${dotsSvg}
        
        <text x="${width - padding}" y="${padding + 10}" fill="var(--code-green)" font-size="11" font-family="var(--font-mono)" text-anchor="end">Actual: 10 SP restantes</text>
        <text x="${width - padding}" y="${padding + 26}" fill="var(--titanium-gray)" font-size="10" font-family="var(--font-mono)" text-anchor="end">Ideal: 14.4 SP</text>
      </svg>
    `;
  }
};

window.TelemetryEngine = TelemetryEngine;
