// tools/gif_scene.html 의 애니메이션을 2.4초 주기로 30프레임 캡처한다.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FRAMES = 30, LOOP_MS = 2400;
(async () => {
  const out = path.join(__dirname, 'frames');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 600, height: 360 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'gif_scene.html'));
  await page.waitForTimeout(800);
  for (let i = 0; i < FRAMES; i++) {
    const t = LOOP_MS * 10 + (LOOP_MS / FRAMES) * i;
    await page.evaluate(t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }), t);
    await page.locator('svg').first().screenshot({ path: path.join(out, `f${String(i).padStart(2, '0')}.png`), animations: 'allow' });
  }
  await browser.close();
})();
