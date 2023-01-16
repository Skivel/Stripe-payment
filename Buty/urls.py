from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from Buty import settings
from page_not_found.views import page_not_found_view
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
    path('success/<girl_id>/<product_id>', SuccessView.as_view(), name='success'),
    path('landing-page/<girl_id>/<product_id>/', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/<pk>/<girl_id>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/icon/favicon.png')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = page_not_found_view

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
