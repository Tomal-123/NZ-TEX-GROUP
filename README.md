# TaskFlow - Task Management System

A modern, professional Task Management System homepage built with Django and Tailwind CSS.

## Features

- **Modern UI/UX**: Clean design with gradient color scheme (blue → purple → indigo)
- **Fully Responsive**: Works on mobile, tablet, and desktop
- **Smooth Animations**: Fade-in, slide-up, and hover effects
- **7 Sections**: Navbar, Hero, Features, Dashboard Preview, Testimonials, CTA, Footer

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS (via CDN)
- **Icons**: Inline SVG (Heroicons style)

## Project Structure

```
task-management-system/
├── taskmanager/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── accounts/             # Django app (placeholder)
│   └── apps.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # Media files
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Installation

1. **Install Django**:
   ```bash
   pip install django
   ```

2. **Run Migrations** (optional for homepage):
   ```bash
   python manage.py migrate
   ```

3. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Open Browser**:
   Navigate to `http://127.0.0.1:8000/`

## Customization

### Colors
Edit the gradient in `templates/base.html`:
- Primary gradient: `linear-gradient(135deg, #3B82F6, #8B5CF6, #6366F1)`

### Content
Edit sections in `templates/index.html`:
- Hero: Lines 8-70
- Features: Lines 72-180
- Testimonials: Lines 240-320
- CTA: Lines 330-360

## License

MIT License