# Cooked - Your Ultimate Cooking Companion

A modern web application for food enthusiasts to discover, share, and rate recipes. Built with Django and Bootstrap 5.

## Overview

Cooked is a full-featured recipe sharing platform that allows users to:
- Create and share their favorite recipes
- Rate and review recipes
- Build a personal collection of favorite recipes
- Interact with other food enthusiasts
- Discover new recipes through various categories and filters

## Depndencie
- Django==5.1.7
- django-allauth==0.61.1
- django-crispy-forms==2.1
- crispy-bootstrap5==2024.2 
- python-dotenv==1.0.1
- Pillow 

## Features

### Recipe Management
- Create and share your favorite recipes
- Upload recipe images
- Categorize recipes by type (Breakfast, Lunch, Dinner, etc.)
- Detailed recipe instructions and ingredients lists
- Search and filter recipes by category
- Recipe categories include:
  - Main meals (Breakfast, Lunch, Dinner)
  - Beverages (Drinks)
  - Desserts
  - Special diets (Keto, Vegetarian)
  - Holiday specials (Mother's Day, New Years)

### User Features
- User registration and authentication
- Personal profile management
- Favorite recipes collection
- Recipe ratings and reviews
- User avatars and profile customization
- Profile view with:
  - User information
  - Favorite recipes
  - Reviews history
  - Recipe management options

### Community Features
- Interactive community feedback section
- Real-time recipe ratings
- User reviews with star ratings
- Latest reviews showcase on homepage
- Recipe sharing and social interaction
- Community feedback section includes:
  - 4 most recent reviews
  - User avatars and usernames
  - Star ratings (1-5)
  - Review comments
  - Links to reviewed recipes
  - Interactive hover effects
  - Animated entrance effects

### Modern UI/UX
- Responsive design for all devices
- Beautiful animations and transitions
- Intuitive navigation
- Clean and modern interface
- Bootstrap 5 styling
- Features include:
  - Animated hero section
  - Card-based recipe display
  - Interactive hover effects
  - Smooth scrolling
  - Mobile-friendly layout

## Technical Stack

- **Backend**: Django 5.1.7
- **Frontend**: 
  - Bootstrap 5
  - HTML5
  - CSS3
  - JavaScript
- **Database**: SQLite (development)
- **Authentication**: Django's built-in authentication system
- **Forms**: Django Forms with Crispy Forms
- **Styling**: Bootstrap 5 with custom CSS

## Project Structure

```
cooked/
├── cooked_app/          # Project settings
├── recipes/             # Main app
│   ├── templates/      # Recipe templates
│   ├── static/        # Static files
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   └── urls.py        # URL routing
├── users/              # User management app
│   ├── templates/     # User templates
│   └── views.py       # User views
├── templates/         # Global templates
└── manage.py         # Django management script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cooked.git
cd cooked
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://localhost:8000 in your browser

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap 5 for the UI framework
- Django for the web framework
- All contributors and users of the platform

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
