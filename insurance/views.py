from django.shortcuts import render, get_object_or_404, redirect
from .models import Insurance
from django.core.paginator import EmptyPage, Page,Paginator
from django import forms
from datetime import datetime
# Create your views here.

def index(request):
    """
    Show listings of the insurances
    """
    listings = Insurance.objects.order_by('-purchase_date')
    if request.method == "POST":
        policy_id = request.POST['policy_id']
        customer_id = request.POST['customer_id']
        if policy_id:
            listings = listings.filter(policy_id=policy_id)
        if customer_id:
            listings = listings.filter(customer_id=customer_id)
    # Use paginator
    paginator = Paginator(listings, 20)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(request, 'insurance/listings.html', context)

def edit_insurance(request, insurance_id, errorMessage=None):
    """
    Get listing to edit with insurance id
    """
    listing = get_object_or_404(Insurance, policy_id=insurance_id)

    context = {
        'listing': listing,
        'errorMessage': errorMessage
    }
    return render(request, 'insurance/listing.html', context)

def edit_action(request):
    """
    edit insurance
    """
    if request.method == "POST":
        policy_id = request.POST['policy_id']
        customer_id = request.POST['customer_id']
        fuel = request.POST['fuel']
        vehicle_segment = request.POST['vehicle_segment']
        premium_amount = request.POST['premium_amount']
        bodily_injury_liability = True if 'bodily_injury_liability' in request.POST else False
        personal_injury_protection = True if 'personal_injury_protection' in request.POST else False
        property_damage_liability = True if 'property_damage_liability' in request.POST else False
        collision = True if 'collision' in request.POST else False
        comprehensive = True if 'comprehensive' in request.POST else False
        customer_gender = True if request.POST['customer_gender'] == "1" else False
        income_group = request.POST['income_group']
        customer_region = request.POST['customer_region']
        maritial_status = True if 'maritial_status' in request.POST else False
        insurance = get_object_or_404(Insurance, policy_id=policy_id)
        # If premium amount is greater than 1 million do not allow
        if (int(premium_amount) > 1000000):
            return redirect("edit_insurance", policy_id, "Policy amount greater than 1 million.")
        # save updated insurance object
        if insurance:
            insurance.customer_id = customer_id
            insurance.fuel = fuel
            insurance.vehicle_segment = vehicle_segment
            insurance.premium_amount = premium_amount
            insurance.bodily_injury_liability = bodily_injury_liability
            insurance.personal_injury_protection = personal_injury_protection
            insurance.property_damage_liability = property_damage_liability
            insurance.collision = collision
            insurance.comprehensive = comprehensive
            insurance.customer_gender = customer_gender
            insurance.income_group = income_group
            insurance.customer_region = customer_region
            insurance.maritial_status = maritial_status
            insurance.save()
        else:
            return HttpResponseForbidden()
    return redirect("/")

def charts(request):
    """
    Show chart data with user data
    """
    data = Insurance.objects.order_by('-purchase_date')
    dataDict = {}
    for course in data:
        if course.purchase_date.strftime("%m%Y") in dataDict:
            dataDict[course.purchase_date.strftime("%m%Y")].append(course.policy_id)
        else:
            dataDict[course.purchase_date.strftime("%m%Y")] = [course.policy_id]
    xData = []
    yData = []
    for key,value in dataDict.items():
        xData.append(key)
        yData.append(str(len(value)))

    context = {
        'xData': ",".join(xData),
        'yData': ",".join(yData)
    }
    return render(request, 'insurance/chart.html', context)