import scrape_fun as sf
import requests


if __name__ == "__main__":
	data = list(sf.from_excel().values)
	data = [data[i][-1] for i in range(len(data))]
	session = requests.Session()
	companies = [sf.inspect_realtor(link, session) for link in data]

	print()


