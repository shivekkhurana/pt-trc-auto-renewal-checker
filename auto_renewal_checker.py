import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import time
from pathlib import Path

# Create Screenshots directory if it doesn't exist
SCREENSHOT_DIR = Path("Screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

def check_trc_renewal():
    # Load environment variables
    load_dotenv()
    print("🔐 Loading credentials...")

    # Get credentials
    username = os.getenv("SEF_USERNAME")
    password = os.getenv("SEF_PASSWORD")
    residence_id = os.getenv("SEF_RESIDENCE_ID")

    if not username or not password or not residence_id:
        print("❌ Error: Please set SEF_USERNAME, SEF_PASSWORD, and SEF_RESIDENCE_ID in your .env file")
        return

    print("\n🌐 Starting browser session...")
    with sync_playwright() as playwright:
        # Launch Safari (WebKit) with specific settings
        browser = playwright.webkit.launch(
            headless=True
        )
        
        # Create a context with smaller viewport size
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},  # Smaller size
            no_viewport=False  # This ensures the viewport size is respected
        )
        
        # Create a new page
        page = context.new_page()
        
        try:
            # Set window size and position (centered and smaller)
            page.set_viewport_size({'width': 1280, 'height': 800})
            
            # Bring window to front by focusing
            page.bring_to_front()
            
            # Add a small pause to ensure window is visible
            time.sleep(0.5)

            # Navigate to SEF portal
            print("🌍 Navigating to SEF homepage...")
            page.goto("https://www.sef.pt/pt/Pages/homepage.aspx")
            print("✅ Loaded SEF homepage")

            # Click login button to open form
            print("🔍 Looking for login button...")
            page.click("text=Login")
            print("✅ Found login button")

            # Wait for login form and fill credentials
            print("🔑 Filling login credentials (first form)...")
            
            # Wait for username field and fill
            page.wait_for_selector("#txtUsername")
            page.fill("#txtUsername", username)
            
            # Wait for password field and fill
            page.wait_for_selector("#txtPassword")
            page.fill("#txtPassword", password)
            
            print("✅ Credentials filled")

            # Submit login form
            print("🚀 Submitting login form...")
            page.click("#btnLogin")

            # Wait for navigation
            print("⏳ Waiting for login process...")
            page.wait_for_load_state("networkidle")
            time.sleep(2)  # Give extra time for the page to settle

            # Verify login success
            if page.is_visible("text=Área Pessoal"):
                print("✅ Login successful!")
            else:
                print("⚠️ Login verification failed")
                print("Taking debug screenshot...")
                page.screenshot(path=str(SCREENSHOT_DIR / "debug_login_verification.png"))
                return

            # Navigate directly to the automatic renewal page
            print("\n🔍 Navigating to automatic renewal page...")
            try:
                # First try clicking the link if visible
                if page.is_visible("#renovacaoAutomaticaLink"):
                    page.click("#renovacaoAutomaticaLink")
                else:
                    # If not visible, try navigating directly
                    page.goto("https://www.sef.pt/pt/mySEF/Pages/renovacao-automatica.aspx")
                
                page.wait_for_load_state("networkidle")
                time.sleep(2)  # Give extra time for the page to settle
                print("✅ Loaded renewal page")

                # Handle the second authentication form
                print("\n🔑 Filling renewal form credentials...")
                
                # Wait for and fill email (should be pre-filled and disabled)
                page.wait_for_selector("#txtAuthPanelEmail")
                
                # Fill password
                page.wait_for_selector("#txtAuthPanelPassword")
                page.fill("#txtAuthPanelPassword", password)
                
                # Fill residence ID
                page.wait_for_selector("#txtAuthPanelDocument")
                page.fill("#txtAuthPanelDocument", residence_id)
                
                print("✅ Renewal form credentials filled")

                # Click the authentication button for the second form
                try:
                    print("⏳ Waiting for authentication button...")
                    page.wait_for_selector("#btnAutenticaUtilizador")
                    page.click("#btnAutenticaUtilizador")
                    print("✅ Clicked authentication button")
                    
                    # Wait for the form submission and page load
                    print("⏳ Waiting for form submission...")
                    page.wait_for_load_state("networkidle")
                    time.sleep(2)  # Give extra time for processing
                    
                    # Check for error message
                    print("\n🔍 Checking renewal availability...")
                    error_selector = "#ctl00_ctl53_g_49abea8d_9129_4f50_bf46_33662dfac0a6_ctl00_lblAuthError"
                    
                    if page.is_visible(error_selector):
                        error_text = page.inner_text(error_selector)
                        print("\n❌ AUTO RENEWAL NOT AVAILABLE")
                        print(f"Reason: {error_text}")
                    else:
                        print("\n✅ AUTO RENEWAL IS AVAILABLE!")
                        print("You can proceed with the renewal process.")
                    
                    # Take a screenshot of the result
                    print("\n📸 Taking screenshot after authentication...")
                    page.screenshot(path=str(SCREENSHOT_DIR / "after_authentication.png"), full_page=True)
                    print("✅ Screenshot saved in Screenshots/after_authentication.png")
                except Exception as e:
                    print(f"⚠️ Error clicking authentication button: {str(e)}")
                    print("Taking debug screenshot...")
                    page.screenshot(path=str(SCREENSHOT_DIR / "debug_authentication_error.png"))
                    raise

            except Exception as e:
                print(f"⚠️ Error in renewal process: {str(e)}")
                print("Trying alternative navigation...")
                # Try finding by text content
                page.click("text=Renovação Automática")

            # Look for renewal information
            print("🔍 Searching for renewal form...")
            
            # Take a screenshot of the renewal page
            print("📸 Taking screenshot of the renewal page...")
            page.screenshot(path=str(SCREENSHOT_DIR / "sef_renewal_page.png"), full_page=True)
            print("✅ Screenshot saved in Screenshots/sef_renewal_page.png")


        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            # Take error screenshot
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            error_filename = f"error_screenshot_{timestamp}.png"
            page.screenshot(path=str(SCREENSHOT_DIR / error_filename))
            print(f"📸 Error screenshot saved in Screenshots/{error_filename}")

        finally:
            print("\n🔒 Closing browser...")
            context.close()
            browser.close()

if __name__ == "__main__":
    print("🤖 Starting SEF TRC Renewal Checker...")
    check_trc_renewal()
    print("\n✨ Process completed!") 