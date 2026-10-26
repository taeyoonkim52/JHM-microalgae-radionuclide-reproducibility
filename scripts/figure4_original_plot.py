matrixcolors={'defined/synthetic medium':'#176D80','synthetic wastewater/effluent':'#B57236','actual contaminated/facility water':'#7760A6','unresolved':'#697582'}
W,H=540,520;fig=Figure('Figure4_D03_D06_Performance_Process');ids=[s for s in M if any(r['study_id']==s for r in REM)];x0,xw,y0,rh=95,210,77,19
for t in [0,20,40,60,80,100]:
 x=x0+xw*t/100;fig.line(x,65,x,425,'#E0E3E8');fig.text(x,53,str(t),7,align='center')
fig.text(x0+xw/2,30,'Reported removal (%)',8,True,'center');fig.text(89,53,'L/N',6,align='right')
ks=['recovery_integration','Recover','Stabilize','pilot_field_facility'];heads=[['Recovery/process','integration'],['Recover'],['Stabilize'],['Pilot/field/facility','validation']]
for j,lines in enumerate(heads):
 for z,l in enumerate(lines):fig.text(340+j*54,33+z*8,l,6.8,True,'center')
process=[]
for i,s in enumerate(ids):
 y=y0+i*rh;rr=[r for r in display if r['study_id']==s];nr=[r for r in rr if r['display_type']=='NUMERIC_RECORD']
 fig.text(10,y-4,f'{s} [{M[s]["group"]}]',6.2 if M[s]['group']=='Mixed/other' else 7.2,True);fig.text(90,y-4,f'{len(rr)}/{len(nr)}',6.5,align='right')
 for n,r in enumerate(rr):
  if r['display_type']=='SOURCE_CONFLICT_ANNOTATION':fig.text(102,y+4,'SC: '+r['observation_id'],6.5,True,color='#697582');continue
  yy=y+(n%5-2)*1.3;co=matrixcolors[r['display_matrix_category']];q=r['value_qualifier']
  if q=='range':
   a,b=map(float,r['value'].split('–'));fig.line(x0+xw*a/100,yy,x0+xw*b/100,yy,co,1.5)
  else:
   v=float(r['value']);x=x0+xw*v/100;fig.rect(x-1.4,yy-1.4,2.8,2.8,co)
   if q in ['>','>=','approximately / >']:fig.line(x,yy,x0+xw,yy,co,.6);fig.line(x,yy,x+3,yy-2,co,.7)
   if q=='up to':fig.line(x0,yy,x,yy,co,.5)
 for j,k in enumerate(ks):
  x=326+j*54;state=E[s][k];fig.rect(x,y-7,29,14,{'1':'#BAD8CC','0':'#E7BE94','NA':'#E2E5EA'}[state])
  if state=='NA':fig.hatch(x,y-7,29,14)
  fig.text(x+14.5,y-4,state+('*' if (s,k) in flagged else ''),7.3,True,'center')
 process.append(dict(study_id=s,**{k:E[s][k] for k in ks},flags='; '.join(k for k in ks if (s,k) in flagged),ledger_records=len(rr),numeric_records=len(nr),source_conflict_annotations=len(rr)-len(nr)))
for j,(cat,co) in enumerate(matrixcolors.items()):
 x=10+(j%2)*268;y=438+(j//2)*13;fig.rect(x,y,7,7,co);fig.text(x+11,y,{'defined/synthetic medium':'Defined medium','synthetic wastewater/effluent':'Synthetic effluent','actual contaminated/facility water':'Actual contaminated water','unresolved':'Matrix unresolved'}[cat],7)
fig.text(10,469,'Ledger: 49 records / 18 studies. Numeric display: 47 records / 17 studies. L/N: ledger/numeric.',6.7)
fig.text(10,485,'SC: 2 nonnumeric source-conflict annotations; U05_02 retained at 99.2%. Ledger unchanged.',6.7)
fig.text(10,499,'* Unresolved binary flag. Process cells are study-wide; no matched engineering success implied.',6.7);fig.save()

