from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'homepage.html'
    title = 'home'


class DeliveryView(TemplateView):
    template_name = 'delivery/app.html'
    title = 'delivery'
