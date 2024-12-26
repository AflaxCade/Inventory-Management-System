# Inventory Management System

An Inventory Management application built using Django. This application provides user authentication, dashboard analytics, and robust management features for customers, suppliers, categories, products, and orders. It also supports invoice generation and data visualization.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
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

---

## Installation
