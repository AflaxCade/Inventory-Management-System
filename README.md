# Inventory Management System

An Inventory Management application built using Django. This application provides user authentication, dashboard analytics, and robust management features for customers, suppliers, categories, products, and orders. It also supports invoice generation and data visualization.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Note](#note)
- [Contributing](#contributing)
- [License](#license)

## Features

### Authentication
- **Login:** Users can log in using either their username or email and password.
- **Login with Gmail:** Google authentication support for seamless login.
- **Sign Up:** Users can register for a new account.
- **Logout:** Users can securely log out.
- **Forgot Password:** Sends an email with a password reset token link to help users reset their password.

### User Profile
- Manage user profiles, including the ability to upload a profile photo.

### Dashboard
The dashboard displays key performance indicators (KPIs) and visualizations:
- **Recent Orders:** Table or list of the most recent orders.
- **Monthly Earnings (KPI):** Total earnings for the current month.
- **Annual Sales (KPI):** Total sales for the year.
- **Total Customers (KPI):** Total number of registered customers.
- **Pending Orders (KPI):** Number of orders still pending.
- **Donut Chart:** Displays order status distribution (e.g., Pending, Delivered, Cancelled).
- **Bar Chart:** Highlights the top-selling products.

### Management Modules
- **Customer Management:** Add, update, and manage customer information.
- **Supplier Management:** Manage suppliers and their details.
- **Category Management:** Organize products into categories.
- **Product Management:** Add, edit, and manage inventory products.
- **Order Management:**
  - Create and manage orders with a single product.
  - Create and manage orders with multiple products.
- **Invoice Management:** Generate and manage invoices for orders.

## Installation

### Prerequisites
- Python 3.13+
- Django 5.1+

### Steps
1. **Clone the repository:**

   ```bash
   git clone https://github.com/AflaxCade/Inventory-Management.git
   ```
   
2. **Navigate to the project directory**:

   ```bash
   cd Inventory-Management
   ```

3. **Create a virtual environment**:

```bash
python -m venv env
```

4. **Activate the virtual environmen**t:

- For Windows:

```bash
env\Scripts\activate
```

- For macOS and Linux:

```bash
source env/bin/activate
```

5. **Install the required dependencies**:

```bash
pip install -r requirements.txt
```

6. **Run the development server**:

```bash
python manage.py runserver
```

# Usage
- **Sign up or log in:** Use either username/email and password or Gmail for authentication.
- **Navigate the dashboard:** View KPIs, charts, and recent orders.
- **Manage records:** Use the management modules to add/update customers, suppliers, categories, products, and orders.
- **Generate invoices:** The invoice is automatically Created for completed orders.
- **Reset password:** Use the forgot password feature if needed.

## Note
A `.env` file must be created in the project root directory with the following configuration:

```env
DEBUG=True
SECRET_KEY=6UHgE9N_jAna4tKAnH_AvkuB9PZ28c0XtC5x8D3Gj6qJS9SIZ3Xc4XybWQLJyfNDuxw
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=Youremail@gmail.com
EMAIL_HOST_PASSWORD=XXXXXXXXXXX
EMAIL_PORT=587
EMAIL_USE_TLS=True

# GoogleOAuth2
OAUTH2_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
OAUTH2_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or additions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
