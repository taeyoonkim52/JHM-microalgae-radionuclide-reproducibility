class Figure:
 def __init__(self,name):
  self.name=name;self.pdf=canvas.Canvas(str(P/(name+'.pdf')),pagesize=(W,H));self.pdf.setTitle(name);self.im=Image.new('RGB',(round(W*scale),round(H*scale)),'white');self.draw=ImageDraw.Draw(self.im)
 def rect(self,x,y,w,h,color):
  self.pdf.setFillColor(color);self.pdf.rect(x,H-y-h,w,h,stroke=0,fill=1);self.draw.rectangle((round(x*scale),round(y*scale),round((x+w)*scale),round((y+h)*scale)),fill=color)
 def line(self,x1,y1,x2,y2,color='#666666',width=.5):
  self.pdf.setStrokeColor(color);self.pdf.setLineWidth(width);self.pdf.line(x1,H-y1,x2,H-y2);self.draw.line(tuple(round(t*scale) for t in (x1,y1,x2,y2)),fill=color,width=max(1,round(width*scale)))
 def text(self,x,y,text,size=9,b=False,align='left',color='#222222'):
  fn='ArialBold' if b else 'Arial';self.pdf.setFont(fn,size);self.pdf.setFillColor(color)
  if align=='center':self.pdf.drawCentredString(x,H-y-size*.85,text)
  elif align=='right':self.pdf.drawRightString(x,H-y-size*.85,text)
  else:self.pdf.drawString(x,H-y-size*.85,text)
  ft=ImageFont.truetype(str(bold if b else font),round(size*scale));anchor={'left':'lt','center':'mt','right':'rt'}[align];self.draw.text((round(x*scale),round(y*scale)),text,font=ft,fill=color,anchor=anchor)
 def hatch(self,x,y,w,h):
  # Bound every diagonal to its segment rectangle.
  for t in range(-round(h),round(w)+1,6):
   x1=max(0,t);x2=min(w,t+h)
   if x2>x1:self.line(x+x1,y+h-(x1-t),x+x2,y+h-(x2-t),'#969DA7',.35)
 def save(self):
  self.pdf.showPage();self.pdf.save();self.im.save(P/(self.name+'.png'),dpi=(300,300));assert len(PdfReader(P/(self.name+'.pdf')).pages)==1
