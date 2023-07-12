import scrape_fun as sf


if __name__ == '__main__':
	# init the urls needed to access the website
	url = "https://www.zillow.com/professionals/real-estate-agent-reviews/moscow-id/"
	companies = sf.get_rel_names(url)

	sf.to_xcel(companies)
	data = sf.from_excel()



