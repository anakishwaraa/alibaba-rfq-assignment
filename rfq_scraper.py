from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime

# क्रोम को हेडलेस मोड में सेट करें
options = Options()
options.add_argument("--headless")

# WebDriver स्टार्ट करें
driver = webdriver.Chrome(options=options)

# Alibaba RFQ पेज खोलें
driver.get("https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y")
time.sleep(5)

# नीचे स्क्रॉल करें ताकि ज़्यादा RFQ लोड हों
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# RFQ कार्ड्स निकालें
rfqs = driver.find_elements(By.CLASS_NAME, "rfq-card")

data = []
for rfq in rfqs:
    try:
        title = rfq.find_element(By.CLASS_NAME, "rfq-title").text
        quantity = rfq.find_element(By.CLASS_NAME, "rfq-amount").text
        country = rfq.find_element(By.CLASS_NAME, "rfq-country").text
        inquiry_time = rfq.find_element(By.CLASS_NAME, "rfq-time").text
        quotes_left = rfq.find_element(By.CLASS_NAME, "rfq-quotes").text.split()[0]
        rfq_id = rfq.get_attribute("data-rfq-id") or "N/A"
        inquiry_url = rfq.find_element(By.CLASS_NAME, "rfq-title").get_attribute("href")

        # बाकी फील्ड्स default रखें
        today = datetime.now().strftime("%d-%m-%Y")

        data.append({
            "RFQ ID": rfq_id,
            "Title": title,
            "Buyer Name": "Unknown",
            "Buyer Image": "",
            "Inquiry Time": inquiry_time,
            "Quotes Left": quotes_left,
            "Country": country,
            "Quantity Required": quantity,
            "Email Confirmed": "No",
            "Experienced Buyer": "No",
            "Complete Order via RFQ": "No",
            "Typical Replies": "No",
            "Interactive User": "No",
            "Inquiry URL": inquiry_url,
            "Inquiry Date": today,
            "Scraping Date": today
        })

    except Exception as e:
        print("Error:", e)

# ब्राउज़र बंद करें
driver.quit()

# CSV सेव करें
df = pd.DataFrame(data)
df.to_csv("rfq_output.csv", index=False)
print("✅ स्क्रैपिंग पूरी हो गई! फाइल बनी: rfq_output.csv")
