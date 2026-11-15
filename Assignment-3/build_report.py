from pathlib import Path
import csv, sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).parent; report=ROOT/'report'; report.mkdir(exist_ok=True)
questions=[
('Q1 — LISTS AND SLICING: DAILY RAINFALL RECORDS','The rainfall list stores one chronological reading per day. Weekly totals use slices; dry dates are indices whose value is zero. A seven-day moving average can be calculated naively by summing each slice (7(n−6) additions) or with a rolling total (7+(n−7) additions, plus n−7 subtractions). Both are O(n), but the running total avoids repeated work. The code handles empty input and fewer than seven readings with an empty result. readings[7:14] selects indices 7 through 13; readings[-7:-1] selects the last seven except the final value; readings[::7] takes every seventh value. Lists support ordered access and append; insert/pop in the middle and sorting cost O(n) / O(n log n). A late reading inserted by date costs O(n) shifts, acceptable for one year but poor for frequent arbitrary insertion. A date-key dictionary needs seven average O(1) lookups per window and O(n) space, with date-gap policy and lower sequential locality.'),
('Q2 — TUPLES, MUTABILITY AND COPYING','Coordinates are immutable tuples and can be dictionary keys because hashable values cannot change their hash during membership. Lists are mutable and unhashable. The repeated-row expression [[0]*cols]*rows makes each row name the same list; changing one cell changes all rows. A row comprehension creates independent rows. A shallow copy duplicates only the outer list; deep copy recursively duplicates nested rows. Function arguments refer to the same mutable object, so in-place changes are visible to the caller. Tuples suit fixed records; lists suit collections expected to change. A list-of-lists grid gives O(1) cell access and O(rows×cols) space; a coordinate-keyed dictionary gives average O(1) occupied-cell access and O(k) space but has hash overhead. sys.getsizeof reports shallow container size only; element memory must be counted separately.'),
('Q3 — DICTIONARIES: FARMER HELPLINE COMPLAINT ANALYSIS','The implementation lowercases and tokenizes text, skips stop words, and counts with dict.get; setdefault groups records by district. Sorting by (-count, word) enforces descending frequency and alphabetical ties, producing seeds 3, price 2, received 2. Hash tables provide average O(1) lookup and O(n) counting time, O(d) count storage; collisions can worsen the theoretical bound. Counting every distinct word with list.count costs O(n×d), and a dictionary is the practical choice for 100,000 complaints. Counter is a concise optimized alternative. Since Python 3.7, dictionaries preserve insertion order; keys(), values(), and items() return dynamic views.'),
('Q4 — SETS: ELECTIVE REGISTRATION CLASH DETECTION','Set intersection finds students in both electives; symmetric difference finds exactly one; all_students minus the union finds neither. Operator and method implementations are compared. Sets remove duplicates and give average O(1) membership, versus O(n) list membership, at the cost of losing duplicates and order. Set operations are average O(n+m) time and O(n+m) additional storage. Nested comparisons are O(nm) time with little extra space; sorting and merging is O(n log n+m log m). Sets cannot contain lists because lists are mutable/unhashable; tuples are valid if all their elements are hashable. Venn regions: center=intersection, two outer crescent regions=symmetric difference, universe outside both circles=neither.'),
('Q5 — LIST COMPREHENSION: CLEANING SENSOR READINGS','Valid values satisfy −5≤x≤5. Loop, comprehension, and filter/lambda implementations return the same values; Fahrenheit conversion is x×9/5+32. enumerate identifies one-based alarm minutes outside 2–8°C. A list comprehension evaluates eagerly and costs O(k) output space; a generator expression is lazy and uses O(1) iterator space, with the same O(n) traversal time. Comprehensions are concise for simple transforms but nested conditions are clearer as loops. Dictionary/set comprehensions provide keyed/unique views. Benchmarks are generated locally; no implementation is presumed fastest on every Python build.'),
('Q6 — NESTED DATA: A RAILWAY TIMETABLE','Each train number maps to metadata; route order is a list; each station arrival/departure is a tuple; running days are a set. The third-stop departure expression is timetable[train]["stops"][2][2]. A direct station/day query scans T trains and S stops, O(TS); an inverted station index costs O(total stops) to build and O(matches) per query, with O(total stops) added memory. A flat list has the same scan cost but simpler record storage; indexing makes repeated queries faster. Unknown stations, non-running days, and missing records return no matches.'),
('Q7 — DESIGN A CONTACT-MERGING PROGRAM FROM FIRST PRINCIPLES','Stage 1 — Interpret: inputs are contact records from multiple sources; outputs are consolidated records with names, valid Indian phones and emails. A normalized valid phone is the identity key; similar names alone never merge. Measurable criteria include canonicalization of +91, spaces, hyphens, duplicate merging, preservation of distinct same-name numbers, invalid-number handling and scaling time. Stage 2 — Design: remove common separators, accept 10-digit Indian mobile numbers or a leading +91/0091 prefix, and store as +91 plus ten digits. Names are casefolded and whitespace/punctuation normalized for display/search only. A dictionary maps each canonical phone to an aggregate; sets deduplicate numbers/emails. Pseudocode: for each record, normalize each phone; skip invalid phones; get/create aggregate by phone; add phone, cleaned emails and source name; emit stable sorted records. Stage 3 — Implement and measure: the standalone script handles missing fields, empty inputs, two email addresses, duplicate formats, same-name/different-number records and invalid numbers. Measurements for 1,000 and 10,000 contacts are printed using timeit on execution. Stage 4 — Defend: dictionary grouping is O(n) average versus O(n²) pairwise comparisons, with O(n) storage. Same-name people remain separate because name is not the key. Limitation: family/shared numbers can combine distinct people; review or stronger identifiers can resolve this.'),
]
pseudocode={
'Q1':['weekly totals = sum each readings slice of up to 7 values','if fewer than 7 readings: return []','running = sum first 7; emit running / 7','for each next day: running += incoming - outgoing; emit running / 7'],
'Q2':['bad = [[0] * cols] * rows  # all row references alias','good = [[0 for each column] for each row]','copy.copy duplicates outer container only','copy.deepcopy recursively copies nested containers'],
'Q3':['initialize empty word-count dictionary','for each complaint: lowercase and tokenize','for each non-stop word: count[word] = count.get(word, 0) + 1','sort by descending count, then alphabetical word'],
'Q4':['A = set(registrations for elective A); B = set(registrations for elective B)','clash = A intersection B','exactly_one = A symmetric_difference B','neither = all_students difference (A union B)'],
'Q5':['valid = [reading for reading in readings if -5 <= reading <= 5]','fahrenheit = [c * 9 / 5 + 32 for c in valid]','alarms = indices whose reading is below 2 or above 8'],
'Q6':['for every train running on requested day:','  inspect each ordered stop','  when stop matches station: add train and departure','sort matches by departure time','for repeated queries: use station-to-train index'],
'Q7':['for each contact, normalize its Indian mobile numbers','discard invalid numbers; use each canonical phone as identity key','get or create aggregate dictionary record for phone','add unique phone, emails and source name to sets','emit sorted consolidated records; never merge on similar names alone']}

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)
def add_table(doc, headers, rows):
    t=doc.add_table(rows=1, cols=len(headers)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,h in enumerate(headers):
        t.rows[0].cells[i].text=str(h); shade(t.rows[0].cells[i],'D9D9D9')
        for r in t.rows[0].cells[i].paragraphs[0].runs: r.bold=True
    for row in rows:
        cells=t.add_row().cells
        for i,val in enumerate(row): cells[i].text=str(val); cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    return t
doc=Document(); sec=doc.sections[0]; sec.page_width=Inches(8.27); sec.page_height=Inches(11.69); sec.top_margin=Inches(.72); sec.bottom_margin=Inches(.67); sec.left_margin=Inches(.72); sec.right_margin=Inches(.72)
for style in doc.styles:
    if style.type==1: style.font.name='Times New Roman'; style.font.size=Pt(11); style.font.color.rgb=RGBColor(0,0,0)
    if style.name=='Normal': style.paragraph_format.space_after=Pt(5); style.paragraph_format.line_spacing=1.04
    if style.type==1 and style.name.startswith('Heading'):
        style.font.name='Times New Roman'; style.font.bold=True; style.font.color.rgb=RGBColor(0,0,0)
        style.paragraph_format.keep_with_next=True; style.paragraph_format.space_before=Pt(9); style.paragraph_format.space_after=Pt(4)
doc.styles['Heading 1'].font.size=Pt(13); doc.styles['Heading 2'].font.size=Pt(11)
for style_name in ('Heading 1','Heading 2','Title'):
    style=doc.styles[style_name]; ppr=style._element.get_or_add_pPr()
    for node in list(ppr):
        if node.tag==qn('w:pBdr'): ppr.remove(node)
for style in doc.styles:
    ppr=getattr(style._element,'pPr',None)
    if ppr is not None:
        for node in list(ppr):
            if node.tag==qn('w:pBdr'): ppr.remove(node)
header=sec.header.paragraphs[0]; header.alignment=WD_ALIGN_PARAGRAPH.CENTER
header.add_run('CSA0809 - PYTHON PROGRAMMING\n').bold=True; header.add_run('Assignment Report')
header.paragraph_format.space_after=Pt(2)
hpPr=header._p.get_or_add_pPr(); borders=OxmlElement('w:pBdr'); bottom=OxmlElement('w:bottom'); bottom.set(qn('w:val'),'single'); bottom.set(qn('w:sz'),'6'); bottom.set(qn('w:space'),'4'); bottom.set(qn('w:color'),'777777'); borders.append(bottom); hpPr.append(borders)
for run in header.runs: run.font.name='Times New Roman'; run.font.size=Pt(8); run.font.color.rgb=RGBColor(0,0,0)
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
footer.add_run('CSA0809 - Python Programming | Page ')
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footer._p.append(fld)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(100)
p.paragraph_format.space_after=Pt(16)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; rr=p.add_run('Assignment 3: List, Set, Tuple, Dictionary'); rr.bold=True; rr.font.size=Pt(16)
add_table(doc,['Item','Details'],[['Student name','P ROHIT'],['Register number','1925260050'],['Course','CSA0809 - Python Programming'],['Python version','3.12.5'],['Topics covered','Lists, tuples, dictionaries, sets and data structure design'],['GitHub repository','https://github.com/rohitnew1115-prog/python-CSA0809'],['Repository folder','Assignment-3']])
doc.add_page_break()
doc.add_heading('DECLARATION',0); doc.add_paragraph('I submit this individual assignment as my work in Python Programming. The programs and experiment outputs are included with this report. Institutional verification and signature fields are intentionally left blank.')
doc.add_paragraph('Student: P ROHIT     Registration Number: 1925260050'); doc.add_paragraph('Signature: ____________________    Date: ____________________')
doc.add_heading('ABSTRACT',0); doc.add_paragraph('This report implements seven Python collection problems and compares their data-structure choices using complexity analysis and reproducible experiments. The implementations cover slicing, aliasing and copying, hash-based counting and membership, comprehensions, nested timetable data, and identity-safe contact merging. Benchmark values are collected by the included scripts on execution and are hardware-dependent.')
doc.add_heading('Part A: Understanding the Assignment',0)
doc.add_heading('Overview',1)
doc.add_paragraph('The assignment studies how Python collection types represent, transform and analyze data. The seven tasks apply lists and slicing, tuple immutability and copying, dictionary counting, set operations, list comprehensions, nested timetable records and a contact-merging design. Each task includes a runnable implementation, captured output, design reasoning, complexity analysis and edge-case observations. Experiments use seeded inputs and report measured values from this execution environment.')
add_table(doc,['Task','Question','Main concepts','Program'],[['1','Daily rainfall records','Slicing, weekly totals, moving averages','q01_rainfall.py'],['2','Tuples, mutability and copying','Aliasing, shallow/deep copies','q02_tuples.py'],['3','Farmer helpline complaints','Counting, grouping and ranking','q03_complaints.py'],['4','Elective registration clash','Set operators and membership','q04_sets.py'],['5','Cleaning sensor readings','Comprehension, map/filter','q05_sensor_readings.py'],['6','Railway timetable','Nested data and station index','q06_railway.py'],['7','Contact merge design','Phone normalization and merging','q07_contacts.py']])
doc.add_heading('Environment and execution',1)
doc.add_heading('Execution Environment',1); doc.add_paragraph('Python 3.12.5 was used. The programs use the standard library; timing values vary with machine load and interpreter version. Benchmark inputs use a fixed seed and repeated measurements.')
doc.add_heading('PART A: IMPLEMENTATION AND ANALYSIS',0)
doc.add_heading('CONTENTS',0)
for title,_ in questions: doc.add_paragraph(title)
for title,body in questions:
    heading=doc.add_heading(title,0); heading.paragraph_format.page_break_before=True; doc.add_heading('Problem Statement and Objectives',1)
    doc.add_paragraph(body)
    qnum='Q0'+title[1] if title.startswith('Q') and title[1].isdigit() else title[:2]
    folder=next((p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith(qnum)),None)
    doc.add_heading('Algorithm and pseudocode',1)
    pseudo=pseudocode.get('Q'+qnum[-1],[])
    t=doc.add_table(rows=1,cols=1); t.style='Table Grid'; cell=t.cell(0,0); shade(cell,'F2F2F2'); cell.text=''
    for ix,line in enumerate(pseudo):
        p=cell.paragraphs[0] if ix==0 else cell.add_paragraph(); p.paragraph_format.space_after=Pt(1)
        r=p.add_run(line); r.font.name='Consolas'; r.font.size=Pt(9)
    if folder:
        doc.add_heading('Implementation and Actual Output',1)
        code=next(folder.glob('q*.py'))
        code_lines=code.read_text(encoding='utf-8').splitlines()
        t=doc.add_table(rows=1,cols=1); t.style='Table Grid'; cell=t.cell(0,0); shade(cell,'F2F2F2'); cell.text=''
        for ix,line in enumerate(code_lines):
            para=cell.paragraphs[0] if ix==0 else cell.add_paragraph(); para.paragraph_format.space_after=Pt(0); para.paragraph_format.line_spacing=1
            run=para.add_run(line if line else ' '); run.font.name='Consolas'; run.font.size=Pt(7.5); run.font.color.rgb=RGBColor(0,0,0)
        out=folder/'output.txt'
        if out.exists():
            ot=doc.add_table(rows=1,cols=1); ot.style='Table Grid'; oc=ot.cell(0,0); shade(oc,'F2F2F2'); oc.text=''
            run=oc.paragraphs[0].add_run(out.read_text(encoding='utf-8')); run.font.name='Consolas'; run.font.size=Pt(8)
    doc.add_heading('Complexity and Conclusion',1)
    doc.add_paragraph(body.split(' A ')[-1] if ' A ' in body else 'The selected structure follows the stated workload and correctness requirements. The included source file can be run independently; benchmark evidence is stored as CSV and regenerated with the shared experiment runner.')
heading=doc.add_heading('PART B: EXPERIMENTAL INVESTIGATION',0); heading.paragraph_format.page_break_before=True
doc.add_heading('EXPERIMENTAL RESULTS',1)
doc.add_paragraph('Run experiments/run_all_benchmarks.py to regenerate raw timing and memory data. Repeated timing uses time.perf_counter and statistics.mean, seeded input generation uses random.Random, and tracemalloc measures peak comprehension allocation. Values below are environment-specific. Empty and undersized edge cases are included in the question programs.')
for csvname in ['benchmark_results.csv','memory_results.csv','membership_results.csv','timetable_index_results.csv','tuple_list_memory.csv']:
    path=ROOT/'experiments'/csvname
    if path.exists():
        doc.add_heading(csvname.replace('_',' ').upper(),1)
        rows=list(csv.DictReader(path.open(encoding='utf-8')))
        if rows: add_table(doc,list(rows[0]),[list(r.values()) for r in rows[:30]])
for graph in sorted((ROOT/'experiments'/'graphs').glob('*.png')) if (ROOT/'experiments'/'graphs').exists() else []:
    doc.add_heading(graph.stem.replace('_',' ').upper(),1)
    doc.add_picture(str(graph),width=Inches(6.1))
doc.add_heading('PART C: GITHUB AND ASSIGNMENT SUBMISSION',0)
doc.add_heading('Folder Structure',1); doc.add_paragraph('Assignment-3 contains separate Q01 through Q07 folders. Each question folder includes source code, a question README and captured output. experiments contains the reproducible runner, measured CSV files and graphs. report contains the editable Word report and matching PDF. screenshots contains per-question evidence folders.')
add_table(doc,['Folder','Contents'],[['Q01 - Q07','Independent implementation, README and output'],['experiments','Benchmark runner, measured CSV files and graphs'],['report','Assignment_3_Report.docx and Assignment_3_Report.pdf'],['screenshots','Evidence folders for each question']])
doc.add_heading('Execution and Requirements',1); doc.add_paragraph('Python 3.10 or later. The seven programs and experiment runner require only the standard library. The README identifies the student and benchmark command. Execute a question with Python from its folder; run experiments/run_all_benchmarks.py to regenerate CSV measurements.')
doc.add_heading('OVERALL CONCLUSION',0); doc.add_paragraph('Choosing a collection depends on ordering, mutability, uniqueness, lookup patterns and data volume. Lists preserve sequence, tuples model fixed records, dictionaries map keys to values, and sets support uniqueness and fast membership. Benchmarks complement rather than replace Big-O analysis.')
target=report/'Assignment_3_Report.docx'; doc.save(target); print(target)
