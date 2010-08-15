# Modified from the following:
#   http://github.com/lethain/django-syntax-colorize

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer, ClassNotFound

register = template.Library()


def generate_pygments_css(path=None):
    if path is None:
        import os
        path = os.path.join(os.getcwd(), 'pygments.css')

    f = open(path, 'w')
    f.write(HtmlFormatter().get_style_defs('.highlight'))
    f.close()


def get_lexer(value, arg):
    if arg is None:
        return guess_lexer(value)

    return get_lexer_by_name(arg)


def __colorize(value, arg=None, linenos='inline', error_line=False):
    prestyles = ''
    if error_line:
        prestyles = 'border: 1px solid #dd0000'

    try:
        return mark_safe(highlight(value, get_lexer_by_name('python'),
                            HtmlFormatter(linenos=linenos, linenostart=arg,
                                            prestyles=prestyles)))
    except ClassNotFound:
        return value


@register.filter(name='colorize')
@stringfilter
def colorize(value, arg=1):
    return __colorize(value, arg)


@register.filter(name='colorize_error')
@stringfilter
def colorize_error(value, arg=1):
    return __colorize(value, arg, error_line=True)


@register.filter(name='colorize_table')
@stringfilter
def colorize_table(value, arg=1):
    return __colorize(value, arg, linenos='table')
