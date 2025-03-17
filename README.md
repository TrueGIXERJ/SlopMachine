# SlopMachine
post slop.

this project allows the automation of posting "slop" to tiktok - by downloading the top video from a chosen subreddit and uploading it to tiktok using [True_Tiktok_Uploader](https://github.com/TrueGIXERJ/True_TikTok_Uploader).

## Features
* Select any subreddit
* Automatically uploads to tiktok (no authentication required, uses cookies)
* Customisable captions with support for #Hashtags and @Mentions

## Requirements
* Python 3.12+ (probably compatible with older versions too tbh)
* Google Chrome
* Compatible version of the ChromeDriver (This should be automatically installed with Chrome)

## Installation
simply clone this repository

```
git clone https://github.com/truegixerj/SlopMachine.git
cd SlopMachine
pip install -r requirements.txt
```

## Usage
### Setup
First, modify the `config.py` file with the following information:
* `SUBREDDIT` - Set this to your subreddit of choice, for example `r/gtaonline`
* `HASHTAGS` - By default, the video caption will be `Video Title - OP - HASHTAGS`. Set this to any hashtags or mentions (or additional caption) you want at the end of the caption.
* `cookies.txt` - Use [Get cookies.txt](https://github.com/kairi003/Get-cookies.txt-LOCALLY) to export your browsing cookies.
After installing, open the extensions menu on TikTok.com and click `Get cookies.txt` to reveal your cookies. Select `Export As ⇩` and specify a name and location. For more information, see the documentation for the [Tiktok Uploader](https://github.com/TrueGIXERJ/True_TikTok_Uploader).

### Execution
Once configured, simply run
```py
python SlopMachine.py
```
and, like magic, slop is posted!

## Licence
This project is licensed under the MIT Licence. See `LICENCE` for details. (US programmers seething rn)

## Disclaimer
This project is purely for personal & educational use. Make sure you are complying with the terms of both Reddit and Tiktok if using this tool.