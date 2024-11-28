from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.shortcuts import render
import logging
import xml.etree.ElementTree as ET

# https://developers.naver.com/products/intro/plan/plan.md


class Naver:

    ''' 네이버 웹 검색
    '''
    @staticmethod
    def cafe_search(request):
        query = request.GET.get('query', '')
        results = []
        error = None

        if query:
            client_id = settings.NAVER_CLIENT_ID
            client_secret = settings.NAVER_CLIENT_SECRET
            headers = {
                "X-Naver-Client-Id": client_id,
                "X-Naver-Client-Secret": client_secret,
            }
            url = "https://openapi.naver.com/v1/search/cafearticle.json"
            params = {"query": query, "display": 10, "start": 1, "sort": "sim"}

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                results = data.get("items", [])
            except requests.exceptions.RequestException as e:
                logging.error(f"Naver API request failed: {e}")
                error = "API 요청 실패. 다시 시도해주세요."

        return render(request, 'cafe_search.html', {"results": results, "error": error})


class Naver_rss:

    def rss(request):
        blog_id = request.GET.get('blog_id')
        rss_url = f"http://rss.blog.naver.com/{blog_id}.xml"

        response = requests.get(rss_url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            posts = []

            for item in root.findall(".//item"):
                post = {
                    "title": item.find("title").text,
                    "link": item.find("link").text,
                    "description": item.find("description").text,
                    "pubDate": item.find("pubDate").text
                }
                posts.append(post)

            return render(request, 'naver_rss.html', {"posts": posts, "blog_id": blog_id})
        else:
            return render(request, 'naver_rss.html', {"error": "RSS 피드를 가져오는 데 실패했습니다."})
