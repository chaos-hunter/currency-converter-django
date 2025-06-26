from django.shortcuts import render
import requests
import os
# Import your mappings
from .currency_data import country_to_currency, country_aliases

API_URL = 'https://v6.exchangerate-api.com/v6/d1d01af0db77065d19d8543a/latest/'

def get_rates(base_code):
    resp = requests.get(f"{API_URL}{base_code}")
    data = resp.json()
    return data.get('conversion_rates', {})


def index(request):
    # Generate list of currency codes
    codes = sorted(set(country_to_currency.values()))
    result = None

    # Preserve user selection/defaults
    selected_base = request.POST.get('from_currency', codes[0] if codes else '')
    selected_target = request.POST.get('to_currency', codes[1] if len(codes) > 1 else codes[0] if codes else '')
    amount = request.POST.get('amount', '1')

    if request.method == 'POST':
        try:
            amt_float = float(amount)
        except ValueError:
            result = 'Invalid amount.'
        else:
            rates = get_rates(selected_base)
            rate = rates.get(selected_target)
            if rate is not None:
                result = f"{amt_float:.2f} {selected_base} = {amt_float*rate:.2f} {selected_target}"
            else:
                result = 'Conversion error.'

    return render(request, 'converter/index.html', {
        'codes': codes,
        'result': result,
        'selected_base': selected_base,
        'selected_target': selected_target,
        'amount': amount,
    })
