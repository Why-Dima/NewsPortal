from django import template

register = template.Library()


@register.filter(name='censor')

def censor(value):
    word = ['жопа', 'блять']
    value = str(value)
    i = value.split()
    p = []
    for j in i:
        if j in word:
            p.append('...')
        else:
            p.append(j)
    return ' '.join(p)

