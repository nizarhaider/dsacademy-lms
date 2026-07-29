import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const manifests = [
  "package.json",
  "yarn.lock",
  "frontend/package.json",
  "frontend/yarn.lock",
];

function isVulnerable(version) {
  const match = version.match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!match) return false;
  const [, major, minor] = match.map(Number);
  return (major === 3 && minor < 15) || (major === 4 && minor < 3);
}

const findings = [];
for (const relativePath of manifests) {
  const filePath = path.join(root, relativePath);
  if (!fs.existsSync(filePath)) continue;
  const source = fs.readFileSync(filePath, "utf8");
  const versions = [
    ...source.matchAll(/js-yaml(?:\/-|["':@\s^~])[^0-9]*(\d+\.\d+\.\d+)/g),
  ].map((match) => match[1]);
  for (const version of new Set(versions)) {
    if (isVulnerable(version)) findings.push(`${relativePath}: js-yaml ${version}`);
  }
}

if (findings.length) {
  console.error(
    [
      "Vulnerable js-yaml versions detected (CVE-2026-59869):",
      ...findings.map((finding) => `- ${finding}`),
      "Upgrade to js-yaml 4.3.0+ or, for dependencies fixed on v3, 3.15.0+.",
    ].join("\n"),
  );
  process.exit(1);
}

console.log("No vulnerable js-yaml release is present in tracked manifests.");
