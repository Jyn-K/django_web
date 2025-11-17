import markdown
from django import template

# 장고 이스케이프에서 안전한 html 태그로 랜더링하기 위해 필요
from django.utils.safestring import mark_safe

# 필터 or 함수를 등록하기 위한 객체화
register = template.Library()

# 필터 or 함수를 실제 등록
@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
