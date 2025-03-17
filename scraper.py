from playwright.async_api import async_playwright
import asyncio
import re
import os

async def main():

    async with async_playwright() as pw:

        browser = await pw.chromium.launch(
            headless=True,
            proxy={"server": "socks5://127.0.0.1:9150"}
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            accept_downloads=True
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
        await page.screenshot(path=f"{company_name}/screenshot.png", clip=bounding_box)

        links = await company_detail.get_by_text("Documents").all()
        dir_files = []
        for link in links:
            dir_files.append(await link.get_attribute("href") + "data/ALL_FILES")
        print(dir_files)

        counter = 1
        for href in dir_files:
            page = await browser.new_page()
    
            async with page.expect_download() as download_info:
                await page.evaluate(f'window.location.href = "{href}"')

            download = await download_info.value  
            file_path = f"./{company_name}/Documents_{counter}.txt"
            await download.save_as(file_path)  

            print(f"Download completed: {file_path}")
    
            counter += 1
            await asyncio.sleep(2)        
            
        await browser.close()


url = input('Enter leak site address: ')
company_name = input('Enter company name: ')
os.mkdir(company_name)

if __name__ == '__main__':
    asyncio.run(main())
