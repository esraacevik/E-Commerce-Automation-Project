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

# List to store product information
products = []
# List for old product data
old_products = []

# Load Excel file
def load_excel_file():
    global old_products
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel File", "*.xlsx")])
    if not file_path:
        return

    try:
        # Read the Excel file
        old_products = pd.read_excel(file_path)

        # Check invalid URLs in the 'url' column
        if 'url' not in old_products.columns:
            messagebox.showerror("Error", "The 'url' column could not be found in the Excel file.")
            return

        # Extract valid URLs and show warning for invalid ones
        valid_url = old_products[old_products['url'].apply(lambda x: isinstance(x, str) and x.startswith('http'))]
        invalid_url = old_products[~old_products.index.isin(valid_url.index)]

        if not invalid_url.empty:
            invalid_url_list = invalid_url['url'].tolist()
            messagebox.showwarning(
                "Warning",
                f"Invalid URLs found and skipped:\n{', '.join([str(url) for url in invalid_url_list])}"
            )

        # Continue with valid URLs
        old_products = valid_url.reset_index(drop=True)
        show_on_gui()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the Excel file: {e}")


# Show Excel data on Tkinter GUI
def show_on_gui():
    if not old_products.empty:
        product_list.delete(1.0, tk.END)  # Clear previous content

        for _, row in old_products.iterrows():
            product_list.insert(tk.END, f"Product Name: {row['name']}\nPrice: {row['price']}\nURL: {row['url']}\n\n")
    else:
        messagebox.showerror("Error", "No data found in the Excel file!")


# Retrieve and display product information
def fetch_and_display_data(email, password):
    global products  # Keep products globally

    # Selenium WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Login process
    driver.get("https://www.zara.com/tr/tr/logon")
    time.sleep(3)

    try:
        # Scroll the page down
        actions = ActionChains(driver)
        actions.move_by_offset(220, 400).click().perform()  # Scroll down 200 pixels

        button = driver.find_element(By.CLASS_NAME, "enhanced-oauth-logon-view__button")
        button.click()
        # Wait for up to 10 seconds
        email_input = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "zds-:r4:"))  # Waiting for element by ID
        )
        # Enter email in the email field
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "zds-:r7:"))  # Waiting for element by ID
        )
        # Enter password in the password field
        password_input.send_keys(password)

        time.sleep(3)
        login_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-qa-id='logon-form-submit']"))
        )
        login_button.click()

        # Wait for the "Cart" link to be clickable and click it
        cart = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='layout-header-go-to-cart']"))
        )
        cart.click()
        print("Successfully clicked the cart.")

    except:
        print("Failed.")

    products = []

    try:
        # Retrieve product information from the cart
        product_containers = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'shop-cart-item__details-container')]"))
        )

        for container in product_containers:
            try:
                # Product name
                product_name_element = container.find_element(By.XPATH,
                                                              ".//div[contains(@class, 'shop-cart-item-header__description')]")
                product_name = product_name_element.text.strip()
                print(f"Product Name: {product_name}")  # For debugging purposes

                # Product price
                product_price_element = container.find_element(By.XPATH, ".//span[@class='money-amount__main']")
                product_price = product_price_element.text.strip()
                print(f"Price: {product_price}")  # For debugging purposes

                # Product URL
                product_url_element = container.find_element(By.XPATH,
                                                             ".//a[contains(@class, 'shop-cart-item-header__description-link link')]")
                product_url = product_url_element.get_attribute("href")
                print(f"URL: {product_url}")  # For debugging purposes

                # Add product info to the list
                products.append({
                    'name': product_name,
                    'price': product_price,
                    'url': product_url
                })

            except StaleElementReferenceException as e:
                print(f"Error: {e}")
                continue

    except TimeoutException:
        messagebox.showerror("Error", "Cart products could not be loaded!")
    finally:
        driver.quit()

    # Display product info on the interface
    product_list.delete(1.0, tk.END)  # Clear previous content
    for product in products:
        product_list.insert(tk.END,
                            f"Product Name: {product['name']}\nPrice: {product['price']}\nURL: {product['url']}\n\n")

    # Ask the user if they want to save product data to an Excel file
    if messagebox.askyesno("Save to Excel", "Do you want to save the product data to an Excel file?"):
        save_to_excel()


# Function to save to Excel
def save_to_excel():
    global products
    if products:
        df = pd.DataFrame(products)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel File", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Data successfully saved.")
    else:
        messagebox.showerror("Error", "No data to save.")


# Function to check price changes
def check_price_changes():
    if old_products.empty:
        messagebox.showerror("Error", "Please load the Excel file first.")
        return

    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
    except Exception as e:
        messagebox.showerror("Error", f"WebDriver could not be started: {e}")
        return

    changes_detected = False
    message = "Price changes:\n"

    try:
        for _, row in old_products.iterrows():
            url = row['url']  # URL from Excel file

            if not isinstance(url, str) or not url.startswith("http"):
                print(f"Invalid URL skipped: {url}")
                continue  # Skip invalid URL

            try:
                driver.get(url)

                # Check the product price on the new page
                product_price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[@id='main']/article/div/div[1]/div[2]/div/div[1]/div[2]/div/span/span/span/div/span"))
                )
                new_price = product_price_element.text.strip()

                # Compare old price and new price
                if new_price != str(row['price']).strip():
                    changes_detected = True
                    message += f"Product: {row['name']}\nOld Price: {row['price']} -> New Price: {new_price}\n\n"

            except TimeoutException:
                message += f"Product: {row['name']}\nPrice could not be fetched (Timeout).\n\n"
            except Exception as e:
                message += f"Product: {row['name']}\nAn error occurred: {e}\n\n"

    finally:
        driver.quit()

    if changes_detected:
        messagebox.showinfo("Price Changes", message)
    else:
        messagebox.showinfo("Price Changes", "No price changes found.")


# GUI
def run_gui():
    global product_list  # Define global variables here

    root = tk.Tk()
    root.title("Store Product Price Tracker")
    root.geometry("600x600")

    # Store selection options
    tk.Label(root, text="Which store's cart products would you like to automatically monitor?").pack(pady=5)
    selected_store = tk.StringVar(value="ZARA")  # Default store is ZARA

    store_dropdown = tk.OptionMenu(root, selected_store, "ZARA")  # Currently, only ZARA option
    store_dropdown.pack(pady=10)

    # Email and password input fields
    email_label = tk.Label(root, text="Email:")
    email_label.pack(pady=2)
    email_entry = tk.Entry(root, width=50)
    email_entry.pack(pady=2)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, show="*", width=50)  # Hide password using show="*"
    password_entry.pack(pady=5)

    # Button to fetch product data
    def fetch_data():
        store = selected_store.get()  # Selected store by the user
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password.")
            return

        if store == "ZARA":
            fetch_and_display_data(email, password)  # Call the function for ZARA
        else:
            messagebox.showinfo("Info", f"No action for {store}.")

    fetch_button = tk.Button(root, text="Fetch Price Data", command=fetch_data)
    fetch_button.pack(pady=10)

    # Place to display products
    product_list = tk.Text(root, height=10, width=70)
    product_list.pack(pady=10)

    load_button_label = tk.Label(root, text="To view the current prices of previously saved products in Excel, follow these steps:",
                                 wraplength=400)  # wraplength defines line length
    load_button_label.pack(pady=5)  # Place the text above the button

    # Button to load Excel file
    load_button = tk.Button(root, text="1. Load Data from Excel", command=load_excel_file)
    load_button.pack(pady=10)

    # Button to check price changes

    check_price_button = tk.Button(root, text="2. Check Price Changes", command=check_price_changes)
    check_price_button.pack(pady=10)

    # Run the Tkinter mainloop
    root.mainloop()

if __name__ == "__main__":
    run_gui()
