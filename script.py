import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
import nest_asyncio
import random
import getindianname as name
from datetime import datetime
import os

nest_asyncio.apply()

# Flag to indicate whether the script is running
running = True

async def start(name, user, wait_time, meetingcode, passcode, EndTime):
    print(f"{name} started!")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
        context = await browser.new_context(permissions=['microphone'], java_script_enabled=True,)
        page = await context.new_page()
        await page.goto(f'https://app.zoom.us/wc/join/{meetingcode}', timeout=200000)

        try:
            await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.click('//button[@id="wc_agree1"]', timeout=5000)
        except Exception as e:
            pass

        try:
            audio_button = await page.wait_for_selector('button#preview-audio-control-button', timeout=200000)
            await audio_button.click()
            audio_button = await page.wait_for_selector('button#preview-audio-control-button', timeout=200000)
            await audio_button.click()
            await page.wait_for_selector('input[type="text"]', timeout=200000)
            await page.fill('input[type="text"]', user)
            await page.fill('input[type="password"]', passcode)
            join_button = await page.wait_for_selector('button.preview-join-button', timeout=200000)
            await join_button.click()

        except Exception as e:
            pass

        try:
            mic =await page.wait_for_selector ('//button[text()="Join Audio by Computer"]',timeout =350000 )#line:57
            await mic .click ()#line:58
            mic_button =await mic .wait_for_selector ('//button[text()="Join with Computer Audio"]',timeout =350000 )#line:60
            await mic_button .click ('//button[text()="Join with Computer Audio"]')#line:61
            await mic .evaluate ('() => { navigator.mediaDevices.getUserMedia({ audio: true }); }')#line:64
            # await asyncio.sleep(13)
            mic_button_locator = await page.query_selector(query)
            await asyncio.sleep(3)
            await mic_button_locator.evaluate_handle('node => node.click()')
            print(f"{name} mic aayenge.")
        except Exception as e:
            print(f"{name} mic nahe aayenge. ", e)

        print(f"{name} sleep for {wait_time} seconds ...")

        try:
            while True:
                if datetime.now().strftime('%H:%M') == EndTime:
                    break
            print(f"{name} ended!")
            await browser.close()
        except Exception as e:
            pass

        try:
            os.system('pkill -f chromium')
        except Exception as e:
            pass


async def main():
    global running
    number = 10
    meetingcode = '7228753715'
    passcode = '123456'
    EndTime = '14:26'

    sec = 90
    wait_time = sec * 60

    with ThreadPoolExecutor(max_workers=number) as executor:
        loop = asyncio.get_running_loop()
        tasks = []
        for i in range(number):
            try:
                # Generate a random Indian name using getindianname
                user = name.randname()
            except IndexError:
                break
            task = loop.create_task(start(f'[Thread{i}]', user, wait_time, meetingcode, passcode, EndTime))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            running = False
            # Wait for tasks to complete
            await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
