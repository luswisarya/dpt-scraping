from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv

website = 'https://cekdptonline.kpu.go.id/'
path = '/Users/Asus/Downloads/chromedriver.exe'


df = pd.read_csv('nik_test.csv')

data_list = []
for index, row in df.iterrows():
    nik = row['NIK']
    nik_str = str(nik)
    kode_wilayah = nik_str[:6] 
    kode_lanjutan = nik_str[6:]
    driver = webdriver.Chrome()
    driver.get(website)
    pencarian = driver.find_element("xpath", '//input[@class="form-control is-valid"]')
    pencarian.clear()
    pencarian.send_keys(nik_str)
    pencarian.send_keys(Keys.RETURN)
    time.sleep(10)

    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="row row-1"]')))
        element = driver.find_element("xpath", '//div[@class="row row-1"]')
        hasil = element.text
        lines = hasil.split('\n')
        nama_pemilih = lines[1] if len(lines) > 1 else ''
        tps = lines[3] if len(lines) > 3 else ''

        element_2 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="row row-1"]')))
        element_2 = driver.find_element("xpath", '//div[@class="row row-3"]')
        hasil_2 = element_2.text
        lines_2 = hasil_2.split('\n')
        kabupaten = lines_2[1] if len(lines_2) > 1 else ''
        kecamatan = lines_2[3] if len(lines_2) > 3 else ''
        kelurahan = lines_2[5] if len(lines_2) > 5 else ''
        
        element_3 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//p[@class="row--left"]')))
        element_3 = driver.find_elements("xpath", '//p[@class="row--left"]')
        if element_3 and len(element_3) >= 2:
            element_yang_kedua = element_3[1]
            hasil_3 = element_yang_kedua.text
            lines_3 = hasil_3.split('\n')
            alamat = lines_3[1] if len(lines_3) > 1 else ''
        #Print Results
        #print("Nama Pemilih: ", nama_pemilih)
        #print("NIK: ", nik)
        #print("TPS: ", tps)
        #print("Kabupaten: ", kabupaten)
        #print("Kecamatan: ", kecamatan)
        #print("Kelurahan: ", kelurahan)
        #print("Alamat TPS: ", alamat)
        #print()
        individual_data = [nama_pemilih, kode_wilayah, kode_lanjutan, tps, kabupaten, kecamatan, kelurahan, alamat]
        data_list.append(individual_data)
        print("Data for NIK:", nik, "bernama:", nama_pemilih, "berhasil ditambahkan ke list data")

    except TimeoutException:
        print("NIK", nik, "Tidak Terdaftar sebagai DPT")

driver.quit

hasil_akhir = 'extracted_data2.csv'
with open(hasil_akhir, 'w', newline='') as csvfile:
    fieldnames = ['Nama Pemilih', 'Kode Daerah','Kode Lanjutan', 'TPS', 'Kabupaten', 'Kecamatan', 'Kelurahan', 'Alamat TPS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in data_list:
        writer.writerow(dict(zip(fieldnames, row)))

print("Data saved to", hasil_akhir)
