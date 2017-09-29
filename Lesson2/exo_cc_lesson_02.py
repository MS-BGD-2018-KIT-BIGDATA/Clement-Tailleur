from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
import requests
import sys

def scrapper_dicscount(URL):
    page = urlopen(URL).read()
    html = lxml.html.fromstring(page)
    scraping = html.xpath("//div[@class='ecoBlk']//span")
    data_list = [sc.text_content() for sc in scraping]
    data_list_cleaned = [dlc.replace('€','.').strip() for dlc in data_list]
    return data_list_cleaned


URL_DELL = "https://www.cdiscount.com/search/10/ordinateur+portable.html#_his_"
URL_ACER = "https://www.cdiscount.com/search/10/ordinateur+portable.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.ContentTypeId=16&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets%5B3%5D=f%2F6%2Facer&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&FacetForm.SelectedFacets.Index=15&FacetForm.SelectedFacets.Index=16&FacetForm.SelectedFacets.Index=17&FacetForm.SelectedFacets.Index=18&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=ordinateur%2Bportable&&_his_"

dell_discount= list(map(float, scrapper_dicscount(URL_DELL)))
acer_discount= list(map(float, scrapper_dicscount(URL_ACER)))
sum_discount_dell = sum(dell_discount)
sum_discount_acer = sum(acer_discount)

print("Ratio discount sum discount/number of computer Dell:", round(sum_discount_dell/len(dell_discount), 3))
print("Sum discount sum discount/number of computer Acer:", round(sum_discount_acer/len(acer_discount), 3))
