# JHM Figures 2 and 4 reproducibility candidate

Offline recovery package for **From aqueous removal to a qualified waste form: a critical review of radionuclide sequestration by microalgae and cyanobacteria**.

**Scientific reproduction: PASS (local Codex verification). Author has approved public release; publication and DOI issuance are pending.**
No GitHub repository/release, Zenodo record or DOI has yet been created.

## Verified inputs and results

The approved Gate5D workbook was freshly read. Sanitized CSV exports are included; the raw workbook contains local provenance paths and is excluded. The historical display CSV is not used. Figure 4 process cells come exclusively from approved study-level classifications.

- 31 studies, 279 decisions, five maturity criteria and four independent CCRS domains.
- Nine binary flags and 107 NA classifications retained.
- 73 quantitative observations; 49 removal records; 47 numeric display records; 72 process cells.
- Original final plotting fragments regenerate PNGs byte-identical to the final manuscript images.
- PDF drawing streams and decoded resources agree. Whole-file hashes differ because of timestamps/document IDs.

The four CCRS domains are controls; Figure 2 displays only the five maturity criteria. Neither figure proves a complete CCRS process.

## Run

Tested with Python 3.12.14. Create an isolated environment, activate it, then use its interpreter:

    python -m venv .venv
    python -m pip install -r requirements.lock.txt
    python scripts/reproduce.py --font ../private-fonts/arial.ttf --bold-font ../private-fonts/arialbd.ttf
    python scripts/validate.py

Activate the environment before running pip, or invoke its Python explicitly. These are execution instructions; this recovery did not install software.

Legally available Arial regular/bold files must be supplied separately. Tested font hashes are in data/figure_settings.json. Mismatched fonts stop execution; no silent substitution occurs. Proprietary font files are not redistributed. Exact pixels with other fonts/platforms are not promised.

Outputs go to figures/regenerated; approved comparisons remain in figures/approved. The four original fragment files are helper code executed by reproduce.py, not standalone entry points. validate.py checks counts, every bar state, all 47 numeric drawing records, all 72 process cells, conflict annotations, overlap, PDF resources and privacy indicators.

## Interpretation and provenance

Read docs/SCIENTIFIC_LIMITATIONS.md and the final captions before using results. U05_01/U13_01 remain conflict annotations; U05_02 remains 99.2%. Mix02 points overlap. SR05 water labels conflict. U06 has published-abstract verification with a preprint-only local long full text. The broad-screen ledger includes Egeria densa.

docs/SOURCE_LINEAGE.json records project-relative source filenames and hashes. Canonical workbook/manuscript hashes are retained, but the private files are not redistributed. Primary bibliography and locators are retained without article text.

Only manuscript-verified scholarly author names appear in CITATION.cff. Emails, affiliations, postal addresses, user accounts and local absolute paths are excluded. Citation names are bibliographic attribution. No manuscript, raw workbook, source-paper PDF, credential, font, stale display CSV or unverified candidate dataset is included.

The author has approved MIT for scripts and CC BY 4.0 for original curated data/documentation; see LICENSE-CODE and LICENSE-DATA. Third-party materials are excluded. No public DOI/URL exists yet.

## File inventory

See docs/PUBLIC_FILE_LIST.csv, docs/DATA_DICTIONARY.md, docs/REPRODUCIBILITY_REPORT.md, docs/VALIDATION_RESULTS.json and SHA256_MANIFEST.csv. The manifest is a local delivery snapshot excluding itself. Re-running checks can rewrite derived reports; finalize release hashes only after review.
