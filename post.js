#!/usr/bin/env node
/**
 * Philosophical King — daily quote poster for Facebook Pages + Instagram
 * via the official Meta Graph API. Node 20+, zero dependencies.
 *
 * Commands:
 *   node post.js generate   Render today's quote card into images/
 *   node post.js publish    Post today's card to Facebook (and Instagram if configured)
 *
 * Env vars:
 *   META_ACCESS_TOKEN  (publish) Page access token
 *   FB_PAGE_ID         (publish) Facebook Page ID
 *   IG_USER_ID         (publish, optional) Instagram business account ID
 *   IMAGE_URL          (publish, required when IG_USER_ID is set) public URL of today's image
 *   QUOTE_INDEX        (optional) override the quote of the day, 0-based
 */

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const GRAPH = "https://graph.facebook.com/v21.0";
const HASHTAGS = "#philosophy #stoicism #wisdom #philosophicalking #dailyquote #quotes";

function fail(msg) {
  console.error(`ERROR: ${msg}`);
  process.exit(1);
}

function requireEnv(name) {
  const v = process.env[name];
  if (!v) fail(`missing required environment variable ${name}`);
  return v;
}

function loadQuotes() {
  const file = path.join(__dirname, "quotes.json");
  const quotes = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!Array.isArray(quotes) || quotes.length === 0) fail("quotes.json is empty");
  return quotes;
}

function quoteOfTheDay() {
  const quotes = loadQuotes();
  let index;
  if (process.env.QUOTE_INDEX !== undefined && process.env.QUOTE_INDEX !== "") {
    index = Number.parseInt(process.env.QUOTE_INDEX, 10);
    if (!Number.isInteger(index) || index < 0) fail(`QUOTE_INDEX must be a non-negative integer, got "${process.env.QUOTE_INDEX}"`);
    index %= quotes.length;
  } else {
    const now = new Date();
    const startOfYear = Date.UTC(now.getUTCFullYear(), 0, 0);
    const dayOfYear = Math.floor((now.getTime() - startOfYear) / 86400000);
    index = dayOfYear % quotes.length;
  }
  return { ...quotes[index], index };
}

function todayImage() {
  const date = new Date().toISOString().slice(0, 10);
  const imageName = `quote-${date}.jpg`;
  return { imageName, imagePath: path.posix.join("images", imageName) };
}

function buildCaption(q) {
  return `“${q.quote}”\n\n— ${q.author}\n\n${HASHTAGS}`;
}

async function graphPost(url, body, what) {
  let res;
  try {
    res = await fetch(url, { method: "POST", body });
  } catch (err) {
    throw new Error(`${what}: network error calling Graph API: ${err.message}`);
  }
  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error(`${what}: Graph API returned non-JSON response (HTTP ${res.status})`);
  }
  if (!res.ok || data.error) {
    const e = data.error || {};
    throw new Error(
      `${what} failed (HTTP ${res.status}): ${e.message || JSON.stringify(data)}` +
        (e.code ? ` [code ${e.code}${e.error_subcode ? `/${e.error_subcode}` : ""}]` : "")
    );
  }
  return data;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function generate() {
  const q = quoteOfTheDay();
  const { imageName, imagePath } = todayImage();
  console.log(`Quote #${q.index}: “${q.quote}” — ${q.author}`);
  execFileSync("bash", [path.join(__dirname, "generate-image.sh"), q.quote, q.author, imagePath], {
    stdio: "inherit",
  });
  if (process.env.GITHUB_OUTPUT) {
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `image_path=${imagePath}\nimage_name=${imageName}\n`);
  }
  console.log(`Generated ${imagePath}`);
}

async function publishFacebook(token, pageId, caption, imagePath, imageName) {
  const form = new FormData();
  form.append("message", caption);
  form.append("access_token", token);
  form.append("published", "true");
  form.append("source", new Blob([fs.readFileSync(imagePath)], { type: "image/jpeg" }), imageName);
  const data = await graphPost(`${GRAPH}/${pageId}/photos`, form, "Facebook photo post");
  console.log(`Facebook: posted photo (id ${data.post_id || data.id})`);
}

async function publishInstagram(token, igUserId, caption, imageUrl) {
  const createBody = new URLSearchParams({
    image_url: imageUrl,
    caption,
    access_token: token,
  });
  const container = await graphPost(`${GRAPH}/${igUserId}/media`, createBody, "Instagram media container");
  if (!container.id) throw new Error("Instagram media container: response had no creation id");
  console.log(`Instagram: media container ${container.id} created, publishing...`);

  // Meta processes the image asynchronously; media_publish can fail for a short
  // while after container creation, so retry with increasing delays.
  const delaysMs = [5000, 10000, 20000, 40000, 60000];
  let lastError;
  for (let attempt = 0; attempt < delaysMs.length; attempt++) {
    try {
      const publishBody = new URLSearchParams({
        creation_id: container.id,
        access_token: token,
      });
      const data = await graphPost(`${GRAPH}/${igUserId}/media_publish`, publishBody, "Instagram media publish");
      console.log(`Instagram: published (id ${data.id})`);
      return;
    } catch (err) {
      lastError = err;
      const delay = delaysMs[attempt];
      console.log(`Instagram publish attempt ${attempt + 1}/${delaysMs.length} failed: ${err.message}`);
      if (attempt < delaysMs.length - 1) {
        console.log(`Retrying in ${delay / 1000}s...`);
        await sleep(delay);
      }
    }
  }
  throw new Error(`Instagram publish failed after ${delaysMs.length} attempts: ${lastError.message}`);
}

async function publish() {
  const token = requireEnv("META_ACCESS_TOKEN");
  const pageId = requireEnv("FB_PAGE_ID");
  const igUserId = process.env.IG_USER_ID || "";

  const q = quoteOfTheDay();
  const { imageName, imagePath } = todayImage();
  if (!fs.existsSync(imagePath)) fail(`${imagePath} not found — run "node post.js generate" first`);
  const caption = buildCaption(q);

  await publishFacebook(token, pageId, caption, imagePath, imageName);

  if (igUserId) {
    const imageUrl = requireEnv("IMAGE_URL");
    await publishInstagram(token, igUserId, caption, imageUrl);
  } else {
    console.log("IG_USER_ID not set — skipping Instagram.");
  }
  console.log("Done.");
}

async function main() {
  const command = process.argv[2];
  if (command === "generate") {
    generate();
  } else if (command === "publish") {
    await publish();
  } else {
    fail(`unknown command "${command || ""}" — use "generate" or "publish"`);
  }
}

main().catch((err) => fail(err.message));
