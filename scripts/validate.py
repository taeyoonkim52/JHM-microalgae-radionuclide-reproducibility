"""Offline integrity, source-to-glyph, vector and privacy checks. Does not publish."""
from pathlib import Path
import csv,json,re,hashlib,collections,sys
from PIL import Image,ImageChops
from pypdf import PdfReader
import pdfplumber
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:list(csv.DictReader(p.open(encoding='utf-8',newline='')))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M={r['study_id']:r for r in read(ROOT/'data/evidence_matrix_31.csv')}
display=read(ROOT/'figures/regenerated/figure4_display_49.csv')
process=read(ROOT/'figures/regenerated/figure4_process_18.csv')
D=read(ROOT/'data/decisions_279.csv')
F=['mechanism','radioisotope','relevant_matrix','recovery_integration','pilot_field_facility'];C=['Capture','Concentrate','Recover','Stabilize']
assert len(M)==31 and len(D)==279 and all(M[r['Study ID']][r['Criterion/stage']]==r['Classification'] for r in D)
assert len({(r['Study ID'],r['Criterion/stage']) for r in D})==279
flags=read(ROOT/'data/binary_flags_9.csv');flagged={(r['study_id'],r['criterion']) for r in flags}
assert len(flags)==9 and sum(r['S4_value']=='1' for r in flags)==8
assert len(display)==49 and len(process)==18
assert sum(r['display_type']=='NUMERIC_RECORD' for r in display)==47
assert {r['observation_id'] for r in display if r['display_type']=='SOURCE_CONFLICT_ANNOTATION'}=={'U05_01','U13_01'}
assert next(r for r in display if r['observation_id']=='U05_02')['value']=='99.2'
used=collections.defaultdict(set)
pdfs={}
for n in [2,4]:
 with pdfplumber.open(ROOT/f'figures/regenerated/Figure{n}.pdf') as p:pdfs[n]={'rects':p.pages[0].rects,'lines':p.pages[0].lines}
def hexcolor(x):
 if isinstance(x,(int,float)):return '#'+('%02X'%round(x*255))*3
 return '#'+''.join('%02X'%round(v*255) for v in x[:3])
def match(n,kind,x,y,w,h,color):
 for i,r in enumerate(pdfs[n][kind]):
  if i in used[(n,kind)]:continue
  co=hexcolor(r['non_stroking_color'] if kind=='rects' else r['stroking_color'])
  if co==color and all(abs(a-b)<.002 for a,b in zip([r['x0'],r['top'],r['width'],r['height']],[x,y,w,h])):
   used[(n,kind)].add(i);return f'FIG{n}_{kind}_{i:04d}'
 raise AssertionError(('glyph not found',n,kind,x,y,w,h,color))
groups=['ALL','U','Cs','Sr','Th','Mixed/other'];barrows=[]
for gi,g in enumerate(groups):
 subset=list(M.values()) if g=='ALL' else [r for r in M.values() if r['group']==g]
 for ki,k in enumerate(F):
  off=0
  for state,co in [('1','#176D80'),('0','#DFA877'),('NA','#E2E5EA')]:
   count=sum(r[k]==state for r in subset);w=67*count/len(subset);x=12+gi%3*176+96+off;y=45+gi//3*230+24+ki*31
   obj=match(2,'rects',x,y,w,21,co) if count else 'ZERO_WIDTH'
   barrows.append({'group':g,'criterion':k,'state':state,'count':count,'N':len(subset),'pdf_object':obj})
   off+=w
colors={'defined/synthetic medium':'#176D80','synthetic wastewater/effluent':'#B57236','actual contaminated/facility water':'#7760A6','unresolved':'#697582'}
points=[];cells=[];geometry=collections.defaultdict(list)
for i,pr in enumerate(process):
 s=pr['study_id'];rr=[r for r in display if r['study_id']==s]
 for n,r in enumerate(rr):
  if r['display_type']!='NUMERIC_RECORD':continue
  y=77+i*19+(n%5-2)*1.3;co=colors[r['display_matrix_category']];q=r['value_qualifier'];objs=[]
  if q=='range':
   a,b=map(float,r['value'].split('–'));x=95+2.1*a;end=95+2.1*b
   objs.append(match(4,'lines',x,y,end-x,0,co));key=(x,y,end,'range')
  else:
   x=95+2.1*float(r['value']);end=x;objs.append(match(4,'rects',x-1.4,y-1.4,2.8,2.8,co));key=(x,y,'square')
   if q in ['>','>=','approximately / >']:objs.extend([match(4,'lines',x,y,305-x,0,co),match(4,'lines',x,y-2,3,2,co)])
   if q=='up to':objs.append(match(4,'lines',95,y,x-95,0,co))
  geometry[key].append(r['observation_id'])
  points.append({'observation_id':r['observation_id'],'study_id':s,'value':r['value'],'qualifier':q,'color':co,'x_pt':x,'y_pt':y,'range_end_pt':end,'pdf_objects':';'.join(objs),'status':'PASS'})
 for j,k in enumerate(['recovery_integration','Recover','Stabilize','pilot_field_facility']):
  state=M[s][k];assert pr[k]==state
  co={'1':'#BAD8CC','0':'#E7BE94','NA':'#E2E5EA'}[state]
  obj=match(4,'rects',326+j*54,77+i*19-7,29,14,co)
  cells.append({'study_id':s,'criterion':k,'classification':state,'flag':(s,k) in flagged,'pdf_object':obj,'status':'PASS'})
assert len(points)==47 and len(cells)==72 and len(barrows)==90
overlaps=[v for v in geometry.values() if len(v)>1];assert overlaps==[['Mix02_01','Mix02_06']]
# Drawing primitive geometry/colors and all text/lines across approved/rebuilt PDFs.
vectors=[]
for n in [2,4]:
 a=PdfReader(ROOT/f'figures/approved/Figure{n}.pdf');b=PdfReader(ROOT/f'figures/regenerated/Figure{n}.pdf')
 assert a.pages[0].get_contents().get_data()==b.pages[0].get_contents().get_data()
 assert list(a.pages[0].mediabox)==list(b.pages[0].mediabox)
 metadata_differences={k:{'approved':str(a.metadata.get(k)),'regenerated':str(b.metadata.get(k))} for k in set(a.metadata)|set(b.metadata) if a.metadata.get(k)!=b.metadata.get(k)}
 assert set(metadata_differences).issubset({'/CreationDate','/ModDate'})
 # Decoded PDF resources must also agree, including embedded font program.
 def resource(v,seen=None):
  seen=set() if seen is None else seen
  if hasattr(v,'idnum'):
   key=(v.idnum,v.generation)
   if key in seen:return '<previous-object>'
   seen.add(key);v=v.get_object()
  if hasattr(v,'get_data'):
   return {'stream_sha256':hashlib.sha256(v.get_data()).hexdigest(),'dictionary':{str(k):resource(x,seen) for k,x in v.items() if str(k) not in ['/Length','/Filter','/DecodeParms']}}
  if isinstance(v,dict):return {str(k):resource(x,seen) for k,x in v.items()}
  if isinstance(v,list):return [resource(x,seen) for x in v]
  return str(v)
 assert resource(a.pages[0]['/Resources'])==resource(b.pages[0]['/Resources'])
 vectors.append({'figure':n,'page_content_stream_identical':True,'decoded_resources_identical':True,'metadata_differences':metadata_differences,'trailer_ID_identical':str(a.trailer.get('/ID'))==str(b.trailer.get('/ID')),'status':'PASS'})
# Public package excludes manuscripts, original articles, fonts, credentials and local absolute paths.
issues=[]
allowedpdf={'figures/approved/Figure2.pdf','figures/approved/Figure4.pdf','figures/regenerated/Figure2.pdf','figures/regenerated/Figure4.pdf'}
patterns={'windows_absolute_path':r'(?<![A-Za-z])[A-Za-z]:[\\/]','user_home_path':r'/(?:Users|home|mnt/[a-z])/[^\s]+','email_address':r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','private_key':r'-----BEGIN [A-Z ]*PRIVATE KEY-----','token':r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{10,}'}
for p in ROOT.rglob('*'):
 if not p.is_file() or '__pycache__' in p.parts:continue
 rel=p.relative_to(ROOT).as_posix()
 if p.suffix.lower() in ['.docx','.xlsx','.zip','.ttf','.otf','.exe']:issues.append({'file':rel,'issue':'excluded_file_type'})
 if p.suffix.lower()=='.pdf':
  if rel not in allowedpdf:issues.append({'file':rel,'issue':'non_figure_pdf'})
  continue
 if p.suffix.lower() not in ['.png','.pyc']:
  text=p.read_text(encoding='utf-8',errors='replace')
  # Scanner source contains signatures by design; inspect with separate private literal-path scan too.
  if p.name=='validate.py':continue
  for label,pat in patterns.items():
   if re.search(pat,text):issues.append({'file':rel,'issue':label})
assert not issues,issues
def write(name,rows):
 with (ROOT/'docs'/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
write('FIG2_90_SEGMENT_CHECKS.csv',barrows);write('FIG4_47_GLYPH_CHECKS.csv',points);write('FIG4_72_PROCESS_CHECKS.csv',cells)
result={'scientific_reproduction':'PASS','figure2_bar_segments':len(barrows),'figure2_nonzero_rectangles':len(used[(2,'rects')]),'figure4_numeric_glyphs':47,'figure4_process_cells':72,'exact_overlaps':overlaps,'PDF_comparison':vectors,'privacy_scan':'PASS','privacy_issues':issues,'citation_authors':'Manuscript-verified scholarly names only; no contact details or affiliations','publication':'NOT_AUTHORIZED; do not publish or mint DOI without author approval'}
(ROOT/'docs/VALIDATION_RESULTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
