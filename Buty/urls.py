from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from Buty import settings
from girls.views import (
    HomePage,
    ModelDetail
)
from products.views import (
    CreateCheckoutSessionView,
    ProductLandingPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home-page'),
    path('model-detail/<girl_id>/', ModelDetail.as_view(), name='model-detail'),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('landing-page/<girl_id>/<product_id>/', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/<pk>/<girl_id>', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
