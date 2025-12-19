from app import create_app, db
from app.models import User, Product
import random

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@brasscart.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create regular user
        print("Creating test user...")
        user = User(
            username='testuser',
            email='user@example.com',
            is_admin=False
        )
        user.set_password('password123')
        db.session.add(user)
        
        # Sample products data - Only products with real images
        products_data = [
            {
                'name': 'Handcrafted Brass Bowl',
                'description': 'Exquisite decorative brass bowl with intricate mythological engravings. Features beautiful gold finish with detailed artwork on the exterior. Perfect for home decor, gifting, or serving dry fruits. Diameter: 10 inches.',
                'price': 1299.00,
                'category': 'Decorative Items',
                'image_filename': 'brass_bowl.jpg'
            },
            {
                'name': 'Designer Brass Serving Tray',
                'description': 'Beautiful brass serving tray with ornate decorative border and textured center. Perfect for serving snacks, dry fruits, or as a decorative centerpiece. Comes with matching small bowls. Diameter: 12 inches.',
                'price': 1599.00,
                'category': 'Tableware',
                'image_filename': 'brass_tray.jpg'
            },
            {
                'name': 'Ornate Brass Peacock Stand',
                'description': 'Magnificent brass peacock decorative stand with intricate scale detailing and traditional bells. Features a graceful curved peacock design with elevated bowl. An exquisite statement piece for your home. Height: 14 inches.',
                'price': 2999.00,
                'category': 'Home Decor',
                'image_filename': 'brass_peacock.jpg'
            },
            {
                'name': 'Lord Ganesha Brass Statue',
                'description': 'Magnificent Lord Ganesha brass idol with stunning multicolor antique finish. Features intricate detailing with traditional posture and ornate decorations. Perfect for home temple, puja room, or as a divine gift. Brings blessings of wisdom and prosperity. Height: 8 inches.',
                'price': 2499.00,
                'category': 'Statues',
                'image_filename': 'ganesh_statue.jpg'
            },
            {
                'name': 'Lakshmi Narayan Brass Idol',
                'description': 'Divine brass statue of Goddess Lakshmi and Lord Vishnu in a graceful resting posture. Exquisite craftsmanship with detailed work on ornaments and the Sheshnag canopy. Symbol of wealth, prosperity, and divine protection. Perfect for worship and home decoration. Height: 9 inches.',
                'price': 3499.00,
                'category': 'Statues',
                'image_filename': 'laxmi_narayan.jpg'
            },
            {
                'name': 'Radha Krishna Brass Statue',
                'description': 'Beautiful brass statue of Radha Krishna in eternal love pose with Lord Krishna playing the flute. Exceptional detailing in traditional attire, jewelry, and expressions. A symbol of divine love and devotion. Perfect for puja room and spiritual gifting. Height: 10 inches.',
                'price': 3299.00,
                'category': 'Statues',
                'image_filename': 'radhakrishna.jpg'
            }
        ]
        
        print("Creating products...")
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"\n{'='*50}")
        print("Database seeded successfully!")
        print(f"{'='*50}")
        print(f"\n✓ Created {len(products_data)} products")
        print(f"✓ Created 1 admin user")
        print(f"✓ Created 1 test user")
        print(f"\n{'='*50}")
        print("Login Credentials:")
        print(f"{'='*50}")
        print("\nAdmin Account:")
        print("  Email: admin@brasscart.com")
        print("  Password: admin123")
        print("\nTest User Account:")
        print("  Email: user@example.com")
        print("  Password: password123")
        print(f"\n{'='*50}\n")

if __name__ == '__main__':
    seed_database()
