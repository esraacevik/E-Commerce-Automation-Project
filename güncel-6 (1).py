import time

import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


# Ürün bilgilerini saklamak için bir liste
urunler = []
# eski ürün verileri için liste
eski_urunler = []

# Excel dosyasını yükleme
def excel_dosyasi_yükle():
    global eski_urunler
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel Dosyası", "*.xlsx")])
    if not file_path:
        return

    try:
        # Excel dosyasını oku
        eski_urunler = pd.read_excel(file_path)

        # url sütunundaki geçersiz url'leri kontrol et
        if 'url' not in eski_urunler.columns:
            messagebox.showerror("Hata", "Excel dosyasında 'url' sütunu bulunamadı.")
            return

        # Geçersiz url'leri ayıkla ve uyarı ver
        gecerli_url = eski_urunler[eski_urunler['url'].apply(lambda x: isinstance(x, str) and x.startswith('http'))]
        gecersiz_url = eski_urunler[~eski_urunler.index.isin(gecerli_url.index)]

        if not gecersiz_url.empty:
            gecersiz_url_listesi = gecersiz_url['url'].tolist()
            messagebox.showwarning(
                "Uyarı",
                f"Geçersiz URL'ler bulundu ve atlandı:\n{', '.join([str(url) for url in gecersiz_url_listesi])}"
            )

        # Geçerli url'leri kullanmaya devam et
        eski_urunler = gecerli_url.reset_index(drop=True)
        gui_ustunde_goster()

    except Exception as e:
        messagebox.showerror("Hata", f"Excel dosyası yüklenirken bir hata oluştu: {e}")


# Excel verilerini Tkinter' da göster
def gui_ustunde_goster():
    if not eski_urunler.empty:
        urunler_listesi.delete(1.0, tk.END)  # Önceki içerikleri temizle

        for _, row in eski_urunler.iterrows():
            urunler_listesi.insert(tk.END, f"Ürün Adı: {row['name']}\nFiyat: {row['price']}\nURL: {row['url']}\n\n")
    else:
        messagebox.showerror("Hata", "Excel dosyasında veri yok!")


# Ürün bilgilerini çekme ve listeleme
def bilgileri_cek_ve_goster(email, password):
    global urunler  # Ürünleri globalde tutalım

    # Selenium WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Oturum açma işlemi
    driver.get("https://www.zara.com/tr/tr/logon")
    time.sleep(3)


    try:
        # Fareyi aşağı kaydır
        actions = ActionChains(driver)
        actions.move_by_offset(220, 400).click().perform() # 200 piksel aşağı kaydır

        button = driver.find_element(By.CLASS_NAME, "enhanced-oauth-logon-view__button")
        button.click()
        # Maksimum 10 saniye bekle
        email_input = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "zds-:r4:"))  # Element ID ile bekleniyor
        )
        # Email giriş alanına email gir
        email_input.send_keys(email)

        sifre_input = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "zds-:r7:"))  # Element ID ile bekleniyor
        )
        # Şifre giriş alanına şifreyi gir
        sifre_input.send_keys(password)

        time.sleep(3)
        oturum_ac_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-qa-id='logon-form-submit']"))
        )
        oturum_ac_button.click()

        # "Sepet" linkini bekle ve tıklanabilir olunca tıkla
        sepet = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='layout-header-go-to-cart']"))
        )
        sepet.click()
        print("Sepete başarıyla tıklandı.")

    except:
        print("Başarısız.")

    # Sepet sayfasına git
    #url = "https://www.zara.com/tr/tr/shop/cart"
    #driver.get(url)

    urunler = []

    try:
        # Sepetteki ürünlerin bilgilerini çek
        ürün_konteynerlari = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'shop-cart-item__details-container')]"))
        )

        for container in ürün_konteynerlari:
            try:
                # Ürün adı bilgisi
                product_name_element = container.find_element(By.XPATH,
                                                              ".//div[contains(@class, 'shop-cart-item-header__description')]")
                product_name = product_name_element.text.strip()
                print(f"Ürün Adı: {product_name}")  # Kontrol etme amaçlı

                # Ürün fiyatı bilgisi
                product_price_element = container.find_element(By.XPATH, ".//span[@class='money-amount__main']")
                product_price = product_price_element.text.strip()
                print(f"Fiyat: {product_price}")  # Kontrol etme amaçlı

                # Ürün URL'si
                product_url_element = container.find_element(By.XPATH,
                                                             ".//a[contains(@class, 'shop-cart-item-header__description-link link')]")
                product_url = product_url_element.get_attribute("href")
                print(f"URL: {product_url}")  # Kontrol etme amaçlı

                # Ürün bilgilerini listeye ekle
                urunler.append({
                    'name': product_name,
                    'price': product_price,
                    'url': product_url
                })


            except StaleElementReferenceException as e:
                print(f"Hata: {e}")
                continue

    except TimeoutException:
        messagebox.showerror("Hata", "Sepet ürünleri yüklenemedi!")
    finally:
        driver.quit()

    # Ürün bilgilerini arayüzde göster
    urunler_listesi.delete(1.0, tk.END)  # Önceki içerikleri temizle
    for product in urunler:
        urunler_listesi.insert(tk.END,
                            f"Ürün Adı: {product['name']}\nFiyat: {product['price']}\nURL: {product['url']}\n\n")

    # Ürünleri Excel dosyasına kaydetmek için kullanıcıya seçenek sun
    if messagebox.askyesno("Excel Kaydet", "Ürün verilerini Excel dosyasına kaydetmek ister misiniz?"):
        excele_kaydet()


# Excel'e kaydetme fonksiyonu
def excele_kaydet():
    global urunler
    if urunler:
        df = pd.DataFrame(urunler)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Dosyası", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Başarılı", "Veriler başarıyla kaydedildi.")
    else:
        messagebox.showerror("Hata", "Kaydedilecek veri yok.")


# Fiyat değişikliklerini kontrol etme fonksiyonu
def fiyat_degisikleri_kontrol_et():
    if eski_urunler.empty:
        messagebox.showerror("Hata", "Lütfen önce Excel dosyasını yükleyin.")
        return

    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
    except Exception as e:
        messagebox.showerror("Hata", f"WebDriver başlatılamadı: {e}")
        return

    changes_detected = False
    message = "Fiyat değişimleri:\n"

    try:
        for _, row in eski_urunler.iterrows():
            url = row['url']  # Excel dosyasındaki url

            if not isinstance(url, str) or not url.startswith("http"):
                print(f"Geçersiz URL atlandı: {url}")
                continue  # Geçersiz URL'yi atla

            try:
                driver.get(url)

                # Ürünün fiyatını yeni sayfada kontrol et
                product_price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[@id='main']/article/div/div[1]/div[2]/div/div[1]/div[2]/div/span/span/span/div/span"))
                )
                new_price = product_price_element.text.strip()

                # Eski fiyatı ve yeni fiyatı karşılaştır
                if new_price != str(row['price']).strip():
                    changes_detected = True
                    message += f"Ürün: {row['name']}\nEski Fiyat: {row['price']} -> Yeni Fiyat: {new_price}\n\n"

            except TimeoutException:
                message += f"Ürün: {row['name']}\nFiyat alınamadı (Timeout).\n\n"
            except Exception as e:
                message += f"Ürün: {row['name']}\nBir hata oluştu: {e}\n\n"

    finally:
        driver.quit()

    if changes_detected:
        messagebox.showinfo("Fiyat Değişiklikleri", message)
    else:
        messagebox.showinfo("Fiyat Değişiklikleri", "Fiyat değişikliği bulunamadı.")


# ARAYÜZ
def gui_calistir():
    global urunler_listesi  # Global değişkenleri burada tanımlıyoruz

    root = tk.Tk()
    root.title("Mağaza Ürün Fiyat Takibi")
    root.geometry("600x600")

    # Mağaza seçimi için seçenekler
    tk.Label(root, text="Hangi mağazadaki hesabınızın sepetteki ürünlerini otomatik kontrole almak istersiniz?").pack(pady=5)
    selected_store = tk.StringVar(value="ZARA")  # Varsayılan mağaza ZARA

    store_dropdown = tk.OptionMenu(root, selected_store, "ZARA")  # Şimdilik sadece ZARA seçeneği
    store_dropdown.pack(pady=10)

    # Email ve şifre giriş alanları
    email_label = tk.Label(root, text="Email:")
    email_label.pack(pady=2)
    email_entry = tk.Entry(root, width=50)
    email_entry.pack(pady=2)

    password_label = tk.Label(root, text="Şifre:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, show="*", width=50)  # Şifreyi gizlemek için show="*"
    password_entry.pack(pady=5)

    # Fiyat verilerini çekme butonu
    def verileri_cek():
        store = selected_store.get()  # Kullanıcının seçtiği mağaza
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Hata", "Lütfen email ve şifreyi girin.")
            return

        if store == "ZARA":
            bilgileri_cek_ve_goster(email, password)  # ZARA için mevcut fonksiyon çağrılır
        else:
            messagebox.showinfo("Bilgi", f"{store} için işlem yapılmadı.")

    fetch_button = tk.Button(root, text="Fiyat Verilerini Çek", command=verileri_cek)
    fetch_button.pack(pady=10)

    # Ürünleri gösterecek yer
    urunler_listesi = tk.Text(root, height=10, width=70)
    urunler_listesi.pack(pady=10)

    load_button_label = tk.Label(root, text="Önceden Excel dosyası olarak kaydettiğiniz ürünlerin "
                                            "şu anki fiyatlarını görmek için sırasıyla şunları yapın:",
                                 wraplength=400)  # wraplength ile satır uzunluğunu belirle
    load_button_label.pack(pady=5)  # Metni butonun üstüne yerleştir

    # Excel dosyasını yükle butonu
    load_button = tk.Button(root, text="1. Excel'den Verileri Yükle", command=excel_dosyasi_yükle)
    load_button.pack(pady=10)

    # Fiyat değişikliklerini kontrol etme butonu
    check_button = tk.Button(root, text="2. Fiyat Değişikliklerini Kontrol Et", command=fiyat_degisikleri_kontrol_et)
    check_button.pack(pady=10)

    root.mainloop()

# Arayüzü çalıştır
gui_calistir()
