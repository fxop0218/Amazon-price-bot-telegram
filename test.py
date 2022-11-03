import unittest

from amazon_scrap import scrap_amz_product, check_existence
from database import add_user_products, user_exists, get_user_products
URL = "https://www.amazon.es/Amazfit-Pro-Smartwatch-Inteligente-Deportativo/dp/B08SW1P74J/?_encoding=UTF8&pd_rd_w=Us0gN&content-id=amzn1.sym.e938e71b-2a18-43eb-855b-f4edce2ba725&pf_rd_p=e938e71b-2a18-43eb-855b-f4edce2ba725&pf_rd_r=ZNS6T8JBATYBMP4PZ0ND&pd_rd_wg=oqm55&pd_rd_r=34980bb2-ac91-48e3-8341-19faa38d8cbc&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
URL2 = "https://www.amazon.es/Govee-Inteligente-Funciona-Assistant-Habitaci%C3%B3n/dp/B09CM1CVCH/?_encoding=UTF8&pd_rd_w=EyCYT&content-id=amzn1.sym.e938e71b-2a18-43eb-855b-f4edce2ba725&pf_rd_p=e938e71b-2a18-43eb-855b-f4edce2ba725&pf_rd_r=NJRXFKJBXDRSBB0VZ497&pd_rd_wg=JwZ8h&pd_rd_r=83ce0b4e-ba9a-4d2c-8117-d1b06e17e0cd&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
print(check_existence("https://www.amazon.es/Diyife-Habitacion-Inteligente-Bluetooth-Sincronizaci%C3%B3n/dp/B09MCZN7TD/?_encoding=UTF8&pd_rd_w=h9dl0&content-id=amzn1.sym.35f0d05b-e18e-4de5-8713-ab11f97bda59&pf_rd_p=35f0d05b-e18e-4de5-8713-ab11f97bda59&pf_rd_r=Q6HYFBBDMXSJE5GP9NZG&pd_rd_wg=ZRz5y&pd_rd_r=44f754b3-0f9d-4185-8936-5a82fec7a0d5&ref_=pd_gw_ci_mcx_mi"))
#scrap_amz_product(URL)
#scrap_amz_product(URL2)
print("Adding new product")
print(f"uset ex{user_exists('exemple')}")
print(f"uset ex{user_exists('c')}")
p = get_user_products("exemple")
print(f"prodcut: {p['products'][0]}")
#add_user_products("exemple", URL)

