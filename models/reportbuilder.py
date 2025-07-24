class ReportBuilder:

    def __init__(self, session: Session):
        self.session = session

    def build(self, output_path: str):
        doc = Document()  # from python-docx

        # Cover Page
        doc.add_heading("Assessment Report", 0)
        doc.add_paragraph(f"Dataset: {self.session.data.name}")

        # Section: Sample Summary
        doc.add_heading("Sample Design", level=1)
        doc.add_paragraph(self.session.sample.summary_text())

        # Section: Composite Indicators
        doc.add_heading("Food Security Indicators", level=1)
        fsl_results = self.session.analysis["fsl"].results_summary()
        self._add_table(doc, fsl_results)

        # Section: Data Quality
        doc.add_heading("Data Quality Checks", level=1)
        quality = self.session.analysis["fsl"].quality_check()
        self._add_table(doc, quality)

        # Visualizations (saved from matplotlib)
        fig_path = self.session.analysis["fsl"].generate_plot()
        doc.add_picture(fig_path, width=Inches(5))

        doc.save(output_path)

    def _add_table(self, doc, table_data: list):
        """
        Helper to add a table to the docx from a list of dicts.
        Example: [{'Indicator': 'FCS', 'Mean': 45.3, ...}, ...]
        """
        if not table_data:
            doc.add_paragraph("No data available.")
            return

        keys = table_data[0].keys()
        table = doc.add_table(rows=1, cols=len(keys))
        hdr_cells = table.rows[0].cells
        for i, key in enumerate(keys):
            hdr_cells[i].text = str(key)

        for row in table_data:
            row_cells = table.add_row().cells
            for i, key in enumerate(keys):
                row_cells[i].text = str(row[key])

    def generate_pdf_report(self, output_path="reports/output.pdf"):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("report_template.html")

        # Example data pulled from your Session object
        sample_data = {
            "design": self.session.sample.design,
            "n_individuals": self.session.sample.n_individuals,
            "n_households": self.session.sample.n_households
        }

        data_info = {
            "n_raw": len(self.session.data.raw_data),
            "n_clean": len(self.session.data.clean_data)
        }

        fsl_summary = self.session.analysis["fsl"].results_summary()  # List of dicts

        html_out = template.render(
            title="FSL Assessment Report",
            date=str(date.today()),
            sample=sample_data,
            data=data_info,
            fsl_indicators=fsl_summary
        )

        # Save to PDF using WeasyPrint
        HTML(string=html_out, base_url=".").write_pdf(output_path)

        print(f"PDF saved to: {output_path}")

    def generate_powerpoint(self):
        pass

    def generate_protocol_tor(self):
        pass