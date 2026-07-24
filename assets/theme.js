document.addEventListener('DOMContentLoaded', function () {
  var menuToggle = document.getElementById('MenuToggle');
  var mobileMenu = document.getElementById('MobileMenu');
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', function () {
      var isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
      mobileMenu.hidden = isOpen;
    });
  }

  var searchToggle = document.getElementById('SearchToggle');
  var searchDrawer = document.getElementById('SearchDrawer');
  if (searchToggle && searchDrawer) {
    searchToggle.addEventListener('click', function () {
      searchDrawer.hidden = !searchDrawer.hidden;
      if (!searchDrawer.hidden) {
        var input = searchDrawer.querySelector('input[name="q"]');
        if (input) input.focus();
      }
    });
  }

  initScrollShowcase();
});

function initScrollShowcase() {
  var section = document.querySelector('[data-scroll-showcase]');
  if (!section) return;

  var track = document.getElementById('ScrollShowcaseTrack');
  var panels = section.querySelectorAll('.scroll-showcase__panel');
  var imageSlides = section.querySelectorAll('.scroll-showcase__image-slide');
  var dots = section.querySelectorAll('.scroll-showcase__dot');
  var count = panels.length;
  if (!track || !count) return;

  var colors = [];
  try {
    colors = JSON.parse(section.getAttribute('data-colors') || '[]');
  } catch (err) {
    colors = [];
  }

  // Progressive enhancement: only stretch the track once JS confirms it can drive the effect.
  // If this script fails to load, the section stays a normal single-viewport panel (CSS fallback).
  track.style.height = (count * 100) + 'vh';

  var activeIndex = 0;
  var ticking = false;

  function setActive(index) {
    if (index === activeIndex) return;
    activeIndex = index;
    for (var i = 0; i < count; i++) {
      var isActive = i === index;
      panels[i].classList.toggle('is-active', isActive);
      if (imageSlides[i]) imageSlides[i].classList.toggle('is-active', isActive);
      if (dots[i]) dots[i].classList.toggle('is-active', isActive);
    }
    if (colors[index]) {
      section.style.setProperty('--bg-left', colors[index].light);
      section.style.setProperty('--bg-right', colors[index].dark);
    }
  }

  function update() {
    var rect = track.getBoundingClientRect();
    var scrollableHeight = track.offsetHeight - window.innerHeight;
    var progress = scrollableHeight > 0 ? (-rect.top) / scrollableHeight : 0;
    if (progress < 0) progress = 0;
    if (progress > 1) progress = 1;
    var index = Math.floor(progress * count);
    if (index >= count) index = count - 1;
    if (index < 0) index = 0;
    setActive(index);
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      var targetTop = track.offsetTop + (track.offsetHeight * (i / count)) + 20;
      window.scrollTo({ top: targetTop, behavior: 'smooth' });
    });
  });

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
}
