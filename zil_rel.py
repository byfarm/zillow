import json
import pandas as pd
import openpyxl
import bs4
import requests
import realetors as r
import scrape_fun as sf
import pandas as pd
import openpyxl

if __name__ == '__main__':
	# init the urls needed to access the website
	url = "https://www.zillow.com/professionals/real-estate-agent-reviews/minneapolis-mn/"
	companies = sf.get_rel_names(url)

	sf.to_xcel(companies)
	data = sf.from_excel()
	print(data)



