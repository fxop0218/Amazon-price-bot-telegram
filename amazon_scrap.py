import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.amazon.es/UTF8&pd_rd_w=O0PtF&-id=amzn1.sym.35f0d05b-e18e-4de5-8713-ab11f97bda59&pf_rd_p=35f0d05b-e18e-4de5-8713-ab11f97bda59&pf_rd_r=ZEY8BHATBN6FVRFJ6EWZ&pd_rd_wg=maulu&pd_rd_r=df0b65f5-b2de-4ec9-980b-a88a3544e899&ref_=pd_gw_ci_mcx_mi')
print(f"Not correct: {request}")
URL = "https://www.amazon.es/Amazfit-Pro-Smartwatch-Inteligente-Deportativo/dp/B08SW1P74J/?_encoding=UTF8&pd_rd_w=Us0gN&content-id=amzn1.sym.e938e71b-2a18-43eb-855b-f4edce2ba725&pf_rd_p=e938e71b-2a18-43eb-855b-f4edce2ba725&pf_rd_r=ZNS6T8JBATYBMP4PZ0ND&pd_rd_wg=oqm55&pd_rd_r=34980bb2-ac91-48e3-8341-19faa38d8cbc&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
request2 = requests.get(URL)
print(f"Correct: {request2}")



def check_existence(url):
    result = requests.get(url)
    if result.status_code != 404:
        return True
    return False

def get_product(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    title = soup.find("span", id="productTitle")
    price = soup.find("span", class_="a-price-whole")
    strs = soup.find("span", class_="a-icon-alt")
    print(f"Hola: {strs.string}")
    strs = strs.string
    strs = strs.replace("de 5 estrellas", "")
    print(strs)
    return True

som_val = get_product(URL)