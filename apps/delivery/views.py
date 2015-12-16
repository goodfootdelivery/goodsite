from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect as redirect
from django.http import HttpResponse as say
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .forms import AddressForm, OrderForm, ServiceForm
from .delivery import Mapper


# Views for Delivery App

start = 'pickup'
end = 'dropoff'
details = 'details'

PRICES = [1.50, 2.34, 7.54]


@login_required
def placeorder(request):
    form1 = AddressForm(request.POST or None, auto_id='%s', prefix=start)
    form2 = AddressForm(request.POST or None, auto_id='%s', prefix=end)
    form3 = OrderForm(request.POST or None, prefix=details)

    if request.method == 'POST':
        if form1.is_valid() & form2.is_valid() & form3.is_valid():
            orig = form1.cleaned_data
            dest = form2.cleaned_data

            # Add exception handling Here
            trip = Mapper(orig['address'], dest['address'])
            # and Rerender this template

            ordd = form3.cleaned_data

            request.session['trip'] = trip
            request.session['form1'] = orig
            request.session['form2'] = dest
            request.session['form3'] = ordd

            return redirect(reverse('delivery:confirmorder'))

    context = {'form1': form1, 'form2': form2, 'form3': form3}
    return render(request, 'delivery/placeorder.html', context)


def confirmorder(request):
    form = ServiceForm(request.POST or None)
    trip = request.session['trip']
    # Calculate Price Vector
    vect = trip.prices(PRICES)
    price_choices = zip(form['service'], vect)

    context = {'form': form}
    context.update({'trip': trip})
    context.update({'prices': price_choices})

    if request.method == 'POST':
        if form.is_valid():
            request.session['form4'] = form
            return redirect(reverse('delivery:success'))

    return render(request, 'delivery/confirmorder.html', context)


def success(request):
    return render(request, 'delivery/success.html')
