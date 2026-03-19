import requests
from bs4 import BeautifulSoup
url = 'https://metanit.com/c/tutorial/1.1.php'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
images = soup.find_all('img')
cnt = 0
for img in images:
    src = img.get('src')

    