from django import template
import math


register = template.Library()


@register.filter
def read_time(value):
    words = str(value).split()
    word_count = len(words)

    minutes = math.ceil(word_count / 200)

    if minutes < 1:
        minutes = 1

    return f"{minutes} min read"