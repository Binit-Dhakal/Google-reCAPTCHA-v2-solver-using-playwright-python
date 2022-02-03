# Google — reCAPTCHA v3 solver using playwright-python
This script solve the google recaptcha using playwright-python with pydub and speech recognization. 

## Installation required
- Install all the library we will need
```bash
pip3 install -r requirements.txt
```

## Motivation
I hate captcha(as a scraper)

## Run script
```bash
python3 main.py
```

## Notes
This script tries for 5 times only but we can increase that for how much long we want.

## Future release plan
- [] More testing on other sites than https://www.google.com/recaptcha/api2/demo
- [] More corner cases catching
- [] Find more accurate algorithm or library to solve the audio captcha problem

## Credits
I will like to give all the credit to this blog https://medium.com/geekculture/how-to-solve-google-recaptcha-v3-with-python-9f92bb0212bf by Romik Kelesh(thank you). There he have written script in selenium and i found that working with iframe in selenium is such a pain. So I used one of my favourite weapon for web scraping - playwright.