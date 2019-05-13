The Littlefield simulation is a business school institution and I felt inspired to find a way to scrape the data from the sim website so that my team could track inventory and capacity more efficiently. Unfortunately our predictive model was decidedly wrong and we lost horribly as you can see from the massive amounts of red in the Excel datafile.

Embarrassing defeat not withstanding, the scaper did its job and pulled data from the simulation effectively although as the simulation progressed it took a few minutes instead of a few seconds to do its job. This was a detriment to our team since our simulation was held over a two-hour time block in class rather than being spaced out over the course of the semester as is more commonly the case. 

GMU MBA 638 Operations Management, Fall 2018, Professor: Bellos.
Packages: openpyxl, selenium, BeautifulSoup, pandas

I based the scraper off of the work of Greg Lewis from his article on Medium although I chose to use Selenium and openpyxl over pandas since I was more comfortable with those tools having learned Python from Al Swiegart's "Automate the Boring Stuff."
Greg Lewis article: https://medium.com/@gregdlewis/scraping-the-littlefield-simulation-with-python-a6bf618c6833
