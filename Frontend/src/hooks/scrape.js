// scrape.js
import puppeteer from "puppeteer";

(async () => {
  const browser = await puppeteer.launch({ headless: true }); // headless = no GUI
  const page = await browser.newPage();

  await page.goto("http://higoodie.com/", {
    waitUntil: "domcontentloaded",
  });

  // Example: extract <h1> text
  const links = await page.$$eval("a", anchors => anchors.map(a => a.href));
  console.log(links);

  await browser.close();
})();
