from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

DEMO = [
    {'title':'Appartement F3 meublé vue mer',     'type':'apartment','city':'Dakar','neighborhood':'Plateau',     'price':280000,'rooms':3,'surface':85,  'lat':14.6892,'lng':-17.4385,'furnished':True, 'has_wifi':True, 'has_ac':True,  'featured':True},
    {'title':'Studio moderne Mermoz',              'type':'studio',   'city':'Dakar','neighborhood':'Mermoz',      'price':95000, 'rooms':1,'surface':32,  'lat':14.7103,'lng':-17.4752,'furnished':True, 'has_wifi':True, 'has_ac':False, 'featured':False},
    {'title':'Villa F5 avec piscine Almadies',     'type':'villa',    'city':'Dakar','neighborhood':'Almadies',    'price':850000,'rooms':5,'surface':280, 'lat':14.7452,'lng':-17.5218,'has_pool':True,  'has_parking':True,             'featured':True},
    {'title':'Chambre meublée climatisée Médina',  'type':'room',     'city':'Dakar','neighborhood':'Médina',      'price':45000, 'rooms':1,'surface':18,  'lat':14.6975,'lng':-17.4520,'furnished':True, 'has_ac':True,                  'featured':False},
    {'title':'Maison F4 avec jardin Ouakam',       'type':'house',    'city':'Dakar','neighborhood':'Ouakam',      'price':380000,'rooms':4,'surface':140, 'lat':14.7289,'lng':-17.4930,'has_garden':True,'has_parking':True,             'featured':True},
    {'title':'Appartement F2 Sacré-Cœur',          'type':'apartment','city':'Dakar','neighborhood':'Sacré-Cœur',  'price':140000,'rooms':2,'surface':58,  'lat':14.7195,'lng':-17.4663,'has_wifi':True,  'has_ac':True,                  'featured':False},
    {'title':'Studio Ngor bord de mer',             'type':'studio',   'city':'Dakar','neighborhood':'Ngor',        'price':120000,'rooms':1,'surface':35,  'lat':14.7532,'lng':-17.5110,'furnished':True, 'has_wifi':True, 'has_ac':True,  'featured':False},
    {'title':'Maison F3 Point E',                   'type':'house',    'city':'Dakar','neighborhood':'Point E',     'price':320000,'rooms':3,'surface':110, 'lat':14.7042,'lng':-17.4712,'has_parking':True,'has_security':True,          'featured':False},
    {'title':'Appartement F3 Liberté 6',            'type':'apartment','city':'Dakar','neighborhood':'Liberté 6',   'price':180000,'rooms':3,'surface':75,  'lat':14.7155,'lng':-17.4590,'furnished':True, 'has_ac':True, 'has_parking':True,'featured':False},
    {'title':'Villa luxe Fann Résidence',           'type':'villa',    'city':'Dakar','neighborhood':'Fann',         'price':650000,'rooms':6,'surface':350, 'lat':14.6965,'lng':-17.4680,'has_pool':True,  'has_security':True,'furnished':True,'featured':True},
    {'title':'Chambre colocation Plateau',          'type':'room',     'city':'Dakar','neighborhood':'Plateau',      'price':60000, 'rooms':1,'surface':20,  'lat':14.6842,'lng':-17.4420,'furnished':True, 'has_wifi':True,                'featured':False},
    {'title':'Appartement F4 grand standing',       'type':'apartment','city':'Dakar','neighborhood':'Les Mamelles', 'price':450000,'rooms':4,'surface':160, 'lat':14.7380,'lng':-17.5050,'has_ac':True,   'has_parking':True,'furnished':True,'featured':True},
    {'title':'Studio meublé Thiès centre',          'type':'studio',   'city':'Thiès','neighborhood':'Centre',       'price':65000, 'rooms':1,'surface':28,  'lat':14.7913,'lng':-16.9249,'furnished':True, 'has_wifi':True,                'featured':False},
    {'title':'Appartement F2 Saint-Louis',          'type':'apartment','city':'Saint-Louis','neighborhood':'Nord',   'price':90000, 'rooms':2,'surface':55,  'lat':16.0179,'lng':-16.4896,'furnished':False,'has_ac':True,                  'featured':False},
]

class Command(BaseCommand):
    help = 'Crée des annonces de démonstration géolocalisées'

    def handle(self, *args, **kwargs):
        owner, created = User.objects.get_or_create(
            username='demo_proprio',
            defaults={
                'email':'proprio@immofacile.sn',
                'first_name':'Mamadou','last_name':'Diallo',
                'role':'owner','city':'Dakar','is_verified':True,
            }
        )
        if created:
            owner.set_password('Demo@1234')
            owner.save()
            self.stdout.write(self.style.SUCCESS('✅ Compte créé : demo_proprio / Demo@1234'))

        agency, cr2 = User.objects.get_or_create(
            username='dakar_immo_pro',
            defaults={
                'email':'contact@dakarimmo.sn',
                'role':'agency','city':'Dakar','is_verified':True,
                'agency_name':'Dakar Immo Pro',
                'agency_address':'Plateau, Dakar',
            }
        )
        if cr2:
            agency.set_password('Demo@1234')
            agency.save()
            self.stdout.write(self.style.SUCCESS('✅ Agence créée : dakar_immo_pro / Demo@1234'))

        count = 0
        for i, d in enumerate(DEMO):
            listing_owner = agency if i % 3 == 0 else owner
            listing, created = Listing.objects.get_or_create(
                title=d['title'],
                defaults={
                    'owner': listing_owner,
                    'description': f"Belle propriété à {d['neighborhood']}, {d['city']}. Logement {d['type']} avec {d['rooms']} pièce(s). Idéalement situé dans un quartier calme et bien desservi.",
                    'type': d['type'], 'status': 'active',
                    'city': d['city'], 'neighborhood': d['neighborhood'],
                    'price': d['price'], 'rooms': d['rooms'],
                    'surface': d.get('surface'), 'bathrooms': 1,
                    'latitude': d['lat'], 'longitude': d['lng'],
                    'furnished':    d.get('furnished', False),
                    'has_parking':  d.get('has_parking', False),
                    'has_wifi':     d.get('has_wifi', False),
                    'has_ac':       d.get('has_ac', False),
                    'has_garden':   d.get('has_garden', False),
                    'has_pool':     d.get('has_pool', False),
                    'has_security': d.get('has_security', False),
                    'is_featured':  d.get('featured', False),
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ {count} annonce(s) créée(s) sur {len(DEMO)}.\n'
            '➡  Lancez : python manage.py runserver\n'
            '➡  Carte  : http://127.0.0.1:8000/carte/'
        ))
