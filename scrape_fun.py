import requests
import bs4
import copy
import random
import time
import pandas as pd
import realetors as r


def get_rel_names(url, new_page=None):
	headers = config_req()
	url_m = copy.deepcopy(url)
	# init the param we want to track
	companies = []
	pages = set()

	# while it is still going through the pages
	while True:
		# go to the next page and assert it has been accessed
		url_m = url + f'?page={new_page}' if len(companies) != 0 else url_m
		result = requests.post(url_m, headers=headers)
		assert result.status_code == 200


		# find all the realitors and parse
		soup = bs4.BeautifulSoup(result.text, 'html.parser')
		result.close()
		tbl = soup.find('tbody').contents

		# find the company name and their link and append to the companies list
		for tbr in tbl:
			company = tbr.td.div.contents[1].a
			comp_name = company.text
			link = company.attrs['href']
			companies.append((comp_name, link))

		# find which page on then set the url to the next page. note that if you do too mainy pages then zillow will block
		if len(pages) < 2:
			nav = soup.find('ul', class_="PaginationList-c11n-8-50-1__sc-14rlw6v-0 jXRymW").contents[1:-2]
			for pg in nav:
				new_page = int(pg.text)
				if new_page not in pages:
					pages.add(new_page)
					n_pgs = True
					time.sleep(0.5)
					break
			else:
				n_pgs = False
		else:
			break

		# if passes through then all pages have been visited and can break
		if n_pgs is False:
			break

	return companies


def to_xcel(lis):
	names = []
	links = []
	for i in lis:
		names.append(i[0])
		links.append(i[1])

	data = [names, links]
	df = pd.DataFrame(data)
	df.to_excel('Zillow_Realtors.xlsx', sheet_name='Realtors on Zil')


def from_excel():
	data = pd.read_excel('Zillow_Realtors.xlsx', sheet_name='Realtors on Zil')
	return data


def config_req():
	# config request
	agent = [
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
	]
	agent = agent[random.randint(0, len(agent) - 1)]
	cookie = [
		'x-amz-continuous-deployment-state=AYABeEWjnTNL3F6DZx3AE3Sro%2FIAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADCm15E%2FLGgMwK6C6iAAwtOmwaorxLdcVxY5lcUzq9ycIyfLgTGyYgWAmBQuP3d%2FwjimjRbvk+KWRxPIHrODxAgAAAAAMAAQAAAAAAAAAAAAAAAAAAIoUQkYD+%2FSmo9bBvL7KvMP%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAzCmoNvJISGUPBq5p+4Nfbu4dKnCqJwkfngatTFbu4dKnCqJwkfngatTA==; zguid=24|%240b282d7d-7e51-4c7d-93ce-37b6bae59c06; _ga=GA1.2.1495600491.1689035540; _gid=GA1.2.2023673835.1689035540; _gcl_au=1.1.1032853577.1689035540; zjs_anonymous_id=%220b282d7d-7e51-4c7d-93ce-37b6bae59c06%22; zjs_user_id=null; zg_anonymous_id=%22c788aa1a-a308-428a-9a9c-fe237774ace9%22; _pxvid=65f516a4-1f82-11ee-83b6-2aae9de7affd; __pdst=4adf809a647647b5bce5ccfe567c8508; _pin_unauth=dWlkPVpHUmlZalpoTnpjdE5HWmlaaTAwWldNNUxUaGxOelF0TVRreE5qZzBNek5oTW1Neg; g_state={"i_p":1689096784129,"i_l":1}; _cs_c=0; search=6|1691705703734%7Crect%3D73.0215502538665%252C-110.91696875%252C47.810759635472515%252C-179.999%26rid%3D3%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%093%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _gac_UA-21174015-56=1.1689113854.CjwKCAjw-7OlBhB8EiwAnoOEk2eUaKpc_Txpg4HMnS80qxDGi72691Z9yHUlcZXWi1yoFRVdfpI5rhoCqaYQAvD_BwE; _gcl_aw=GCL.1689113854.CjwKCAjw-7OlBhB8EiwAnoOEk2eUaKpc_Txpg4HMnS80qxDGi72691Z9yHUlcZXWi1yoFRVdfpI5rhoCqaYQAvD_BwE; optimizelyEndUserId=oeu1689113907795r0.8242233990642849; zgcus_aeut=AEUUT_dc7ed181-2038-11ee-a3b8-1646f2d921fb; zgcus_aeuut=AEUUT_dc7ed181-2038-11ee-a3b8-1646f2d921fb; _clck=ngs9vu|2|fd8|0|1287; zgsession=1|b73274d3-cf2c-40b3-aaa0-e0f67d3c37e7; pxcts=2137dbd6-205f-11ee-b091-63446176666d; DoubleClickSession=true; _cs_id=98d40222-8442-a84d-8bea-80b37e91da27.1689089961.6.1689136131.1689135111.1.1723253961632; JSESSIONID=CB2C0FA0CFA2A237B5A37910E8AD3AE8; _hp2_id.1215457233=%7B%22userId%22%3A%22597707652264534%22%2C%22pageviewId%22%3A%226579794488939943%22%2C%22sessionId%22%3A%222543602231528646%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _uetsid=66b71b701f8211eeb59c13bfdc3ac844; _uetvid=66b739901f8211ee9d731d67bf46f187; _hp2_ses_props.1215457233=%7B%22ts%22%3A1689172426315%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; _px3=04649fd4f35927402f2fddd1913d9b8f6d35033da5d6ff3e03a05eb5245bbca9:KDhg4mjeh5fCOerh/QFzvFtEO5KxIIRuFQaTXmCBfNED900Rtis3+gnYpPud2ZHgFJUqWBnilgA7JH82B6WXRw==:1000:vI/BfpcIPSTZD5RBI6PZvfSPFvOQCy3D4q/GMl38IIwYfSjslurmE9i83HvIHyzw7UFkpW/hLEp1hMKNEnrrnO0e21VcxMZdYeXrJZzj90bMqTkBlAizqaAv2Uz0pnlqP9oFHtyniDYZYIvboknLvpUWKK35wlCTPn7YmWUHqSrcQ1wsP+SPSDUuvgU1+NcSJHIK944je3Tqt5spStwLuQ==; _clsk=ef69gs|1689172427221|1|0|t.clarity.ms/collect; AWSALB=iTOYp1GxKm14miCrK5WJt2ykGla1bxG1cwkLB22GcmaHtJ+gWBl2cIV1aphaY1yxEUOkEGjZ3Q2ukoVdPTQr5iQCqIVHL+Kg04WO3Rg/ammHW83tyQCiPj5ffIj+; AWSALBCORS=iTOYp1GxKm14miCrK5WJt2ykGla1bxG1cwkLB22GcmaHtJ+gWBl2cIV1aphaY1yxEUOkEGjZ3Q2ukoVdPTQr5iQCqIVHL+Kg04WO3Rg/ammHW83tyQCiPj5ffIj+; x-amz-continuous-deployment-state=AYABeEWjnTNL3F6DZx3AE3Sro%2FIAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADCm15E%2FLGgMwK6C6iAAwtOmwaorxLdcVxY5lcUzq9ycIyfLgTGyYgWAmBQuP3d%2FwjimjRbvk+KWRxPIHrODxAgAAAAAMAAQAAAAAAAAAAAAAAAAAAIoUQkYD+%2FSmo9bBvL7KvMP%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAzCmoNvJISGUPBq5p+4Nfbu4dKnCqJwkfngatTFbu4dKnCqJwkfngatTA==; _gat=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_cfp=1; _pxff_bsco=1'
		]
	#cookie = cookie[random.randint(0, len(cookie) - 1)]
	headers = {
		"User-Agent": agent,
		"Cookie": cookie[0]
	}
	return headers


def inspect_realtor(realtor_link, session, company=None):
	headers = config_req()

	b_url = "https://www.zillow.com"
	url = b_url + realtor_link
	time.sleep(0.5)
	result = session.get(url, headers=headers, timeout=3)
	assert result.status_code == 200

	# find the main part of the soup
	soup = bs4.BeautifulSoup(result.text, 'html.parser')
	result.close()
	sec = soup.find('main').contents

	# find the boss and company name and all the contact info
	boss = sec[0].find('div', class_="ctcd-title").h1.text
	company = sec[0].find('div', class_="ctcd-title").div.text if company is None else company
	address, websites, phone = find_info(soup)

	if sec[1].contents[0].h2.text == "Our Members":
		# if it is a company with multiple members, find each member and create a new realtor
		members = sec[1].find('ul', class_="Flex-c11n-8-91-4__sc-n94bjd-0 MrIkl").contents
		reltor_list = [inspect_realtor(li.div.a["href"], session, company) for li in members[:7]]

		# create the new boss and compnay and return the company
		boss = r.Realtor(boss, phone, company, address, websites)
		company = r.Company(company, phone, address, websites, boss)
		for realtor in reltor_list:
			company.add_rel(realtor)
		return company

	else:

		# create the new realetor and return
		realtor = r.Realtor(boss, phone, company, address, websites)

		return realtor


def find_info(soup):
	websites = []
	address = None
	phone = None
	# find all the contact info for the company
	info = soup.find('div', class_="Flex-c11n-8-91-4__sc-n94bjd-0 eyGHKF").div.dl.contents
	for row in info:
		label = row.dt.text
		if label == "Broker address:":
			addy = row.dd.span.contents
			address = ''
			for n in addy:
				address += str(n)
			address = address.replace("<br/>", ';')
		elif label == 'Websites:':
			websites = [i['href'] for i in row.dd.contents[0].contents if i.name is not None]
		elif label == "Cell phone:":
			phone = row.dd.text
	return address, websites, phone


def write_finish(companies):
	with open('realtors.txt', 'w') as f:
		for company in companies:
			if isinstance(company, r.Company):
				f.write(f'company name: {company.name}\n')
				f.write(f'address: {company.address}\n')
				f.write(f'phone: {company.phone}\n')
				f.write('websites: ')
				for i in company.websites:
					f.write(f'{i} ')
				f.write('\n')
				f.write(f'realtors: ')
				for i in company.realtors:
					f.write(f'{i}, ')
				f.write('\n')

				for reltor in company.realtors:
					f.write(f'{reltor.name}\n')
					f.write('websites: ')
					for i in reltor.websites:
						f.write(f'{i} ')
					f.write('\n')
					f.write(f'phone: {reltor.phone}\n\n')
			else:
				f.write(f'{company.name}\n')
				f.write('websites: ')
				for i in company.websites:
					f.write(f'{i} ')
				f.write('\n')
				f.write(f'address: {company.address}\n')
				f.write(f'phone: {company.phone}\n\n')
