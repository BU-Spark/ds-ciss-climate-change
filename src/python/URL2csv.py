URLS = ["https://www.nyc.gov/site/nycha/about/press/2020-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2019-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2018-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2017-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2016-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2015-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2014-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2013-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2012-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2011-press-releases.page",
        "https://www.nyc.gov/site/nycha/about/press/2010-press-releases.page"]

# Save the keyword list to a CSV file
with open('URLS.csv', 'w') as f:
    for url in URLS:
        f.write(f"{url}\n")
