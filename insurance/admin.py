from django.contrib import admin
from .models import Insurance
from django.urls import path
from django import forms
from django.shortcuts import render, redirect
import csv
import pandas as pd
import datetime

# Register your models here.
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class InsuranceAdmin(admin.ModelAdmin):
    """
    Insurance admin
    """
    list_per_page = 25
    change_list_template = "entities/insurance_changelist.html"

    def get_urls(self):
        """
        Override function to add custom url
        """
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def _get_date_time_formatted(self, given_date):
        """
            Function to get formatted date
        """
        if '/' in given_date:
            format_str = '%m/%d/%Y'
        else:
            format_str = '%m-%d-%Y'
        return datetime.datetime.strptime(given_date, format_str)

    def _get_gender_Bool(self, gender_string):
        """
           Function to get gender
        """
        if gender_string == "Male":
            return False
        else:
            return True
    """
    Function to import csv
    """
    def import_csv(self, request):
        """
           Request as param
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            df = pd.read_csv(csv_file)
            row_iter = df.iterrows()
            # Using pandas data frames to import csv
            insurances = [
                Insurance(
                    policy_id=row['Policy_id'],
                    purchase_date=self._get_date_time_formatted(row['Date of Purchase']),
                    customer_id=row['Customer_id'],
                    fuel=row['Fuel'],
                    vehicle_segment=row['VEHICLE_SEGMENT'],
                    premium_amount=row['Premium'],
                    bodily_injury_liability=row['bodily injury liability'],
                    personal_injury_protection=row['personal injury protection'],
                    property_damage_liability=row['property damage liability'],
                    collision=row['collision'],
                    comprehensive=row['comprehensive'],
                    customer_gender=self._get_gender_Bool(row['Customer_Gender']),
                    income_group=row['Customer_Income group'],
                    customer_region=row['Customer_Region'],
                    maritial_status=row['Customer_Marital_status'],
                )
                for index, row in row_iter
            ]
            Insurance.objects.bulk_create(insurances)
            self.message_user(request, "Your csv file has been imported")
            return redirect("admin/")
        # Send form in get request
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )
admin.site.register(Insurance, InsuranceAdmin)