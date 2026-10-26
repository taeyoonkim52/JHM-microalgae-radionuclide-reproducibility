"""Reproduce approved figures using extracted original plotting commands and canonical CSV exports.
No network, source-paper access, manuscript editing, or automatic font substitution.
"""
from pathlib import Path
import argparse,csv,json,hashlib,collections,sys,platform,importlib.metadata
from PIL import Image,ImageDraw,ImageFont,ImageChops
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import rl_config
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
def read(path):
 with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--font',type=Path,required=True,help='Licensed Arial regular TTF; not distributed')
parser.add_argument('--bold-font',type=Path,required=True,help='Licensed Arial bold TTF; not distributed')
parser.add_argument('--output',type=Path,default=ROOT/'figures/regenerated')
args=parser.parse_args()
settings=json.loads((ROOT/'data/figure_settings.json').read_text(encoding='utf-8'))
font=args.font;bold=args.bold_font
assert digest(font)==settings['font']['regular_sha256'],'Regular font differs: stop; do not silently substitute'
assert digest(bold)==settings['font']['bold_sha256'],'Bold font differs: stop; do not silently substitute'
# Stable PDF metadata for repeat builds; drawing commands unchanged.
rl_config.invariant=1
pdfmetrics.registerFont(TTFont('Arial',str(font)));pdfmetrics.registerFont(TTFont('ArialBold',str(bold)))
P=args.output;P.mkdir(parents=True,exist_ok=True);scale=settings['dpi']/72
F=['mechanism','radioisotope','relevant_matrix','recovery_integration','pilot_field_facility']
C=['Capture','Concentrate','Recover','Stabilize'];GROUPS=['ALL','U','Cs','Sr','Th','Mixed/other']
colors=['#176D80','#DFA877','#E2E5EA']
labels={'mechanism':['Mechanistic','evidence'],'radioisotope':['Radioisotope','validation'],'relevant_matrix':['Relevant matrix'],'recovery_integration':['Recovery/process','integration'],'pilot_field_facility':['Pilot/field/facility','validation']}
E={r['study_id']:r for r in read(ROOT/'data/evidence_matrix_31.csv')};M=E
FLAGS=read(ROOT/'data/binary_flags_9.csv');flagged={(r['study_id'],r['criterion']) for r in FLAGS}
PERF=read(ROOT/'data/quantitative_73.csv');REM=[r for r in PERF if r['metric']=='removal_efficiency']
assert REM==read(ROOT/'data/removal_ledger_49.csv')
D=read(ROOT/'data/decisions_279.csv');assert len(D)==279
assert len({(r['Study ID'],r['Criterion/stage']) for r in D})==279
assert all(E[r['Study ID']][r['Criterion/stage']]==r['Classification'] for r in D)
assert sum(r[k]=='NA' for r in E.values() for k in F+C)==107
assert len(E)==31 and len(FLAGS)==9 and len(PERF)==73 and len(REM)==49
for r in FLAGS:assert E[r['study_id']][r['criterion']]==r['S4_value']
A=[]
for g in GROUPS:
 subset=list(E.values()) if g=='ALL' else [r for r in E.values() if r['group']==g]
 for k in F+C:
  counts=collections.Counter(r[k] for r in subset)
  A.append(dict(group=g,criterion=k,N=len(subset),n1=counts['1'],n0=counts['0'],nNA=counts['NA']))
expected={'mechanism':(28,2,1),'radioisotope':(13,1,17),'relevant_matrix':(10,15,6),'recovery_integration':(10,15,6),'pilot_field_facility':(1,22,8),'Capture':(30,0,1),'Concentrate':(2,0,29),'Recover':(7,14,10),'Stabilize':(2,0,29)}
for k,v in expected.items():
 r=next(r for r in A if r['group']=='ALL' and r['criterion']==k);assert tuple(r[x] for x in ['n1','n0','nNA'])==v
def fragment(name):
 p=ROOT/'scripts'/name;exec(compile(p.read_text(encoding='utf-8'),name,'exec'),globals())
fragment('drawing_primitive.py')
fragment('figure2_original_plot.py')
plot_counts(F,[r for r in A if r['criterion'] in F],'Figure2_S4_Evidence_Maturity')
fragment('figure4_original_display.py')
fragment('figure4_original_plot.py')
# Export fully reconciled derived inputs; they never drive this run.
def write(path,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
write(P/'figure2_counts.csv',A)
write(P/'figure4_display_49.csv',display)
write(P/'figure4_process_18.csv',process)
audit=read(ROOT/'data/process_cells_72.csv')
assert len(audit)==72 and all(E[r['study_id']][r['criterion']]==r['classification'] for r in audit)
assert len(process)*4==72
assert [r['observation_id'] for r in display if r['display_type']=='SOURCE_CONFLICT_ANNOTATION']==['U05_01','U13_01']
assert next(r for r in numeric if r['observation_id']=='U05_02')['value']=='99.2'
targets={}
results=[]
for num,name in [(2,'Figure2_S4_Evidence_Maturity'),(4,'Figure4_D03_D06_Performance_Process')]:
 for ext in ['png','pdf']:(P/(name+'.'+ext)).replace(P/(f'Figure{num}.'+ext))
 actual=Image.open(ROOT/f'figures/approved/Figure{num}.png').convert('RGB')
 made=Image.open(P/f'Figure{num}.png').convert('RGB')
 assert actual.size==made.size
 diff=ImageChops.difference(actual,made);bbox=diff.getbbox()
 # PNG equality is assessed independently of compressed-file metadata.
 p1=PdfReader(ROOT/f'figures/approved/Figure{num}.pdf');p2=PdfReader(P/f'Figure{num}.pdf')
 assert len(p1.pages)==len(p2.pages)==1
 stream_equal=p1.pages[0].get_contents().get_data()==p2.pages[0].get_contents().get_data()
 results.append({'figure':num,'dimensions':list(made.size),'pixel_identical_to_manuscript':bbox is None,'difference_bbox':bbox,'png_file_bytes_identical':digest(ROOT/f'figures/approved/Figure{num}.png')==digest(P/f'Figure{num}.png'),'pdf_page_content_stream_identical':stream_equal,'pdf_file_bytes_identical':digest(ROOT/f'figures/approved/Figure{num}.pdf')==digest(P/f'Figure{num}.pdf'),'pdf_note':'Original drawing operators retained. Whole-file differences may reflect deterministic metadata, document IDs or serialization; see vector check.'})
run={'python':platform.python_version(),'dependencies':{k:importlib.metadata.version(k) for k in ['Pillow','reportlab','pypdf','pdfplumber']},'fonts':settings['font'],'data_counts':settings['expected_counts'],'aggregate_counts':expected,'joint_CCRS_prefixes':[sum(all(r[k]=='1' for k in C[:i]) for r in E.values()) for i in range(1,5)],'results':results,'scientific_data_status':'PASS','pixel_comparison_status':'PASS' if all(r['pixel_identical_to_manuscript'] for r in results) else 'FAIL','publication_status':'NOT_AUTHORIZED; author/license/citation metadata approval required'}
assert run['joint_CCRS_prefixes']==[30,2,1,1]
(P/'REPRODUCTION_RESULTS.json').write_text(json.dumps(run,indent=2),encoding='utf-8')
print(json.dumps(run,indent=2))
if run['pixel_comparison_status']!='PASS':sys.exit(1)
