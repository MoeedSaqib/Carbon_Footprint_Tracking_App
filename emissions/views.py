# emissions/views.py
# emissions/views.py

from django.shortcuts import render , redirect 
from django.contrib.auth.decorators import login_required
from .models import Action
from .forms import RegisterForm
from django.http import JsonResponse
from django.db.models import Sum
import requests
from .models import EmissionLog

@login_required
def dashboard(request):
    actions = Action.objects.filter(user=request.user)
    total_saved = sum(action.co2_saved_kg for action in actions)
    return render(request, 'dashboard.html', {
        'total_saved': total_saved
    })
def register(request):
    return render(request, 'registration/register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login  # Import login if you want auto-login
from .forms import RegisterForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import EmissionLog, TreePlanting  # add TreePlanting here
from .models import EmissionLog, TreePlanting, Mission


@never_cache
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            print(form.errors)  # <-- Add this to print form errors
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import TreePlanting, Mission

@login_required
@csrf_exempt
def log_eco_action(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = data.get('category')
            user = request.user

            if category == 'tree':
                number_of_trees = int(data.get('number_of_trees', 0))
                TreePlanting.objects.create(user=user, number_of_trees=number_of_trees)
                return JsonResponse({'status': 'success'})
            elif category == 'solar':
                system_size = float(data.get('system_size_kw', 0))
                days_active = int(data.get('days_active', 0))
                Mission.objects.create(user=user, name='Solar Energy System', status='active')
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'error': 'Unknown category'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

# Emission Factors (example values, adjust as per your data)
EMISSIONS_FACTORS = {
    'car': 0.25,  # g CO2 per km for gasoline cars
    'plane': 0.15,  # g CO2 per mile for flights
    'methane': 0.5,  # methane emissions factor for landfill (kg CO2 per kg of waste)
    'electricity': 0.2,  # g CO2 per kWh
    'tree_sequestration': 22,  # kg CO2 sequestered per tree per year
}
# Function to calculate emissions for traveling
def calculate_travel_emissions(distance, travel_type='car'):
    if travel_type == 'car':
        return distance * EMISSIONS_FACTORS['car']
    elif travel_type == 'plane':
        return distance * EMISSIONS_FACTORS['plane']
    else:
        return 0

# Function to calculate emissions from waste management
def calculate_waste_emissions(waste_amount, waste_type='landfill'):
    if waste_type == 'landfill':
        return waste_amount * EMISSIONS_FACTORS['methane']
    else:
        return 0  # You could add more waste types like recycling if needed

# Function to calculate carbon sequestration through eco projects (e.g., trees planted)
def calculate_eco_project_emissions(trees_planted):
    return trees_planted * EMISSIONS_FACTORS['tree_sequestration']

# Function to calculate saved energy emissions
def calculate_saved_energy_emissions(energy_saved_kWh):
    return energy_saved_kWh * EMISSIONS_FACTORS['electricity']

def calculate_saved_light_emissions(wattage, duration):
    # Energy saved in kWh
    energy_saved_kWh = (wattage * duration) / 1000
    # Calculate CO2 saved (use a fixed conversion factor for average electricity CO2 intensity)
    return energy_saved_kWh * EMISSIONS_FACTORS['electricity']

def calculate_saved_ac_emissions(ac_type, temperature_change, duration):
    # Assumed energy saving percentage per degree (you can refine based on actual data)
    energy_saving_percentage_per_degree = 0.03
    
    # Energy savings based on temperature change
    energy_saved_percentage = temperature_change * energy_saving_percentage_per_degree
    
    # Calculate energy saved in kWh based on duration and assumed AC power usage (e.g., 1000W per hour)
    energy_saved_kWh = 1 * (1 - energy_saved_percentage) * duration  # Assuming 1 kW for AC power usage
    return energy_saved_kWh * EMISSIONS_FACTORS['electricity']

def calculate_saved_fan_emissions(fan_type, duration):
    # Assuming an energy saving of 30% for DC inverter fans
    fan_power_usage = 0.06  # kWh per hour for a regular fan (estimate)
    
    if fan_type == 'dc_inverter':
        fan_power_usage *= 0.7  # Save 30% energy with DC inverter fans
    
    # Calculate energy saved in kWh
    energy_saved_kWh = fan_power_usage * duration
    return energy_saved_kWh * EMISSIONS_FACTORS['electricity']



# View to handle emissions calculation
def calculate_emissions(request):
    if request.method == 'POST':
        try:
            # Get data from the form (or from API, depending on how you send it)
            distance = float(request.POST.get('distance', 0))
            travel_type = request.POST.get('travel_type', 'car')
            waste_amount = float(request.POST.get('waste_amount', 0))
            energy_saved_kWh = float(request.POST.get('energy_saved_kWh', 0))
            trees_planted = int(request.POST.get('trees_planted', 0))

            # Calculate emissions for each category
            travel_emissions = calculate_travel_emissions(distance, travel_type)
            waste_emissions = calculate_waste_emissions(waste_amount)
            energy_saved_emissions = calculate_saved_energy_emissions(energy_saved_kWh)
            eco_project_emissions = calculate_eco_project_emissions(trees_planted)

            # Total Emissions
            total_emissions = travel_emissions + waste_emissions + energy_saved_emissions - eco_project_emissions

            # Return the results as JSON
            return JsonResponse({
                'travel_emissions': travel_emissions,
                'waste_emissions': waste_emissions,
                'energy_saved_emissions': energy_saved_emissions,
                'eco_project_emissions': eco_project_emissions,
                'total_emissions': total_emissions
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # If GET request, just show the form
   
    return render(request, 'calculation_form.html')  # Render the form if GET request


# In your log_action view or any related view:
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render
from .models import EmissionLog

@login_required
def terminal(request):
    user = request.user
    trees_planted = TreePlanting.objects.filter(user=user).aggregate(total=Sum('number_of_trees'))['total'] or 0
    green_missions_active = Mission.objects.filter(user=user, status='active').count()

    # Existing emissions sums
    travel_data = EmissionLog.objects.filter(category='travel', user=user).aggregate(total_saved=models.Sum('saved'))
    energy_data = EmissionLog.objects.filter(category='energy', user=user).aggregate(total_saved=models.Sum('saved'))
    food_data = EmissionLog.objects.filter(category='food', user=user).aggregate(total_saved=models.Sum('saved'))
    waste_data = EmissionLog.objects.filter(category='waste', user=user).aggregate(total_saved=models.Sum('saved'))

    # Example: Get number of trees planted by user (replace with your actual model/field)
    trees_planted = TreePlanting.objects.filter(user=user).count()

    # Example: Get number of active green missions for user
    green_missions_active = Mission.objects.filter(user=user, status='active').count()

    data = {
        'travel': travel_data['total_saved'] or 0,
        'energy': energy_data['total_saved'] or 0,
        'food': food_data['total_saved'] or 0,
        'waste': waste_data['total_saved'] or 0,
        'total': (travel_data['total_saved'] or 0) + (energy_data['total_saved'] or 0) +
                 (food_data['total_saved'] or 0) + (waste_data['total_saved'] or 0),
        'username': user.username,
        'trees_planted': trees_planted,
        'green_missions_active': green_missions_active,
    }

    return render(request, 'terminal.html', {'data': data})

    
from django.shortcuts import render
from django.contrib import messages
from django.db import models
from .models import EmissionLog

def log_action(request):
    # Initialize variables to hold the data to pass to the terminal page
    travel_saved = 0
    energy_saved = 0
    food_saved = 0
    waste_saved = 0

    if request.method == 'POST':
        category = request.POST.get('category')
        
        # Get the 'distance' from the form data and check if it exists
        distance = request.POST.get('distance')
        if distance is not None:
            amount = float(distance)  # convert to float if valid
        else:
            amount = 0  # Set default value or handle the error
            
        emitted = 0
        saved = 0

        # Emission factors for travel modes (updated)
        CARBON_FACTORS = { 
            'car': 0.192,  # kg CO2 per km (Gasoline car)
            'bus': 0.105,  # kg CO2 per km (Diesel bus)
            'train': 0.041,  # kg CO2 per km
            'electric_car': 0.060,  # kg CO2 per km (depends on electricity source)
            'bicycle': 0,  # 0 CO2 per km (Zero emission)
            'flight': 0.15 * 1.60934,  # kg CO2 per km (converted from per mile)
            'ebike': 0.020,  # kg CO2 per km (Electric bicycle)
            'motorbike': 0.085  # kg CO2 per km (Petrol-powered motorbike)
        }

        if category == 'travel':
            used = request.POST.get('modeUsed')        # Transport mode used
            baseline = request.POST.get('modeReplaced')  # Transport mode replaced (baseline)

            # Calculate emissions for used mode and baseline mode
            used_emission = CARBON_FACTORS.get(used, 0) * amount
            base_emission = CARBON_FACTORS.get(baseline, 0) * amount
            emitted = used_emission
            saved = base_emission - used_emission

            if saved > 0:
                # Success: Emissions saved
                messages.success(request, f"Great job! You saved {saved:.2f} kg of CO₂ by using {used} instead of {baseline}.")
            else:
                # Warning: Action increased emissions
                messages.error(request, f"This action is not sustainable. Rather than saving emissions, it increases them by {abs(saved):.2f} kg CO₂. It can't be logged as a climate action.")

            # Save the log entry
  # Save log with user
        EmissionLog.objects.create(
            user=request.user,   # Add user here
            category=category,
            amount=amount,
            emitted=emitted,
            saved=saved
        )

            # Fetching total saved emissions from all categories to pass to the terminal page
        travel_data = EmissionLog.objects.filter(category='travel').aggregate(total_saved=models.Sum('saved'))
        energy_data = EmissionLog.objects.filter(category='energy').aggregate(total_saved=models.Sum('saved'))
        food_data = EmissionLog.objects.filter(category='food').aggregate(total_saved=models.Sum('saved'))
        waste_data = EmissionLog.objects.filter(category='waste').aggregate(total_saved=models.Sum('saved'))

        # Calculate the total saved emissions across categories
        total_saved = (travel_data['total_saved'] or 0) + (energy_data['total_saved'] or 0) + \
                      (food_data['total_saved'] or 0) + (waste_data['total_saved'] or 0)

        # Prepare the data to pass to the template (this will be used for displaying the graphs)
        data = {
            'travel': travel_data['total_saved'] or 0,
            'energy': energy_data['total_saved'] or 0,
            'food': food_data['total_saved'] or 0,
            'waste': waste_data['total_saved'] or 0,
            'total': total_saved
        }

        # Render the same page with the message and the data (stay on log_action page)
        return render(request, 'calculation_form.html', {'data': data})

    # If the request is GET, render the form (no data to display)
    return render(request, 'calculation_form.html')

def blog(request):
    news_url = 'https://newsapi.org/v2/everything'
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'

    # 🔐 Use your real keys
    news_params = {
        'q': 'climate change environment',
        'language': 'en',
        'apiKey': '0ff7d43500a74d898c1c78e3ffe25f69'
    }

    weather_params = {
        'q': 'Lahore',
        'appid': '3c50a02efc74a53ded676fffd96e8e6a',
        'units': 'metric'
    }

    news_data = requests.get(news_url, params=news_params).json()
    weather_data = requests.get(weather_url, params=weather_params).json()

    articles = news_data.get('articles', [])[:5]
    temperature = weather_data.get('main', {}).get('temp')
    humidity = weather_data.get('main', {}).get('humidity')
    aqi = 50 + (hash(request.user.username) % 100)  # Simulated AQI

    return render(request, 'blog.html', {
        'articles': articles,
        'temp': temperature,
        'humidity': humidity,
        'aqi': aqi
    })

def eco_page(request):
    return render(request, 'eco.html')
def csr_page(request):
    return render(request, 'csr_page.html')