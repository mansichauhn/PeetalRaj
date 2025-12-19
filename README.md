# 🏺 BrassCart - Premium Moradabad Brass E-Commerce Platform

A professional, full-featured e-commerce web application for selling authentic Moradabad Brass (Peetal) products. Built with Flask and featuring a modern, responsive design with integrated payment processing via Razorpay.

## ✨ Features

### Customer Features
- 🛍️ **Product Catalog**: Browse beautiful selection of brass products with search and category filtering
- 🖼️ **Product Details**: View high-quality product images and detailed descriptions
- 🛒 **Shopping Cart**: Full-featured cart with quantity management and real-time updates
- 👤 **User Authentication**: Secure registration and login system
- 💳 **Payment Gateway**: Razorpay integration for secure online payments
- 📦 **Order Tracking**: View order history and order details
- 📱 **Responsive Design**: Mobile-optimized with elegant gold-themed brass aesthetics

### Admin Features
- 📊 **Admin Dashboard**: Complete overview with statistics and analytics
- ➕ **Product Management**: Add, edit, and delete products with image uploads
- 📋 **Order Management**: View and manage all customer orders
- 📈 **User Analytics**: Track total users, revenue, and sales data

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python Flask 3.0 |
| Database | SQLite with SQLAlchemy ORM |
| Authentication | Flask-Login with Werkzeug |
| Frontend | Bootstrap 5 + Custom CSS |
| Image Processing | Pillow |
| Payment Gateway | Razorpay |
| Forms | Flask-WTF with validation |

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Razorpay account (for payment integration)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd BrassCart
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` and add your Razorpay credentials:
```
FLASK_ENV=development
FLASK_DEBUG=True
SESSION_SECRET=your-secret-key-here

# Razorpay API Keys (get from https://dashboard.razorpay.com)
RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXXXXXXXX
RAZORPAY_KEY_SECRET=your_secret_key_here
```

⚠️ **Important**: Never commit `.env` file. It's already in `.gitignore`.

### 5. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📝 Database Setup

The database will automatically initialize on first run. To reset the database:

```bash
# Delete the existing database
rm instance/brasscart.db

# Reinitialize with seed data
python seed.py
```

## 🧪 Testing the Payment Gateway

Use the following test card details in Razorpay:
- **Card Number**: 4111 1111 1111 1111
- **Expiry**: Any future date (MM/YY format)
- **CVV**: Any 3 digits

## 📂 Project Structure

```
BrassCart/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── models.py                   # Database models (User, Product, Order)
│   ├── routes.py                   # Main routes and payment handling
│   ├── auth_routes.py              # Authentication routes
│   ├── admin_routes.py             # Admin dashboard routes
│   ├── forms.py                    # WTForms validation
│   ├── static/
│   │   ├── css/styles.css          # Custom styling
│   │   └── uploads/                # Product images
│   └── templates/
│       ├── base.html               # Base template
│       ├── home.html               # Home page
│       ├── products.html           # Products listing
│       ├── checkout.html           # Checkout with Razorpay
│       ├── cart.html               # Shopping cart
│       └── admin/                  # Admin templates
├── run.py                          # Application entry point
├── seed.py                         # Database seeding script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🔑 API Keys & Security

### Getting Razorpay Credentials

1. Sign up at [Razorpay](https://razorpay.com)
2. Go to Dashboard → Settings → API Keys
3. Copy your Key ID and Key Secret
4. Add them to your `.env` file

### Security Best Practices

- ✅ **Never commit `.env`** - Use `.env.example` as template
- ✅ **Keep secret keys private** - Rotate keys periodically
- ✅ **Use environment variables** - For all sensitive data
- ✅ **HTTPS in production** - Always use HTTPS for payments
- ✅ **Secure headers** - Implement CSRF protection (already included)

## 🚢 Deployment

### Local Production Build
```bash
# Install gunicorn
pip install gunicorn

# Run with Gunicorn (production WSGI server)
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Deploy on Cloud Platforms

**Heroku**:
```bash
heroku create your-app-name
git push heroku main
heroku config:set RAZORPAY_KEY_ID=your_key_id
heroku config:set RAZORPAY_KEY_SECRET=your_secret
```

**PythonAnywhere**:
- Upload project files
- Configure virtual environment
- Set environment variables in Web app settings
- Reload web app

## 📱 Default Admin Login

Default admin credentials (from seed.py):
- **Email**: admin@brasscart.com
- **Password**: admin123

⚠️ **Change these credentials in production!**

## 🐛 Troubleshooting

### "ImportError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Database errors
```bash
# Reset database
rm instance/brasscart.db
python seed.py
```

### Razorpay payment errors
- Verify Key ID and Key Secret in `.env`
- Check test mode is enabled in Razorpay dashboard
- Ensure SSL certificate for HTTPS (required for production)

## 📧 Contact & Support

For issues or questions, please create an issue in the repository.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Razorpay for payment processing
- Bootstrap for UI framework
- Flask community for excellent documentation

---

**Made with ❤️ for selling beautiful Moradabad brass products**
