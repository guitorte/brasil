/* Indicadores do Brasil: motor comum dos capítulos (gráficos em SVG, tabelas, glossário,
   compartilhar e baixar imagem). Cada página define IB.hooks e chama IB.start(). */
(function () {
'use strict';
const NS = 'http://www.w3.org/2000/svg';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const nf = (d) => new Intl.NumberFormat('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
const f0 = (x) => nf(0).format(x), f1 = (x) => nf(1).format(x), f2 = (x) => nf(2).format(x);
const pct1 = (x) => f1(x) + '%';
const spp = (x) => (x > 0 ? '+' : '') + f1(x) + ' p.p.';

// ---------- glossário: as definições valem para todo o site; cada página lista só as que usa
const GLOSS = {
  'pib-hab': ['PIB por habitante', 'Tudo o que o país produz num ano, dividido pelo número de habitantes. Aqui, descontada a inflação, para comparar anos diferentes.'],
  'indice': ['Valendo 100', 'O primeiro ano vale 100, e os outros mostram quanto mudou desde então. 151 quer dizer 51% a mais; 200 quer dizer o dobro.'],
  'pp': ['Pontos percentuais', 'A diferença entre duas porcentagens. Se o Brasil cresceu 2% e o mundo 3%, o Brasil ficou 1 ponto percentual abaixo.'],
  'ppc': ['Paridade de poder de compra', 'Converte as moedas pelo que elas compram em cada país, e não pelo câmbio. Um corte de cabelo custa menos em São Paulo do que em Nova York; essa conta leva isso em conta.'],
  'commodities': ['Commodities', 'Matérias-primas vendidas no mundo inteiro por preços parecidos, como soja, minério de ferro, petróleo e café.'],
  'termos': ['Termos de troca', 'Quanto o país consegue comprar lá fora com o que vende. Sobem quando o preço do que ele exporta sobe mais que o do que importa.'],
  'projecao': ['Projeção', 'O que o FMI estima que vai acontecer. Pode mudar a cada nova edição do relatório.'],
};
let pop = null, popFor = null;
const closePop = () => { if (pop) pop.hidden = true; if (popFor) popFor.setAttribute('aria-expanded', 'false'); popFor = null; };
function glossaryInit() {
  pop = $('#pop');
  if (!pop) { pop = document.createElement('div'); pop.className = 'pop'; pop.id = 'pop'; pop.setAttribute('role', 'dialog'); pop.hidden = true; document.body.appendChild(pop); }
  const dl = $('#glossario');
  if (dl) {
    const used = Array.from(new Set($$('.term').map((t) => t.dataset.term))).filter((k) => GLOSS[k]);
    dl.replaceChildren(...used.flatMap((k) => {
      const dt = document.createElement('dt'); dt.textContent = GLOSS[k][0];
      const dd = document.createElement('dd'); dd.textContent = GLOSS[k][1];
      return [dt, dd];
    }));
  }
  $$('.term').forEach((t) => t.setAttribute('aria-expanded', 'false'));
  document.addEventListener('click', (ev) => {
    const t = ev.target.closest('.term');
    if (!t) { if (!ev.target.closest('#pop')) closePop(); return; }
    if (popFor === t) { closePop(); return; }
    const [title, text] = GLOSS[t.dataset.term] || [t.textContent, ''];
    pop.innerHTML = '';
    const b = document.createElement('b'); b.textContent = title;
    pop.append(b, document.createTextNode(text));
    pop.hidden = false;
    const r = t.getBoundingClientRect(), pw = pop.offsetWidth;
    pop.style.left = Math.max(12, Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - pw - 12)) + 'px';
    pop.style.top = (window.scrollY + r.bottom + 8) + 'px';
    t.setAttribute('aria-expanded', 'true');
    popFor = t;
  });
  document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') closePop(); });
}

// ---------- utilidades de gráfico
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const T = () => ({ ink: css('--ink'), ink2: css('--ink2'), muted: css('--muted'), grid: css('--grid'), axis: css('--axis'), surface: css('--panel'), page: css('--surface'),
  c1: css('--c1'), c2: css('--c2'), c3: css('--c3'), c4: css('--c4'), pos: css('--pos'), neg: css('--neg'), gray: css('--gray'), band: css('--band'), proj: css('--proj'), hi: css('--hi') });
const el = (tag, attrs, parent) => {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
};
const txt = (parent, s, attrs) => { const e = el('text', attrs, parent); e.textContent = s; return e; };
const lin = (d0, d1, r0, r1) => { const f = (v) => r0 + ((v - d0) / (d1 - d0)) * (r1 - r0); f.inv = (p) => d0 + ((p - r0) / (r1 - r0)) * (d1 - d0); return f; };
function ticks(lo, hi, n) {
  const raw = (hi - lo) / n, mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((s) => s * mag).find((s) => s >= raw);
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(Math.round(v * 1e6) / 1e6);
  return out;
}
const yearTicks = (a, b, w) => { const step = w < 420 ? 10 : 5; const out = []; for (let t = Math.ceil(a / step) * step; t <= b; t += step) out.push(t); return out; };
const FONT = 'Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif';
function svgFor(box, H, label) {
  const W = box.clientWidth;
  box.replaceChildren();
  const svg = el('svg', { xmlns: NS, width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': label, 'font-family': FONT }, box);
  return { svg, W, H };
}
function measure(svg, strings, size) {
  const p = txt(svg, '', { 'font-size': size }); let w = 0;
  strings.forEach((s) => { p.textContent = s; w = Math.max(w, p.getComputedTextLength()); });
  p.remove(); return w;
}
function tipBox(box) { const d = document.createElement('div'); d.className = 'tip'; d.hidden = true; box.appendChild(d); return d; }
function showTip(tip, box, px, title, rows) {
  tip.replaceChildren();
  const b = document.createElement('b'); b.textContent = title; tip.appendChild(b);
  rows.forEach(([name, color, value]) => {
    const s = document.createElement('span');
    if (color) { const i = document.createElement('i'); i.style.background = color; s.appendChild(i); }
    s.appendChild(document.createTextNode((name ? name + ': ' : '') + value));
    tip.appendChild(s);
  });
  tip.hidden = false;
  const W = box.clientWidth, tw = tip.offsetWidth;
  tip.style.left = Math.max(0, Math.min(W - tw, px + 14 + tw > W ? px - 14 - tw : px + 14)) + 'px';
  tip.style.top = '4px';
}
const roundedBar = (x, w, y0, y1, r) => {
  r = Math.min(r, w / 2, Math.abs(y1 - y0));
  if (y1 < y0) return `M${x},${y0}V${y1 + r}Q${x},${y1} ${x + r},${y1}H${x + w - r}Q${x + w},${y1} ${x + w},${y1 + r}V${y0}Z`;
  return `M${x},${y0}V${y1 - r}Q${x},${y1} ${x + r},${y1}H${x + w - r}Q${x + w},${y1} ${x + w},${y1 - r}V${y0}Z`;
};

// gráfico de linhas: séries {name, color, width, dash, pts:[{x,y}], clip, fade}
function lineChart(box, cfg) {
  if (!box.clientWidth) return;
  const t = T();
  const H = cfg.height || (box.clientWidth < 480 ? 290 : 320);
  const { svg, W } = svgFor(box, H, cfg.label);
  const yt = cfg.yTicks;
  const ml = cfg.ml || Math.ceil(measure(svg, yt.map(cfg.yFmt), 12)) + 10;
  const endW = cfg.endLabels ? Math.ceil(measure(svg, cfg.series.map((s) => s.name), 12)) + 18 : 0;
  const m = { t: 18, r: Math.max(12, endW), b: 26, l: ml };
  const x = lin(cfg.xDomain[0], cfg.xDomain[1], m.l, W - m.r), y = lin(cfg.yDomain[0], cfg.yDomain[1], H - m.b, m.t);
  (cfg.bands || []).forEach((b) => {
    el('rect', { x: x(b.x0), y: m.t, width: Math.max(0, x(b.x1) - x(b.x0)), height: H - m.b - m.t, fill: b.fill || t.band }, svg);
    if (b.label) txt(svg, b.label, { x: x(b.x0) + 4, y: m.t - 5, 'font-size': 11, fill: t.ink2 });
  });
  if (cfg.projFrom !== undefined) {
    el('rect', { x: x(cfg.projFrom), y: m.t, width: x(cfg.xDomain[1]) - x(cfg.projFrom), height: H - m.b - m.t, fill: t.proj }, svg);
    txt(svg, 'projeção', { x: x(cfg.projFrom) + 4, y: m.t - 5, 'font-size': 11, fill: t.ink2 });
  }
  yt.forEach((v) => {
    el('line', { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), stroke: t.grid }, svg);
    txt(svg, cfg.yFmt(v), { x: m.l - 8, y: y(v), dy: '0.32em', 'font-size': 12, fill: t.muted, 'text-anchor': 'end' });
  });
  (cfg.refs || []).forEach((r) => {
    el('line', { x1: m.l, x2: W - m.r, y1: y(r.y), y2: y(r.y), stroke: t.axis }, svg);
    if (r.label) txt(svg, r.label, { x: W - m.r, y: y(r.y) - 5, 'font-size': 11, fill: t.muted, 'text-anchor': 'end' });
  });
  el('line', { x1: m.l, x2: W - m.r, y1: H - m.b, y2: H - m.b, stroke: t.axis }, svg);
  (cfg.xTicks || yearTicks(cfg.xDomain[0], cfg.xDomain[1], W)).forEach((v) => txt(svg, String(v), { x: x(v), y: H - m.b + 17, 'font-size': 12, fill: t.muted, 'text-anchor': 'middle' }));
  const d = (pts) => pts.map((p, i) => (i ? 'L' : 'M') + x(p.x).toFixed(1) + ',' + y(p.y).toFixed(1)).join('');
  const ends = [];
  cfg.series.forEach((s) => {
    const pts = s.pts.filter((p) => p.x <= (s.clip === undefined ? Infinity : s.clip));
    if (!pts.length) return;
    const style = { fill: 'none', stroke: s.color, 'stroke-width': s.width || 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' };
    if (s.projFrom !== undefined) {
      el('path', { d: d(pts.filter((p) => p.x <= s.projFrom)), ...style }, svg);
      el('path', { d: d(pts.filter((p) => p.x >= s.projFrom)), ...style, 'stroke-dasharray': '5 4' }, svg);
    } else el('path', { d: d(pts), ...style, 'stroke-dasharray': s.dash || null }, svg);
    const last = pts[pts.length - 1];
    el('circle', { cx: x(last.x), cy: y(last.y), r: 4, fill: s.color, stroke: t.surface, 'stroke-width': 2 }, svg);
    if (cfg.endLabels && s.label !== false) ends.push({ s, y: y(last.y), x: x(last.x) });
  });
  if (ends.length) {   // rótulos no fim das linhas, afastados entre si, com fio até a linha
    ends.sort((a, b) => a.y - b.y);
    const gap = 15;
    ends.forEach((e, i) => { e.ly = Math.max(e.y, i ? ends[i - 1].ly + gap : m.t); });
    const over = ends.length ? ends[ends.length - 1].ly - (H - m.b) : 0;
    if (over > 0) ends.forEach((e) => { e.ly -= over; });
    for (let i = ends.length - 2; i >= 0; i--) if (ends[i].ly > ends[i + 1].ly - gap) ends[i].ly = ends[i + 1].ly - gap;
    ends.forEach((e) => {
      const lx = W - m.r + 10;
      if (Math.abs(e.ly - e.y) > 2) el('path', { d: `M${e.x + 5},${e.y}L${lx - 3},${e.ly}`, stroke: t.axis, fill: 'none' }, svg);
      txt(svg, e.s.name, { x: lx, y: e.ly, dy: '0.32em', 'font-size': 12, fill: e.s.labelStrong ? t.ink : t.ink2, 'font-weight': e.s.labelStrong ? 650 : 400 });
    });
  }
  // camada de leitura: régua vertical e caixa com os valores
  const tip = tipBox(box);
  const rule = el('line', { y1: m.t, y2: H - m.b, stroke: t.axis, display: 'none' }, svg);
  const marks = el('g', {}, svg);
  const xs = Array.from(new Set(cfg.series.flatMap((s) => s.pts.filter((p) => p.x <= (s.clip ?? Infinity)).map((p) => p.x)))).sort((a, b) => a - b);
  const hit = el('rect', { x: m.l, y: 0, width: W - m.l - m.r + 6, height: H, fill: 'transparent' }, svg);
  const move = (ev) => {
    const r = svg.getBoundingClientRect(); const px = (ev.clientX - r.left) * (W / r.width);
    const xv = x.inv(px); let best = xs[0];
    xs.forEach((v) => { if (Math.abs(v - xv) < Math.abs(best - xv)) best = v; });
    marks.replaceChildren();
    const rows = [];
    cfg.series.slice().sort((a, b) => (b.tipOrder || 0) - (a.tipOrder || 0)).forEach((s) => {
      const p = s.pts.find((q) => q.x === best && q.x <= (s.clip ?? Infinity));
      if (!p) return;
      el('circle', { cx: x(p.x), cy: y(p.y), r: 4.5, fill: s.color, stroke: t.surface, 'stroke-width': 2 }, marks);
      rows.push([s.name, s.color, cfg.tipFmt(p.y)]);
    });
    rule.setAttribute('x1', x(best)); rule.setAttribute('x2', x(best)); rule.removeAttribute('display');
    showTip(tip, box, x(best), cfg.tipTitle ? cfg.tipTitle(best) : String(best), rows);
  };
  const leave = () => { tip.hidden = true; rule.setAttribute('display', 'none'); marks.replaceChildren(); };
  hit.addEventListener('pointermove', move); hit.addEventListener('pointerdown', move); hit.addEventListener('pointerleave', leave);
  return { svg, x, y, m, W, H };
}

// barras divergentes: {bars:[{x, v, note}], xDomain, yDomain, bands}
function divBars(box, cfg) {
  if (!box.clientWidth) return;
  const t = T();
  const H = cfg.height || (box.clientWidth < 480 ? 260 : 290);
  const { svg, W } = svgFor(box, H, cfg.label);
  const yt = cfg.yTicks, fmt = (v) => (v > 0 ? '+' : '') + f0(v);
  const ml = cfg.ml || Math.ceil(measure(svg, yt.map(fmt), 12)) + 10;
  const m = { t: cfg.bands ? 18 : 10, r: 12, b: cfg.noX ? 8 : 26, l: ml };
  const n = cfg.xDomain[1] - cfg.xDomain[0] + 1, step = (W - m.l - m.r) / n;
  const bw = Math.max(1.5, Math.min(24, step - 2));
  const x = (yr) => m.l + (yr - cfg.xDomain[0]) * step + (step - bw) / 2;
  const xc = (yr) => x(yr) + bw / 2;
  const y = lin(cfg.yDomain[0], cfg.yDomain[1], H - m.b, m.t);
  (cfg.bands || []).forEach((b, i) => {
    const x0 = m.l + (Math.max(b.x0, cfg.xDomain[0]) - cfg.xDomain[0]) * step, x1 = m.l + (Math.min(b.x1, cfg.xDomain[1]) - cfg.xDomain[0] + 1) * step;
    if (x1 <= x0) return;
    if (b.fill || i % 2 === 0) el('rect', { x: x0, y: m.t, width: x1 - x0, height: H - m.b - m.t, fill: b.fill || t.band }, svg);
    const lab = [b.label, b.short].find((l) => l && x1 - x0 > measure(svg, [l], 10.5) + 6);
    if (lab) txt(svg, lab, { x: x0 + 3, y: m.t - 5, 'font-size': 10.5, fill: t.ink2 });
  });
  yt.forEach((v) => {
    el('line', { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), stroke: v === 0 ? t.axis : t.grid }, svg);
    txt(svg, fmt(v), { x: m.l - 8, y: y(v), dy: '0.32em', 'font-size': 12, fill: t.muted, 'text-anchor': 'end' });
  });
  const bars = cfg.bars.filter((b) => b.x >= cfg.xDomain[0] && b.x <= cfg.xDomain[1]);
  const shapes = bars.map((b) => el('path', { d: roundedBar(x(b.x), bw, y(0), y(b.v), 3), fill: b.v >= 0 ? t.pos : t.neg }, svg));
  if (!cfg.noX) yearTicks(cfg.xDomain[0], cfg.xDomain[1], W).forEach((v) => txt(svg, String(v), { x: xc(v), y: H - m.b + 17, 'font-size': 12, fill: t.muted, 'text-anchor': 'middle' }));
  const tip = tipBox(box);
  const hit = el('rect', { x: m.l, y: 0, width: W - m.l - m.r, height: H, fill: 'transparent' }, svg);
  const move = (ev) => {
    const r = svg.getBoundingClientRect(); const px = (ev.clientX - r.left) * (W / r.width);
    const i = Math.max(0, Math.min(bars.length - 1, Math.floor((px - m.l) / step)));
    shapes.forEach((s, k) => s.setAttribute('opacity', k === i ? 1 : 0.4));
    const b = bars[i];
    showTip(tip, box, xc(b.x), String(b.x), [['', '', spp(b.v)], ...b.note]);
  };
  const leave = () => { tip.hidden = true; shapes.forEach((s) => s.removeAttribute('opacity')); };
  hit.addEventListener('pointermove', move); hit.addEventListener('pointerdown', move); hit.addEventListener('pointerleave', leave);
}

// halteres: linhas = países; círculo vazio = início, cheio = fim
function dumbbell(box, cfg) {
  if (!box.clientWidth) return;
  const t = T();
  const rowH = 32, top = 26, H = top + cfg.rows.length * rowH + 8;
  const { svg, W } = svgFor(box, H, cfg.label);
  const ml = Math.ceil(measure(svg, cfg.rows.map((r) => r.name), 13)) + 14, mr = 44;
  const x = lin(cfg.domain[0], cfg.domain[1], ml, W - mr);
  cfg.ticks.forEach((v) => {
    el('line', { x1: x(v), x2: x(v), y1: top - 6, y2: H - 6, stroke: t.grid }, svg);
    txt(svg, cfg.fmt(v), { x: x(v), y: top - 12, 'font-size': 11.5, fill: t.muted, 'text-anchor': 'middle' });
  });
  const tip = tipBox(box);
  cfg.rows.forEach((r, i) => {
    const cy = top + i * rowH + rowH / 2;
    const g = el('g', {}, svg);
    if (r.hl) el('rect', { x: 0, y: cy - rowH / 2 + 2, width: W, height: rowH - 4, rx: 6, fill: t.hi }, g);
    txt(g, r.name, { x: ml - 10, y: cy, dy: '0.32em', 'font-size': 13, fill: r.hl ? t.ink : t.ink2, 'text-anchor': 'end', 'font-weight': r.hl ? 700 : 400 });
    const col = r.hl ? t.c1 : (r.agg ? t.gray : t.ink2);
    el('line', { x1: x(r.a), x2: x(r.b), y1: cy, y2: cy, stroke: col, 'stroke-width': r.hl ? 3 : 2, 'stroke-opacity': r.hl ? 1 : 0.55 }, g);
    el('circle', { cx: x(r.a), cy, r: 5, fill: t.surface, stroke: col, 'stroke-width': 2 }, g);
    el('circle', { cx: x(r.b), cy, r: 5.5, fill: col, stroke: t.surface, 'stroke-width': 2 }, g);
    txt(g, cfg.fmt(r.b), { x: x(Math.max(r.a, r.b)) + 10, y: cy, dy: '0.32em', 'font-size': 12, fill: r.hl ? t.ink : t.muted, 'font-weight': r.hl ? 650 : 400 });
    const hit = el('rect', { x: 0, y: cy - rowH / 2, width: W, height: rowH, fill: 'transparent' }, g);
    const show = () => { showTip(tip, box, x(r.b), r.name, [['1990', '', cfg.fmt(r.a)], ['2025', '', cfg.fmt(r.b)], ['Variação', '', spp(r.b - r.a)]]); tip.style.top = (cy + 14) + 'px'; };
    hit.addEventListener('pointerenter', show); hit.addEventListener('pointerdown', show);
    hit.addEventListener('pointerleave', () => { tip.hidden = true; });
  });
}

// pontos por período: linhas = períodos; um ponto por série
function dotRows(box, cfg) {
  if (!box.clientWidth) return;
  const t = T();
  const rowH = 30, top = 24, H = top + cfg.rows.length * rowH + 6;
  const { svg, W } = svgFor(box, H, cfg.label);
  const ml = Math.ceil(measure(svg, cfg.rows.map((r) => r.label), 12.5)) + 14;
  const x = lin(cfg.domain[0], cfg.domain[1], ml, W - 12);
  cfg.ticks.forEach((v) => {
    el('line', { x1: x(v), x2: x(v), y1: top - 6, y2: H - 4, stroke: v === 0 ? t.axis : t.grid }, svg);
    txt(svg, f0(v) + '%', { x: x(v), y: top - 12, 'font-size': 11.5, fill: t.muted, 'text-anchor': 'middle' });
  });
  const tip = tipBox(box);
  cfg.rows.forEach((r, i) => {
    const cy = top + i * rowH + rowH / 2;
    txt(svg, r.label, { x: ml - 10, y: cy, dy: '0.32em', 'font-size': 12.5, fill: t.ink2, 'text-anchor': 'end', 'font-weight': r.bold ? 650 : 400 });
    const vals = cfg.keys.map((k) => r[k.key]).filter((v) => v !== null);
    el('line', { x1: x(Math.min(...vals)), x2: x(Math.max(...vals)), y1: cy, y2: cy, stroke: t.axis, 'stroke-width': 2 }, svg);
    cfg.keys.slice().reverse().forEach((k) => { if (r[k.key] !== null) el('circle', { cx: x(r[k.key]), cy, r: 5.5, fill: t[k.color], stroke: t.surface, 'stroke-width': 2 }, svg); });
    const hit = el('rect', { x: 0, y: cy - rowH / 2, width: W, height: rowH, fill: 'transparent' }, svg);
    const show = () => { showTip(tip, box, x(r.brasil), r.label + (r.contexto ? ' · ' + r.contexto : ''), cfg.keys.map((k) => [k.name, t[k.color], r[k.key] === null ? '—' : pct1(r[k.key])])); tip.style.top = (cy + 14) + 'px'; };
    hit.addEventListener('pointerenter', show); hit.addEventListener('pointerdown', show);
    hit.addEventListener('pointerleave', () => { tip.hidden = true; });
  });
}

// ---------- tabelas
function table(host, cols, rows, opt = {}) {
  const tb = document.createElement('table');
  const thead = tb.createTHead(), hr = thead.insertRow();
  cols.forEach((c) => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = c.label; hr.appendChild(th); });
  const body = tb.createTBody();
  let prevProj = false;
  rows.forEach((r) => {
    const tr = body.insertRow();
    if (opt.pin && opt.pin(r)) tr.className = 'pin';
    const proj = opt.proj && opt.proj(r);
    if (proj) tr.className = prevProj ? 'proj' : 'proj proj-first';
    prevProj = !!proj;
    cols.forEach((c, i) => {
      const cell = document.createElement(i ? 'td' : 'th');
      if (!i) cell.scope = 'row';
      const v = c.get(r);
      cell.textContent = v === null || v === undefined || Number.isNaN(v) ? '' : (c.fmt ? c.fmt(v) : v);
      if (!i && proj) { const s = document.createElement('span'); s.className = 'tag'; s.textContent = 'proj.'; cell.appendChild(s); }
      tr.appendChild(cell);
    });
  });
  host.replaceChildren(tb);
  requestAnimationFrame(() => host.style.setProperty('--thead-h', thead.offsetHeight + 'px'));
}


// ---------- compartilhar e baixar imagem
let toast = null;
let toastT = 0;
const say = (s) => { if (!toast) { toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status'); document.body.appendChild(toast); } toast.textContent = s; toast.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => { toast.hidden = true; }, 2200); };
async function share(card) {
  const url = location.origin + location.pathname + '#' + card.id;
  const title = card.querySelector('h2').textContent;
  try {
    if (navigator.share) { await navigator.share({ title, text: title, url }); return; }
    await navigator.clipboard.writeText(url); say('Link copiado');
  } catch (e) { if (e && e.name !== 'AbortError') say('Não foi possível compartilhar'); }
}
function wrap(ctx, s, maxW) {
  const words = s.split(' '), lines = []; let cur = '';
  words.forEach((w) => { const tryS = cur ? cur + ' ' + w : w; if (ctx.measureText(tryS).width > maxW && cur) { lines.push(cur); cur = w; } else cur = tryS; });
  if (cur) lines.push(cur);
  return lines;
}
async function exportImage(card) {
  const svgs = $$('[data-pane="chart"] svg', card);
  if (!svgs.length || card.querySelector('[data-pane="chart"]').hidden) { say('Mude para “Gráfico” para baixar a imagem'); return; }
  const t = T(), S = 2, W = 540, pad = 24;
  const imgs = await Promise.all(svgs.map((svg) => new Promise((res, rej) => {
    const c = svg.cloneNode(true); c.setAttribute('xmlns', NS);
    const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(c)], { type: 'image/svg+xml' }));
    const im = new Image(); im.onload = () => { URL.revokeObjectURL(url); res({ im, w: svg.width.baseVal.value, h: svg.height.baseVal.value }); }; im.onerror = rej; im.src = url;
  })));
  const probe = document.createElement('canvas').getContext('2d');
  probe.font = '700 22px ' + FONT;
  const tl = wrap(probe, card.querySelector('h2').textContent, W - 2 * pad);
  const legend = $$('[data-pane="chart"] .legend .lg', card).map((l) => [getComputedStyle(l.querySelector('i')).backgroundColor, l.textContent, l.querySelector('i').className]);
  const chartW = W - 2 * pad;
  const chartH = imgs.reduce((h, i) => h + i.h * (chartW / i.w) + 6, 0);
  const H = 44 + 20 + tl.length * 28 + (legend.length ? 30 : 8) + chartH + 64;
  const cv = document.createElement('canvas'); cv.width = W * S; cv.height = H * S;
  const ctx = cv.getContext('2d'); ctx.scale(S, S);
  ctx.fillStyle = t.page; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = '#f5d93a'; ctx.fillRect(0, 0, W, 44); ctx.fillStyle = '#0b0b0b'; ctx.fillRect(0, 44, W, 3);
  ctx.font = '800 15px ' + FONT; ctx.fillText('INDICADORES DO BRASIL', pad, 28);
  ctx.font = '600 12px ' + FONT; ctx.textAlign = 'right'; ctx.fillText('guitorte.github.io/brasil', W - pad, 28); ctx.textAlign = 'left';
  let yy = 47 + 30;
  ctx.fillStyle = t.ink; ctx.font = '700 22px ' + FONT;
  tl.forEach((l) => { ctx.fillText(l, pad, yy); yy += 28; });
  if (legend.length) {
    let lx = pad; ctx.font = '400 12px ' + FONT;
    legend.forEach(([col, label, cls]) => {
      ctx.fillStyle = col === 'rgba(0, 0, 0, 0)' ? t.panel || t.surface : col;
      if (cls.includes('ring')) { ctx.strokeStyle = t.ink2; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(lx + 5, yy - 4, 5, 0, 7); ctx.stroke(); }
      else ctx.fillRect(lx, cls.includes('ln') ? yy - 5 : yy - 9, 10, cls.includes('ln') ? 3 : 10);
      ctx.fillStyle = t.ink2; ctx.fillText(label, lx + 15, yy); lx += 15 + ctx.measureText(label).width + 16;
    });
    yy += 14;
  }
  imgs.forEach(({ im, w, h }) => { const hh = h * (chartW / w); ctx.drawImage(im, pad, yy, chartW, hh); yy += hh + 6; });
  ctx.fillStyle = t.muted; ctx.font = '400 11px ' + FONT;
  wrap(ctx, card.dataset.source, W - 2 * pad).forEach((l, i) => ctx.fillText(l, pad, H - 34 + i * 14));
  cv.toBlob(async (blob) => {
    const name = (document.body.dataset.slug || 'grafico') + '-' + card.id + '.png';
    const file = new File([blob], name, { type: 'image/png' });
    try {
      if (navigator.canShare && navigator.canShare({ files: [file] })) { await navigator.share({ files: [file], title: card.querySelector('h2').textContent }); return; }
    } catch (e) { if (e && e.name === 'AbortError') return; }
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    say('Imagem baixada');
  }, 'image/png');
}


// ---------- controles comuns: botões de escolha, gráfico/tabela, aprofundar, compartilhar
const hooks = {};
function controlsInit() {
  document.addEventListener('click', (ev) => {
    $$('details.menu[open]').forEach((m) => { if (!m.contains(ev.target)) m.open = false; });
    const chip = ev.target.closest('.chip[data-v]');
    if (chip) {
      const grp = chip.closest('[data-ctl]');
      if (!grp) return;
      if (!grp.hasAttribute('data-multi')) $$('.chip', grp).forEach((b) => b.setAttribute('aria-pressed', b === chip ? 'true' : 'false'));
      if (hooks.chip) hooks.chip(grp.dataset.ctl, chip.dataset.v, chip);
      return;
    }
    const seg = ev.target.closest('.seg button');
    if (seg) {
      const card = seg.closest('.card'), v = seg.dataset.view;
      $$('.seg button', card).forEach((b) => b.setAttribute('aria-pressed', b === seg ? 'true' : 'false'));
      $$('[data-pane]', card).forEach((p) => { p.hidden = p.dataset.pane !== v; });
      if (hooks.view) hooks.view(card.id, v);
      return;
    }
    const act = ev.target.closest('.act');
    if (act) { const card = act.closest('.card'); if (act.dataset.act === 'share') share(card); else exportImage(card); }
  });
  $$('details.more').forEach((d) => d.addEventListener('toggle', () => { if (d.open && hooks.more) hooks.more(d.closest('.card').id, d); }));
}

// ---------- progresso de leitura, redesenho e tema
function start() {
  glossaryInit();
  controlsInit();
  const bar = $('.progress span');
  if (bar) {
    const onScroll = () => { const h = document.documentElement; bar.style.width = (100 * h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight)) + '%'; };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  const redraw = (full) => { closePop(); if (hooks.redraw) hooks.redraw(full); };
  let lastW = document.documentElement.clientWidth, rt = 0;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(rt);
    rt = requestAnimationFrame(() => { const w = document.documentElement.clientWidth; redraw(w !== lastW); lastW = w; });
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => redraw(true));
  redraw(true);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => redraw(true));
  document.documentElement.dataset.ready = '1';
}

window.IB = { $, $$, NS, reduce, nf, f0, f1, f2, pct1, spp, T, el, txt, lin, ticks, yearTicks, lineChart, divBars, dumbbell, dotRows, table,
  GLOSS, closePop, say, share, exportImage, hooks, start };
})();
