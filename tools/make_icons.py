from PIL import Image, ImageDraw
def icon(size, path, pad=0):
    s=size; im=Image.new("RGBA",(s,s),(10,82,70,255)); d=ImageDraw.Draw(im)
    w=max(2,s//22); cx=s//2; top=int(s*0.30)+pad; bot=int(s*0.78)-pad; l=int(s*0.20)+pad; r=int(s*0.80)-pad
    d.rectangle([l,top,r,top+w],fill="white"); d.rectangle([cx-w//2,top,cx+w//2,bot],fill="white")
    # debit / credit bars
    bh=max(2,s//30)
    for i,y in enumerate([0.42,0.52,0.62]):
        yy=int(s*y); d.rounded_rectangle([l+s//30,yy,cx-s//18,yy+bh],radius=bh//2,fill=(120,166,240,255))
        d.rounded_rectangle([cx+s//18,yy,r-s//30,yy+bh],radius=bh//2,fill=(242,162,92,255))
    cr=int(s*0.11); d.ellipse([r-cr-int(s*0.02),int(s*0.10),r+cr-int(s*0.02),int(s*0.10)+2*cr],fill=(244,200,74,255))
    im.save(path)
icon(192,"pwa/icon-192.png"); icon(512,"pwa/icon-512.png"); icon(180,"pwa/apple-touch-icon.png"); icon(512,"pwa/icon-maskable.png",pad=40)
