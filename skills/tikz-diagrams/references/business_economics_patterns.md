# Business and Economics Pattern Map

Use these mappings to retrieve a suitable template for Faculty of Business and Economics research and teaching tasks.

## Economics

- Supply-demand equilibrium: `axis-curve`, tags `economics`, `market-equilibrium`.
- Tax incidence: `axis-curve-field`, tags `tax`, `elasticity`, `burden`, `deadweight-loss`.
- Monopoly markup: `axis-curve`, tags `market-power`, `welfare`.
- Externality: `axis-curve`, tags `private-cost`, `social-cost`, `pigouvian-tax`.
- Macroeconomic response lag: `delayed-adjustment-path`, tags `macro`, `policy`, `lag`, `overshoot`, `stabilization`.
- J-curve / delayed adjustment path: `delayed-adjustment-path`, tags `j-curve`, `trade-balance`, `exchange-rate`, `lag`, `recovery`.
- Game theory: `matrix-grid` or `tree`, tags `game`, `payoff`, `strategy`.
- Public goods: `matrix-grid`, tags `free-rider`, `strategic`.
- Labour market: `axis-curve`, tags `minimum-wage`, `employment`, `wage`.

## Econometrics and Business Statistics

- Causal DAG: `dag`, tags `confounding`, `treatment`, `outcome`, `identification`.
- Mediation/collider/bad controls: `dag`, tags `causal`, `bias`, `controls`.
- Difference-in-differences: `axis-curve` plus `timeline`, tags `parallel-trends`, `event-study`.
- Regression discontinuity: `axis-curve`, tags `threshold`, `cutoff`, `local`.
- IV/LATE compliance: `matrix-grid`, tags `instrument`, `complier`, `late`.
- Robustness checks: `matrix-grid`, tags `robustness`, `specification`, `appendix`.
- Estimation convergence: `feedback-loop`, tags `diagnostics`, `model`, `criteria`.

## Finance

- Portfolio frontier: `axis-curve`, tags `risk`, `return`, `efficient-frontier`.
- CAPM/security market line: `axis-curve`, tags `beta`, `expected-return`.
- Yield curve: `axis-curve`, tags `maturity`, `rates`.
- VaR/expected shortfall: `axis-curve`, tags `tail-risk`, `loss`.
- Drawdown and recovery path: `delayed-adjustment-path`, tags `shock`, `drawdown`, `recovery`, `liquidity`, `time-path`.
- Balance sheet shock: `stack-comparison`, tags `assets`, `liabilities`, `banking`.
- Liquidity spiral: `threshold-phase-transition`, tags `liquidity`, `margin-call`, `fire-sale`.
- Belief corridor / survival region: `threshold-corridor-trajectory`, tags `beliefs`, `threshold`, `survival`, `exit`, `trajectory`.

## Marketing and Analytics

- Customer funnel: `flow`, tags `funnel`, `conversion`, `journey`.
- Attribution path: `dag`, tags `channels`, `purchase`, `attribution`.
- Segmentation/RFM: `quadrant`, tags `segments`, `customer`.
- Campaign response lag: `delayed-adjustment-path`, tags `launch`, `response`, `wear-in`, `adoption`, `retention`.
- Churn decision: `tree`, tags `retention`, `classification`.
- Confusion matrix: `matrix-grid`, tags `classification`, `threshold`.
- Uplift modelling: `quadrant`, tags `treatment`, `incremental-impact`.
- Customer data flow: `transformation-flow`, tags `features`, `latent-state`, `privacy`, `uplift`.

## Management and Operations

- Bottleneck/process: `flow`, tags `capacity`, `process`, `operations`.
- Queue: `flow`, tags `arrival`, `server`, `waiting`.
- Inventory/reorder: `axis-curve`, tags `stock`, `lead-time`, `reorder-point`.
- Process change or adoption lag: `delayed-adjustment-path`, tags `change-management`, `adoption`, `learning-curve`, `recovery`, `performance`.
- Risk matrix: `matrix-grid`, tags `probability`, `impact`, `mitigation`.
- Stakeholder map: `quadrant`, tags `influence`, `interest`.
- Ensemble decision support: `ensemble-aggregation`, tags `decision`, `model`, `constraint`, `override`.

## Research Workflow

- Claim verification: `matrix-grid`, tags `claim`, `evidence`, `code`, `figure`.
- Citation audit: `flow`, tags `citation`, `source`, `verification`.
- Variable dictionary: `matrix-grid`, tags `variable`, `definition`, `source`.
- Model specification: `matrix-grid`, tags `specification`, `controls`, `fixed-effects`.
- Replication checklist: `flow`, tags `readme`, `data`, `logs`, `outputs`.
- Robustness grid: `matrix-grid`, tags `robustness`, `placebo`, `sensitivity`.

## Teaching Workflow

- Lecture module: `flow`, tags `motivation`, `concept`, `practice`.
- Concept check: `branch`, tags `quiz`, `feedback`, `misconception`.
- Lab notebook: `flow`, tags `setup`, `data`, `code`, `interpret`.
- Assessment guide: `stack-comparison`, tags `marking`, `criteria`, `feedback`.
