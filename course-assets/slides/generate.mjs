import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(SCRIPT_DIR, "../..");
const PYTHON = process.env.PYTHON || "python3";
const COVER = path.join(REPO, "lms/public/images/dsacademy/course-cover.png");
const LOGO_LIGHT = path.join(REPO, "lms/public/images/dsacademy/logo-light.png");
const LOGO_DARK = path.join(REPO, "lms/public/images/dsacademy/logo-dark.png");
const OUTPUT_ROOT = path.join(REPO, "course-assets/slides");

const C = {
  ink: "#0B1220",
  graphite: "#243244",
  muted: "#607086",
  mist: "#EEF4F7",
  line: "#CAD6DF",
  blue: "#176BDB",
  cyan: "#00A8C8",
  lime: "#A8D95B",
  coral: "#F06B5F",
  white: "#FFFFFF",
  navy: "#0E263E",
  ice: "#DFF5FA",
};

const FONT = "Aptos";
const MONO = "Aptos Mono";
const PAGE = { width: 1280, height: 720 };
const args = process.argv.slice(2);
function requestedNumber(...flags) {
  for (const flag of flags) {
    const index = args.indexOf(flag);
    if (index >= 0) return Number(args[index + 1] || 0);
  }
  return 0;
}
const requestedWeek = requestedNumber("--module", "--week");
const requestedSession = requestedNumber("--lesson", "--session");

const curriculum = JSON.parse(
  execFileSync(
    PYTHON,
    [
      "-c",
      [
        "import json",
        "from lms.dsacademy.curriculum import COURSE, WEEKS",
        "from lms.dsacademy.deck_content import build_slide_outline",
        "payload={'course': COURSE, 'weeks': []}",
        "for wi, week in enumerate(WEEKS, 1):",
        "  item=dict(week)",
        "  item['sessions']=[dict(session, deck=build_slide_outline(wi, si, week, session)) for si, session in enumerate(week['sessions'], 1)]",
        "  payload['weeks'].append(item)",
        "print(json.dumps(payload, ensure_ascii=False))",
      ].join("\n"),
    ],
    { cwd: REPO, encoding: "utf8", maxBuffer: 16 * 1024 * 1024 },
  ),
);

async function bytes(filePath) {
  const value = await fs.readFile(filePath);
  return value.buffer.slice(value.byteOffset, value.byteOffset + value.byteLength);
}

function addText(slide, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontFamily: FONT,
    fontSize: 22,
    color: C.ink,
    ...style,
  };
  return shape;
}

function addRect(slide, position, fill, line = "none", geometry = "rect") {
  return slide.shapes.add({
    geometry,
    position,
    fill,
    line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
  });
}

function addRule(slide, left, top, width, color = C.line, height = 2) {
  return addRect(slide, { left, top, width, height }, color);
}

function addImage(slide, blob, alt, position, fit = "cover") {
  return slide.images.add({
    blob,
    contentType: "image/png",
    alt,
    fit,
    position,
  });
}

function setNotes(
  slide,
  narration,
  weekNumber,
  sessionNumber,
  pageNumber,
  title,
  sources = [],
) {
  const sourceLines = sources.length
    ? sources.map((source) => `- ${source}`).join("\n")
    : `- DS Academy teaching outline, module ${weekNumber}, lesson ${sessionNumber}, slide ${pageNumber}: ${title}`;
  slide.speakerNotes.textFrame.setText(
    `${narration}\n\n[Sources]\n${sourceLines}\n[/Sources]`,
  );
}

function addChrome(slide, context, pageNumber, inverse = false) {
  const color = inverse ? "#B7CAD9" : C.muted;
  addText(
    slide,
    `M${String(context.weekNumber).padStart(2, "0")} / L${String(context.sessionNumber).padStart(2, "0")}`,
    { left: 54, top: 28, width: 110, height: 22 },
    { fontSize: 11, bold: true, color: inverse ? C.cyan : C.blue },
  );
  addText(
    slide,
    context.session.deck[0].title,
    { left: 176, top: 28, width: 650, height: 22 },
    { fontSize: 11, color },
  );
  addText(
    slide,
    `DS ACADEMY   ${String(pageNumber).padStart(2, "0")}`,
    { left: 1002, top: 28, width: 224, height: 22 },
    { fontSize: 11, bold: true, color, horizontalAlignment: "right" },
  );
}

function addSlideTitle(slide, title, inverse = false, eyebrow = "") {
  if (eyebrow) {
    addText(
      slide,
      eyebrow.toUpperCase(),
      { left: 62, top: 78, width: 560, height: 22 },
      { fontSize: 12, bold: true, color: inverse ? C.cyan : C.blue },
    );
  }
  addText(
    slide,
    title,
    { left: 62, top: eyebrow ? 108 : 80, width: 1110, height: 62 },
    {
      fontSize: title.length > 58 ? 32 : title.length > 44 ? 35 : 38,
      bold: true,
      color: inverse ? C.white : C.ink,
    },
  );
}

function addNotesFor(slide, item, context, pageNumber) {
  setNotes(
    slide,
    item.notes || item.narration,
    context.weekNumber,
    context.sessionNumber,
    pageNumber,
    item.title,
    item.sources || [],
  );
}

async function buildCover(presentation, item, context, pageNumber, assets) {
  const slide = presentation.slides.add();
  slide.background.fill = C.navy;
  addRect(slide, { left: 0, top: 0, width: 1280, height: 12 }, C.cyan);
  addImage(
    slide,
    assets.cover,
    "Data science workflow from raw data to a deployed decision system",
    { left: 724, top: 0, width: 556, height: 720 },
    "cover",
  );
  addRect(slide, { left: 692, top: 0, width: 32, height: 720 }, C.cyan);
  addText(
    slide,
    `MODULE ${String(context.weekNumber).padStart(2, "0")}  /  LESSON ${String(context.sessionNumber).padStart(2, "0")}`,
    { left: 70, top: 70, width: 430, height: 26 },
    { fontSize: 13, bold: true, color: C.cyan },
  );
  addText(
    slide,
    item.title,
    { left: 70, top: 148, width: 548, height: 250 },
    {
      fontSize: item.title.length > 48 ? 44 : item.title.length > 36 ? 48 : 52,
      bold: true,
      color: C.white,
    },
  );
  addRule(slide, 70, 430, 96, C.coral, 6);
  addText(
    slide,
    item.subtitle,
    { left: 70, top: 472, width: 530, height: 102 },
    { fontSize: 22, color: "#D5E2EC" },
  );
  addImage(
    slide,
    assets.logoDark,
    "DS Academy",
    { left: 70, top: 620, width: 182, height: 52 },
    "contain",
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildStatement(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addText(
    slide,
    "WHY THIS MATTERS",
    { left: 64, top: 94, width: 300, height: 25 },
    { fontSize: 12, bold: true, color: C.blue },
  );
  addRule(slide, 64, 146, 110, C.coral, 6);
  addText(
    slide,
    item.title,
    { left: 64, top: 178, width: 1020, height: 72 },
    { fontSize: 40, bold: true, color: C.ink },
  );
  addText(
    slide,
    item.body,
    { left: 64, top: 274, width: 1020, height: 62 },
    { fontSize: 27, bold: true, color: C.blue },
  );
  (item.items || []).forEach((outcome, index) => {
    const top = 374 + index * 72;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: 66, top, width: 56, height: 30 },
      { fontSize: 13, bold: true, color: index === 2 ? C.coral : C.cyan },
    );
    addText(
      slide,
      outcome,
      { left: 144, top: top - 6, width: 900, height: 52 },
      { fontSize: 21, bold: true, color: C.ink },
    );
  });
  addRect(slide, { left: 1146, top: 128, width: 64, height: 476 }, C.ice);
  addRect(slide, { left: 1166, top: 220, width: 24, height: 210 }, C.cyan);
  addNotesFor(slide, item, context, pageNumber);
}

function buildOutcomes(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Session contract");
  item.items.forEach((outcome, index) => {
    const top = 190 + index * 150;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: 66, top, width: 100, height: 76 },
      { fontSize: 45, bold: true, color: index === 1 ? C.cyan : C.blue },
    );
    addRule(slide, 184, top + 33, 94, index === 2 ? C.coral : C.line, 4);
    addText(
      slide,
      outcome,
      { left: 310, top: top - 2, width: 820, height: 82 },
      { fontSize: 27, bold: true, color: C.ink },
    );
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildMap(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.navy;
  addChrome(slide, context, pageNumber, true);
  addSlideTitle(slide, item.title, true, "Four connected ideas");
  const colors = [C.blue, C.cyan, C.white, C.coral];
  item.items.forEach((concept, index) => {
    const left = 64 + index * 296;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left, top: 232, width: 70, height: 30 },
      { fontSize: 13, bold: true, color: colors[index] },
    );
    addRule(slide, left, 282, 220, colors[index], 5);
    addText(
      slide,
      concept,
      { left, top: 312, width: 230, height: 126 },
      {
        fontSize: concept.length > 24 ? 23 : 28,
        bold: true,
        color: C.white,
      },
    );
    if (index < item.items.length - 1) {
      addText(
        slide,
        "→",
        { left: left + 232, top: 324, width: 42, height: 52 },
        { fontSize: 31, bold: true, color: "#8BA2B6", horizontalAlignment: "center" },
      );
    }
  });
  addText(
    slide,
    item.body,
    { left: 64, top: 540, width: 1100, height: 58 },
    { fontSize: 21, color: "#C9D8E4" },
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildConcept(presentation, item, context, pageNumber) {
  const index = item.index || 1;
  const inverse = item.inverse || false;
  const slide = presentation.slides.add();
  slide.background.fill = inverse ? C.navy : C.white;
  addChrome(slide, context, pageNumber, inverse);
  addText(
    slide,
    "CORE CONCEPT",
    { left: 64, top: 100, width: 220, height: 24 },
    { fontSize: 12, bold: true, color: inverse ? C.cyan : C.blue },
  );
  addText(
    slide,
    item.title,
    { left: 64, top: 150, width: 1080, height: 72 },
    { fontSize: 40, bold: true, color: inverse ? C.white : C.ink },
  );
  addRule(slide, 64, 246, 112, C.cyan, 6);
  addText(
    slide,
    item.body,
    { left: 64, top: 278, width: 1110, height: 96 },
    {
      fontSize: item.body.length > 250 ? 17 : item.body.length > 180 ? 19 : 21,
      color: inverse ? "#D6E2EB" : C.graphite,
    },
  );
  const itemCount = (item.items || []).length;
  const columns = itemCount > 4 ? 3 : 2;
  const columnWidth = columns === 3 ? 368 : 574;
  const cardWidth = columns === 3 ? 344 : 540;
  (item.items || []).forEach((detail, itemIndex) => {
    const column = itemIndex % columns;
    const row = Math.floor(itemIndex / columns);
    const left = 64 + column * columnWidth;
    const top = 390 + row * 116;
    addRect(
      slide,
      { left, top, width: cardWidth, height: 96 },
      inverse ? "#183B59" : C.mist,
    );
    addText(
      slide,
      detail,
      { left: left + 18, top: top + 10, width: cardWidth - 36, height: 76 },
      {
        fontSize: detail.length > 125 ? 12 : detail.length > 90 ? 13 : 15,
        bold: true,
        color: inverse ? C.white : C.ink,
      },
    );
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildApplication(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Apply the concept");
  const sections = [
    ["PURPOSE", item.body, C.blue],
    ["IN PRACTICE", item.lab, C.cyan],
    ["WATCH FOR", item.risk, C.coral],
  ];
  sections.forEach(([label, detail, color], index) => {
    const top = 190 + index * 146;
    addText(
      slide,
      label,
      { left: 66, top: top + 5, width: 180, height: 24 },
      { fontSize: 12, bold: true, color },
    );
    addRule(slide, 66, top + 44, 160, color, 4);
    addText(
      slide,
      detail,
      { left: 292, top, width: 850, height: 94 },
      { fontSize: index === 1 ? 22 : 25, bold: index !== 1, color: C.ink },
    );
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildProcess(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.navy;
  addChrome(slide, context, pageNumber, true);
  addSlideTitle(slide, item.title, true, "Reasoning sequence");
  const verbs = ["Frame", "Transform", "Validate", "Explain"];
  item.items.forEach((concept, index) => {
    const left = 62 + index * 296;
    addText(
      slide,
      verbs[index],
      { left, top: 230, width: 220, height: 40 },
      { fontSize: 27, bold: true, color: index === 3 ? C.coral : C.cyan },
    );
    addText(
      slide,
      concept,
      { left, top: 294, width: 230, height: 88 },
      {
        fontSize: concept.length > 90 ? 15 : concept.length > 60 ? 17 : 20,
        bold: true,
        color: C.white,
      },
    );
    addRule(slide, left, 394, 230, index === 3 ? C.coral : "#46627B", 4);
    addText(
      slide,
      String(index + 1),
      { left, top: 428, width: 70, height: 52 },
      { fontSize: 35, bold: true, color: "#7892A8" },
    );
  });
  addText(
    slide,
    item.body,
    { left: 62, top: 544, width: 1110, height: 84 },
    {
      fontSize: item.body.length > 210 ? 16 : item.body.length > 150 ? 18 : 20,
      color: "#D1DEE8",
    },
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildExampleSetup(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Worked example");
  addText(
    slide,
    item.body,
    { left: 66, top: 180, width: 1090, height: 128 },
    { fontSize: 31, bold: true, color: C.ink },
  );
  item.items.forEach((label, index) => {
    const left = 66 + index * 384;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left, top: 400, width: 70, height: 36 },
      { fontSize: 16, bold: true, color: index === 2 ? C.coral : C.blue },
    );
    addRule(slide, left, 454, 316, index === 2 ? C.coral : C.cyan, 5);
    addText(
      slide,
      label,
      { left, top: 488, width: 320, height: 72 },
      { fontSize: 25, bold: true, color: C.ink },
    );
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildCode(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.mist;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Worked example");
  addRect(slide, { left: 58, top: 170, width: 824, height: 458 }, C.ink);
  addRect(slide, { left: 58, top: 170, width: 824, height: 34 }, C.graphite);
  [C.coral, "#F2C94C", C.lime].forEach((color, index) => {
    addRect(slide, { left: 76 + index * 25, top: 181, width: 12, height: 12 }, color, "none", "ellipse");
  });
  addText(
    slide,
    item.code,
    { left: 82, top: 226, width: 760, height: 364 },
    { fontFamily: MONO, fontSize: 17, color: "#E8F1F7" },
  );
  addText(
    slide,
    "DESIGN RULE",
    { left: 934, top: 214, width: 220, height: 24 },
    { fontSize: 12, bold: true, color: C.blue },
  );
  addRule(slide, 934, 260, 84, C.coral, 5);
  addText(
    slide,
    item.body,
    { left: 934, top: 302, width: 270, height: 190 },
    { fontSize: 25, bold: true, color: C.ink },
  );
  addText(
    slide,
    "Read it. Run it. Break it. Explain it.",
    { left: 934, top: 548, width: 270, height: 62 },
    { fontSize: 17, color: C.muted },
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildCodeOutput(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.mist;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Run it and inspect the result");

  addRect(slide, { left: 54, top: 170, width: 684, height: 408 }, C.ink);
  addRect(slide, { left: 54, top: 170, width: 684, height: 32 }, C.graphite);
  [C.coral, "#F2C94C", C.lime].forEach((color, index) => {
    addRect(slide, { left: 72 + index * 24, top: 180, width: 11, height: 11 }, color, "none", "ellipse");
  });
  addText(
    slide,
    item.code,
    { left: 76, top: 220, width: 642, height: 336 },
    { fontFamily: MONO, fontSize: 15, color: "#E8F1F7" },
  );

  addRect(slide, { left: 770, top: 170, width: 454, height: 408 }, C.white, C.line);
  addText(
    slide,
    "OUTPUT",
    { left: 796, top: 194, width: 120, height: 22 },
    { fontSize: 12, bold: true, color: C.blue },
  );
  addText(
    slide,
    item.output,
    { left: 796, top: 234, width: 398, height: 312 },
    { fontFamily: MONO, fontSize: 14, color: C.ink },
  );

  addRect(slide, { left: 54, top: 602, width: 1170, height: 62 }, C.ice);
  addText(
    slide,
    item.takeaway,
    { left: 76, top: 612, width: 1128, height: 44 },
    {
      fontSize: item.takeaway.length > 150 ? 15 : item.takeaway.length > 105 ? 17 : 20,
      bold: true,
      color: C.ink,
    },
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildDataset(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Inspect the evidence");
  addText(
    slide,
    item.subtitle,
    { left: 64, top: 158, width: 1080, height: 44 },
    { fontSize: 19, color: C.muted },
  );

  const values = [item.headers, ...item.rows];
  const table = slide.tables.add({
    rows: values.length,
    columns: item.headers.length,
    left: 64,
    top: 228,
    width: 1152,
    height: 300,
    columnWidths:
      item.headers.length === 5
        ? [350, 290, 130, 190, 192]
        : [300, 240, 300, 312],
    values,
  });
  const header = table.cells.block({
    row: 0,
    column: 0,
    rowCount: 1,
    columnCount: item.headers.length,
  });
  header.fill = C.navy;
  header.textStyle.bold = true;
  header.textStyle.color = C.white;
  header.textStyle.fontSize = 14;
  const body = table.cells.block({
    row: 1,
    column: 0,
    rowCount: item.rows.length,
    columnCount: item.headers.length,
  });
  body.textStyle.fontSize = 14;
  body.textStyle.color = C.ink;

  addRect(slide, { left: 64, top: 560, width: 1152, height: 74 }, C.ice);
  addText(
    slide,
    item.callout,
    { left: 88, top: 580, width: 1104, height: 38 },
    { fontSize: 21, bold: true, color: C.ink },
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildChart(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Evidence and interpretation");

  slide.charts.add(item.chartType, {
    position: { left: 58, top: 176, width: 820, height: 440 },
    categories: item.categories,
    series: item.series.map((series, index) => ({
      ...series,
      fill: index === 0 ? C.blue : C.coral,
    })),
    hasLegend: item.series.length > 1,
    legend: { position: "bottom" },
    barOptions: {
      direction: "column",
      grouping: "clustered",
      gapWidth: 48,
    },
    dataLabels: { showValue: true, position: "outEnd" },
    yAxis: {
      majorGridlines: { style: "solid", fill: C.line, width: 1 },
    },
  });

  addRect(slide, { left: 922, top: 190, width: 302, height: 410 }, C.navy);
  addText(
    slide,
    "READ THE CHART",
    { left: 950, top: 222, width: 240, height: 24 },
    { fontSize: 12, bold: true, color: C.cyan },
  );
  addRule(slide, 950, 270, 76, C.coral, 5);
  addText(
    slide,
    item.insight,
    { left: 950, top: 306, width: 244, height: 240 },
    { fontSize: 23, bold: true, color: C.white },
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildSources(presentation, item, context, pageNumber, assets) {
  const slide = presentation.slides.add();
  slide.background.fill = C.navy;
  addChrome(slide, context, pageNumber, true);
  addSlideTitle(slide, item.title, true, "Lesson synthesis");
  item.items.forEach((detail, index) => {
    const top = 194 + index * 78;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: 66, top, width: 56, height: 30 },
      { fontSize: 13, bold: true, color: index === 3 ? C.coral : C.cyan },
    );
    addText(
      slide,
      detail,
      { left: 142, top: top - 5, width: 580, height: 48 },
      { fontSize: 23, bold: true, color: C.white },
    );
  });
  addText(
    slide,
    "OPEN SOURCES",
    { left: 790, top: 190, width: 260, height: 24 },
    { fontSize: 12, bold: true, color: C.coral },
  );
  addText(
    slide,
    item.source_labels.join("\n\n"),
    { left: 790, top: 238, width: 414, height: 290 },
    { fontSize: 13, color: "#D3E1EB" },
  );
  addImage(
    slide,
    assets.logoDark,
    "DS Academy",
    { left: 1010, top: 620, width: 180, height: 48 },
    "contain",
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildVerify(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Worked example");
  item.items.forEach((detail, index) => {
    const top = 200 + index * 144;
    addRect(
      slide,
      { left: 68, top, width: 66, height: 66 },
      index === 2 ? C.coral : index === 1 ? C.cyan : C.blue,
    );
    addText(
      slide,
      String(index + 1),
      { left: 68, top: top + 12, width: 66, height: 38 },
      { fontSize: 24, bold: true, color: C.white, horizontalAlignment: "center" },
    );
    addText(
      slide,
      detail,
      { left: 182, top: top - 2, width: 900, height: 74 },
      { fontSize: 27, bold: true, color: C.ink },
    );
    addRule(slide, 182, top + 94, 910);
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildPitfalls(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = "#FFF8F6";
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Risk review");
  addRect(slide, { left: 0, top: 0, width: 16, height: 720 }, C.coral);
  item.items.forEach((detail, index) => {
    const top = 196 + index * 148;
    addText(
      slide,
      `0${index + 1}`,
      { left: 74, top, width: 78, height: 42 },
      { fontSize: 18, bold: true, color: C.coral },
    );
    addText(
      slide,
      detail,
      { left: 190, top: top - 8, width: 930, height: 92 },
      { fontSize: 25, bold: true, color: C.ink },
    );
    addRule(slide, 74, top + 105, 1048, "#E7C9C4");
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildChecklist(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Quality gate");
  item.items.forEach((detail, index) => {
    const top = 182 + index * 112;
    addRect(slide, { left: 72, top: top + 3, width: 34, height: 34 }, C.white, C.cyan);
    addText(
      slide,
      "✓",
      { left: 73, top: top + 1, width: 32, height: 30 },
      { fontSize: 20, bold: true, color: C.cyan, horizontalAlignment: "center" },
    );
    addText(
      slide,
      detail,
      { left: 146, top: top - 4, width: 970, height: 68 },
      { fontSize: 20, bold: true, color: C.ink },
    );
    addRule(slide, 146, top + 76, 970);
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildLab(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.navy;
  addChrome(slide, context, pageNumber, true);
  addText(
    slide,
    "GUIDED LAB",
    { left: 64, top: 92, width: 220, height: 24 },
    { fontSize: 12, bold: true, color: C.cyan },
  );
  addText(
    slide,
    item.body,
    { left: 64, top: 154, width: 1100, height: 154 },
    {
      fontSize: item.body.length > 58 ? 31 : item.body.length > 42 ? 34 : 37,
      bold: true,
      color: C.white,
    },
  );
  item.items.forEach((label, index) => {
    const left = 64 + index * 290;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left, top: 410, width: 62, height: 28 },
      { fontSize: 13, bold: true, color: index === 3 ? C.coral : C.cyan },
    );
    addRule(slide, left, 462, 214, index === 3 ? C.coral : "#4A657D", 5);
    addText(
      slide,
      label,
      { left, top: 500, width: 220, height: 52 },
      {
        fontSize: label.length > 52 ? 17 : label.length > 38 ? 19 : label.length > 24 ? 22 : 25,
        bold: true,
        color: C.white,
      },
    );
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildPortfolio(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addChrome(slide, context, pageNumber);
  addText(
    slide,
    "PORTFOLIO EVIDENCE",
    { left: 66, top: 96, width: 300, height: 25 },
    { fontSize: 12, bold: true, color: C.blue },
  );
  addText(
    slide,
    item.body,
    { left: 66, top: 164, width: 1040, height: 200 },
    { fontSize: 39, bold: true, color: C.ink },
  );
  addRule(slide, 66, 400, 1100, C.coral, 6);
  item.items.forEach((label, index) => {
    const left = 66 + index * 366;
    addText(
      slide,
      label,
      { left, top: 474, width: 300, height: 54 },
      { fontSize: 25, bold: true, color: index === 2 ? C.coral : C.blue },
    );
    addText(
      slide,
      ["Can be rebuilt", "Has boundary tests", "Supports a decision"][index],
      { left, top: 544, width: 300, height: 46 },
      { fontSize: 17, color: C.muted },
    );
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildQuiz(presentation, item, context, pageNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = C.ice;
  addChrome(slide, context, pageNumber);
  addSlideTitle(slide, item.title, false, "Pause and answer");
  item.items.forEach((question, index) => {
    const top = 190 + index * 148;
    addText(
      slide,
      `Q${index + 1}`,
      { left: 70, top, width: 70, height: 42 },
      { fontSize: 18, bold: true, color: index === 2 ? C.coral : C.blue },
    );
    addText(
      slide,
      question,
      { left: 172, top: top - 8, width: 920, height: 82 },
      { fontSize: 27, bold: true, color: C.ink },
    );
    addRule(slide, 70, top + 104, 1020, "#B8DCE4");
  });
  addNotesFor(slide, item, context, pageNumber);
}

function buildSummary(presentation, item, context, pageNumber, assets) {
  const slide = presentation.slides.add();
  slide.background.fill = C.navy;
  addChrome(slide, context, pageNumber, true);
  addText(
    slide,
    "SESSION SYNTHESIS",
    { left: 64, top: 88, width: 300, height: 25 },
    { fontSize: 12, bold: true, color: C.cyan },
  );
  addText(
    slide,
    "Keep the system, not isolated definitions.",
    { left: 64, top: 136, width: 1040, height: 72 },
    { fontSize: 40, bold: true, color: C.white },
  );
  item.items.forEach((concept, index) => {
    const top = 266 + index * 86;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: 66, top, width: 60, height: 30 },
      { fontSize: 13, bold: true, color: index === 3 ? C.coral : C.cyan },
    );
    addText(
      slide,
      concept,
      { left: 148, top: top - 5, width: 520, height: 58 },
      { fontSize: 20, bold: true, color: C.white },
    );
  });
  addText(
    slide,
    "NEXT EVIDENCE",
    { left: 760, top: 286, width: 250, height: 24 },
    { fontSize: 12, bold: true, color: C.coral },
  );
  addText(
    slide,
    item.body,
    { left: 760, top: 336, width: 430, height: 178 },
    { fontSize: 26, bold: true, color: C.white },
  );
  addImage(
    slide,
    assets.logoDark,
    "DS Academy",
    { left: 1010, top: 620, width: 180, height: 48 },
    "contain",
  );
  addNotesFor(slide, item, context, pageNumber);
}

function buildSlide(presentation, item, context, pageNumber, assets) {
  switch (item.kind) {
    case "cover":
      return buildCover(presentation, item, context, pageNumber, assets);
    case "statement":
      return buildStatement(presentation, item, context, pageNumber);
    case "outcomes":
      return buildOutcomes(presentation, item, context, pageNumber);
    case "map":
      return buildMap(presentation, item, context, pageNumber);
    case "concept":
      return buildConcept(presentation, item, context, pageNumber);
    case "application":
      return buildApplication(presentation, item, context, pageNumber);
    case "process":
      return buildProcess(presentation, item, context, pageNumber);
    case "example_setup":
      return buildExampleSetup(presentation, item, context, pageNumber);
    case "code":
      return buildCode(presentation, item, context, pageNumber);
    case "code_output":
      return buildCodeOutput(presentation, item, context, pageNumber);
    case "dataset":
      return buildDataset(presentation, item, context, pageNumber);
    case "chart":
      return buildChart(presentation, item, context, pageNumber);
    case "verify":
      return buildVerify(presentation, item, context, pageNumber);
    case "pitfalls":
      return buildPitfalls(presentation, item, context, pageNumber);
    case "checklist":
      return buildChecklist(presentation, item, context, pageNumber);
    case "lab":
      return buildLab(presentation, item, context, pageNumber);
    case "portfolio":
      return buildPortfolio(presentation, item, context, pageNumber);
    case "quiz":
      return buildQuiz(presentation, item, context, pageNumber);
    case "summary":
      return buildSummary(presentation, item, context, pageNumber, assets);
    case "sources":
      return buildSources(presentation, item, context, pageNumber, assets);
    default:
      throw new Error(`Unsupported slide kind: ${item.kind}`);
  }
}

async function generateDeck(week, weekNumber, session, sessionNumber, assets) {
  if (session.deck.length < 10 || session.deck.length > 12) {
    throw new Error(
      `Expected 10–12 slides for ${session.title}; found ${session.deck.length}`,
    );
  }
  const presentation = Presentation.create({ slideSize: PAGE });
  const context = { week, weekNumber, session, sessionNumber };
  for (const [index, item] of session.deck.entries()) {
    await buildSlide(presentation, item, context, index + 1, assets);
  }

  const outputDir = path.join(
    OUTPUT_ROOT,
    `module-${String(weekNumber).padStart(2, "0")}`,
    `lesson-${String(sessionNumber).padStart(2, "0")}`,
  );
  const renderDir = path.join(outputDir, "rendered");
  await fs.rm(renderDir, { recursive: true, force: true });
  await fs.mkdir(renderDir, { recursive: true });

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(
      path.join(renderDir, `${stem}.png`),
      new Uint8Array(await png.arrayBuffer()),
    );
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(
      path.join(renderDir, `${stem}.layout.json`),
      await layout.text(),
    );
  }

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(path.join(outputDir, "slides.pptx"));
  return outputDir;
}

const assets = {
  cover: await bytes(COVER),
  logoLight: await bytes(LOGO_LIGHT),
  logoDark: await bytes(LOGO_DARK),
};

for (const [weekIndex, week] of curriculum.weeks.entries()) {
  const weekNumber = weekIndex + 1;
  if (requestedWeek && weekNumber !== requestedWeek) continue;
  for (const [sessionIndex, session] of week.sessions.entries()) {
    const sessionNumber = sessionIndex + 1;
    if (requestedSession && sessionNumber !== requestedSession) continue;
    const output = await generateDeck(
      week,
      weekNumber,
      session,
      sessionNumber,
      assets,
    );
    console.log(output);
  }
}
