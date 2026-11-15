"""Draw the incorrect and independent nested-list row reference layouts."""
from PIL import Image,ImageDraw
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'experiments'/'graphs'; out.mkdir(exist_ok=True)
im=Image.new('RGB',(960,560),'white'); d=ImageDraw.Draw(im)
d.text((60,25),'Aliased grid: every outer row refers to one inner list',fill='black')
for j in range(3):
 y=80+j*55; d.text((60,y+12),f'bad[{j}]',fill='black'); d.line((120,y+22,300,190),fill='#d1495b',width=3)
d.rounded_rectangle((300,160,740,230),radius=8,outline='#333',width=3,fill='#fbecee'); d.text((330,185),'shared row object: [0, 7, 0, 0]',fill='black')
d.text((60,275),'Correct grid: each outer row refers to a distinct list',fill='black')
for j in range(3):
 y=330+j*55; d.text((60,y+12),f'good[{j}]',fill='black'); d.line((120,y+22,300,y+22),fill='#1769aa',width=3)
 d.rounded_rectangle((300,y,740,y+45),radius=6,outline='#333',width=2,fill='#eaf3fb'); d.text((330,y+12),f'row {j}: '+('[0, 7, 0, 0]' if j==0 else '[0, 0, 0, 0]'),fill='black')
im.save(out/'q2_grid_aliasing.png')
