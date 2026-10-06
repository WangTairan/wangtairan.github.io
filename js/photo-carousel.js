document.querySelectorAll('.photo-container').forEach(carousel => {
  const track = carousel.querySelector('.photo-track');
  const slides = Array.from(carousel.querySelectorAll('.photo-slide'));
  const controls = carousel.querySelector('.photo-dots');
  const status = carousel.querySelector('.photo-status');
  if (!track || !controls || slides.length < 2) return;

  let current = 0;
  let pendingFrame = false;
  const buttons = slides.map((slide, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'photo-dot';
    button.setAttribute('aria-label', `Show portrait: ${slide.dataset.label}`);
    button.setAttribute('aria-pressed', String(index === 0));
    button.addEventListener('click', () => goTo(index));
    controls.append(button);
    return button;
  });
  controls.hidden = false;

  function goTo(index, behavior) {
    const target = Math.max(0, Math.min(index, slides.length - 1));
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    track.scrollTo({left: target * track.clientWidth, behavior: behavior || (reducedMotion ? 'auto' : 'smooth')});
  }

  function update() {
    pendingFrame = false;
    if (!track.clientWidth) return;
    const index = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
    if (index === current) return;
    current = index;
    buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === current)));
    if (status) status.textContent = slides[current].dataset.label;
  }

  track.addEventListener('scroll', () => {
    if (!pendingFrame) {
      pendingFrame = true;
      requestAnimationFrame(update);
    }
  }, {passive: true});

  track.addEventListener('keydown', event => {
    const targets = {ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: slides.length - 1};
    if (!(event.key in targets)) return;
    event.preventDefault();
    goTo(targets[event.key]);
  });

  if ('ResizeObserver' in window) {
    new ResizeObserver(() => goTo(current, 'auto')).observe(track);
  }
});
