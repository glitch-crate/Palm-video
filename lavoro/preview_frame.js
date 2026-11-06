// node preview_frame.js page.html clip.mp4 t out.png  -> fotogramma di controllo (grafica sopra clip)
const { chromium } = require('playwright'); const path=require('path'); const {execSync}=require('child_process');
(async()=>{const [pg,clip,t,out]=process.argv.slice(2);
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve(pg)); await p.evaluate(()=>document.fonts.ready);
await p.evaluate(t=>window.seek(t),Number(t)); await p.screenshot({path:'/tmp/claude-0/ov.png',omitBackground:true}); await b.close();
if(clip==='-'){execSync(`ffmpeg -v error -y -f lavfi -i color=c=0x777777:s=1920x1080 -i /tmp/claude-0/ov.png -filter_complex overlay -frames:v 1 ${out}`);}
else execSync(`ffmpeg -v error -y -ss ${t} -i ${clip} -i /tmp/claude-0/ov.png -filter_complex overlay -frames:v 1 ${out}`);})();
