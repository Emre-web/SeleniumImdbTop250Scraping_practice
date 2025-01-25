import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://imdb.com'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)  # Keep the browser open after the script ends
options.add_argument("--disable-popup-blocking")  # Pop-up'ları engelle
options.add_argument("--disable-notifications")  # Bildirimleri devre dışı bırak
driver = webdriver.Chrome(options=options)

driver.get(url)

time.sleep(3)

try:
    # Öğeyi bekleyerek bul
    clear_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ipc-icon.ipc-icon--clear"))
    )
    # Öğeye tıklama işlemi (örnek)
    clear_icon.click()

    print("Öğe başarıyla bulundu ve işlem yapıldı.")
    
except Exception as e:
    print(f"Bir hata oluştu: {e}")

time.sleep(3)

# Öğeyi bekleyerek buluyorum.
reject_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='reject-button']"))
)
reject_button.click()

time.sleep(3)

driver.find_element(By.ID, "imdbHeader-navDrawerOpen").click()

time.sleep(3)

driver.find_element(By.XPATH, "//span[text()='Top 250 Movies']").click()

time.sleep(12)

try:
    # XPath ile öğeyi bekleyerek film başlıklarını bul
    title_elements = driver.find_elements(By.XPATH, "//h3[@class='ipc-title__text']")

    if not title_elements:
        print("Film başlıkları bulunamadı.")
        driver.quit()

    # Film başlıklarını ve tarihleri eşleştirme
    for title_index in range(min(21, len(title_elements))):  # İlk 21 öğeyi işleme al
        film_title = title_elements[title_index].text
        print(f"Film Başlığı: {film_title}")  # Film başlığını yazdır

        # Tarih öğelerini almak için
        # Her film başlığına karşılık gelen tarihleri bul
        film_tarihleri_elements = driver.find_elements(By.CLASS_NAME, "cli-title-metadata")

        if film_tarihleri_elements:
            # Her film için tarih öğesini al
            film_tarihleri = film_tarihleri_elements[title_index].text[:4]  # Tarihin ilk dört harfini al (yıl kısmı)
            
            # Yılı sayıya dönüştürüp karşılaştırma yap
            try:
                year = int(film_tarihleri)  # Yılı sayıya dönüştür
                if year >= 2000:
                    print(f"Tarih: {year}")  # Yıl 2000 ve üzeriyse yazdır
                else:
                    print(f"Film '{film_title}' 2000'den önce çıkmış. Atlanıyor.")
            except ValueError:
                print(f"Geçerli bir yıl bulunamadı: {film_tarihleri}.")

        else:
            print("Tarih bulunamadı.")

    print("Öğeler başarıyla bulundu ve işlem yapıldı.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")

time.sleep(3)
input("Press Enter to continue...")
