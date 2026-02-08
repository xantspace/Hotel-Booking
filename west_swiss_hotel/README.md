# West-Swiss Hotel Aba

A modern, professional hotel management and booking system built with Django.

## Features
- **Responsive Design**: Premium look and feel across all devices.
- **Room Booking**: Real-time availability check and booking system.
- **Price Comparison**: Display direct rates vs OTA competitors.
- **Dynamic Amenities**: Showcase hotel facilities with modern UI.
- **Contact System**: Fully functional contact form with email integration.

## Render Deployment
This project is pre-configured for **Render** using a Blueprint (`render.yaml`).

### Steps to Deploy:
1. **GitHub**: Push this codebase to a GitHub repository.
2. **Render**: In the Render dashboard, click **New** -> **Blueprint**.
3. **Connect**: Link your GitHub repository.
4. **Approve**: Render will automatically detect `render.yaml` and set up the Web Service and PostgreSQL database.

### Manual Configuration
If you prefer manual setup:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn west_swiss_hotel.wsgi`
- **Env Vars**: See `.env.example` for required variables.

## Tech Stack
- Django 6.x
- Tailwind CSS (via CDN)
- WhiteNoise (Static file serving)
- Gunicorn (WSGI Server)
