"""
Management command to seed initial restaurant data for demonstration
Run with: python manage.py seed_restaurants
"""
from django.core.management.base import BaseCommand
from core.models import Restaurant, MenuItem

class Command(BaseCommand):
    help = 'Seed initial restaurant and menu data'

    def handle(self, *args, **options):
        # Check if data already exists
        if Restaurant.objects.exists():
            self.stdout.write(self.style.WARNING('Restaurants already exist. Skipping seed.'))
            return

        restaurants_data = [
            {
                'name': 'Pizza Palace',
                'description': 'Authentic Italian pizzas and pastas',
                'address': '123 Food Street, Downtown',
                'is_active': True,
            },
            {
                'name': 'Burger Barn',
                'description': 'Juicy burgers and crispy fries',
                'address': '456 Main Ave, City Center',
                'is_active': True,
            },
            {
                'name': 'Curry House',
                'description': 'Delicious Indian cuisine',
                'address': '789 Spice Lane, Market District',
                'is_active': True,
            },
            {
                'name': 'Sushi Spot',
                'description': 'Fresh Japanese sushi and rolls',
                'address': '321 Ocean Blvd, Waterfront',
                'is_active': True,
            },
            {
                'name': 'Taco Fiesta',
                'description': 'Authentic Mexican tacos and burritos',
                'address': '654 Latino Row, North Side',
                'is_active': True,
            },
            {
                'name': 'Dragon Bowl',
                'description': 'Chinese noodles and dim sum',
                'address': '987 Asia Street, East End',
                'is_active': True,
            },
        ]

        for r_data in restaurants_data:
            restaurant = Restaurant.objects.create(**r_data)
            
            # Add menu items
            menu_items = [
                {'name': f'Dish 1 at {r_data["name"]}', 'price': 12.99, 'is_veg': True, 'available': True},
                {'name': f'Dish 2 at {r_data["name"]}', 'price': 14.99, 'is_veg': False, 'available': True},
                {'name': f'Dish 3 at {r_data["name"]}', 'price': 16.99, 'is_veg': True, 'available': True},
            ]
            
            for item in menu_items:
                MenuItem.objects.create(restaurant=restaurant, **item)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created {r_data["name"]} with 3 menu items'))

        self.stdout.write(self.style.SUCCESS('✓ Successfully seeded restaurant data!'))
