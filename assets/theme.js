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
  initHeroProductSlider();
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

function initHeroProductSlider() {
  var root = document.querySelector('[data-hero-slider]');
  if (!root) return;

  var slides = root.querySelectorAll('.hero__feature-slide');
  var captions = root.querySelectorAll('.hero__feature-caption');
  var dots = root.querySelectorAll('.hero__feature-dot');
  var count = slides.length;
  if (!count) return;

  var activeIndex = 0;
  var timer = null;
  var intervalMs = 3500;
  var prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setActive(index) {
    activeIndex = (index + count) % count;
    for (var i = 0; i < count; i++) {
      var isActive = i === activeIndex;
      slides[i].classList.toggle('is-active', isActive);
      if (captions[i]) captions[i].classList.toggle('is-active', isActive);
      if (dots[i]) dots[i].classList.toggle('is-active', isActive);
    }
  }

  function next() {
    setActive(activeIndex + 1);
  }

  function start() {
    if (prefersReducedMotion || count < 2) return;
    stop();
    timer = window.setInterval(next, intervalMs);
  }

  function stop() {
    if (timer) {
      window.clearInterval(timer);
      timer = null;
    }
  }

  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      setActive(i);
      start();
    });
  });

  // Pause the automatic advance while a visitor is looking at/interacting
  // with the slider, resume once they move away — an autoplaying carousel
  // that fights the user's own navigation is worse than no autoplay.
  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);
  root.addEventListener('focusin', stop);
  root.addEventListener('focusout', start);

  start();
}
