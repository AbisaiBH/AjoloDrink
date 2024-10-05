from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cocktail
from datetime import datetime
import ephem
import json
import uuid

def Stations(tdy):
    year = tdy.year
    date = ephem.Date(tdy)
    seasons = {
        'Winter': ephem.Date(f'{year}-12-21'),
        'Spring': ephem.Date(f'{year}-03-20'),
        'Summer': ephem.Date(f'{year}-06-21'),
        'Fall': ephem.Date(f'{year}-09-23')
    }
    for season, start_date in sorted(seasons.items(), key=lambda x: x[1]):
        if date < start_date:
            break
        s = season
    season = Cocktail.get_season_value(s)
    return season

##########
#########
########
######
#####
#### Modelos de prueba de software
##

# Pruebas Unitarias 

class CocktailViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cocktail = Cocktail.objects.create(
            uid=uuid.uuid4(),
            image='http://example.com/mojito.png',
            name='Mojito',
            description={"en": "Refreshing mint cocktail."},
            season=2,  
            alcohol_lvl=2, 
            tags=["Mint", "Rum"],
            liquor='Rum'
        )
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_stations(self):
        date = datetime(2024, 6, 22)
        season = Stations(date)
        self.assertEqual(season, 2)

    def test_season_cocktail_get(self):
        response = self.client.get(reverse('Season_cocktail'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('pages', data)
        self.assertIn('current_page', data)
        self.assertIn('data', data)

    def test_all_cocktail_get(self):
        response = self.client.get(reverse('All_cocktail'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('pages', data)
        self.assertIn('current_page', data)
        self.assertIn('data', data)
        self.assertGreater(len(data['data']), 0)

    def test_create_account_post(self):
        response = self.client.post(reverse('Create_account'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_account_missing_username(self):
        response = self.client.post(reverse('Create_account'), {
            'email': 'new@example.com',
            'password': 'newpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Missing username')

    def test_login_post(self):
        response = self.client.post(reverse('Login'), {
            'username': 'testuser',
            'password': 'password'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401) 

    def test_login_missing_username(self):
        response = self.client.post(reverse('Login'), {
            'password': 'password'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Missing username')

    def test_logout_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('LogOut'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Logout successful')

    def test_logout_not_logged_in(self):
        response = self.client.get(reverse('LogOut'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'No user is currently logged in')

# Pruebas de Integración 

class CocktailViewsTestIntegration(TestCase):
    def setUp(self):
        self.client = Client()
        self.cocktail = Cocktail.objects.create(
            uid=1,
            image='test_image.png',
            name='Test Cocktail',
            description={"en": "Refreshing mint cocktail."},
            season=2,  
            alcohol_lvl=2, 
            tags=["Mint", "Rum"],
            liquor='Rum'
        )
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_season_cocktail(self):
        response = self.client.get(reverse('Season_cocktail'), {'page': 1})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        # self.assertGreater(len(data['data']), 0)


    def test_all_cocktail(self):
        response = self.client.get(reverse('All_cocktail'), {'page': 1})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('data', data)
        self.assertGreater(len(data['data']), 0)

    def test_create_account(self):
        response = self.client.post(reverse('Create_account'), data=json.dumps({
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '"User Created"')
        
        response = self.client.post(reverse('Create_account'), data=json.dumps({
            'username': self.username,
            'email': 'anotheruser@example.com',
            'password': 'anotherpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = self.client.post(reverse('Login'), data=json.dumps({
            'username': self.username,
            'password': "testpass"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid credentials", str(response.content))

        response = self.client.post(reverse('Login'), data=json.dumps({
            'username': self.username,
            'password': self.password
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn("Login successful", str(response.content))

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('LogOut'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logout successful"})

        self.client.logout()
        response = self.client.get(reverse('LogOut'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "No user is currently logged in"})

###### Pruebas dinamica ***

###### Pruebas estaticas ***

###### Caja Negra

###### Caja Blanca

###### Caja Gris




