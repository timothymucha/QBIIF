import streamlit as st
import pandas as pd
import io
import csv
from datetime import datetime

st.title("QuickBooks IIF Formatter")

uploaded_file = st.file_uploader("Upload receipt CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    output = io.StringIO()
    writer = csv.writer(output, delimiter='\t')

    # Write headers
    writer.writerow(["!TRNS", "TRNSTYPE", "DATE", "ACCNT", "NAME", "AMOUNT", "DOCNUM", "MEMO"])
    writer.writerow(["!SPL", "TRNSTYPE", "DATE", "ACCNT", "NAME", "AMOUNT", "DOCNUM",
                     "MEMO", "ITEM", "QNTY", "PRICE", "CLASS", "TAXABLE", "INVITEM"])
    writer.writerow(["!ENDTRNS"])

    for receipt_no, group in df.groupby('Receipt number'):
        try:
            date_obj = pd.to_datetime(group.iloc[0]['Date'], errors='coerce')
            date = date_obj.strftime('%m/%d/%Y')
        except:
            date = ""

        total = group['Net sales'].sum()
        customer = "Walk In"
        docnum = f"RCP-{str(receipt_no).strip().replace(' ', '').replace('/', '-')}"

        writer.writerow(["TRNS", "INVOICE", date, "Accounts Receivable", customer,
                         f"{total:.2f}", docnum, ""])

        for _, row in group.iterrows():
            item = row['Item']
            amount = float(row['Net sales'])
            qty = float(row.get('Quantity', 1))
            price = amount / qty if qty != 0 else amount

            writer.writerow(["SPL", "INVOICE", date, "Revenue:Confectionaries", customer,
                             f"{-amount:.2f}", docnum, item, item, f"{qty:.2f}",
                             f"{price:.2f}", "", "N", item])

        writer.writerow(["ENDTRNS"])

    st.download_button("Download IIF File", data=output.getvalue(),
                       file_name="formatted_output.iif", mime="text/plain")