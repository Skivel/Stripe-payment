from .models import Models
from products.models import Product
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        models = Models.objects.all()
        context = super(HomePage, self).get_context_data(**kwargs)
        context.update({
            'title': 'Home Page',
            'models': models
        })
        return context


class ModelDetail(TemplateView):
    template_name = 'model-detail.html'

    def get_context_data(self, **kwargs):
        model_id = self.kwargs["girl_id"]
        models = Models.objects.get(id=model_id)
        products = Product.objects.all()
        context = super(ModelDetail, self).get_context_data(**kwargs)
        context.update({
            'title': f'{models.name}',
            'models': models,
            'products': products
        })
        return context
