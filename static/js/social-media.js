/* ── Pause on hover ─────────────────────── */
const wraps = document.querySelectorAll('.card-wrap');

    wraps.forEach(wrap => {
    wrap.addEventListener('mouseenter', () => {
        wraps.forEach(w => {
        const elapsed = getComputedStyle(w).animationDelay;
        w.style.animationPlayState = 'paused';
        });
    });
    wrap.addEventListener('mouseleave', () => {
        wraps.forEach(w => {
        w.style.animationPlayState = 'running';
        });
    });
});