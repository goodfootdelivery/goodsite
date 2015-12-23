from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect as redirect
from django.http import HttpResponse as say
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .forms import AddressForm, OrderForm, ServiceForm
from .models import Order


# Views for Delivery App

start = 'pickup'
end = 'dropoff'
details = 'details'


@login_required
def placeorder(request):
    form1 = AddressForm(request.POST or None, auto_id='%s', prefix=start)
    form2 = AddressForm(request.POST or None, auto_id='%s', prefix=end)
    form3 = OrderForm(request.POST or None, prefix=details)

    if request.method == 'POST':
        if form1.is_valid() & form2.is_valid() & form3.is_valid():
            origin = form1.save(commit=False)
            destin = form2.save(commit=False)
            ordd = form3.cleaned_data

            order = Order(pickup=origin, dropoff=destin)
            order.delivery_date = ordd['delivery_date']
            order.envelopes = ordd['envelopes']
            order.boxes = ordd['boxes']
            order.rolls = ordd['rolls']

            order.set_dist_mat()

            # Add exception handling Here
            # and Rerender this template

            request.session['orig'] = origin
            request.session['dest'] = destin
            request.session['order'] = order

            return redirect(reverse('delivery:confirmorder'))

    context = {'form1': form1, 'form2': form2, 'form3': form3}
    return render(request, 'delivery/placeorder.html', context)


def confirmorder(request):
    form = ServiceForm(request.POST or None)
    order = request.session['order']
    price_choices = zip(form['service'], order.get_prices)

    context = {'form': form}
    context.update({'prices': price_choices,
                    'order': order,
                    'orig': request.session['orig'],
                    'dest': request.session['dest'],
                    })

    if request.method == 'POST':
        if form.is_valid():
            ordd = form.cleaned_data
            orig = request.session['orig']
            dest = request.session['dest']
            order = request.session['order']

            orig.user = User.objects.get(username=request.user)
            dest.user = User.objects.get(username=request.user)
            order.user = User.objects.get(username=request.user)
            orig.save()
            dest.save()

            order.service = ordd['service']
            order.save()

            return redirect(reverse('delivery:success'))

    return render(request, 'delivery/confirmorder.html', context)


def success(request):
    return render(request, 'delivery/success.html')
