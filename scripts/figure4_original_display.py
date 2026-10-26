display=[]
for r in REM:
 d=dict(r);d['ledger_value']=r['value'];d['display_type']='NUMERIC_RECORD';d['display_value']=r['value'];d['display_matrix_category']=r['matrix_category'];d['display_note']='Frozen observation retained; qualifiers preserved.'
 if r['observation_id'] in ['U05_01','U13_01']:
  d.update(display_type='SOURCE_CONFLICT_ANNOTATION',display_value='NA',display_note=('Source abstract >98% conflicts with concentration-specific body values; no numeric representation.' if r['observation_id']=='U05_01' else 'Source removal 92.91% versus 92.21% and temperature 25 versus 20 degrees C; no numeric representation.'))
 if r['study_id']=='U05':d.update(display_matrix_category='defined/synthetic medium',display_note=d['display_note']+' Prepared aqueous experiment; display color only, relevant_matrix unchanged.')
 display.append(d)
numeric=[r for r in display if r['display_type']=='NUMERIC_RECORD'];assert len(numeric)==47 and len({r['study_id'] for r in numeric})==17

