import re

from django import template

from social_core.backends.oauth import OAuthAuth

from social_django.utils import Storage


register = template.Library()

name_re = re.compile(r'([^O])Auth')


@register.filter
def backend_name(backend):
    name = backend.__class__.__name__
    name = name.replace('OAuth', ' OAuth')
    name = name.replace('OpenId', ' OpenId')
    name = name.replace('Sandbox', '')
    name = name_re.sub(r'\1 Auth', name)
    return name


@register.filter
def backend_class(backend):
    return backend.name.replace('-', ' ')

@register.filter
def order_backends(backends):
    order = {
        'wykop': 0,
        'facebook': 1,
        'github': 2,
        'twitter': 3,
        'google-oauth2': 4,
    }
    backends = list(backends)
    backends.sort(key=lambda backend: order[backend[0]])
    return backends

@register.filter
def icon_name(name):
    return {
        'google-oauth': 'google',
        'google-oauth2': 'google',
        'facebook-app': 'facebook',
    }.get(name, name)


@register.filter
def social_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if name not in ['username', 'email']]
    backends.sort(key=lambda b: b[0])
    return [backends[n:n + 10] for n in range(0, len(backends), 10)]


@register.filter
def legacy_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if name in ['username', 'email']]
    backends.sort(key=lambda b: b[0])
    return backends


@register.filter
def oauth_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if issubclass(backend, OAuthAuth)]
    backends.sort(key=lambda b: b[0])
    return backends


@register.simple_tag(takes_context=True)
def associated(context, backend):
    user = context.get('user')
    context['association'] = None
    if user and user.is_authenticated():
        context['association'] = Storage.user.get_social_auth_for_user(
            user,
            backend.name
        ).first()
    return ''
