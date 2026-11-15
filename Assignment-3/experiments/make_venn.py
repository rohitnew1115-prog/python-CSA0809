"""Draw a Venn diagram for the three elective registration result regions."""
from PIL import Image,ImageDraw
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'experiments'/'graphs'; out.mkdir(exist_ok=True)
im=Image.new('RGB',(900,460),'white'); d=ImageDraw.Draw(im)
d.text((300,20),'Elective registrations and result regions',fill='black')
d.ellipse((110,90,510,400),outline='#1769aa',width=5,fill='#eaf3fb')
d.ellipse((390,90,790,400),outline='#d1495b',width=5,fill='#fbecee')
d.text((190,110),'Elective A',fill='#1769aa'); d.text((585,110),'Elective B',fill='#d1495b')
d.text((160,240),'Only A\n001, 007',fill='black'); d.text((460,240),'Both\n004, 009',fill='black'); d.text((620,240),'Only B\n002, 010',fill='black')
d.rectangle((95,90,805,410),outline='#444444',width=2); d.text((110,415),'Neither, within all_students: 003, 005, 006, 008',fill='black')
im.save(out/'q4_venn.png')
