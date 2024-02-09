from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserDataForm
from .models import Person, CalculatedData


# Helper functions (utils)
def select_required_fields(calculator, form):
    if calculator == 'bmi_calculator':
        form.fields['height'].required = True
        form.fields['weight'].required = True
        form.fields['gender'].required = True
    elif calculator in ['bmr_calculator', 'tmr_calculator']:
        form.fields['age'].required = True
        form.fields['gender'].required = True
        form.fields['height'].required = True
        form.fields['weight'].required = True
        if calculator == 'tmr_calculator':
            form.fields['pal'].required = True


def checking_bmi_category(bmi):

    bmi_categories = {
        'severe thinnes': 'Your weight is too low and your life may be at risk. Try to gain weight but if you may have problems with an eating disorder, please contant an experienced specialist.',
        'underweight': 'Your weight is too low. You may be suffering from deficiency of multiple nutrient elements. Try to gain weight or meet with a dietitian to receive a specific menu included your calorie needs.',
        'normal weight': 'Your weight is perfect! Congratulations and keep going. Still try to eat healthy and exercise at least three times a week for maintaining your weight and good health.',
        'overweight': 'Your weight is slightly too high and indicates a risk of obese. For improving your body appearance and health you should lose a few kilograms by changing a diet and trying to exercises more than before. Simple things can make a huge difference.',
        'obese': 'You have first degree obesity. It is a diseases that should be treated. At first you can try to do it on your own by changing diet, eating less calories and exercising more but if you notices that your efforts do not yield expected results, contact with an experienced specialist like a dietitian or personal trainer.',
        'severely obese': 'You have second degree obesity. It is a serious danger for your health. Start treating as soon as it is possible. Contact with a dietitian who has an experience in working with patients with obese and changed your whole lifestyle.',
        'morbidly obese': 'You have third degree obesity. This is a really danger diseases that threatens your health and even your life. You should meet an experienced specialist immediately. Sometimes in the treatment it becomes necessary to involve psychologists, especially eating disorder therapists.'
    }

    if bmi < 16:
        category = 'severe thinnes'
    elif bmi < 18.5:
        category = 'underweight'
    elif 18.5 <= bmi < 25:
        category = 'normal weight'
    elif 25 <= bmi < 30:
        category = 'overweight'
    elif 30 <= bmi < 35:
        category = 'obese'
    elif 35 <= bmi < 40:
        category = 'severely obese'
    else:
        category = 'morbidly obese'

    return {
        'calculated_bmi': bmi,
        'category': category,
        'description': bmi_categories[category]
    }


def calculate_bmi_save_data(request, form):
    height = form.cleaned_data['height']
    weight = form.cleaned_data['weight']
    gender = form.cleaned_data['gender']
    calculated_bmi = round(weight / (height * 0.01) ** 2, 2)

    if request.user.is_authenticated:
        person_instance, created = Person.objects.get_or_create(user=request.user)
        calculated_data_instance, created = CalculatedData.objects.get_or_create(
            user=request.user)

        person_instance.update_or_create_data({
            'weight': weight,
            'height': height,
            'gender': gender
        })
        calculated_data_instance.update_or_create_data({
            'bmi': calculated_bmi,
            'bmi_category': checking_bmi_category(calculated_bmi)['category']
        })

    return calculated_bmi


def calculate_bmr_save_data(request, form):
    age = form.cleaned_data['age']
    gender = form.cleaned_data['gender']
    height = form.cleaned_data['height']
    weight = form.cleaned_data['weight']

    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    if request.user.is_authenticated:
        person_instance, created = Person.objects.get_or_create(user=request.user)
        calculated_data_instance, created = CalculatedData.objects.get_or_create(
            user=request.user)

        person_instance.update_or_create_data({
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight
        })
        calculated_data_instance.update_or_create_data({
            'bmr': bmr
        })

    return bmr


def calculate_tmr_save_data(request, form):
    age = form.cleaned_data['age']
    gender = form.cleaned_data['gender']
    height = form.cleaned_data['height']
    weight = form.cleaned_data['weight']
    pal = float(form.cleaned_data['pal'])

    if gender == 'male':
        tmr = round(((10 * weight) + (6.25 * height) - (5 * age) + 5) * pal, 2)
    else:
        tmr = round(((10 * weight) + (6.25 * height) -
                    (5 * age) - 161) * pal, 2)

    return tmr


def add_success_message(request):
    messages.success(
        request, '<strong>Your data has been successfully saved.</strong> You will be able to use them later to refill if you want to!')


# Main views
def home(request):
    return redirect('bmi')


def bmi_calculator(request):
    form = UserDataForm(request.POST or None)
    select_required_fields('bmi_calculator', form=form)

    if request.user.is_authenticated:
        try:
            calculated_data = CalculatedData.objects.get(user=request.user)
            last_bmi = calculated_data.bmi if calculated_data.bmi != 0 else "Sorry you don't have any saved data."
        except CalculatedData.DoesNotExist:
            last_bmi = "Sorry you don't have any saved data."
    else:
        last_bmi = "Sorry you don't have any saved data."

    if request.method == 'POST' and form.is_valid():
        calculated_bmi = calculate_bmi_save_data(request, form)
        return render(request, 'calculator/bmiresult.html', checking_bmi_category(calculated_bmi))

    return render(request, 'calculator/bmi.html', {'form': form, 'last_bmi': last_bmi})


@login_required
def bmi_calculator_filled_out(request):
    try:
        person = Person.objects.get(user=request.user)
        initial_data = {
            'height': person.height,
            'weight': person.weight,
            'gender': person.gender
        }
    except Person.DoesNotExist:
        return redirect('bmi')

    form = UserDataForm(request.POST or None, initial=initial_data)
    select_required_fields('bmi_calculator', form=form)

    if request.method == 'POST' and form.is_valid():
        add_success_message(request)
        calculated_bmi = calculate_bmi_save_data(request, form)
        return render(request, 'calculator/bmiresult.html', checking_bmi_category(calculated_bmi))
    return render(request, 'calculator/bmi.html', {'form': form})


def bmr_calculator(request):
    form = UserDataForm(request.POST or None)
    select_required_fields('bmr_calculator', form=form)

    if request.user.is_authenticated:
        try:
            calculated_data = CalculatedData.objects.get(user=request.user)
            last_bmr = calculated_data.bmr if calculated_data.bmr != 0 else "Sorry you don't have any saved data."
        except CalculatedData.DoesNotExist:
            last_bmr = "Sorry you don't have any saved data."
    else:
        last_bmr = "Sorry you don't have any saved data."

    if request.method == 'POST' and form.is_valid():
        bmr = calculate_bmr_save_data(request, form)
        return render(request, 'calculator/bmrresult.html', {'bmr': bmr})

    return render(request, 'calculator/bmr.html', {'form': form, 'last_bmr': last_bmr})


@login_required
def bmr_calculator_filled_out(request):
    try:
        person = Person.objects.get(user=request.user)
        initial_data = {
            'age': person.age,
            'gender': person.gender,
            'height': person.height,
            'weight': person.weight
        }
    except Person.DoesNotExist:
        return redirect('bmr')

    form = UserDataForm(request.POST or None, initial=initial_data)
    select_required_fields('bmr_calculator', form=form)

    if request.method == 'POST' and form.is_valid():
        add_success_message(request)
        bmr = calculate_bmr_save_data(request, form)
        return render(request, 'calculator/bmrresult.html', {'bmr': bmr})
    return render(request, 'calculator/bmr.html', {'form': form})


def pal_calculator(request):
    return render(request, 'calculator/pal.html')


def tmr_calculator(request):
    form = UserDataForm(request.POST or None)
    select_required_fields('tmr_calculator', form=form)

    if request.user.is_authenticated:
        try:
            calculated_data = CalculatedData.objects.get(user=request.user)
            last_tmr = calculated_data.tmr if calculated_data.tmr != 0 else "Sorry you don't have any saved data."
        except CalculatedData.DoesNotExist:
            last_tmr = "Sorry you don't have any saved data."
    else:
        last_tmr = "Sorry you don't have any saved data."

    if request.method == 'POST' and form.is_valid():
        tmr = calculate_tmr_save_data(request, form)
        return render(request, 'calculator/tmrresult.html', {'tmr': tmr})

    return render(request, 'calculator/tmr.html', {'form': form, 'last_tmr': last_tmr})


@login_required
def tmr_calculator_filled_out(request):
    try:
        person = Person.objects.get(user=request.user)
        calculated_data = CalculatedData.objects.get(user=request.user)
        initial_data = {
            'age': person.age,
            'gender': person.gender,
            'weight': person.weight,
            'height': person.height,
            'pal': calculated_data.pal
        }
    except Person.DoesNotExist or CalculatedData.DoesNotExist:
        return redirect('tmr')

    form = UserDataForm(request.POST or None, initial=initial_data)
    select_required_fields('tmr_calculator', form=form)

    if request.method == 'POST' and form.is_valid():
        add_success_message(request)
        tmr = calculate_tmr_save_data(request, form)
        return render(request, 'calculator/tmrresult.html', {'tmr': tmr})
    return render(request, 'calculator/tmr.html', {'form': form})
