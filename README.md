# KAFEI – Web and Mobile Coffee Shop System

ICT 2207Y(3) Web and Mobile Application Development 2025/2026

KAFEI is an online coffee shop platform developed by team **Git-it-done**. The system allows customers to browse menu items and deals, register or log in, add products to cart, place orders, leave reviews, save favourites, and interact with location-aware features. The project also includes Django REST API endpoints and a Flet-based mobile frontend that consumes the backend APIs.

---

## Team Members

- Sewnarain Downeshwari | 2416337 | 1-ritika-1
- Milena Nathalie Jacquette | 2416866 | MinaKozume
- Ramkhalawon Bhimarika Rye | 2416454 | hans-init
- Oozeer Muhammad Is-haaq Hussein | 2415962 | Borgishq
- Beegoo Muhammad Farhaan Ally | 2416664 | Farhaanbg

---

## Main Features

### Web Application

- Customer registration and login
- Menu browsing with product details
- Deals page
- Cart system
- Checkout with bank transfer or cash pickup
- Order creation and order history
- Reviews
- Favourites
- Admin panel for managing data

### Location-Aware Web Checkout

- Browser geolocation request
- Interactive Leaflet map
- Marker for KAFEI location
- Marker for customer location
- Distance calculation between customer and KAFEI
- Google Maps directions button
- Latitude, longitude, and distance stored with the order for internal processing
- Only distance is displayed to the user for better privacy

### Backend APIs

- JWT login and token refresh
- Menu API
- Deals API
- Reviews API
- Cart API
- Favourites API
- Account register/current-user API
- Order history API
- Order placement API for mobile/API clients

### Mobile Frontend

- Built using Flet
- Runs as a web/mobile-style frontend
- Login using JWT authentication
- Register account
- Load menu from Django API
- Add menu items to mobile cart
- Capture GPS location when supported by the device/browser
- Demo location fallback for local testing
- Map display using Flet Map
- Google Maps directions
- Place mobile order through Django API

---

## Technologies Used

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- HTML, CSS, JavaScript
- Bootstrap
- Leaflet.js
- Flet
- Flet Map
- Flet Geolocator
- Requests
- ngrok
- Git and GitHub

---


## Project Structure

```text
KAFEI_project/          Django project settings and main URL routing
accounts/               Login, signup, account management, account APIs
menu/                   Menu models, pages, serializers, and menu API
cart/                   Cart models, pages, serializers, and cart API
orders/                 Checkout, order models, order APIs, location storage
reviews/                Review pages and APIs
deals/                  Deals pages and APIs
favourites/             Favourite item pages and APIs
homepage/               Homepage and homepage API data
mobile_frontend/        Flet mobile frontend
requirements.txt        Python package requirements
manage.py               Django command-line entry point
```

---

# How to Run the Project Locally

These steps assume you are on Windows and opened a terminal inside the project root folder, where `manage.py` is located.

## 1. Install Python packages

```powershell
py -m pip install -r requirements.txt
```

If Flet is not found later, install or update these packages manually:

```powershell
py -m pip install flet flet-map flet-geolocator requests
```

## 2. Apply database migrations

```powershell
py manage.py makemigrations
py manage.py migrate
```

## 3. Create an admin account

```powershell
py manage.py createsuperuser
```

Follow the prompts to create the username and password.

## 4. Run the Django web application

```powershell
py manage.py runserver 127.0.0.1:8000
```

Open the website:

```text
http://127.0.0.1:8000/
```

Open the admin panel:

```text
http://127.0.0.1:8000/admin/
```

Test the menu API:

```text
http://127.0.0.1:8000/menu/api/
```

---

# How to Run the Mobile Frontend on the Laptop

Keep the Django server running in Terminal 1.

Open Terminal 2 in the same project root folder and run:

```powershell
py -m flet.cli run --web --port 8550 mobile_frontend/main.py
```

If this command does not work on your machine, use the `flet` command directly:

```powershell
flet run --web --port 8550 mobile_frontend/main.py
```

Then open:

```text
http://127.0.0.1:8550
```

In the mobile frontend, test this flow:

1. Login using a Django user account.
2. Click **Load Menu**.
3. Add menu items to cart.
4. Use GPS location or demo location.
5. Open directions in Google Maps.
6. Place the mobile order.
7. Check the order in Django admin.

---

# How to Test the Mobile Frontend on Android or iOS Using ngrok

Mobile browsers often block GPS on local non-HTTPS links such as `http://192.168.x.x:8550`. To test GPS reliably on Android or iOS, expose the Flet frontend through an HTTPS ngrok URL.

## 1. Make sure the mobile frontend uses localhost for the API

In `mobile_frontend/main.py`, keep:

```python
API_BASE_URL = "http://127.0.0.1:8000"
```


## 2. Run Django in Terminal 1

```powershell
py manage.py runserver 127.0.0.1:8000
```

Check:

```text
http://127.0.0.1:8000/menu/api/
```

## 3. Run Flet in Terminal 2

```powershell
py -m flet.cli run --web --port 8550 mobile_frontend/main.py
```

If needed, use:

```powershell
flet run --web --port 8550 mobile_frontend/main.py
```

Check:

```text
http://127.0.0.1:8550
```

## 4. Add your ngrok authtoken once

Create or log into an ngrok account. In the ngrok dashboard, copy the authtoken command. It looks like this:

```powershell
ngrok config add-authtoken YOUR_TOKEN_HERE
```

Paste it into PowerShell. This only needs to be done once per computer.

## 5. Start ngrok in Terminal 3

```powershell
ngrok http 8550
```

Ngrok will show a forwarding link like:

```text
https://example-name.ngrok-free.app -> http://localhost:8550
```

Copy the HTTPS link.

## 6. Open the ngrok HTTPS link on Android or iOS

Open the HTTPS link on the mobile device:

```text
https://example-name.ngrok-free.app
```

Use the HTTPS link, not the local IP address.

## 7. Test the mobile demo flow

1. Open the ngrok HTTPS URL on the phone/tablet.
2. Login.
3. Load Menu.
4. Add item to cart.
5. Press **Use My GPS Location**.
6. Allow location permission.
7. Confirm that the map updates and distance appears.
8. Press **Open Directions in Google Maps**.
9. Place the order.
10. Check the order in Django admin.

---

