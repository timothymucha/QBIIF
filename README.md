# QBIIFConverter

A simple Streamlit-based web utility to convert receipts exported in CSV format into QuickBooks-compatible IIF files for importing invoices.

## Features

- Upload your CSV file with receipt data.
- Automatically formats data with correct invoice structure.
- Generates `.iif` file ready for QuickBooks Desktop import.

## Installation

```bash
git clone https://github.com/timothymucha/QBIIFConverter.git
cd QBIIFConverter
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## CSV Format Required

| Date | Receipt number | Item | Quantity | Net sales |
|------|----------------|------|----------|-----------|

## Output Format

QuickBooks IIF format with `TRNS`, `SPL`, and `ENDTRNS` rows.

## License

MIT License