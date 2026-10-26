def plot_counts(keys,rows,name,ccrs=False):
 global W,H
 W,H=540,500 if not ccrs else 425
 fig=Figure(name)
 for x,co,lab in [(12,colors[0],'1  Demonstrated'),(170,colors[1],'0  Not demonstrated in assessed scope'),(390,colors[2],'NA  Unresolved')]:
  fig.rect(x,12,9,9,co)
  if co==colors[2]:fig.hatch(x,12,9,9)
  fig.text(x+13,12,lab,7.2)
 for i,g in enumerate(GROUPS):
  x=12+i%3*176;y=45+(i//3)*(230 if not ccrs else 190);n=next(r['N'] for r in rows if r['group']==g);fig.text(x,y,('All studies' if g=='ALL' else g)+f' (n={n})',9,True)
  bx=x+96;bw=67;rh=31
  for j,k in enumerate(keys):
   r=next(r for r in rows if r['group']==g and r['criterion']==k);yy=y+24+j*rh;labs=[k] if ccrs else labels[k]
   for z,l in enumerate(labs):fig.text(bx-5,yy+4+z*8,l,7.2,align='right')
   off=0
   for state,co in zip(['1','0','NA'],colors):
    count=r['n'+state];w=bw*count/n
    if count:
     fig.rect(bx+off,yy,w,21,co)
     if state=='NA':fig.hatch(bx+off,yy,w,21)
     if w>=6:fig.text(bx+off+w/2,yy+7,str(count),7,True,'center','white' if state=='1' else '#111111')
     else:fig.text((bx+bw+3 if state=='NA' else bx+off+w/2),(yy+7 if state=='NA' else yy-7),str(count),6.8,True,('left' if state=='NA' else 'center'));fig.line(bx+off+w/2,yy-1,bx+off+w/2,yy+2)
    off+=w
  ay=y+24+len(keys)*rh
  for tick in [0,50,100]:
   xx=bx+bw*tick/100;fig.line(xx,ay-4,xx,ay-1);fig.text(xx,ay+2,str(tick),6.7,align='center')
  fig.text(bx+bw/2,ay+14,'Evidence coverage (%)',6.5,align='center')
 fig.text(12,H-20,'Numbers in bars are study counts; NA is unresolved, not a negative result.',7.2)
 fig.save()
