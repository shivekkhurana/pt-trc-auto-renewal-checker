# Auto Renewal Checker

This script automates the process of checking TRC auto-renewal availability on the SEF portal using Playwright.

## Demo

https://raw.githubusercontent.com/shivekkhurana/pt-trc-auto-renewal-checker/refs/heads/master/demo.mp4


## Setup

1. Install UV (if not already installed):
```bash
pip install uv
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/MacOS
# OR
.venv\Scripts\activate  # On Windows
```

3. Install dependencies using UV:
```bash
uv pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install webkit
```

5. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the `.env` file with your SEF credentials:
  ```
  SEF_USERNAME=your.email@example.com
  SEF_PASSWORD=your_password
  SEF_RESIDENCE_ID=your_9_digit_id
  ```

## Usage

Run the script:
```bash
python auto_renewal_checker.py
```

The script will:
1. Launch Safari (WebKit) browser in visible mode
2. Log in to the SEF portal
3. Navigate to the auto-renewal page
4. Fill in the second authentication form
5. Check if auto-renewal is available for your residence permit
6. Save screenshots in the Screenshots directory

## Features
- Visual browser automation so you can see what's happening
- Automatic screenshot capture for documentation
- Error handling with debug screenshots
- Clear terminal output showing progress

## Note
- The browser will run in visible mode (not headless) for transparency
- Screenshots are saved in the Screenshots directory for reference
- The window is sized to 1280x800 for better visibility 