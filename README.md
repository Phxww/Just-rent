# RentalCars

![screenshot_home](/public/screenshot_home.png)

## Project Overview

RentalCars is a web application designed to streamline the process of renting cars. The project aims to provide a seamless user experience for browsing, booking, and managing car rentals. It includes both a customer-facing frontend and an administrative backend.

## Key Features

### User Authentication

- **Sign Up/Login/Logout**: Users can sign up with email and password or use Google for authentication. Authentication is required for most functionalities beyond browsing.
- **Third-Party Authentication**: Planned support for Google and Facebook login.

### Homepage

- **Popular Cars**: Browse popular car models.
- **Promotions**: View current promotional offers and discounts.

### Car Browsing

- **Comprehensive Filters**: Filter cars by brand, seating capacity, and model.
- **Favorites**: Users can add cars to their favorites for quick access.
- **Detailed Specifications**: View detailed specifications and images for each car.
- **Comparison Tool**: Compare specifications of multiple car models.

### Favorites Management

- **Authentication Required**: Only logged-in users can save favorites.
- **Interactive Icons**: Heart icon toggles between filled and empty states for favoriting/unfavoriting.
- **Notifications**: Receive alerts for price drops on favorited cars.

### Car Details

- **In-depth Information**: Access detailed information and images for each car model.
- **User Reviews**: Read reviews and ratings from other users.

### Booking System

- **Flexible Booking**: Choose pickup and drop-off locations and rental duration.
- **Availability Checks**: Real-time availability checks prevent double booking.
- **Online Payment**: Secure online payments through TapPay.
- **Booking Expiry**: Bookings expire if not completed within 15 minutes.

### User Profile

- **Profile Management**: Update username and phone number. Email updates are restricted.
- **Favorites List**: View and manage favorited cars.
- **Order History**: Track current and past bookings, including payment status.
- **Order Cancellation**: Cancel bookings directly from the profile page.
- **Avatar Upload**: Add or update profile pictures.

### Admin Dashboard

- **User Management**: Admins can view all customer profiles.
- **Car Inventory**: Add, remove, or update car details.
- **Order Management**: View and manage all orders placed through the platform.
- **Data Analytics**: Access usage statistics, rental trends, and generate reports.

## Development Technologies

### Frontend

- **HTML5/CSS**: Structure and styling of the web pages.
- **Bootstrap**: Responsive design framework.

### Backend

- **Python**: Primary programming language.
- **Flask**: Web framework for server-side logic.
- **MySQL**: Database management system.
- **SQLAlchemy**: ORM for database interactions.
- **Flask-Migrate**: Handles database migrations.

### DevOps

- **Containerization**: Docker (In Progress)
- **Deployment**: AWS (In Progress)

## Development Approach

- **Frontend**: Client-Side Rendering (CSR)
- **Backend**: Server-Side Rendering (SSR)
- **Architecture**: MTV (Model-Template-View) pattern

## Getting Started

To get started with the RentalCars project, clone the repository and follow the instructions in the setup guide. Ensure you have the necessary dependencies installed and configured before running the application.

```bash
... 
```


## Future Enhancements

- **Containerization**: Complete Docker integration for seamless deployment.
- **AWS Deployment**: Deploy the application on AWS for scalability and reliability.
- **Enhanced Notifications**: Add push notifications for booking reminders and promotional offers.
- **User Reviews**: Implement a user review system for cars.
- **Social Sharing**: Enable users to share their favorite cars with friends and family.

