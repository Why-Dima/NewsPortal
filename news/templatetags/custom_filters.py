from django import template

register = template.Library()


@register.filter(name='censor')

def censor(value):
    word = ['жопа', 'блять']
    value = str(value)
    i = value.split()
    for j in i:
        if j in word:
            return 'мат'
        else:
            return str(j)

