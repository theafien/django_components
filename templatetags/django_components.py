from django import template
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.urls import reverse
from django.template.base import FilterExpression, kwarg_re
from django.template.context import make_context

register = template.Library()


def parse_tag(token, parser):
    bits = token.split_contents()
    tag_name = bits.pop(0)
    args = []
    kwargs = {}
    for bit in bits:
        match = kwarg_re.match(bit)
        kwarg_format = match and match.group(1)
        if kwarg_format:
            key, value = match.groups()
            kwargs[key] = FilterExpression(value, parser)
        else:
            args.append(FilterExpression(bit, parser))

    return (tag_name, args, kwargs)

@register.simple_tag(name="component")
def component_singletag(name, *args, **kwargs):
    return Component(name).render({}, *args, **kwargs)


@register.tag(name="component_block")
def do_component(parser, token):
    tag_name, args, kwargs = parse_tag(token, parser)

    component_name = args[0]

    nodelist = parser.parse(('endcomponent_block',))
    parser.delete_first_token()

    return ComponentBlockNode(nodelist, component_name, *args, **kwargs)


class ComponentBlockNode(template.Node):
    def __init__(self, nodelist, template_name, *args, **kwargs):
        self.nodelist = nodelist
        self.template_name = template_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        self.kwargs['children'] = self.nodelist.render(context)
        return Component(self.template_name).render(context, *self.args, **self.kwargs)


class Component(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context, *args, **kwargs):

        if isinstance(self.template_name, FilterExpression):
            self.template_name = self.template_name.resolve(context)

        for k in kwargs.keys():
            if isinstance(kwargs[k], FilterExpression):
                kwargs[k] = kwargs[k].resolve(context)

            if k in ['url', 'href']:
                kwargs[k] = reverse(kwargs[k])

            elif k.startswith("_"):
                kwargs[k[1:]] = _(kwargs[k])

        default_context = {'props': kwargs}

        return render_to_string("components/%s.html" % self.template_name, default_context)
