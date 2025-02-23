# Product Price Tracking and Shopping Automation Project for Stores

This project enables an application that logs into your account on Inditex stores (currently applicable only to Zara) and tracks the prices and stock availability of the products in your cart or favorites list. It monitors price changes and records this data in an Excel file. Additionally, if there is a price change or stock update for an item in your favorites list, it automatically adds the item to your cart.


Features
This is a two-step application. You can either log into your account and manage your cart or simply upload a previously saved Excel file to track prices and stock without logging in.

Upload Excel File: Load existing product and price data from an Excel file. This step is optional. If you prefer to use the application without logging in, you must upload a file. However, if you log in, no file upload is necessary as the application will automatically retrieve data from your cart and favorites list.
Price Tracking: Retrieve product names, prices, and URLs from your Zara shopping cart.
Save to Excel: Export collected data as an Excel file. This step is optional; you can also view the data instantly on the GUI screen.
User-Friendly Interface: A Tkinter-based graphical interface.*: Tkinter tabanlı grafik arayüz.

## Gereksinimler
To run this project, you need the following software and tools:
Python 3.8 or later
Chrome Browser and ChromeDriver: Required for Selenium to function properly.
Python Libraries:
pandas
tkinter
selenium

## Kurulum
Installation
Follow these steps to set up the project:

Install the required Python libraries:
Download and install ChromeDriver, ensuring it matches your installed Chrome browser version:
    - [ChromeDriver İndir](https://developer.chrome.com/docs/chromedriver/downloads?hl=tr)
    -Copy ChromeDriver to a directory and add it to your system’s PATH environment variable.
    -Download and run the project files.

## Usage
Start the program and fill in the necessary fields on the interface.
Enter your email and password, select a store, and log in to your account.
You can perform the following actions:
When you log in, the products in your cart are automatically saved to an Excel file. If you save this file and later click the "Check Price Differences" button, you will be notified if there are any price changes.
Fetch and list new product prices.
Export all data as an Excel file (optional—you can also view real-time changes in the panel).
Manage your cart and perform operations based on the products in it.
Add products from your favorites list to your cart if their price drops.

-NOTES-

When the program runs, the panel appears as follows.
<img width="446" alt="Panelin Görünümü" src="https://github.com/user-attachments/assets/d831810b-db94-4aa9-8b15-00cac2590446" />
