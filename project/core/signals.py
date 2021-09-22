

from django_cas_ng.signals import cas_user_authenticated, cas_user_logout
from django.conf import settings
import json
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Market

User = get_user_model()

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    args = {}
    args.update(kwargs)
    user = args.get('user')
    attributes = args.get('attributes')
    markets_owned_by = attributes.get('markets_owned_by')
    waiters_owned_by = attributes.get('waiters_owned_by')
    if type(markets_owned_by).__name__ == 'list':
        for market_url in markets_owned_by:
            market, created = Market.objects.get_or_create(url=market_url)
            user.markets_owned_by.add(market.id)
    else:
        market, created = Market.objects.get_or_create(url=markets_owned_by)
        user.markets_owned_by.add(market.id)

    if type(waiters_owned_by).__name__ == 'list':
        for waiter_url in waiters_owned_by:
            market, created = Market.objects.get_or_create(url=waiter_url)
            print(market)
            user.waiters_owned_by.add(market.id)
    else:
        market, created = Market.objects.get_or_create(url=waiters_owned_by)
        user.waiters_owned_by.add(market.id)

    print('''cas_user_authenticated_callback:
    user: %s
    created: %s
    attributes: %s
    ''' % (
        args.get('user'),
        args.get('created'),
        json.dumps(args.get('attributes'), sort_keys=True, indent=2)))


@receiver(cas_user_logout)
def cas_user_logout_callback(sender, **kwargs):
    args = {}
    args.update(kwargs)
    user = args.get('user')
    user.markets_owned_by.set([])
    user.waiters_owned_by.set([])
    user.save()
    print('''cas_user_logout_callback:
    user: %s
    session: %s
    ticket: %s
    ''' % (
        args.get('user'),
        args.get('session'),
        args.get('ticket')))

