import sys
from PIL import Image
from pathlib import Path
names=sys.argv[2:]; out=sys.argv[1]
ims=[Image.open(f"out/png/{n}.png").convert("RGB").resize((400,400)) for n in names]
cols=min(4,len(ims)); rows=(len(ims)+cols-1)//cols
S=Image.new("RGB",(cols*400,rows*400),"white")
for i,im in enumerate(ims): S.paste(im,((i%cols)*400,(i//cols)*400))
S.save(out)
