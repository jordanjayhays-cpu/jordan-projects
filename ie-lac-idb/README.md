# Eight Patents — LAC for the IDB

IE University · Economics for Public Sector · Group Project · Group 1.
Rebuilt 2026-10-20 to conform to the assignment's required section structure.

## Section conformance

The brief's structure is "recommended but not mandatory" and is **not in the rubric**
(which grades Diagnosis, Evidence, Recommendations, Presentation Quality, Teamwork/Q&A).
The deck nonetheless now lands inside every stated slide range.

| Required section | Brief | This deck | Slides |
| --- | --- | --- | --- |
| Title slide | 1 | 1 | 1 |
| Executive summary | 1–2 | 2 | 2–3 |
| Regional context | 2–3 | 3 | 4–6 |
| Diagnostic | 4–5 | 5 | 7–11 |
| International benchmarks | 2–3 | 2 | 12–13 |
| Policy recommendations | 4–5 | 5 | 14–18 |
| Conclusion & next steps | 1–2 | 2 | 19–20 |
| *Appendix (post-deck)* | — | 1 | 21 |

20 numbered slides plus one appendix. **Confirm with the professor that a backup slide
shown only in Q&A does not count against the 20-slide cap.** If it does, cut it.

## What changed from the previous version

- **Added an executive summary (2 slides).** The previous deck had none. A Big Four deck
  for a development bank leads with the answer.
- **Added regional context (3 slides)** with figures pulled fresh, which the previous
  version listed as "not pulled yet": GDP per capita, real growth and poverty headcount
  for all eight countries.
- **Added a conclusion with four priority actions.** The previous close was the one ask only.
- **Compressed the signal and reversal** from seven slides to five to make room.
- The narrative (signal → reversal → bill → what we do) is preserved — it is the deck's
  Presentation Quality asset and flattening it would have cost marks.

## Data

Every figure pulled from the World Bank API on **2026-10-20** by `build.js` reading `wb.json`,
produced by the script in the session scratchpad. Indicators used:

| Indicator | Code |
| --- | --- |
| Patent applications, residents | `IP.PAT.RESD` |
| GDP per capita, constant 2015 US$ | `NY.GDP.PCAP.KD` |
| Real GDP growth | `NY.GDP.MKTP.KD.ZG` |
| Poverty headcount, national line | `SI.POV.NAHC` |
| Researchers in R&D per million | `SP.POP.SCIE.RD.P6` |

All reconcile with the previous deck's figures. New this version: Guatemala has **1**
researcher in R&D per million people (2023), against Korea's 9,472. Mexico grew **0.6%**
in 2025 against 2.7–4.9% across its neighbours.

## Still open

1. **Pick the consulting firm.** Slide 1 and slide 20 both read `[FIRM: Deloitte / EY / KPMG / PwC]`.
2. **Informality rate** — still UNSURE, still the one figure the diagnostic leans on. ILOSTAT.
3. **Costings** — none of the three programmes is costed. The deck says so on every relevant slide.
4. **Mexico's share of subregional output** — stated as ~40% on slide 5, flagged UNSURE.
5. **Visual QA was not possible** — LibreOffice cannot load any .pptx in the build container
   (a one-textbox test file fails identically). The file passes schema validation, zip
   integrity and opens in python-pptx at 21 slides, but **nobody has looked at it rendered.**
   Open it once in PowerPoint before the presentation.

## Rebuild

```bash
npm install pptxgenjs
NODE_PATH=$PWD/node_modules node build.js
```
