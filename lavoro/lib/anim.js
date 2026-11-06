// Helper di animazione deterministici: ogni pagina espone window.seek(t) (t in secondi).
const A = {
  clamp: (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)),
  p: (t, start, dur) => A.clamp((t - start) / dur),
  outCubic: x => 1 - Math.pow(1 - x, 3),
  inOutCubic: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  outBack: (x, s = 1.2) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
  lerp: (a, b, k) => a + (b - a) * k,
  // entrata standard: dissolvenza + piccolo scorrimento (dy px) + scala leggera
  enter(el, t, start, { dur = .45, dy = 18, dx = 0, scale = .985, exit = null, exitDur = .35 } = {}) {
    let k = A.outCubic(A.p(t, start, dur));
    let o = k, y = (1 - k) * dy, x = (1 - k) * dx, s = A.lerp(scale, 1, k);
    if (exit !== null && t >= exit) {
      const e = A.inOutCubic(A.p(t, exit, exitDur));
      o = k * (1 - e); y -= e * Math.abs(dy) * .6;
    }
    el.style.opacity = o.toFixed(4);
    el.style.transform = `translate(${x.toFixed(2)}px, ${y.toFixed(2)}px) scale(${s.toFixed(4)})`;
  },
};
window.A = A;
