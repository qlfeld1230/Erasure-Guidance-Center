import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

query = input('뭘 원하니? ')
url = f"https://www.google.com/search?q={query}"

# HTTP 헤더 설정 (필수)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 구글 검색 결과의 제목과 링크 가져오기
    for result in soup.find_all('h3'):
        title = result.get_text()
        parent = result.find_parent('a')
        link = parent['href'] if parent else '링크 없음'

        print(f"제목: {title}")
        print(f"링크: {link}")
        print('---')
else:
    print(f'Failed to retrieve search results: {response.status_code}')