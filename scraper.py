from playwright.async_api import async_playwright
import asyncio
import re

url = input('Enter leak site address: ')
company_name = input('Enter company name: ')

async def main():

    async with async_playwright() as pw:

        browser = await pw.chromium.launch(
            headless=True,
            proxy={"server": "socks5://127.0.0.1:9150"}
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        await page.goto(url)
        await page.get_by_text(re.compile("^\d+\sCompanies$", re.IGNORECASE)).click()
        
        base_locator = page.locator(".modal-body").locator(".row.m-2").locator(".col-10")
        company_locator = base_locator.filter(has_text=company_name)  
        await company_locator.get_by_role("button", name="More").click()

        company_detail = page.locator("[id^='company_modal_']").locator(".modal-content")
        await company_detail.wait_for(state="visible")
        await page.wait_for_function("getComputedStyle(document.querySelector('.modal.show')).opacity === '1'")
        bounding_box = await company_detail.bounding_box()
        await page.screenshot(path="test.png", clip=bounding_box)


        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
