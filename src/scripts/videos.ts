/**
 * Muted looping cover videos:
 * - never autoplay under prefers-reduced-motion
 * - play only while on screen, pause when off screen
 * - a visible toggle lets users pause/play (WCAG 2.2.2)
 */
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const wrappers = document.querySelectorAll<HTMLElement>('[data-loop-video]');

function setState(wrapper: HTMLElement, playing: boolean) {
  wrapper.classList.toggle('is-playing', playing);
  const btn = wrapper.querySelector<HTMLButtonElement>('[data-video-toggle]');
  if (btn) {
    btn.setAttribute('aria-pressed', String(!playing));
    const label = playing ? btn.dataset.labelPause : btn.dataset.labelPlay;
    if (label) btn.setAttribute('aria-label', label);
  }
}

wrappers.forEach((wrapper) => {
  const video = wrapper.querySelector('video');
  if (!video) return;
  let userPaused = reduce.matches;
  let visible = false;

  const sync = () => {
    if (visible && !userPaused) {
      if (video.preload === 'none') video.preload = 'auto';
      video.play().then(() => setState(wrapper, true)).catch(() => setState(wrapper, false));
    } else {
      video.pause();
      setState(wrapper, false);
    }
  };

  new IntersectionObserver(([entry]) => {
    visible = entry!.isIntersecting;
    sync();
  }, { threshold: 0.25 }).observe(wrapper);

  const toggle = wrapper.querySelector<HTMLButtonElement>('[data-video-toggle]');
  toggle?.addEventListener('click', (e) => {
    e.preventDefault();
    userPaused = !video.paused;
    sync();
  });

  reduce.addEventListener('change', () => {
    userPaused = reduce.matches;
    sync();
  });
});
