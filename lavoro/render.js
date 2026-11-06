// Uso: node render.js <pagina.html> <n_fotogrammi> <cartella_png> [fps=24]
// Apre la pagina a 1920x1080 con sfondo trasparente e salva un PNG RGBA per fotogramma, chiamando window.seek(t).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [page_, n, out, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 24);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: Number(process.env.VW || 1920), height: Number(process.env.VH || 1080) }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => typeof window.seek === 'function');
  for (let i = 0; i < Number(n); i++) {
    const t = i / fps;
    await page.evaluate(t => window.seek(t), t);
    await page.screenshot({ path: path.join(out, `f_${String(i).padStart(5, '0')}.png`), omitBackground: true });
  }
  await browser.close();
})();
