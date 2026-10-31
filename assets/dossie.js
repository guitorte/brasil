/* Comportamento dos dossiês: notas ao toque, sumário em folha, seção atual e barra de leitura.
   Sem dependências. Sem este arquivo a página continua legível: as notas levam à lista de
   referências e o botão "Sumário" leva ao sumário do topo. */
(function () {
  'use strict';
  var folhaNota = document.getElementById('folha-nota');
  var folhaSumario = document.getElementById('folha-sumario');
  var corpoNota = document.getElementById('folha-nota-corpo');
  var tituloNota = document.getElementById('folha-nota-titulo');
  var botao = document.querySelector('.bt-sumario');
  var rotulo = botao && botao.querySelector('span');
  var topo = document.querySelector('.bt-topo');
  var barra = document.querySelector('.progresso span');
  var secoes = [].slice.call(document.querySelectorAll('main section[id]'));

  function ir(hash) {
    var alvo = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!alvo) return;
    if (location.hash === hash) alvo.scrollIntoView();
    else location.hash = hash;
  }

  function mostrarNotas(sup) {
    var links = sup.querySelectorAll('a');
    corpoNota.textContent = '';
    links.forEach(function (a) {
      var n = a.getAttribute('href').replace('#ref-', '');
      var li = document.getElementById('ref-' + n);
      if (!li) return;
      var p = document.createElement('p');
      p.innerHTML = '<b>[' + n + ']</b> ' + li.querySelector('.ref-txt').innerHTML +
        ' <a href="#ref-' + n + '">ver na lista</a>';
      corpoNota.appendChild(p);
    });
    tituloNota.textContent = links.length > 1 ? 'Referências' : 'Referência';
    folhaNota.showModal();
  }

  function mostrarTermo(t) {
    var id = t.getAttribute('href');                     // '#g-fgc'
    var item = document.getElementById(id.slice(1));
    if (!item) return;
    corpoNota.textContent = '';
    var p = document.createElement('p');
    p.innerHTML = item.querySelector('dd').innerHTML + ' <a href="' + id + '">ver no glossário</a>';
    corpoNota.appendChild(p);
    tituloNota.textContent = item.querySelector('dt').textContent;
    folhaNota.showModal();
  }

  // Folhas que sobem de baixo (só onde o navegador tem <dialog>).
  if (folhaNota && typeof folhaNota.showModal === 'function') {
    var toc = document.querySelector('#sumario .toc');
    if (toc) document.getElementById('folha-sumario-corpo').appendChild(toc.cloneNode(true));

    [folhaNota, folhaSumario].forEach(function (d) {
      d.addEventListener('click', function (e) {
        if (e.target === d) { d.close(); return; }          // toque fora da folha fecha
        var a = e.target.closest('a[href^="#"]');
        if (a) { e.preventDefault(); d.close(); ir(a.getAttribute('href')); }
      });
    });

    document.addEventListener('click', function (e) {
      if (e.target.closest('dialog')) return;
      var a = e.target.closest('sup.nota a');
      if (a) { e.preventDefault(); mostrarNotas(a.parentNode); return; }
      var t = e.target.closest('a.termo');
      if (t) { e.preventDefault(); mostrarTermo(t); }
    });

    if (botao) botao.addEventListener('click', function (e) {
      e.preventDefault();
      folhaSumario.showModal();
      var atual = folhaSumario.querySelector('[aria-current]');
      if (atual) atual.scrollIntoView({ block: 'center' });
    });
  }

  // Seção atual (no botão e no sumário) e barra de leitura.
  var atual = null, agendado = false;
  function atualizar() {
    agendado = false;
    var h = document.documentElement;
    var total = h.scrollHeight - h.clientHeight;
    if (barra) barra.style.transform = 'scaleX(' + (total > 0 ? window.scrollY / total : 0) + ')';
    if (topo) topo.hidden = window.scrollY < window.innerHeight;
    var s = null;
    for (var i = 0; i < secoes.length; i++) {
      if (secoes[i].getBoundingClientRect().top <= 120) s = secoes[i];
      else break;
    }
    if (s === atual) return;
    atual = s;
    if (rotulo) rotulo.textContent = s ? s.querySelector('h2').textContent : 'Sumário';
    document.querySelectorAll('.toc a[aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    if (s) document.querySelectorAll('.toc a[href="#' + s.id + '"]').forEach(function (a) {
      a.setAttribute('aria-current', 'location');
    });
  }
  window.addEventListener('scroll', function () {
    if (!agendado) { agendado = true; requestAnimationFrame(atualizar); }
  }, { passive: true });
  window.addEventListener('resize', atualizar);
  atualizar();
})();
