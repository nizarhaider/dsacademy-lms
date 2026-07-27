import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(SCRIPT_DIR, "../..");
const PYTHON = process.env.PYTHON || "python3";
const COVER = path.join(REPO, "lms/public/images/dsacademy/course-cover.png");
const LOGO = path.join(REPO, "lms/public/images/dsacademy/logo-light.png");
const OUTPUT_ROOT = path.join(REPO, "course-assets/slides");

const C = {
  ink: "#172033",
  muted: "#58657A",
  soft: "#EDF4FA",
  line: "#D7E2EC",
  blue: "#176BDB",
  cyan: "#08A7C9",
  coral: "#EF7768",
  white: "#FFFFFF",
  dark: "#12253C",
};

const FONT = "Aptos";
const PAGE = { width: 1280, height: 720 };
const args = process.argv.slice(2);
const requestedWeek = Number(args[args.indexOf("--week") + 1] || 0);
const requestedSession = Number(args[args.indexOf("--session") + 1] || 0);

const curriculum = JSON.parse(
  execFileSync(
    PYTHON,
    [
      "-c",
      "import json; from lms.dsacademy.curriculum import COURSE,WEEKS; print(json.dumps({'course':COURSE,'weeks':WEEKS}, ensure_ascii=False))",
    ],
    { cwd: REPO, encoding: "utf8" },
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

function addRect(slide, position, fill, line = "none", radius = "rect") {
  return slide.shapes.add({
    geometry: radius,
    position,
    fill,
    line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
  });
}

function addRule(slide, left, top, width, color = C.line, height = 2) {
  return addRect(slide, { left, top, width, height }, color);
}

function addHeader(slide, weekNumber, sessionNumber, title) {
  addRect(slide, { left: 0, top: 0, width: 12, height: 720 }, C.cyan);
  addText(
    slide,
    `WEEK ${String(weekNumber).padStart(2, "0")}  /  SESSION ${String(sessionNumber).padStart(2, "0")}`,
    { left: 52, top: 28, width: 340, height: 24 },
    { fontSize: 12, bold: true, color: C.blue },
  );
  addText(
    slide,
    title,
    { left: 52, top: 57, width: 920, height: 56 },
    { fontSize: 34, bold: true, color: C.ink },
  );
  addText(
    slide,
    "DS ACADEMY",
    { left: 1085, top: 34, width: 145, height: 24 },
    { fontSize: 12, bold: true, color: C.muted, horizontalAlignment: "right" },
  );
  addRule(slide, 52, 124, 1178);
}

function addFooter(slide, pageNumber) {
  addText(
    slide,
    "End-to-End Data Science & AI",
    { left: 52, top: 680, width: 360, height: 18 },
    { fontSize: 10, color: C.muted },
  );
  addText(
    slide,
    String(pageNumber).padStart(2, "0"),
    { left: 1184, top: 680, width: 46, height: 18 },
    { fontSize: 10, bold: true, color: C.blue, horizontalAlignment: "right" },
  );
}

function setNotes(slide, narration, sourceDetail) {
  slide.speakerNotes.textFrame.setText(
    `${narration}\n\n[Sources]\n- DS Academy curriculum manifest: ${sourceDetail}\n[/Sources]`,
  );
  slide.speakerNotes.setVisible(true);
}

async function addTitleSlide(presentation, weekNumber, sessionNumber, weekData, sessionData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addRect(slide, { left: 0, top: 0, width: 18, height: 720 }, C.cyan);
  addRect(slide, { left: 18, top: 0, width: 590, height: 720 }, C.white);
  slide.images.add({
    blob: await bytes(COVER),
    contentType: "image/png",
    alt: "Data pipeline from raw records to deployed AI application",
    fit: "cover",
    position: { left: 608, top: 0, width: 672, height: 720 },
  });
  addText(
    slide,
    `WEEK ${String(weekNumber).padStart(2, "0")}  ·  SESSION ${sessionNumber}`,
    { left: 70, top: 80, width: 410, height: 28 },
    { fontSize: 14, bold: true, color: C.blue },
  );
  addText(
    slide,
    sessionData.title,
    { left: 70, top: 156, width: 474, height: 188 },
    { fontSize: 49, bold: true, color: C.ink },
  );
  addRule(slide, 70, 370, 74, C.coral, 6);
  addText(
    slide,
    weekData.focus,
    { left: 70, top: 408, width: 466, height: 112 },
    { fontSize: 21, color: C.muted },
  );
  slide.images.add({
    blob: await bytes(LOGO),
    contentType: "image/png",
    alt: "DS Academy logo",
    fit: "contain",
    position: { left: 70, top: 610, width: 180, height: 60 },
  });
  setNotes(
    slide,
    sessionData.narration_en,
    `Week ${weekNumber}, session ${sessionNumber}: ${sessionData.title}`,
  );
}

function addOutcomesSlide(presentation, weekNumber, sessionNumber, sessionData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addHeader(slide, weekNumber, sessionNumber, "Learning outcomes");
  sessionData.outcomes.forEach((outcome, index) => {
    const top = 164 + index * 150;
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: 66, top, width: 84, height: 58 },
      { fontSize: 36, bold: true, color: index === 1 ? C.cyan : C.blue },
    );
    addRule(slide, 163, top + 26, 84, index === 2 ? C.coral : C.line, 4);
    addText(
      slide,
      outcome,
      { left: 276, top: top - 3, width: 850, height: 72 },
      { fontSize: 25, bold: true, color: C.ink },
    );
  });
  addFooter(slide, 2);
  setNotes(slide, `By the end of this session, learners should be able to ${sessionData.outcomes.join(" ")}`, `Learning outcomes for ${sessionData.title}`);
}

function addConceptsSlide(presentation, weekNumber, sessionNumber, sessionData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addHeader(slide, weekNumber, sessionNumber, "The concept system");
  const positions = [
    { left: 76, top: 182 },
    { left: 654, top: 182 },
    { left: 76, top: 420 },
    { left: 654, top: 420 },
  ];
  sessionData.concepts.forEach((concept, index) => {
    const p = positions[index];
    addRect(
      slide,
      { left: p.left, top: p.top, width: 500, height: 170 },
      index % 2 === 0 ? C.soft : C.white,
      index % 2 === 0 ? "none" : C.line,
      "roundRect",
    );
    addRect(
      slide,
      { left: p.left, top: p.top, width: 10, height: 170 },
      index === 3 ? C.coral : index === 1 ? C.cyan : C.blue,
    );
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: p.left + 34, top: p.top + 25, width: 58, height: 30 },
      { fontSize: 14, bold: true, color: C.muted },
    );
    addText(
      slide,
      concept,
      { left: p.left + 34, top: p.top + 69, width: 420, height: 68 },
      { fontSize: 27, bold: true, color: C.ink },
    );
  });
  addFooter(slide, 3);
  setNotes(slide, `Use these four concepts as a system rather than isolated vocabulary: ${sessionData.concepts.join(", ")}.`, `Core concepts for ${sessionData.title}`);
}

function addFlowSlide(presentation, weekNumber, sessionNumber, sessionData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  addText(
    slide,
    "FROM QUESTION TO EVIDENCE",
    { left: 64, top: 50, width: 410, height: 26 },
    { fontSize: 13, bold: true, color: C.cyan },
  );
  addText(
    slide,
    "A repeatable reasoning loop",
    { left: 64, top: 92, width: 720, height: 62 },
    { fontSize: 38, bold: true, color: C.white },
  );
  const labels = ["Define", "Transform", "Validate", "Communicate"];
  labels.forEach((label, index) => {
    const left = 64 + index * 294;
    addRect(
      slide,
      { left, top: 260, width: 236, height: 168 },
      index === 0 ? C.blue : index === 1 ? C.cyan : index === 2 ? C.white : C.coral,
      "none",
      "roundRect",
    );
    addText(
      slide,
      String(index + 1).padStart(2, "0"),
      { left: left + 22, top: 282, width: 50, height: 28 },
      { fontSize: 13, bold: true, color: index === 2 ? C.muted : C.white },
    );
    addText(
      slide,
      label,
      { left: left + 22, top: 340, width: 190, height: 50 },
      { fontSize: 25, bold: true, color: index === 2 ? C.ink : C.white },
    );
    if (index < labels.length - 1) {
      addText(
        slide,
        "→",
        { left: left + 246, top: 322, width: 42, height: 55 },
        { fontSize: 30, bold: true, color: C.white, horizontalAlignment: "center" },
      );
    }
  });
  addText(
    slide,
    sessionData.lab,
    { left: 64, top: 514, width: 1120, height: 82 },
    { fontSize: 22, color: C.white, horizontalAlignment: "center" },
  );
  addText(
    slide,
    "DS ACADEMY  ·  PRACTICAL REASONING",
    { left: 64, top: 665, width: 400, height: 18 },
    { fontSize: 10, bold: true, color: "#AFC4D9" },
  );
  setNotes(slide, `Apply the session content through a four-stage reasoning loop: define the question, transform deliberately, validate assumptions, and communicate the evidence.`, `DS Academy teaching framework applied to ${sessionData.title}`);
}

function addLabSlide(presentation, weekNumber, sessionNumber, sessionData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addHeader(slide, weekNumber, sessionNumber, "Guided lab");
  addRect(slide, { left: 70, top: 170, width: 510, height: 420 }, C.dark, "none", "roundRect");
  addText(
    slide,
    "LAB BRIEF",
    { left: 104, top: 206, width: 180, height: 25 },
    { fontSize: 12, bold: true, color: C.cyan },
  );
  addText(
    slide,
    sessionData.lab,
    { left: 104, top: 264, width: 416, height: 166 },
    { fontSize: 27, bold: true, color: C.white },
  );
  addText(
    slide,
    "workbook  /  tests  /  evidence",
    { left: 104, top: 522, width: 380, height: 26 },
    { fontSize: 13, color: "#AFC4D9" },
  );
  const steps = [
    ["01", "Frame", "Define inputs, outputs, and success criteria."],
    ["02", "Build", "Implement the smallest correct workflow."],
    ["03", "Verify", "Test normal, boundary, and failure cases."],
    ["04", "Explain", "Record the evidence and remaining limits."],
  ];
  steps.forEach(([number, title, detail], index) => {
    const top = 174 + index * 102;
    addText(slide, number, { left: 646, top, width: 42, height: 28 }, { fontSize: 13, bold: true, color: index === 3 ? C.coral : C.blue });
    addText(slide, title, { left: 710, top: top - 3, width: 160, height: 32 }, { fontSize: 21, bold: true, color: C.ink });
    addText(slide, detail, { left: 710, top: top + 34, width: 450, height: 48 }, { fontSize: 16, color: C.muted });
    if (index < 3) addRule(slide, 646, top + 88, 514);
  });
  addFooter(slide, 5);
  setNotes(slide, `Guide learners through the lab without completing the reasoning for them. Ask for an explicit frame, a minimal implementation, boundary tests, and an evidence note.`, `Guided lab for ${sessionData.title}`);
}

function addDeliverableSlide(presentation, weekNumber, sessionNumber, sessionData, weekData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addHeader(slide, weekNumber, sessionNumber, "Portfolio deliverable");
  addText(
    slide,
    sessionData.deliverable,
    { left: 70, top: 170, width: 760, height: 108 },
    { fontSize: 31, bold: true, color: C.ink },
  );
  addText(
    slide,
    "QUALITY GATE",
    { left: 70, top: 334, width: 180, height: 26 },
    { fontSize: 12, bold: true, color: C.blue },
  );
  const gates = ["Reproducible", "Tested", "Decision-relevant"];
  gates.forEach((gate, index) => {
    addRect(slide, { left: 70, top: 386 + index * 65, width: 20, height: 20 }, index === 2 ? C.coral : C.cyan, "none", "roundRect");
    addText(slide, gate, { left: 112, top: 378 + index * 65, width: 330, height: 38 }, { fontSize: 20, bold: true, color: C.ink });
  });
  addRect(slide, { left: 864, top: 168, width: 330, height: 426 }, C.soft, "none", "roundRect");
  addText(slide, "WEEKLY ASSESSMENT", { left: 900, top: 206, width: 250, height: 25 }, { fontSize: 12, bold: true, color: C.blue });
  addText(slide, weekData.assignment[0], { left: 900, top: 260, width: 250, height: 86 }, { fontSize: 25, bold: true, color: C.ink });
  addText(slide, weekData.assignment[2], { left: 900, top: 388, width: 250, height: 132 }, { fontSize: 16, color: C.muted });
  addFooter(slide, 6);
  setNotes(slide, `The deliverable is ${sessionData.deliverable} Use the weekly assessment rubric as a quality gate, not as an after-the-fact scoring checklist.`, `Portfolio deliverable and assessment rubric for week ${weekNumber}`);
}

function addSummarySlide(presentation, weekNumber, sessionNumber, sessionData) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addRect(slide, { left: 0, top: 0, width: 1280, height: 16 }, C.cyan);
  addText(slide, "SESSION CHECKPOINT", { left: 72, top: 68, width: 260, height: 28 }, { fontSize: 13, bold: true, color: C.blue });
  addText(slide, "What should remain after the lesson?", { left: 72, top: 116, width: 920, height: 66 }, { fontSize: 38, bold: true, color: C.ink });
  const summaries = [
    ["CONCEPT", sessionData.concepts.slice(0, 2).join(" + ")],
    ["PRACTICE", sessionData.lab],
    ["EVIDENCE", sessionData.deliverable],
  ];
  summaries.forEach(([label, detail], index) => {
    const top = 244 + index * 120;
    addText(slide, label, { left: 76, top, width: 140, height: 25 }, { fontSize: 12, bold: true, color: index === 2 ? C.coral : C.cyan });
    addText(slide, detail, { left: 242, top: top - 7, width: 880, height: 68 }, { fontSize: 23, bold: true, color: C.ink });
    addRule(slide, 76, top + 84, 1068);
  });
  addText(slide, "Narration available in English and", { left: 76, top: 628, width: 305, height: 28 }, { fontSize: 15, bold: true, color: C.blue });
  addText(slide, "සිංහල", { left: 384, top: 625, width: 92, height: 32 }, { fontFamily: "Sinhala Sangam MN", fontSize: 16, bold: true, color: C.blue });
  addText(slide, "DS ACADEMY", { left: 1050, top: 628, width: 140, height: 28 }, { fontSize: 12, bold: true, color: C.muted, horizontalAlignment: "right" });
  setNotes(slide, sessionData.narration_en, `Session summary for ${sessionData.title}`);
}

async function generateDeck(weekData, weekNumber, sessionData, sessionNumber) {
  const presentation = Presentation.create({ slideSize: PAGE });
  await addTitleSlide(presentation, weekNumber, sessionNumber, weekData, sessionData);
  addOutcomesSlide(presentation, weekNumber, sessionNumber, sessionData);
  addConceptsSlide(presentation, weekNumber, sessionNumber, sessionData);
  addFlowSlide(presentation, weekNumber, sessionNumber, sessionData);
  addLabSlide(presentation, weekNumber, sessionNumber, sessionData);
  addDeliverableSlide(presentation, weekNumber, sessionNumber, sessionData, weekData);
  addSummarySlide(presentation, weekNumber, sessionNumber, sessionData);

  const outputDir = path.join(
    OUTPUT_ROOT,
    `week-${String(weekNumber).padStart(2, "0")}`,
    `session-${String(sessionNumber).padStart(2, "0")}`,
  );
  const renderDir = path.join(outputDir, "rendered");
  await fs.mkdir(renderDir, { recursive: true });

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(renderDir, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(renderDir, `${stem}.layout.json`), await layout.text());
  }

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(path.join(outputDir, "slides.pptx"));
  return outputDir;
}

for (const [weekIndex, weekData] of curriculum.weeks.entries()) {
  const weekNumber = weekIndex + 1;
  if (requestedWeek && weekNumber !== requestedWeek) continue;
  for (const [sessionIndex, sessionData] of weekData.sessions.entries()) {
    const sessionNumber = sessionIndex + 1;
    if (requestedSession && sessionNumber !== requestedSession) continue;
    const output = await generateDeck(weekData, weekNumber, sessionData, sessionNumber);
    console.log(output);
  }
}

execFileSync(PYTHON, [path.join(SCRIPT_DIR, "montage.py")], {
  cwd: REPO,
  stdio: "inherit",
});
