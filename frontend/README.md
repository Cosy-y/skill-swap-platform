# Skill Swap Platform - Frontend

This is the frontend for our skill swap platform. It's built with plain HTML, CSS, and JavaScript - keeping it simple and easy to understand.

## Files Overview

### HTML Pages
- **index.html** - Login page where users sign in
- **home.html** - Main page showing all users and their skills
- **profile.html** - User's own profile page for editing info
- **user-profile.html** - View other users' profiles  
- **swap-request.html** - Form to request a skill swap
- **requests.html** - Manage incoming and outgoing swap requests

### Styling
- **styles.css** - All the CSS styles for the entire frontend

## Design
- Navy blue (#1e3a8a) as the main color
- Clean white backgrounds
- Modern card-based layout
- Responsive design that works on mobile
- Amateur-friendly code (no fancy frameworks)

## How to Use
1. Open index.html in your browser to start
2. The pages are linked together with navigation
3. Currently uses sample data - will connect to backend API later
4. All the forms and buttons have basic JavaScript functionality

## Features
- User authentication (login page)
- Browse users and their skills
- Search and filter users
- View detailed user profiles
- Create skill swap requests  
- Manage swap requests (accept/reject)
- Edit your own profile

## Backend Integration
The frontend is designed to work with our FastAPI backend. You'll need to:
1. Update the API URLs in the JavaScript code
2. Connect the authentication system
3. Replace sample data with real API calls

## Browser Compatibility
Works in all modern browsers - Chrome, Firefox, Safari, Edge. No special requirements.
