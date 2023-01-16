import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View

from girls.models import Models
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        girl_id = self.kwargs["girl_id"]
        girl = Models.objects.get(id=girl_id)
        product_id = self.kwargs["product_id"]
        product = Product.objects.get(id=product_id)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            'girl': girl
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        girl_id = self.kwargs["girl_id"]
        girl = Models.objects.get(id=girl_id)
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'aed',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            'images': [f'https://static.wikia.nocookie.net/arianagrande/images/f/f1/Ariana_Grande_-_Grammys_2020_-_Red_carpet.jpg/revision/latest?cb=20210513080156&path-prefix=pl'],
                            'description': girl.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id,
                'product_name': product.name,
                'price': product.price,
                'girl_id': girl.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + f'/success/{girl.id}/{product.id}',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)

        product_id = session["metadata"]["product_id"]
        product = Product.objects.get(id=product_id)

        girl_id = session["metadata"]["girl_id"]
        girl = Models.objects.get(id=girl_id)

        girl.score = girl.score + product.vote
        girl.save()

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})