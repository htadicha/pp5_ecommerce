# 🛒 Hawashmart - Django E-Commerce Platform

[![Django](https://img.shields.io/badge/Django-3.2.25-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🌐 Live Demo

**🚀 [Visit Hawashmart Live Website](https://hawashmart-3331ff5cdce2.herokuapp.com/)**

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

Hawashmart is a full-featured, production-ready e-commerce platform built with Django. This enterprise-grade solution provides a complete online shopping experience with advanced features including user authentication, product management, shopping cart functionality, order processing, payment integration, and comprehensive admin controls.

### 🏆 Key Highlights

- **Scalable Architecture**: Built with Django's robust framework for enterprise-level scalability
- **Advanced User Management**: Custom user authentication with profile management
- **Product Variations**: Support for product colors, sizes, and other variations
- **Review & Rating System**: Comprehensive product review and rating functionality
- **Secure Payment Processing**: Integrated Stripe payment gateway with transaction tracking
- **Responsive Design**: Modern, mobile-first UI with Bootstrap framework
- **Admin Dashboard**: Powerful Django admin interface for complete store management

## ✨ Features

### 🛍️ Core E-Commerce Features

- **Product Catalog Management**
  - Unlimited product categories and subcategories
  - Product variations (color, size, etc.)
  - Product gallery with multiple images
  - Stock management and availability tracking
  - SEO-friendly URLs with slug support

- **Shopping Cart System**
  - Persistent cart across sessions
  - Real-time cart updates
  - Quantity management
  - Cart item variations support
  - Guest and authenticated user cart handling

- **Order Management**
  - Complete order lifecycle tracking
  - Order status management (New, Accepted, Completed, Cancelled)
  - Order history for users
  - Invoice generation
  - Email notifications

- **Payment Integration**
  - Stripe payment gateway integration
  - Secure payment processing
  - Transaction tracking
  - Payment status management

### 👤 User Management

- **Custom User Authentication**
  - Email-based authentication
  - User profile management
  - Address book functionality
  - Profile picture upload
  - Account verification system

- **User Profiles**
  - Personal information management
  - Shipping address management
  - Order history tracking
  - Wishlist functionality

### ⭐ Review & Rating System

- **Product Reviews**
  - Star-based rating system (1-5 stars)
  - Written review submissions
  - Review moderation system
  - Average rating calculations
  - Review count tracking

### 🔍 Search & Filtering

- **Advanced Search**
  - Product name search
  - Description-based search
  - Category-based filtering
  - Price range filtering
  - Availability filtering

### 📱 Responsive Design

- **Mobile-First Approach**
  - Bootstrap 5 framework
  - Responsive navigation
  - Touch-friendly interface
  - Cross-browser compatibility

## 🛠️ Technology Stack

### Backend
- **Django 3.2.25** - High-level Python web framework
- **Python 3.12** - Programming language
- **SQLite** - Database (production-ready for PostgreSQL/MySQL)
- **Pillow** - Image processing library
- **Stripe** - Payment processing
- **WhiteNoise** - Static file serving

### Frontend
- **Bootstrap 5** - CSS framework for responsive design
- **jQuery** - JavaScript library
- **FontAwesome** - Icon library
- **Material Icons** - Google's material design icons

### Development Tools
- **Git** - Version control
- **Virtual Environment** - Python environment isolation
- **Django Admin** - Built-in admin interface
- **Heroku** - Cloud deployment platform

## 🏗️ Architecture

### Project Structure
```
pp5_ecommerce-1/
├── Hawashmart/                 # Main project directory
│   ├── settings.py            # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── static/               # Static files (CSS, JS, Images)
│   └── wsgi.py              # WSGI configuration
├── accounts/                 # User authentication app
├── category/                 # Product categories app
├── store/                    # Product management app
├── carts/                    # Shopping cart app
├── orders/                   # Order management app
├── storages/                 # File storage app
├── templates/                # HTML templates
├── media/                    # User-uploaded files
├── staticfiles/              # Collected static files
└── manage.py                # Django management script
```

## 🚀 Installation

### Prerequisites
- Python 3.12+
- Git
- Virtual Environment

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/htadicha/pp5_ecommerce.git
   cd pp5_ecommerce-1
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Environment File**
   ```bash
   # Create .env file with the following variables:
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   USE_AWS=False
   STRIPE_PUBLIC_KEY=your-stripe-public-key
   STRIPE_SECRET_KEY=your-stripe-secret-key
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application**
   - Open your browser and visit `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# AWS Settings (for production)
USE_AWS=False
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=eu-west-1

# Stripe Payment Keys
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production Configuration

For production deployment, ensure:
- Set `DEBUG=False`
- Use a production database (PostgreSQL recommended)
- Configure proper `ALLOWED_HOSTS`
- Set up AWS S3 for static/media files
- Configure email backend
- Set up proper logging

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set USE_AWS=True
   heroku config:set AWS_ACCESS_KEY_ID=your-aws-access-key
   heroku config:set AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket-name
   heroku config:set AWS_S3_REGION_NAME=eu-west-1
   heroku config:set STRIPE_PUBLIC_KEY=your-stripe-public-key
   heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key
   ```

5. **Deploy to Heroku**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic
   ```

6. **Open Your App**
   ```bash
   heroku open
   ```

### Other Deployment Options

- **Docker**: Use the provided Dockerfile for containerized deployment
- **AWS**: Deploy using AWS Elastic Beanstalk or EC2
- **DigitalOcean**: Use DigitalOcean App Platform
- **Railway**: Deploy using Railway platform

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test store

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/htadicha/pp5_ecommerce.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow PEP 8 coding standards
   - Add tests for new features
   - Update documentation

4. **Commit Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create Pull Request**

### Development Guidelines

- **Code Style**: Follow PEP 8 and Django coding standards
- **Documentation**: Update README and docstrings
- **Testing**: Maintain test coverage
- **Security**: Follow security best practices

## 🔒 Security Features

- **Authentication & Authorization**: Custom user model with email-based authentication
- **Data Protection**: Input validation, SQL injection prevention, XSS protection
- **Payment Security**: Secure Stripe payment processing with transaction encryption
- **CSRF Protection**: Cross-site request forgery protection
- **Session Management**: Secure session handling

## ⚡ Performance Features

- **Database Optimization**: Efficient queries with select_related and prefetch_related
- **Static File Compression**: Minified CSS/JS with WhiteNoise
- **Image Optimization**: Compressed product images
- **Caching**: Django caching framework integration
- **CDN Ready**: Content delivery network support

## 📞 Support

For support and questions:

- **Email**: support@hawashmart.com
- **Issues**: [GitHub Issues](https://github.com/htadicha/pp5_ecommerce/issues)
- **Discussions**: [GitHub Discussions](https://github.com/htadicha/pp5_ecommerce/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community**: For the excellent web framework
- **Bootstrap Team**: For the responsive CSS framework
- **FontAwesome**: For the comprehensive icon library
- **Stripe**: For secure payment processing
- **Heroku**: For reliable cloud deployment platform

---

**Made with ❤️ by the Hawashmart Team**

🌐 **Live Website**: [https://hawashmart-3331ff5cdce2.herokuapp.com/](https://hawashmart-3331ff5cdce2.herokuapp.com/)