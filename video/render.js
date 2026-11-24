// node render.js frames pt 8.4 12.5 18 25   -> PNG checks
// node render.js video pt out.mp4           -> 31.5 s at 30 fps, frames piped into ffmpeg
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
(async () => {
  const [mode, lang, ...rest] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await pg.goto('file://' + __dirname + '/scene.html?lang=' + lang);
  await pg.evaluate(() => document.fonts.ready);
  if (mode === 'frames') {
    for (const t of rest) { await pg.evaluate(t => render(t), Number(t)); await pg.screenshot({ path: `frame-${lang}-${t}.png` }); }
  } else {
    const out = rest[0], tmp = out.replace(/\.mp4$/, '.part.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp]);
    const fps = 30, dur = 31.5;
    for (let i = 0; i < fps * dur; i++) {
      await pg.evaluate(t => render(t), i / fps);
      const jpg = await pg.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(jpg)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    const code = await new Promise(r => ff.on('close', r));
    if (code !== 0) { console.error('ffmpeg failed', code); process.exit(1); }
    fs.renameSync(tmp, out); console.log('wrote', out);
  }
  await b.close();
})();
