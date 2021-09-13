from django.http import JsonResponse

import stripe

# Create your views here.
def custom_webhook():
    # Use an existing Customer ID if this is a returning customer
    customer = stripe.Customer.create()
    ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2020-08-27',
    )
    paymentIntent = stripe.PaymentIntent.create(
        amount=1099,
        currency='try',
        customer=customer['id']
    )
    return JsonResponse({"paymentIntent":paymentIntent.client_secret,
                         "ephemeralKey":ephemeralKey.secret,
                         "customer":customer.id})