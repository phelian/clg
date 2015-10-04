__author__ = 'Alexander Felix'

from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, pdf_format):
        FPDF.__init__(self, format=pdf_format)

    def generate(self, labels_y=None, labels_x=None, cell_width=None, brewery=None, name=None, style=None, abv=None,
                 og=None, fg=None, ibu=None, ebc=None, batch=None, date='ADD ME'):
        labels_x = int(labels_x)
        labels_y = int(labels_y)
        cell_width = float(cell_width)
        for _ in range(0, labels_y):
            for i in range(0, labels_x):
                self.set_font("Cambria", 'B', size=12)
                self.cell(cell_width, 5, brewery, 0, 0)

            self.ln()
            for i in range(0,labels_x):
                self.cell(cell_width, 5, name, 0, 0)

            self.set_font("Cambria", '', size=12)
            self.ln()
            self.ln()
            for i in range(0,labels_x):
                self.cell(cell_width, 5, 'Style: ' + style, 0, 0)

            self.ln()
            for i in range(0,labels_x):
                self.cell(cell_width, 5, 'ABV: ' + abv + '%', 0, 0)

            self.ln()
            for i in range(0,labels_x):
                self.cell(cell_width, 5, 'OG: ' + og + ' ' + u"\u00B0" + u"\u00D6", 0, 0)

            self.ln()
            for i in range(0,labels_x):
                self.cell(cell_width, 5, 'FG: ' + fg + ' ' + u"\u00B0" + u"\u00D6", 0, 0)

            if ibu:
                self.ln()
                for i in range(0,labels_x):
                    self.cell(cell_width, 5, 'IBU: ' + ibu, 0, 0)

            if ebc:
                self.ln()
                for i in range(0,labels_x):
                    self.cell(cell_width, 5, 'EBC: ' + ebc, 0, 0)

            if batch:
                self.ln()
                for i in range(0,labels_x):
                    self.cell(cell_width, 5, 'Batch: ' + str(batch), 0, 0)

            self.ln()
            for i in range(0,labels_x):
                self.cell(cell_width, 5, 'Date: ' + date, 0, 0)

            for i in range(0,4):
                self.ln()

        filename = brewery.lower().replace(" ", "_") + "_" + name.lower().replace("-", "").strip().replace(" ", "_") + "_" + date + ".pdf"
        self.output(filename)
        return filename
