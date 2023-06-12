from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from calculator.forms import UserDataForm
from calculator.views import checking_bmi_category, calculate_bmi_save_data, calculate_bmr_save_data, calculate_tmr_save_data

# Main views
class URLSViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_url_returns_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/bmi_calculator/')
    
    def test_bmi_url_returns_success(self):
        response = self.client.get(reverse('bmi'))
        self.assertEqual(response.status_code, 200)

    def test_bmi_url_filled_returns_redirect(self):
        response = self.client.get(reverse('bmi-filled'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/bmi_calculator/')

    def test_bmr_url_returns_success(self):
        response = self.client.get(reverse('bmr'))
        self.assertEqual(response.status_code, 200)

    def test_bmr_url_filled_returns_redirect(self):
        response = self.client.get(reverse('bmr-filled'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/bmr_calculator/')
    
    def test_pal_url_returns_success(self):
        response = self.client.get(reverse('pal'))
        self.assertEqual(response.status_code, 200)

    def test_tmr_url_returns_success(self):
        response = self.client.get(reverse('tmr'))
        self.assertEqual(response.status_code, 200)

    def test_tmr_filled_returns_redirect(self):
        response = self.client.get(reverse('tmr-filled'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/tmr_calculator/')


# Additional Functions
class AdditionalFunctionsTestCase(TestCase):
            
    bmi_categories = {
            'severe thinnes': 'Your weight is too low and your life may be at risk. Try to gain weight but if you may have problems with an eating disorder, please contant an experienced specialist.',
            'underweight': 'Your weight is too low. You may be suffering from deficiency of multiple nutrient elements. Try to gain weight or meet with a dietitian to receive a specific menu included your calorie needs.',
            'normal weight': 'Your weight is perfect! Congratulations and keep going. Still try to eat healthy and exercise at least three times a week for maintaining your weight and good health.',
            'overweight': 'Your weight is slightly too high and indicates a risk of obese. For improving your body appearance and health you should lose a few kilograms by changing a diet and trying to exercises more than before. Simple things can make a huge difference.',
            'obese': 'You have first degree obesity. It is a diseases that should be treated. At first you can try to do it on your own by changing diet, eating less calories and exercising more but if you notices that your efforts do not yield expected results, contact with an experienced specialist like a dietitian or personal trainer.',
            'severely obese': 'You have second degree obesity. It is a serious danger for your health. Start treating as soon as it is possible. Contact with a dietitian who has an experience in working with patients with obese and changed your whole lifestyle.',
            'morbidly obese': 'You have third degree obesity. This is a really danger diseases that threatens your health and even your life. You should meet an experienced specialist immediately. Sometimes in the treatment it becomes necessary to involve psychologists, especially eating disorder therapists.'
        }
    
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_checking_bmi_category_function(self):
        bmi_data = {
            14: 'severe thinnes', 
            17: 'underweight',
            20: 'normal weight',
            25: 'overweight',
            33: 'obese',
            37: 'severely obese',
            45: 'morbidly obese'
        }

        for bmi, bmi_category in bmi_data.items():
            result = {
                'calculated_bmi': bmi,
                'category': bmi_category,
                'description': self.bmi_categories[bmi_category]
            }   
            self.assertEqual(result, checking_bmi_category(bmi))

        

    def test_calculating_values(self):
        self.factory = RequestFactory()
        request = self.factory.get("/bmi_calculator/filled")
        request.user = self.user

        male_form = UserDataForm(data={'age': 40, 'weight': 100, 'height': 190, 'gender': 'male', 'pal': 1.2})
        male_form.is_valid()
        female_form = UserDataForm(data={'age': 50, 'weight': 70, 'height': 150, 'gender': 'female', 'pal': 1.8})
        female_form.is_valid()
        
        expected_values_male = {
            'expected_bmi': 27.70,
            'expected_bmr': 1992.50,
            'expected_tmr': 2391.00
        }
        expected_values_female = {
            'expected_bmi': 31.11,
            'expected_bmr': 1226.50,
            'expected_tmr': 2207.70
        }
        self.assertEqual(calculate_bmi_save_data(request, male_form), expected_values_male['expected_bmi'])
        self.assertEqual(calculate_bmr_save_data(request, male_form), expected_values_male['expected_bmr'])
        self.assertEqual(calculate_tmr_save_data(request, male_form), expected_values_male['expected_tmr'])
        self.assertEqual(calculate_bmi_save_data(request, female_form), expected_values_female['expected_bmi'])
        self.assertEqual(calculate_bmr_save_data(request, female_form), expected_values_female['expected_bmr'])
        self.assertEqual(calculate_tmr_save_data(request, female_form), expected_values_female['expected_tmr'])
