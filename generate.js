import puppeteer from "puppeteer";
import fs from "fs";

export async function generatePoster() {
  if (!fs.existsSync("output")) {
    fs.mkdirSync("output");
  }

  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });

  await page.goto("http://localhost:5000/templates/default/template.html", {
    waitUntil: "networkidle0"
  });

  await page.waitForSelector(".poster");
  await page.evaluateHandle("document.fonts.ready");

  await page.screenshot({
    path: "output/poster.png"
  });

  await browser.close();
}
