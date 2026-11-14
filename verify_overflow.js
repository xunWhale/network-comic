const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 800 });
  await page.goto('file:///home/fish/workspace/network-comic/ospf.html');
  const isOk = await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);
  console.log('Mobile overflow check:', isOk);
  await browser.close();
})();
