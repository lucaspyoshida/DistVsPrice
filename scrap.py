
import asyncio
from playwright.async_api import async_playwright
from lerhtml import parse_response
import json

async def fetch_with_playwright(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        if page.url.startswith("https://consent.google.com"):
            await page.click('text="Accept all"')
        # locator = page.locator('.eQ35Ce')
        # await locator.wait_for()
        await page.wait_for_load_state("networkidle")
        body = await page.evaluate(
            "() => document.querySelector('[role=\"main\"]').innerHTML"
        )
        await browser.close()
    return body

def lerurl(url):
    body = asyncio.run(fetch_with_playwright(url))
    return body

if __name__ == "__main__":
    url = "https://www.google.com/travel/flights?tfs=GiASCjIwMjUtMDktMTUoADICRzNqBRIDQlNCcgUSA0dSVUIBAUgBmAEC&hl=en"
    body = lerurl(url)
    print(json.dumps(parse_response(body)))
    