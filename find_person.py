import scrape_fun as sf
import requests


if __name__ == "__main__":

	data = list(sf.from_excel().values)
	data = list(zip(data[0], data[1]))
	links = [i[-1] for i in data[1:]][:4]

	session = requests.Session()

	companies = [sf.inspect_realtor(link, session) for link in links]

	sf.write_finish(companies)



