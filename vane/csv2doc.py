import csv
import re
import docx 
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.oxml.ns import qn, nsdecls
from docx.oxml import OxmlElement, parse_xml
from docx.enum.text import WD_COLOR_INDEX

# Input Variables
# Name of CSV to use for test output
CSVFILE = "../Arista Agora Test Plan V9.3 - EOS Test Items.csv"
DOCFILE = "../test_summary_results.docx"
# Column number of interesting values
TESTCASE_ID = 0 # column A
CASE_NAME = 2 # column C
PROCEDURE = 16 # column Q
EXPECTED_RESULT = 17 # column R
PASS_FAIL = 13 # column N
OBSERVATION = 14 # column O

def parse_csv():
    print(f"Parsing CSV file: {CSVFILE} for test data...")
    test_data = []

    # open csv
    with open(CSVFILE, 'r') as file:
        csv_reader = csv.reader(file)
        # regex for matching header
        pattern = r"\d{1,2}\.\d{1,2}"

        for row in csv_reader:
            test_data_entry = []
            # parse csv row for a test case ids
            if "TN" in row[TESTCASE_ID]:
                test_data_entry.append(row[TESTCASE_ID])
                test_data_entry.append(row[CASE_NAME])
                test_data_entry.append(row[PROCEDURE])
                test_data_entry.append(row[EXPECTED_RESULT])
                test_data_entry.append(row[PASS_FAIL])
                test_data_entry.append(row[OBSERVATION])

                # raw data entry for output data
                test_data.append(test_data_entry)
            # parse csv row for header
            elif re.match(pattern, row[CASE_NAME]):  
                test_data_entry.append(row[CASE_NAME])
                test_data.append(test_data_entry)

    return test_data

def write_report(test_data):
    print(f"Writing report doc: {DOCFILE}")

    # Open doc
    document = docx.Document()
    # Change margins
    section = document.sections[0]
    section.left_margin = Inches(.5)
    section.right_margin = Inches(.5)

    write_header(document)
    write_results_table(document, test_data)

    doc_text = (
        "\n\n\nPlease note – for more details on test outputs please reference "
        "the test case output appendix docs.\n"
    )
    write_text(document, doc_text)

    # Close doc
    document.save(DOCFILE)

def write_header(document):
    heading = document.add_heading(level=2)
    run = heading.add_run("4	Test Summary Result")
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(204,0,0)

    para = document.add_paragraph()
    doc_text = (
        "\nTest Cases for Arista BAU Hardware & EOS 4.27.2F Certification. "
        "Please note – for more details on test outputs please reference "
        "the test case output appendix docs.\n\n\n"
    )
    write_text(document, doc_text)

def write_text(document, doc_text):
    para = document.add_paragraph()
    run = para.add_run(doc_text)
    run.font.size = Pt(10)
    run.font.name = "Arial"

def write_results_table(document, test_data):
    headers = ["Test Case", "Case Name", "Procedure", "Expected result", "Pass/Fail", "Observation"]
    table = document.add_table(rows=1, cols=6, style="Table Grid")
    
    for count, header in enumerate(headers):
        para = table.rows[0].cells[count].paragraphs[0]
        
        cell = table.cell(0, count)
        run = para.add_run(header)
        run.font.name = "Arial"
        run.font.size = Pt(9)
        run.font.bold = True

        cell = table.cell(0, count)
        shading_blue = parse_xml(r'<w:shd {} w:fill="00FFFF"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading_blue)


    pattern = r"\d{1,2}\.\d{1,2}"

    for count, test_case_entry in enumerate(test_data):
        count += 1

        if re.match(pattern, test_case_entry[0]):
            row_cells = table.add_row().cells
            merged_cell = row_cells[0].merge(row_cells[5])
            row_cells[0].text = ''
            run = row_cells[0].paragraphs[0].add_run(test_case_entry)
            run.font.name = "Arial"
            run.font.size = Pt(9)
            run.bold = True

            cell = table.cell(count, 0)
            shading_blue = parse_xml(r'<w:shd {} w:fill="CCFFFF"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shading_blue)

        elif "TN" in test_case_entry[0]:
            row_cells = table.add_row().cells

            for counter, test_data_entry in enumerate(test_case_entry):
                row_cells[counter].text = ''
                run.font.name = "Arial"
                run.font.size = Pt(9)  

                if counter == 0:
                    test_data_entry = format_test_id(test_data_entry)
                    run = row_cells[counter].paragraphs[0].add_run(test_data_entry)
                elif counter == 4:
                    run = row_cells[counter].paragraphs[0].add_run(test_data_entry.upper())

                    if test_data_entry.upper() == "PASS":
                        run.font.highlight_color = WD_COLOR_INDEX.BRIGHT_GREEN
                        run.font.bold = True
                    elif test_data_entry.upper() == "FAIL":
                        run.font.highlight_color = WD_COLOR_INDEX.RED
                        run.font.bold = True
                    else:
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                        run.font.bold = True
                else:
                    run = row_cells[counter].paragraphs[0].add_run(test_data_entry)

                run.font.name = "Arial"
                run.font.size = Pt(9)

    # set_col_widths(table)
        
def format_test_id(test_data_entry):
    if "TN" in test_data_entry:
        test_data_entry = test_data_entry.split("TN")[1]

    return test_data_entry

def format_pass_fail(test_data_entry):
    pass

def set_col_widths(table):
    widths = (Inches(.5), Inches(1.17), Inches(1.55), Inches(1.25), Inches(.85), Inches(2.15))
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = width

def main():
    print("Starting...")
    test_data = parse_csv()
    write_report(test_data)
    print("Complete")

if __name__ == "__main__":
    main()