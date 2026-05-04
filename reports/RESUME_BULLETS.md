# Resume bullets - Olist Marketplace Health Audit

**Project:** https://github.com/Prashant5B2026/olist-marketplace-audit

Pick 3-4 of the bullets below for the resume. The first two are the strongest; the rest support specific skills.

## Strong bullets (use these)

- Built an end-to-end marketplace health audit on the Olist Brazilian e-commerce dataset (1.55M rows across 9 tables in SQLite via SQLAlchemy), covering data quality, two falsifiable hypothesis tests, a custom composite metric, and geographic visualisation.

- Designed and validated a custom 0-100 Seller Trust Score combining route-adjusted delivery rate, mean review, one-star rate, and category penalty; identified bottom 10% of sellers (handling 6% of orders) drive 13.4% of all one-star reviews.

- Tested two hypotheses with falsification design: delivery timeliness drives 2.48x more variance in review scores than product category (H1), and top 1% of state-pair routes drive 51% of all late deliveries (H2).

- Built a Plotly choropleth of Brazil's 27 states identifying Maranhão as the worst origin state and the São Paulo to northeast corridor as the highest-impact intervention target.

## Skills-specific bullets (alternates)

- Implemented a layered Python data pipeline (raw CSV to SQLite to denormalised analysis dataframe via `src/load.py`); each notebook starts from the same prepared data with a single import.

- Surfaced three previously undocumented data quality issues in the Olist dataset (review_id non-uniqueness, geolocation 26% duplicates, customer_id per-order semantics) and designed downstream code to handle them explicitly rather than silently.

- Stack: Python (Pandas), SQL (SQLite via SQLAlchemy), visualisation (Matplotlib, Seaborn, Plotly), Jupyter, git with conventional commits.

## Interview pitch (30 seconds spoken)

"I built a marketplace health audit on Olist's Brazilian e-commerce data, asking who actually destroys customer trust on a multi-seller marketplace: the platform, the sellers, or the logistics network. Two hypothesis tests showed delivery timeliness drives 2.48x more review variance than product category, and top 1% of state-pair routes drive 51% of all late deliveries. The signature deliverable is a custom Seller Trust Score that combines route-adjusted delivery, reviews, and a category penalty into a single 0-100 metric per seller. The honest finding: bad behaviour on Olist is real but moderately concentrated, not a textbook 80/20 - meaningful improvement requires touching the bottom 20-30% of sellers, not just the worst handful."
