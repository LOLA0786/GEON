import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


# def scrape_website(website):
#     print("Launching chrome browser")   

#     service = Service(ChromeDriverManager().install())
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=service, options=options)

#     try:
#         driver.get(website)
#         print("Page loaded....")
#         time.sleep(10)  # Ensure the page fully loads

#         return driver.page_source  # Return HTML content
#     finally:
#         driver.quit()

import time
import undetected_chromedriver as uc

def scrape_website(website):
    print("Launching undetected Chrome browser")

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # Uncomment if you want to run headless
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(
        # version_main=136, 
        options=options)

    try:
        driver.get(website)
        print("Page loaded....")
        time.sleep(10)  # Ensure the page fully loads

        return driver.page_source  # Return HTML content
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content , "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return " "

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content , "html.parser")

    for script_or_style in soup(["script" , "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator='\n')        
    cleaned_content = '\n'.join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content , max_length=6000):
    return [dom_content[i:i+max_length] for i in range(0,len(dom_content) , max_length)]

def extract_dom_structure(element, max_depth=3, current_depth=0):
    if current_depth > max_depth:
        return None

    structure = {
        "tag": element.name,
        "attributes": dict(element.attrs),
        "children": [],
        "text": element.get_text(strip=True)[:100]  # truncate for brevity
    }

    for child in element.find_all(recursive=False):
        if child.name is not None:
            child_struct = extract_dom_structure(child, max_depth, current_depth + 1)
            if child_struct:
                structure["children"].append(child_struct)

    return structure

def structure_of_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    dom_structure = extract_dom_structure(body)
    return dom_structure