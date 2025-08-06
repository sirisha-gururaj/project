import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PyPDF2 import PdfReader

# --- Configuration ---
# The absolute path to your local college website folder
DUMMY_SITE_DIR = r"C:\Users\Sirisha G\Desktop\NeoStats\AI_UseCase\college-website" 
# It's best to start at the homepage to discover all links naturally
START_FILE = "index.html"
# The directory where all extracted text will be saved
DATA_DIR = "data"
# Wait time for JavaScript to execute
WAIT_SEC = 1

# A set to keep track of visited files to avoid scraping the same page twice
visited_files = set()

def local_file_to_url(file_path):
    """Converts a local file path to a file:/// URL for the browser."""
    abspath = os.path.abspath(file_path)
    return "file:///" + abspath.replace("\\", "/")

def extract_pdf_text(pdf_path):
    """Extracts all text from a local PDF file."""
    if not os.path.exists(pdf_path):
        print(f"  [PDF Error] File not found: {pdf_path}")
        return ""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # Save the extracted PDF text to its own file
        if text:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
            output_filename = os.path.join(DATA_DIR, f"pdf_{pdf_filename}.txt")
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  > Extracted and saved text from PDF: {os.path.basename(pdf_path)}")
        return text.strip()
    except Exception as e:
        print(f"  [PDF Error] Could not read {pdf_path}: {e}")
        return ""

def scrape_page_content(soup, file_path):
    """Extracts the main visible text content from a BeautifulSoup object."""
    # This selector is customized for your website's HTML structure
    content_container = soup.find('div', class_='main') or soup.body
    if content_container:
        page_text = content_container.get_text(separator='\n', strip=True)
        if page_text:
            filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
            with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(page_text)
            print(f"  > Saved main page content to {filename}")

def scrape_department_modals(driver,base_dir):
    """Finds and clicks department cards to scrape the JS-loaded modal content."""
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, ".department-card")
        if not cards:
            return # No department cards on this page

        print(f"  > Found {len(cards)} department cards. Extracting modal details...")
        for i in range(len(cards)):
            # Re-find the cards in each iteration to avoid stale element errors
            card = driver.find_elements(By.CSS_SELECTOR, ".department-card")[i]
            btn = card.find_element(By.CSS_SELECTOR, ".view-details")
            btn.click()
            time.sleep(WAIT_SEC) # Wait for modal to appear

            modal = driver.find_element(By.ID, "deptModal")
            modal_soup = BeautifulSoup(modal.get_attribute("outerHTML"), "html.parser")
            
            dept_title = modal_soup.find("h2").get_text(strip=True)
            modal_text = modal_soup.get_text(separator='\n', strip=True)

            # Save modal content to a department-specific file
            filename = os.path.join(DATA_DIR, f"department_{dept_title.replace(' ', '_')}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(modal_text)
            print(f"    - Saved modal text for '{dept_title}'")

            for link in modal_soup.select('a[href$=".pdf"]'):
                href = link['href']
                # Construct the full path to the PDF
                pdf_path = os.path.abspath(os.path.join(base_dir, href))
                extract_pdf_text(pdf_path)

            # Close the modal before proceeding to the next card
            close_btn = driver.find_element(By.ID, "deptModalClose")
            close_btn.click()
            time.sleep(0.5)

    except Exception as e:
        print(f"  > No department modals found or an error occurred: {e}")

def scrape_all_content(file_path, driver):
    """Main function to scrape a single local file."""
    abs_path = os.path.abspath(file_path)
    if abs_path in visited_files:
        return []
    
    print(f"\nScraping: {file_path}")
    visited_files.add(abs_path)

    try:
        url = local_file_to_url(file_path)
        driver.get(url)
        time.sleep(WAIT_SEC) # Wait for the page and any initial JS to render

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 1. Scrape the main, static text content from the page
        scrape_page_content(soup, file_path)

        # 2. Scrape the dynamic, JavaScript-loaded department modals (if any exist)
        scrape_department_modals(driver, os.path.dirname(file_path))

        # 3. Find and extract text from all linked PDFs on the page
        for link in soup.select('a[href$=".pdf"]'):
            href = link['href']
            # Build the full, absolute path to the local PDF file
            pdf_path = os.path.abspath(os.path.join(os.path.dirname(file_path), href))
            extract_pdf_text(pdf_path)

        # 4. Find all other local HTML files linked from this page to scrape next
        new_files_to_scrape = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.html'):
                next_file_path = os.path.abspath(os.path.join(os.path.dirname(file_path), href))
                if os.path.exists(next_file_path):
                    new_files_to_scrape.append(next_file_path)
        return new_files_to_scrape

    except Exception as e:
        print(f"An error occurred while scraping {file_path}: {e}")
        return []

# --- Main Script Execution ---
if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Setup Selenium to run a headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        start_path = os.path.join(DUMMY_SITE_DIR, START_FILE)
        files_to_scrape = [start_path]

        # Loop until all discoverable pages have been scraped
        while files_to_scrape:
            current_file = files_to_scrape.pop(0)
            newly_found_files = scrape_all_content(current_file, driver)
            for f in newly_found_files:
                if os.path.abspath(f) not in visited_files:
                    files_to_scrape.append(f)

        print(f"\nLocal scraping complete. Visited {len(visited_files)} files.")

    finally:
        # Ensure the browser is always closed properly
        driver.quit()