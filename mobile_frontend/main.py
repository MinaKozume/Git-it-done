import asyncio
import math

import flet as ft
import flet_geolocator as ftg
import flet_map as ftm
import requests


# The Flet Python process runs on the laptop, so it can call Django through localhost.
API_BASE_URL = "http://127.0.0.1:8000"
print("USING API_BASE_URL:", API_BASE_URL)

KAFEI_LATITUDE = -20.3180
KAFEI_LONGITUDE = 57.5250


def calculate_distance_km(lat1, lon1, lat2, lon2):
    # Earth radius in kilometres, used by the Haversine formula.
    earth_radius_km = 6371

    # Convert latitude and longitude differences from degrees to radians.
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    # Calculate the central angle between the two coordinates.
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    # Convert the central angle into distance.
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c


def main(page: ft.Page):
    page.title = "KAFEI Mobile"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.bgcolor = ft.Colors.GREY_100

    # The JWT token is stored in memory and attached to protected API requests.
    access_token = {"value": None}
    logged_user = {"username": None, "email": None}

    # These lists hold the mobile cart and menu data loaded from the Django API.
    cart_items = []
    menu_items_cache = []

    # Coordinates are kept internally for distance calculation, directions, and order submission.
    user_location = {
        "latitude": None,
        "longitude": None,
        "distance": None,
    }

    status_text = ft.Text("", color=ft.Colors.RED)

    logged_in_text = ft.Text(
        "Not logged in",
        size=14,
        color=ft.Colors.GREY_700,
    )

    username_field = ft.TextField(label="Username")
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
    )

    menu_column = ft.Column(spacing=10)
    cart_column = ft.Column(spacing=10)
    location_text = ft.Text("Location not captured yet.")

    gps_button = ft.ElevatedButton("Use My GPS Location")
    demo_location_button = ft.OutlinedButton("Use Demo Location")
    directions_button = ft.OutlinedButton("Open Directions in Google Maps")

    map_marker_layer = ftm.MarkerLayer(
        markers=[
            ftm.Marker(
                coordinates=ftm.MapLatitudeLongitude(
                    KAFEI_LATITUDE,
                    KAFEI_LONGITUDE,
                ),
                content=ft.Icon(
                    ft.Icons.LOCATION_ON,
                    color=ft.Colors.BROWN,
                    size=35,
                ),
            )
        ]
    )

    map_control = ftm.Map(
        expand=True,
        initial_center=ftm.MapLatitudeLongitude(
            KAFEI_LATITUDE,
            KAFEI_LONGITUDE,
        ),
        initial_zoom=14,
        layers=[
            ftm.TileLayer(
                url_template="https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png",
            ),
            map_marker_layer,
        ],
    )

    geo = ftg.Geolocator(
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.HIGH,
        )
    )

    def show_message(message, is_error=False):
        status_text.value = message
        status_text.color = ft.Colors.RED if is_error else ft.Colors.GREEN
        page.update()

    def get_auth_headers():
        # Protected endpoints require the JWT token in the Authorization header.
        if access_token["value"] is None:
            return {}

        return {
            "Authorization": f"Bearer {access_token['value']}",
        }

    def update_location_state(user_latitude, user_longitude):
        # Calculate the distance between the user and KAFEI.
        distance = calculate_distance_km(
            user_latitude,
            user_longitude,
            KAFEI_LATITUDE,
            KAFEI_LONGITUDE,
        )

        # Store coordinates internally so they can be sent to the order API.
        user_location["latitude"] = user_latitude
        user_location["longitude"] = user_longitude
        user_location["distance"] = distance

        # Show only the distance for privacy instead of raw coordinates.
        location_text.value = f"You are approximately {distance:.2f} km away from KAFEI."

        # Show KAFEI marker and user marker on the map.
        map_marker_layer.markers = [
            ftm.Marker(
                coordinates=ftm.MapLatitudeLongitude(
                    KAFEI_LATITUDE,
                    KAFEI_LONGITUDE,
                ),
                content=ft.Icon(
                    ft.Icons.LOCATION_ON,
                    color=ft.Colors.BROWN,
                    size=35,
                ),
            ),
            ftm.Marker(
                coordinates=ftm.MapLatitudeLongitude(
                    user_latitude,
                    user_longitude,
                ),
                content=ft.Icon(
                    ft.Icons.MY_LOCATION,
                    color=ft.Colors.BLUE,
                    size=35,
                ),
            ),
        ]

    def refresh_cart():
        cart_column.controls.clear()

        if not cart_items:
            cart_column.controls.append(ft.Text("Cart is empty."))
            page.update()
            return

        total = 0

        for item in cart_items:
            subtotal = item["price"] * item["quantity"]
            total += subtotal

            cart_column.controls.append(
                ft.Container(
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.BROWN_50,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"{item['name']} x {item['quantity']} = Rs {subtotal:.2f}",
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.REMOVE_CIRCLE,
                                tooltip="Remove one",
                                data=item["id"],
                                on_click=remove_one_from_cart,
                            ),
                        ],
                    ),
                )
            )

        cart_column.controls.append(
            ft.Text(
                f"Total: Rs {total:.2f}",
                weight=ft.FontWeight.BOLD,
            )
        )

        page.update()

    def add_to_cart(e):
        selected_item = e.control.data

        existing_item = None

        for item in cart_items:
            if item["id"] == selected_item["id"]:
                existing_item = item
                break

        if existing_item:
            existing_item["quantity"] += 1
        else:
            cart_items.append(
                {
                    "id": selected_item["id"],
                    "name": selected_item["name"],
                    "price": float(selected_item["price"]),
                    "quantity": 1,
                }
            )

        refresh_cart()
        show_message(f"{selected_item['name']} added to cart.")

    def remove_one_from_cart(e):
        item_id = e.control.data

        for item in cart_items:
            if item["id"] == item_id:
                item["quantity"] -= 1

                if item["quantity"] <= 0:
                    cart_items.remove(item)

                break

        refresh_cart()

    def render_menu(items):
        menu_column.controls.clear()

        if not items:
            menu_column.controls.append(ft.Text("No menu items found."))
            page.update()
            return

        for item in items:
            category = item.get("category", {})
            category_name = category.get("name", "") if isinstance(category, dict) else ""

            menu_column.controls.append(
                ft.Container(
                    padding=12,
                    border_radius=15,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(
                        blur_radius=8,
                        color=ft.Colors.BLACK12,
                    ),
                    content=ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text(
                                item["name"],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(category_name),
                            ft.Text(item.get("description", "")),
                            ft.Text(
                                f"Rs {item['price']}",
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.ElevatedButton(
                                "Add to Cart",
                                data=item,
                                on_click=add_to_cart,
                            ),
                        ],
                    ),
                )
            )

        page.update()

    def load_menu(e=None):
        menu_column.controls.clear()
        menu_column.controls.append(ft.ProgressRing())
        page.update()

        try:
            response = requests.get(
                f"{API_BASE_URL}/menu/api/",
                timeout=10,
            )

            data = response.json()

            if isinstance(data, dict) and "items" in data:
                items = data["items"]
            else:
                items = data

            menu_items_cache.clear()

            for item in items:
                menu_items_cache.append(
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "description": item.get("description", ""),
                        "price": float(item.get("price", 0)),
                        "category": item.get("category", {}),
                        "image": item.get("image", ""),
                    }
                )

            render_menu(menu_items_cache)
            show_message("Menu loaded from Django API.")

        except Exception as ex:
            menu_column.controls.clear()
            show_message(f"Could not load menu: {ex}", is_error=True)

    def login_user(e):
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/token/",
                json={
                    "username": username_field.value,
                    "password": password_field.value,
                },
                timeout=10,
            )

            data = response.json()

            if "access" not in data:
                show_message("Login failed. Check username/password.", is_error=True)
                return

            access_token["value"] = data["access"]
            logged_user["username"] = username_field.value

            logged_in_text.value = f"Logged in as: {username_field.value}"

            show_message(f"Logged in as {username_field.value}.")
            load_me()

        except Exception as ex:
            show_message(f"Login error: {ex}", is_error=True)

    def register_user(e):
        try:
            response = requests.post(
                f"{API_BASE_URL}/accounts/api/register/",
                json={
                    "username": username_field.value,
                    "email": email_field.value,
                    "password": password_field.value,
                },
                timeout=10,
            )

            data = response.json()

            if response.status_code >= 400:
                show_message(str(data), is_error=True)
                return

            show_message("Account created. You can now login.")

        except Exception as ex:
            show_message(f"Registration error: {ex}", is_error=True)

    def logout_user(e):
        # Remove the token so protected API requests are no longer authorized.
        access_token["value"] = None

        # Clear stored user details in the mobile interface.
        logged_user["username"] = None
        logged_user["email"] = None

        # Empty the cart so another user starts with a clean session.
        cart_items.clear()
        refresh_cart()

        # Reset account display and clear the password field.
        logged_in_text.value = "Not logged in"
        password_field.value = ""

        show_message("Logged out successfully.")
        page.update()

    def load_me():
        try:
            response = requests.get(
                f"{API_BASE_URL}/accounts/api/me/",
                headers=get_auth_headers(),
                timeout=10,
            )

            data = response.json()

            logged_user["username"] = data.get(
                "username",
                logged_user["username"],
            )
            logged_user["email"] = data.get(
                "email",
                email_field.value,
            )

            if logged_user["email"]:
                email_field.value = logged_user["email"]

            page.update()

        except Exception:
            pass

    async def capture_location(e):
        gps_button.disabled = True
        gps_button.text = "Capturing..."
        show_message("Capturing your location. Please wait.")
        page.update()

        try:
            await geo.request_permission()

            # Give the browser/device a short moment to finish permission handling.
            await asyncio.sleep(1)

            try:
                position = await geo.get_current_position()
            except Exception:
                show_message(
                    "GPS could not be captured. Please allow location permission or use demo location.",
                    is_error=True,
                )
                return

            if position is None:
                show_message(
                    "GPS returned no location. Please allow location permission or use demo location.",
                    is_error=True,
                )
                return

            user_latitude = position.latitude
            user_longitude = position.longitude

            update_location_state(user_latitude, user_longitude)

            await map_control.center_on(
                point=ftm.MapLatitudeLongitude(
                    user_latitude,
                    user_longitude,
                ),
                zoom=14,
            )

            show_message("Location captured.")

        except Exception as ex:
            show_message(f"Location error: {ex}", is_error=True)

        finally:
            gps_button.disabled = False
            gps_button.text = "Use My GPS Location"
            page.update()

    def use_demo_location(e):
        # Demo coordinates are used when a browser blocks GPS during local testing.
        user_latitude = -20.3165
        user_longitude = 57.5255

        update_location_state(user_latitude, user_longitude)

        page.update()
        show_message("Demo location added.")

    async def open_directions(e):
        # Google Maps is opened only after coordinates have been captured or selected.
        if user_location["latitude"] is None or user_location["longitude"] is None:
            show_message("Use GPS location or demo location first.", is_error=True)
            return

        url = (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={user_location['latitude']},{user_location['longitude']}"
            f"&destination={KAFEI_LATITUDE},{KAFEI_LONGITUDE}"
        )

        await page.launch_url(url)

    def place_order(e):
        # The mobile order API requires login so the order can be linked to a user.
        if access_token["value"] is None:
            show_message("Please login before placing an order.", is_error=True)
            return

        if not cart_items:
            show_message("Cart is empty.", is_error=True)
            return

        try:
            payload = {
                "payment_method": "CASH",
                "latitude": user_location["latitude"],
                "longitude": user_location["longitude"],
                "distance_from_kafei": user_location["distance"],
                "items": [
                    {
                        "id": item["id"],
                        "quantity": item["quantity"],
                    }
                    for item in cart_items
                ],
            }

            response = requests.post(
                f"{API_BASE_URL}/order/api/place/",
                json=payload,
                headers=get_auth_headers(),
                timeout=10,
            )

            data = response.json()

            if response.status_code >= 400:
                show_message(str(data), is_error=True)
                return

            cart_items.clear()
            refresh_cart()

            order_id = data.get("order_id") or data.get("id")
            show_message(f"Order placed successfully. Order ID: {order_id}")

        except Exception as ex:
            show_message(f"Order error: {ex}", is_error=True)

    gps_button.on_click = capture_location
    demo_location_button.on_click = use_demo_location
    directions_button.on_click = open_directions

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Container(
                        padding=15,
                        border_radius=20,
                        bgcolor=ft.Colors.BROWN,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    "KAFEI Mobile",
                                    size=30,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    "Order coffee, view location, and place orders from your phone.",
                                    color=ft.Colors.WHITE,
                                ),
                            ],
                        ),
                    ),
                    status_text,
                    ft.Container(
                        padding=15,
                        border_radius=15,
                        bgcolor=ft.Colors.BROWN_50,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "Account",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                logged_in_text,
                                username_field,
                                email_field,
                                password_field,
                                ft.Row(
                                    wrap=True,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Login",
                                            on_click=login_user,
                                        ),
                                        ft.OutlinedButton(
                                            "Register",
                                            on_click=register_user,
                                        ),
                                        ft.TextButton(
                                            "Logout",
                                            on_click=logout_user,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Divider(),
                    ft.Text(
                        "Menu",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ElevatedButton(
                        "Load Menu",
                        on_click=load_menu,
                    ),
                    menu_column,
                    ft.Divider(),
                    ft.Text(
                        "Cart",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    cart_column,
                    ft.Divider(),
                    ft.Text(
                        "Location Map",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(
                        height=300,
                        border_radius=15,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=map_control,
                    ),
                    ft.Row(
                        wrap=True,
                        controls=[
                            gps_button,
                            demo_location_button,
                        ],
                    ),
                    location_text,
                    directions_button,
                    ft.Divider(),
                    ft.ElevatedButton(
                        "Place Mobile Order",
                        on_click=place_order,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BROWN,
                            color=ft.Colors.WHITE,
                        ),
                    ),
                ],
            )
        )
    )

    refresh_cart()


ft.app(target=main)