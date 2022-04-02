# for playwright
from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync
import datetime
import json

# for recaptcha
import urllib
import pydub
from speech_recognition import Recognizer, AudioFile
import random
import os

configs = {
    'CHROME_BUNDLE': '/home/binit/driver/chrome-linux/chrome',
    'HEADLESS': 'false',
}


def browsersetup(p):
    headless = True if configs["HEADLESS"] == "true" else False

    args = [
        '--deny-permission-prompts',
        '--no-default-browser-check',
        '--no-first-run',
        '--deny-permission-prompts',
        '--disable-popup-blocking',
        '--ignore-certificate-errors',
        '--no-service-autorun',
        '--password-store=basic',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        '--window-size=640,480',
        '--disable-audio-output'
    ]
    browser = p.chromium.launch(
        headless=headless, executable_path=configs["CHROME_BUNDLE"], args=args)

    return browser


class SolveCaptcha:
    def __init__(self, page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None

    def delay(self):
        self.page.wait_for_timeout(random.randint(1, 3) * 1000)

    def presetup(self):
        name = self.page.locator(
            "//iframe[@title='reCAPTCHA']").get_attribute("name")
        self.recaptcha = self.page.frame(name=name)

        self.recaptcha.click("//div[@class='recaptcha-checkbox-border']")
        self.delay()
        s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
        if s.get_attribute("aria-checked") != "false":  # solved already
            return

        self.main_frame = self.page.frame(name=page.locator(
            "//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute("name"))
        self.main_frame.click("id=recaptcha-audio-button")

    def start(self):
        self.presetup()
        tries = 0
        while (tries <= 5):
            self.delay()
            try:
                self.solve_captcha()
            except Exception as e:
                print(e)
                self.main_frame.click("id=recaptcha-reload-button")
            else:
                s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
                if s.get_attribute("aria-checked") != "false":
                    self.page.click("id=recaptcha-demo-submit")
                    self.delay()
                    break
            tries += 1

    def solve_captcha(self):
        self.main_frame.click(
            "//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = self.main_frame.locator(
            "//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")

        urllib.request.urlretrieve(href, "audio.mp3")

        sound = pydub.AudioSegment.from_mp3(
            "audio.mp3").export("audio.wav", format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(text)
        self.main_frame.fill("id=audio-response", text)
        self.main_frame.click("id=recaptcha-verify-button")
        self.delay()

    def __del__(self):
        os.remove("audio.mp3")
        os.remove("audio.wav")


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = browsersetup(p)
        context = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 640, "height": 480}
        )
        page = context.new_page()
        stealth_sync(page)

        try:
            page.goto("https://www.google.com/recaptcha/api2/demo")
            captcha_solver = SolveCaptcha(page)
            captcha_solver.start()
            del captcha_solver
        except Exception as e:
            print(e)
        context.close()
        browser.close()
