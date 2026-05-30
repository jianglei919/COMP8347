const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  LevelFormat, BorderStyle, PageBreak, ImageRun,
} = require('docx');

const SCREENSHOT_PATH = '/Users/logcabin/Workspace/uwindsor/COMP8347/labs/lab4/part3_output.png';
const PART2_SCREENSHOT_PATH = '/Users/logcabin/Workspace/uwindsor/COMP8347/labs/lab4/part2_output.png';

// Helpers
const P = (text, opts = {}) => new Paragraph({
  children: [new TextRun({ text, ...opts })],
  spacing: { after: 100 },
});
const Code = (text) => new Paragraph({
  children: [new TextRun({ text, font: 'Consolas', size: 20 })],
  spacing: { before: 60, after: 120 },
  indent: { left: 360 },
  shading: { type: 'clear', fill: 'F2F2F2' },
});
const H1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun(text)],
});
const H2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun(text)],
});
const H3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  children: [new TextRun(text)],
});
const Result = (text) => new Paragraph({
  children: [
    new TextRun({ text: 'Result: ', bold: true }),
    new TextRun(text),
  ],
  spacing: { after: 200 },
});
const Note = (text) => new Paragraph({
  children: [new TextRun({ text, italics: true, color: '666666', size: 20 })],
  spacing: { after: 240 },
  indent: { left: 360 },
});

// Build items for one query
function query(letter, question, code, result, note) {
  const items = [
    H3(`${letter}. ${question}`),
    Code(code),
    Result(result),
  ];
  if (note) items.push(Note(note));
  return items;
}

const children = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'COMP 8347 — Lab #4 Report', bold: true, size: 36 })],
    spacing: { after: 120 },
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Query Section (Part 2.6 and Part 3)', size: 24 })],
    spacing: { after: 360 },
  }),
  P('Project: Django 6.0.5, app myapp. All queries reproducible via:'),
  Code('python manage.py shell < queries.py'),

  H1('Part 2.6 — Basic queries'),
  Code('import django\nfrom myapp.models import Publisher, Book, Member, Order'),

  H2('Screenshot — full shell output (a–d)'),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({
      type: 'png',
      data: fs.readFileSync(PART2_SCREENSHOT_PATH),
      transformation: { width: 600, height: 100 },
      altText: { title: 'Part 2.6 query output', description: 'Shell output for basic queries a-d', name: 'part2_output' },
    })],
    spacing: { after: 240 },
  }),

  ...query('a', 'List all the books in the db',
    'Book.objects.all()',
    'Machine Learning For Dummies, Data Science For Dummies, Artificial Intelligence, Computer Networking, The Night Circus, The Underground Railroad, Becoming, A Walk in the Woods'),

  ...query('b', 'List all the members in the db',
    'Member.objects.all()',
    'Elena Kwon, Marcus Reed, Priya Shah, James Bennett, Aisha Ncube, Leo Kwon'),

  ...query('c', 'List all the orders in the db',
    'Order.objects.all()',
    '7 orders — #1 elena Borrow, #2 marcus Borrow, #3 aisha Borrow, #4 james Borrow, #5 leo Purchase, #6 elena Purchase, #7 aisha Purchase'),

  ...query('d', 'List all the publishers in the db',
    'Publisher.objects.all()',
    'Wiley, Pearson, Penguin Random House'),

  H1('Part 3 — Query practice'),

  H2('Screenshot — full shell output (a–o)'),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({
      type: 'png',
      data: fs.readFileSync(SCREENSHOT_PATH),
      transformation: { width: 540, height: 496 },
      altText: { title: 'Part 3 query output', description: 'Shell output of queries.py showing a-o results', name: 'part3_output' },
    })],
    spacing: { after: 240 },
  }),

  ...query('a', "Members whose last name is 'Kwon'",
    "Member.objects.filter(last_name='Kwon')",
    'Elena Kwon, Leo Kwon'),

  ...query('b', "Publishers with headquarters in 'USA'",
    "Publisher.objects.filter(country='USA')",
    'Wiley, Penguin Random House'),

  ...query('c', "Members that live in 'Ottawa'",
    "Member.objects.filter(city='Ottawa')",
    'Marcus Reed, James Bennett, Leo Kwon'),

  ...query('d', "Members that live on an 'Avenue' and live in ON province",
    "Member.objects.filter(address__icontains='Avenue', province='ON')",
    'James Bennett',
    'Elena also lives on an Avenue but in BC, so correctly excluded.'),

  ...query('e', "Members that have borrowed the book 'The Night Circus'",
    "Member.objects.filter(borrowed_books__title='The Night Circus')",
    'Elena Kwon, Marcus Reed, James Bennett'),

  ...query('f', 'Books that cost more than $40.00',
    'Book.objects.filter(price__gt=40.00)',
    'Artificial Intelligence ($197.32), Computer Networking ($143.99), The Night Circus ($41.00), Becoming ($45.00)'),

  ...query('g', 'Members that do NOT live in province ON',
    "Member.objects.exclude(province='ON')",
    'Elena Kwon (BC), Priya Shah (SK), Aisha Ncube (MB)'),

  ...query('h', "Orders placed by a client whose first_name is 'Elena'",
    "Order.objects.filter(member__first_name='Elena')",
    'Order #1 (Borrow), Order #6 (Purchase)'),

  ...query('i', "Members whose status are 'Regular Member'",
    'Member.objects.filter(status=1)',
    'Marcus Reed, Priya Shah'),

  ...query('j', "Books with 300–500 pages (inclusive) in category 'Science&Tech'",
    "Book.objects.filter(num_pages__range=(300, 500), category='S')",
    'Machine Learning For Dummies (464p), Data Science For Dummies (432p)'),

  ...query('k', 'First name of Members who have borrowed exactly 2 books',
    "from django.db.models import Count\nMember.objects.annotate(n=Count('borrowed_books')).filter(n=2).values_list('first_name', flat=True)",
    'Elena, James, Marcus'),

  ...query('l', "Books that Member with username 'Marcus' is currently borrowing",
    "Book.objects.filter(member__username='marcus')",
    'Artificial Intelligence, The Night Circus'),

  ...query('m', 'Members who live in ON and have auto_renew enabled',
    "Member.objects.filter(province='ON', auto_renew=True)",
    'Marcus Reed, James Bennett'),

  ...query('n', "Books that 'Leo' has purchased",
    "Book.objects.filter(order__member__username='leo', order__order_type=0)",
    'The Night Circus, A Walk in the Woods',
    'order_type 0 = Purchase.'),

  ...query('o', "City where the headquarters of the publisher of the book purchased by 'Elena' is located",
    "Publisher.objects.filter(\n    books__order__member__first_name='Elena',\n    books__order__order_type=0,\n).values_list('city', flat=True).distinct()",
    'London',
    "Elena purchased 'Artificial Intelligence' → published by Pearson → headquartered in London."),
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Calibri', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true, color: '1F3864' },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, color: '2E74B5' },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 22, bold: true, color: '1F3864' },
        paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  const out = process.argv[2] || '/tmp/lab4_report.docx';
  fs.writeFileSync(out, buffer);
  console.log('wrote', out, buffer.length, 'bytes');
});
