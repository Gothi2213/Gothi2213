import sys,re
from playwright.sync_api import sync_playwright
from PIL import Image
src,out,t,W,bg=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),sys.argv[5]; names=sys.argv[6:]
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for n in names:
        s=open(f'{src}/assets/{n}.svg').read()
        vb=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',s); w,h=float(vb[1]),float(vb[2]); H=int(W*h/w)
        pg=b.new_page(viewport={'width':W,'height':H})
        pg.set_content(f'<body style="margin:0;background:{bg}">'+s.replace('<svg ',f'<svg style="width:{W}px;height:auto;display:block" ',1)+'</body>')
        pg.evaluate(f"(()=>{{const s=document.querySelector('svg');s.pauseAnimations();s.setCurrentTime({t});document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t*1000}}})}})()")
        pg.screenshot(path=f'{out}/{n}.png'); ims.append(Image.open(f'{out}/{n}.png').convert('RGB')); pg.close()
    b.close()
Hh=sum(i.height for i in ims)+12*len(ims); c=Image.new('RGB',(W,Hh),bg); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+12
c.save(f'{out}/sheet.png'); print(c.size)
