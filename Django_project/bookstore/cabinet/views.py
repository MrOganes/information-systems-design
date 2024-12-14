from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from cabinet.models import Customer
from cabinet.forms import CustomerForm

COUNT_ITEMS_ON_PAGE = 10


def home(request, page=None):
    if not page:
        page = 1

    start_index = (page - 1) * COUNT_ITEMS_ON_PAGE

    if start_index > Customer.objects.count():
        raise Http404

    end_index = start_index + COUNT_ITEMS_ON_PAGE
    customers = Customer.objects.all().order_by('id')[start_index:end_index]

    for customer in customers:
        start_index += 1
        customer.index = start_index
        customer.form = CustomerForm(instance=customer)

    prev = False if page == 1 else True
    next = False if Customer.objects.count() <= end_index else True
    next_page = page + 1 if next else 0
    prev_page = page - 1 if prev else 0

    data = {
        'prev': prev,
        'next': next,
        'next_page': next_page,
        'page': page,
        'prev_page': prev_page,
        'customers': customers,
    }

    return render(request, 'cabinet/home.html', data)


def delete(request, customer_id, page=None):
    if not page:
        page = 1

    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()

    return HttpResponseRedirect(f'/cabinet/{page}')


def update(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    data = {
        'customer_id': customer_id,
        'title': 'Изменение данных',
    }
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            message = 'Данные успешно обновлены!'
            data['message'] = message
    else:
        form = CustomerForm(instance=customer)
    data['form'] = form
    return render(request, 'cabinet/update_form.html', data)


def add(request):
    data = {
        'title': 'Добавление пользователя',
        'form': CustomerForm(),
    }

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            message = 'Данные успешно сохранены!'
            data['message'] = message
            form = CustomerForm()
    else:
        form = CustomerForm()
    data['form'] = form
    return render(request, 'cabinet/update_form.html', data)
