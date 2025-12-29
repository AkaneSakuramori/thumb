import puppeteer from "puppeteer";
import path from "path";

export async function generatePoster() {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });

  const filePath = path.resolve("templates/default/template.html");
  await page.goto(`file://${filePath}`);

  await page.waitForTimeout(500);

  await page.screenshot({
    path: "output/poster.png"
  });

  await browser.close();
}
