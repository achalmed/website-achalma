// about/trayectoria.js — conducta de la página «Sobre mí» (about/index.qmd), 2026-10-21.
// 1. Filtros de la trayectoria por área (los botones y los data-areas los escribe scripts/cv-a-web.py desde el CV).
// 2. Índice de la página: marca la sección visible. Sin dependencias; sin JS, la página se lee entera igual.
(() => {
  const raiz = document.querySelector('[data-trayectoria]');
  if (raiz) {
    const botones = [...raiz.querySelectorAll('[data-filtro]')];
    const hitos = [...raiz.querySelectorAll('.hito')];
    botones.forEach((b) => b.addEventListener('click', () => {
      const filtro = b.dataset.filtro;
      botones.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      hitos.forEach((h) => { h.hidden = filtro !== 'todo' && !(h.dataset.areas || '').split(' ').includes(filtro); });
    }));
  }

  const enlaces = new Map([...document.querySelectorAll('.ficha-indice a[href^="#"]')].map((a) => [a.getAttribute('href').slice(1), a]));
  if (enlaces.size && 'IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entradas) => {
      entradas.forEach((e) => {
        if (!e.isIntersecting) return;
        enlaces.forEach((a) => a.removeAttribute('aria-current'));
        const a = enlaces.get(e.target.id);
        if (!a) return;
        a.setAttribute('aria-current', 'location');
        // Solo el índice se desliza (en horizontal, en el celular): nunca la página.
        const nav = a.parentElement;
        nav.scrollTo({ left: a.offsetLeft - (nav.clientWidth - a.offsetWidth) / 2, behavior: 'smooth' });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    enlaces.forEach((_, id) => { const s = document.getElementById(id); if (s) obs.observe(s); });
  }
})();
