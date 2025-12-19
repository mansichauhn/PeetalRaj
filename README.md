# PeetalRaj -Moradabad Brass E-Commerce Platform

A e-commerce web application for selling authentic Moradabad Brass (Peetal) products. Built with Flask and featuring a modern, responsive design with integrated payment processing via Razorpay.

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


## 🔑 API Keys & Security

### Getting Razorpay Credentials

1. Sign up at [Razorpay](https://razorpay.com)
2. Go to Dashboard → Settings → API Keys
3. Copy your Key ID and Key Secret
4. Add them to your `.env` file


## 📱 Default Admin Login

Default admin credentials (from seed.py):
- **Email**: admin@brasscart.com
- **Password**: admin123

⚠️ **Change these credentials in production!**




**Made with ❤️to support elderly artisans by digitally preserving traditional crafts at risk of
extinction.**
