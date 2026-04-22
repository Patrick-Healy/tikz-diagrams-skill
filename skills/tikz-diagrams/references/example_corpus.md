# Example Corpus

Use a curated local corpus as the quality baseline for business/economics TikZ examples when the user provides one.

## Current Endpoint

Folder:

`$TIKZ_DIAGRAMS_EXAMPLE_CORPUS`

Key files:

- Generator: `$TIKZ_DIAGRAMS_EXAMPLE_CORPUS/generate_all_listed_examples.py`
- QA log: `$TIKZ_DIAGRAMS_EXAMPLE_CORPUS/all_listed_examples_qa_log.md`
- Optional test battery: a user-provided path or task-local QA note

Verification recorded for this corpus:

- 115 `.tex` examples generated.
- 8 category contact sheets generated.
- All 115 passed P3/P4 static TikZ checks.
- All 115 compiled with XeLaTeX.
- All 115 rendered to PNG.

## Categories

- econometrics_causal_inference: 18 examples
- microeconomics_policy: 15 examples
- macroeconomics_forecasting: 15 examples
- finance: 15 examples
- business_analytics_marketing: 18 examples
- operations_management: 12 examples
- research_workflow: 12 examples
- teaching_workflow: 10 examples

## How To Use This Corpus

- Use it as the visual and structural baseline for stock templates.
- Prefer its stable generator/template patterns over quick one-off diagrams.
- Use the contact sheets to inspect quality across many diagrams.
- When creating new business/economics templates, compare them against the relevant category here before finalizing.
- Do not treat quick smoke-test diagrams as examples of good visual design; smoke tests are only for script validation.

## Contact Sheets

- `business_analytics_marketing/business_analytics_marketing-contact-sheet.png`
- `econometrics_causal_inference/econometrics_causal_inference-contact-sheet.png`
- `finance/finance-contact-sheet.png`
- `macroeconomics_forecasting/macroeconomics_forecasting-contact-sheet.png`
- `microeconomics_policy/microeconomics_policy-contact-sheet.png`
- `operations_management/operations_management-contact-sheet.png`
- `research_workflow/research_workflow-contact-sheet.png`
- `teaching_workflow/teaching_workflow-contact-sheet.png`
