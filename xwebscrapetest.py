
import trafilatura
downloaded = trafilatura.fetch_url('https://www.nbcnews.com/latest-stories')
response = trafilatura.extract(downloaded,include_links=True,include_formatting=True)

print(response)
