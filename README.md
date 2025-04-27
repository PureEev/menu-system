# menu-system

A Django project providing a flexible, hierarchical menu system as a reusable app.

## Features

- Unlimited nested menu levels
- Supports both named URL reversals and custom URLs
- Automatic active menu item detection
- Django admin integration for creating Menus and MenuItems
- Easily override templates and styles

## Requirements

- Python 3.8+
- Django 5.2+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PureEev/menu-system.git
   cd menu-system
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   venv\Scripts\activate     # Windows
   pip install Django
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. (Optional) Create a superuser to access the admin:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser to see the demo.

## Configuration

The `menu` app is already included in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'menu',
]
```

## Usage

### Admin

1. Navigate to the Django admin at `/admin/`.
2. Create a new **Menu**, giving it a unique name.
3. Add **MenuItem**s under that menu:
   - **Title**: The display text.
   - **URL**: Custom URL or named route.
   - **Named URL**: Toggle if using Django's named URL reversing.
   - **Parent**: Set to nest items.
   - **Order**: Controls the display order.

### Template Tag

Load and render your menu in any template:

```django
{% load menu_tags %}
{% draw_menu 'Your Menu Name' %}
```

This will include the following templates:

- `menu/menu.html`
- `menu/menu_level.html`

## Customization

- **Templates**: Override by placing your own versions at `templates/menu/menu.html` and `templates/menu/menu_level.html`.
- **CSS**: Style the classes:
  - `.menu-container`
  - `.main-menu`
  - `.sub-menu`
  - `.active`
