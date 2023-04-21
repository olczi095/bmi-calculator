from django.shortcuts import render, redirect, HttpResponse
from .forms import UserDataForm
    
def home(request):
   return redirect('bmi')

def bmi_calculator(request):
    if request.method == 'POST':
            form = UserDataForm(request.POST)
            if form.is_valid():
                height = form.cleaned_data['height']
                weight = form.cleaned_data['weight']
                calculated_bmi = round(weight / (height * 0.01) ** 2, 2)
                return render(request, 'calculator/bmiresult.html', checking_bmi_category(calculated_bmi))
    else:
        form = UserDataForm()
        return render(request, 'calculator/bmi.html', {'form': form})
    
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
        return {'calculated_bmi': bmi, 'category': 'severe thinness', 'description': bmi_categories['severe thinnes']}
    elif bmi < 18.5:
        return {'calculated_bmi': bmi, 'category': 'underweight', 'description': bmi_categories['underweight']}
    elif 18.5 <= bmi < 25:
        return {'calculated_bmi': bmi, 'category': 'normal weight', 'description': bmi_categories['normal weight']}
    elif 25 <= bmi < 30:
        return {'calculated_bmi': bmi, 'category': 'overweight', 'description': bmi_categories['overweight']}
    elif 30 <= bmi < 35:
        return {'calculated_bmi': bmi, 'category': 'obese', 'description': bmi_categories['obese']}
    elif 35 <= bmi < 40:
        return {'calculated_bmi': bmi, 'category': 'severely obese', 'description': bmi_categories['severely obese']}
    else:
        return {'calculated_bmi': bmi, 'category': 'morbidly obese', 'description': bmi_categories['morbidly obese']}


def bmr_calculator(request):
    if request.method == "POST":
        form = UserDataForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            if gender == 'male':
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

            return render(request, 'calculator/bmrresult.html', {'bmr': bmr})
    else:
        form = UserDataForm()
        return render(request, 'calculator/bmr.html', {'form': form})
    
def pal_calculator(request):
    return render(request, 'calculator/pal.html')

def tmr_calculator(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            pal = float(form.cleaned_data['pal'])
            if gender == 'male':
                tmr = round(((10 * weight) + (6.25 * height) - (5 * age) + 5) * pal, 2)
            else:
                tmr = round(((10 * weight) + (6.25 * height) - (5 * age) - 161) * pal, 2)
            return render(request, 'calculator/tmrresult.html', {'tmr': tmr})
    else:
        form = UserDataForm()
        return render(request, 'calculator/tmr.html', {'form': form})
