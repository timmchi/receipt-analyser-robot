from RPA.PDF import PDF

def create_pdf_report(
    category_totals: dict[str, float],
    store_totals: dict[str, float],
    chart_files: list[str],
    output_file: str,
) -> None:
    pdf = PDF()

    grand_total = sum(category_totals.values())

    html = """
    <html>
    <body>
        <h1>Receipt Expense Report</h1>
        <p>This report summarizes processed receipt expenses.</p>

        <h2>Overall Total</h2>
        <p><strong>{grand_total:.2f} €</strong></p>

        <h2>Totals by Category</h2>
        <table border="1" cellspacing="0" cellpadding="6">
            <tr>
                <th>Category</th>
                <th>Total (€)</th>
            </tr>
            {category_rows}
        </table>

        <h2>Totals by Store</h2>
        <table border="1" cellspacing="0" cellpadding="6">
            <tr>
                <th>Store</th>
                <th>Total (€)</th>
            </tr>
            {store_rows}
        </table>
    </body>
    </html>
    """

    category_rows = "".join(
        f"<tr><td>{category}</td><td>{total:.2f}</td></tr>"
        for category, total in category_totals.items()
    )

    store_rows = "".join(
        f"<tr><td>{store}</td><td>{total:.2f}</td></tr>"
        for store, total in store_totals.items()
    )

    final_html = html.format(
        grand_total=grand_total,
        category_rows=category_rows,
        store_rows=store_rows,
    )

    pdf.html_to_pdf(final_html, output_file)

    if chart_files:
        pdf.add_files_to_pdf(
            files=chart_files,
            target_document=output_file,
            append=True,
        )