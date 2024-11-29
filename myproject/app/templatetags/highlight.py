from django import template
import re

register = template.Library()


@register.filter
def highlight(text, query):
    """
    검색어를 강조하는 필터
    """
    if not query:
        return text  # 검색어가 없으면 원본 텍스트 반환

    # 검색어를 대소문자 구분 없이 강조
    pattern = re.compile(rf"({re.escape(query)})", re.IGNORECASE)
    highlighted_text = pattern.sub(r"<mark>\1</mark>", text)
    return highlighted_text
