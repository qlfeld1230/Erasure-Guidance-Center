from django.shortcuts import render
import requests
import xml.etree.ElementTree as ET


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
