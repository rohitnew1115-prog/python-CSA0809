const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  AlignmentType, PageNumber, BorderStyle, WidthType, PageBreak, Header, Footer,
} = require('docx');

const root = __dirname;
const mdPath = path.join(root, 'report', 'Assignment_5_Report.md');
const outPath = path.join(root, 'report', 'Assignment_5_Report.docx');
const source = fs.readFileSync(mdPath, 'utf8').replace(/\r/g, '');
const lines = source.split('\n');

function inlineRuns(text) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, match;
  while ((match = re.exec(text))) {
    if (match.index > last) out.push(new TextRun({ text: text.slice(last, match.index), font: 'Times New Roman' }));
    if (match[0].startsWith('**')) out.push(new TextRun({ text: match[0].slice(2, -2), bold: true, font: 'Times New Roman' }));
    else out.push(new TextRun({ text: match[0].slice(1, -1), font: 'Consolas', size: 19 }));
    last = match.index + match[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: 'Times New Roman' }));
  return out.length ? out : [new TextRun({ text: '', font: 'Times New Roman' })];
}

const border = { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6' };
const tableBorders = { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border };
function splitRow(line) { return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(x => x.trim()); }
function makeTable(rows) {
  const n = rows[0].length;
  let ratios = n === 2 ? [30, 70] : n === 3 ? [23, 39, 38] : n === 4 ? [8, 22, 34, 36] : Array(n).fill(100/n);
  const widths = ratios.map(v => Math.round(9360 * v / 100));
  const docRows = rows.map((row, ri) => new TableRow({
    cantSplit: true,
    tableHeader: ri === 0,
    children: row.map((cell, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA },
      shading: { fill: ri === 0 ? 'D9D9D9' : (ri % 2 ? 'FFFFFF' : 'F5F5F5'), type: 'clear' },
      margins: { top: 70, bottom: 70, left: 95, right: 95 },
      verticalAlign: 'center',
      children: [new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { before: 0, after: 0, line: 240 },
        children: inlineRuns(cell.replace(/\\\|/g, '|')),
      })],
    })),
  }));
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: widths,
    rows: docRows,
    borders: tableBorders,
    layout: 'fixed',
  });
}

function paragraph(text, opts = {}) {
  return new Paragraph({
    alignment: opts.alignment || AlignmentType.JUSTIFIED,
    spacing: { before: opts.before ?? 0, after: opts.after ?? 130, line: 250 },
    indent: opts.indent ? { left: 300 } : undefined,
    keepNext: opts.keepNext || false,
    children: opts.children || inlineRuns(text),
  });
}

// Cover slots: the reference report uses a centered title and a two-column metadata table.
const title = lines[0].replace(/^#\s*/, '').trim();
const detailStart = lines.findIndex(x => x.startsWith('| Item | Details |'));
let detailEnd = detailStart;
while (detailEnd + 1 < lines.length && lines[detailEnd + 1].startsWith('|')) detailEnd++;
const detailRows = lines.slice(detailStart, detailEnd + 1).filter(x => !/^\|\s*-/.test(x)).map(splitRow);
const bodyLines = lines.slice(detailEnd + 1);

const children = [];
for (let i = 0; i < 5; i++) children.push(new Paragraph({ spacing: { before: 0, after: 1250 } }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 0, after: 230 },
  children: [new TextRun({ text: title, bold: true, size: 30, font: 'Times New Roman' })],
}));
children.push(makeTable(detailRows));
children.push(new Paragraph({ children: [new PageBreak()] }));

let inFence = false, code = [], i = 0;
while (i < bodyLines.length) {
  const line = bodyLines[i];
  if (line.trim().startsWith('```')) {
    if (!inFence) { inFence = true; code = []; }
    else {
      for (const codeLine of code) {
        if (!codeLine) { children.push(new Paragraph({ spacing: { after: 10 } })); continue; }
        children.push(new Paragraph({
          alignment: AlignmentType.LEFT,
          spacing: { before: 0, after: 20, line: 220 },
          indent: { left: 240 },
          children: [new TextRun({ text: codeLine, font: 'Consolas', size: 17 })],
        }));
      }
      children.push(new Paragraph({ spacing: { after: 120 } }));
      inFence = false;
    }
    i++; continue;
  }
  if (inFence) { code.push(line); i++; continue; }
  if (!line.trim()) { i++; continue; }
  if (line.trim() === '<!--PAGEBREAK-->') {
    children.push(new Paragraph({ children: [new PageBreak()] }));
    i++; continue;
  }
  const imageMatch = line.trim().match(/^!\[([^\]]+)\]\(([^)]+)\)$/);
  if (imageMatch) {
    const imagePath = path.resolve(path.dirname(mdPath), imageMatch[2]);
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 30, after: 140 },
      children: [new ImageRun({ data: fs.readFileSync(imagePath), type: 'png', transformation: { width: 450, height: 253 }, altText: { title: imageMatch[1], description: imageMatch[1], name: imageMatch[1] } })],
    }));
    i++; continue;
  }
  if (line.startsWith('|')) {
    const rows = [];
    while (i < bodyLines.length && bodyLines[i].startsWith('|')) {
      if (!/^\|\s*-/.test(bodyLines[i])) rows.push(splitRow(bodyLines[i]));
      i++;
    }
    if (rows.length) children.push(makeTable(rows), new Paragraph({ spacing: { after: 90 } }));
    continue;
  }
  if (/^#{1,6}\s/.test(line)) {
    const level = (line.match(/^#+/)[0].length);
    const text = line.replace(/^#+\s*/, '').trim();
    const size = level <= 2 ? 27 : level === 3 ? 24 : 22;
    children.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      heading: level === 1 ? 'Heading1' : level === 2 ? 'Heading2' : 'Heading3',
      spacing: { before: level <= 2 ? 240 : 180, after: 100, line: 245 },
      keepNext: true,
      children: [new TextRun({ text: text.toUpperCase(), bold: true, size, color: '000000', font: 'Times New Roman' })],
    }));
    i++; continue;
  }
  if (/^\s*-\s+/.test(line)) {
    const text = line.replace(/^\s*-\s+/, '');
    children.push(new Paragraph({
      bullet: { indent: 360 },
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 60, line: 240 },
      children: inlineRuns(text),
    }));
    i++; continue;
  }
  children.push(paragraph(line));
  i++;
}

const header = new Header({
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0, line: 220 }, children: [new TextRun({ text: 'CSA0809 - PYTHON PROGRAMMING', bold: true, size: 18, font: 'Times New Roman' })] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 50, line: 220 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: '808080', space: 3 } },
        children: [new TextRun({ text: 'Assignment Report', size: 18, font: 'Times New Roman' })],
      }),
    ],
});
const footer = new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0 },
      children: [
        new TextRun({ text: 'CSA0809 - Python Programming | Page ', size: 18, font: 'Times New Roman' }),
        new TextRun({ children: [PageNumber.CURRENT], size: 18, font: 'Times New Roman' }),
      ],
    })],
});

const doc = new Document({
  creator: 'P ROHIT',
  title,
  subject: 'CSA0809 Python Programming Assignment 5',
  description: 'Assignment report and experimental evidence',
  styles: {
    default: { document: { run: { font: 'Times New Roman', size: 21 }, paragraph: { spacing: { after: 130, line: 250 } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', run: { font: 'Times New Roman', size: 27, bold: true, color: '000000' }, paragraph: { spacing: { before: 260, after: 100 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', run: { font: 'Times New Roman', size: 24, bold: true, color: '000000' }, paragraph: { spacing: { before: 220, after: 90 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', run: { font: 'Times New Roman', size: 22, bold: true, color: '000000' }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1080, right: 936, bottom: 900, left: 936, header: 420, footer: 420 } } },
    headers: { default: header },
    footers: { default: footer },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log(`Wrote ${outPath} (${buffer.length} bytes)`);
}).catch(err => { console.error(err); process.exit(1); });
