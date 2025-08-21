# APAC-IB-Deal-Simulation

Designed for educational and simulation purposes, it demonstrates end-to-end M&A analysis aligned with a strategic narrative for APAC cross-border e-commerce expansion.

## Overview

This repository simulates an investment banking deal for Sea Limited's (NYSE: SE) hypothetical acquisition of 11Street Korea (SK Telecom subsidiary). It automates data extraction, financial modeling (DCF, comps, precedents, merger accretion/dilution), and output generation including a pitchbook PDF, teaser PDF, and optional research brief. The pipeline leverages Python for efficiency, fetching real-time data via Yahoo Finance where possible, and runs in under 10 minutes. 

Key metrics:
~$4.8B enterprise value (11.5% discount rate),
15% FCF CAGR,
12x NTM EV/EBITDA multiples,
~8.3% EPS accretion with $75M synergies.

## Features

- **Data Extraction**: Dynamic fetching of Sea Limited metrics/FCF from Yahoo Finance; static/hypothetical data for 11Street.
- **Financial Models**: DCF (5-year projections), comparable companies, precedent transactions, and merger model.
- **Outputs**: Excel models, 10-slide pitchbook PDF (with charts/tables), 2-page teaser PDF, optional macro/geopolitical brief PDF.
- **Automation**: Sequential scripts with error handling, fallbacks, and optional custom parameters (e.g., discount rate, synergies).
- **Dependencies**: Minimal; Python libraries for data processing and document generation.
- **Extensibility**: Modular code for adding slides, integrations (e.g., PDF parsing), or custom data.

## File Structure

```
APAC-IB-Deal-Simulation/
├── 00_Raw_Data/                 # Input filings, CSVs, PDFs (e.g., comps.csv, Precedents.xlsx, SE_20F_2024.pdf)
├── 01_Pitchbook.pdf             # Generated pitchbook deck
├── 02_Financial_Model.xlsx      # Valuation and merger Excel models
├── 03_Deal_Overview.pdf         # 2-page teaser document
├── 04_Research_Brief.pdf        # Optional macro/geopolitical brief
├── src/                         # Core Python scripts
│   ├── 01_build_cim.py          # Data preparation and fact generation
│   ├── 02_valuation.py          # DCF, comps, and precedents modeling
│   ├── 03_merger_model.py       # Accretion/dilution merger analysis
│   ├── 04_slide_maker.py        # Pitchbook generation (PPTX to PDF)
│   └── 05_pdf_writer.py         # Teaser and brief PDF creation
├── templates/                   # Optional: template.pptx for pitchbook
├── outputs/                     # Optional: Intermediate files (e.g., logs, charts)
└── README.md                    # This documentation
```

## Prerequisites

- **Python**: Version 3.8+.
- **Libraries**: Install via `pip install pandas numpy yfinance openpyxl reportlab python-pptx`.
- **Optional Tools**:
  - LibreOffice: For optimal PPTX-to-PDF conversion in pitchbook generation (fallback PDF used otherwise).
- **Environment Setup**: Clone the repository and create folders as per the structure. No internet required beyond initial yfinance calls (fallbacks provided).

## Inputs

- **Required Raw Data (in `00_Raw_Data/`)**:
  - `comps.csv`: Comparable companies dataset (columns: Ticker, EV/EBITDA, etc.).
- **Optional Raw Data**:
  - `Precedents.xlsx`: Precedent transactions (loaded if present).
  - `SE_20F_2024.pdf`, `SKT_2024_Annual.pdf`: Reference filings (not parsed; for manual review).
- **Generated Inputs**: Scripts auto-generate `SEA_facts.csv`, `SEA_fcf.csv`, `11Street_facts.csv` via yfinance or static mocks.
- **Custom Parameters**: Flags for rates (e.g., `--discount_rate 0.115`), structure (e.g., `--cash_pct 0.60`), synergies (e.g., `--synergies 75.0`).
- **Template**: `templates/template.pptx` for custom pitchbook styling (default generated if absent).

## Usage

Run scripts sequentially from the project root. Commands use relative paths for integration.

1. **Prepare Data**:
   ```
   python src/01_build_cim.py
   ```
   - Outputs: CSVs in `00_Raw_Data/` (e.g., SEA facts with real/static data).

2. **Build Valuation Model**:
   ```
   python src/02_valuation.py --comps 00_Raw_Data/comps.csv --fcf 00_Raw_Data/SEA_fcf.csv --output 02_Financial_Model.xlsx
   ```
   - Sheets: Trading_Comps, Precedent_Trans, DCF.
   - Customize: `--discount_rate`, `--perp_growth`.

3. **Build Merger Model**:
   ```
   python src/03_merger_model.py --acquirer 00_Raw_Data/SEA_facts.csv --target 00_Raw_Data/11Street_facts.csv --output 02_Financial_Model.xlsx
   ```
   - Appends Merger_Model sheet.
   - Customize: `--cash_pct`, `--stock_pct`, `--synergies`.

4. **Generate Pitchbook**:
   ```
   python src/04_slide_maker.py --valuation 02_Financial_Model.xlsx --template templates/template.pptx --output 01_Pitchbook.pdf
   ```
   - Outputs: PDF with title, DCF chart, merger table (expand code for full 10 slides).
   - Logs: `slide_maker.log`.

5. **Generate Teaser**:
   ```
   python src/05_pdf_writer.py --type teaser --output 03_Deal_Overview.pdf
   ```

6. **Generate Research Brief (Optional)**:
   ```
   python src/05_pdf_writer.py --type brief --output 04_Research_Brief.pdf
   ```

- **Full Pipeline Runtime**: <10 minutes.
- **Verification**: Inspect Excel for metrics alignment; PDFs for visuals. Use static data if yfinance unavailable.

## Outputs

- **Excel**: `02_Financial_Model.xlsx` – Comprehensive models (DCF: ~$4.8B EV; Merger: ~8.3% accretion).
- **PDFs**:
  - `01_Pitchbook.pdf`: Visual deck with charts/tables.
  - `03_Deal_Overview.pdf`: Transaction teaser (overview, rationale).
  - `04_Research_Brief.pdf`: Macro/geopolitical context.
- **Intermediates**: CSVs in `00_Raw_Data/`; logs in root.

## Limitations and Notes

- **Data Sources**: Relies on yfinance for real-time accuracy; static mocks ensure fallback. 11Street data is hypothetical.
- **Customization**: Edit scripts for advanced features (e.g., more slides, PDF extraction via additional libs like PyMuPDF).
- **Legal/Disclaimer**: For simulation only; not financial advice. Metrics based on 2024 estimates (update as needed).
- **Contributions**: Fork and PR for enhancements. Issues: Report bugs with logs.
- **License**: MIT (open-source; see LICENSE file if added).
