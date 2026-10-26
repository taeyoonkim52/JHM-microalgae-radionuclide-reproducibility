# Data dictionary

UTF-8 CSVs preserve canonical textual values. No imputation/recoding occurs. Local paths in nested provenance are replaced with LOCAL_SOURCE plus a filename. Scientific values, source locators and bibliographic URLs remain.

| File | Rows | Purpose |
|---|---:|---|
| studies_31.csv |31| Study identities and bibliographic/experimental metadata |
| evidence_matrix_31.csv |31| Five criteria plus four CCRS domains, 1/0/NA |
| decisions_279.csv |279| Individual decisions and canonical verification/provenance |
| binary_flags_9.csv |9| Retained unresolved binary decisions |
| quantitative_73.csv |73| Quantitative observations, conditions and qualifiers |
| removal_ledger_49.csv |49| Exactly the removal subset, including conflicts |
| process_cells_72.csv |72| Approved 18-study x4 process matrix |
| figure_settings.json |—| Dimensions, DPI, tested font/baseline hashes |
| approved_assets.json |—| Manuscript image-part identities and asset hashes |

Duplicated process classifications/counts are omitted from quantitative inputs. Those fields are joined from the approved study matrix, never stale historical display metadata.

Reproduce.py derives display_49 and process_18 files under figures/regenerated after validation. These derivatives are not primary inputs. The 90-segment, 47-glyph and 72-cell CSV audits in docs map data to actual PDF drawing objects.

Canonical FULL_TEXT_VERIFIED/ABSTRACT_PRIMARY_SOURCE_VERIFIED labels are not automatically upgraded by source availability. NA remains unresolved. U06's separate final-version limitation is retained.

The raw source XLSX is excluded because it contains private filesystem provenance. Canonical SHA256: a095dad60ae1915d45d685b7b5c3f10f9b70e795b4e9cf162dd9ffb9b5b6f639. Original workbook/manuscript remain unchanged.
