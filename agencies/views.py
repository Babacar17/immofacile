from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

def agency_list(request):
    agencies = User.objects.filter(role='agency', is_verified=True)
    return render(request, 'agencies/list.html', {'agencies': agencies})

def agency_detail(request, pk):
    agency   = get_object_or_404(User, pk=pk, role='agency')
    listings = agency.listings.filter(status='active')
    reviews  = agency.reviews.all()
    return render(request, 'agencies/detail.html', {
        'agency': agency, 'listings': listings, 'reviews': reviews,
    })
