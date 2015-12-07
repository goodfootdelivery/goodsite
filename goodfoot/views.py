from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'homepage.html'
    title = 'home'


class OrderView(TemplateView):
    template_name = 'placeorder.html'
    title = 'placeorder'
