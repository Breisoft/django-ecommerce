# Django E-commerce Project

An e-commerce platform meticulously designed with Django to provide a comprehensive shopping experience. Built with a modular approach, this platform houses several apps, each catering to a unique aspect of the e-commerce ecosystem.

## Key Features:

- **Django REST framework**: The platform extensively uses Django REST framework to provide a set of API endpoints for its functionalities, enabling seamless integration with frontend or mobile applications.
- **JWT Authentication**: Leveraging `rest_framework_simplejwt`, the platform offers JWT (JSON Web Token) based authentication, ensuring secure user sessions and data exchanges.

## App Features:

### User Account Management (`account` app):

The account app is a cornerstone of the platform, offering functionalities centered around user management. Integrated with Django's authentication system, it facilitates the creation, retrieval, and management of user accounts. A notable feature is the inclusion of user addresses, allowing for streamlined shipping and billing operations.

### Shopping Cart (`cart` app):

A quintessential component of any e-commerce platform, the cart app manages users' shopping carts, ensuring smooth product selection and checkout processes. It holds structures for the cart and its items, linking them to users and products respectively.

### Product Categories (`category` app):

To bring order to the myriad of products available, the category app classifies products into distinct categories. It's built upon an abstract model, `SlugModel`, which provides unique slug generation based on category names, ensuring user-friendly URLs.

### Product Management (`product` app):

The product app manages the intricate details of individual products. Each product is equipped with attributes like description, price, quantity, and a unique slug. Moreover, products are associated with categories, ensuring systematic product organization.

### Shared Utilities (`common` app):

The common app provides shared utilities and functionalities that the platform's other apps leverage. Its `SlugModel` is an abstract model that offers slug generation capabilities, ensuring unique, user-friendly URLs for models that inherit from it.

### Configuration and Routing (`ecommerce` directory):

The main ecommerce directory holds the project's settings, configurations, and URL routing. It integrates the Django admin site, providing a backend interface for platform management.
