import os
import sys
from pyPdf import PdfFileWriter, PdfFileReader
output_pdf = PdfFileWriter()

assert len(sys.argv) == 3

page_order = []

with open(sys.argv[1], 'rb') as readfile:
    input_pdf = PdfFileReader(readfile)

    total_pages = input_pdf.getNumPages()
    is_odd = bool(total_pages % 2)
    total_pages += is_odd

    frontside = True
    def add_page(*page_numbers):
        for page_number in page_numbers:
            page_order.append(page_number)
            # getPage is 0 indexed
            try:
                page = input_pdf.getPage(page_number - 1)
                if not frontside:
                    page.rotateClockwise(180)
                output_pdf.addPage(page)
            except IndexError:
                output_pdf.addBlankPage()

    i = total_pages / 2
    total_pages = 0
    while i > 0:
        p1 = i
        total_pages += 1
        if frontside:
            i += total_pages
        else:
            i -= total_pages
        p2 = i
        total_pages += 1

        if frontside:
            add_page(p1, p2)
        else:
            add_page(p2, p1)

        if frontside:
            i += 1
        else:
            i -= 1
        frontside = not frontside

    with open(sys.argv[2], "wb") as writefile:
        output_pdf.write(writefile)

print page_order