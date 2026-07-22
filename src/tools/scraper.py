import requests
from bs4 import BeautifulSoup

def scraper(url : str):
    """Scrape a web page and return its title and paragraph text."""
    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'html.parser')

        # Title
        title = soup.title.get_text(strip=True) if soup.title else "Untitled"

        # Body
        paragraphs = soup.find_all("p")

        content = "\n".join(
            p.get_text(strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        return {
            "title": title,
            "content": content
        }

    except requests.exceptions.HTTPError as errh:
        print("HTTP Error")
        print(errh.args[0])
        


            