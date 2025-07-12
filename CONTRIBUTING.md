# Contributing to SkillSwap Platform 🤝

Thank you for your interest in contributing to SkillSwap! This guide will help you get started.

## 📋 Prerequisites

- Python 3.10 or higher
- Git
- A Firebase account (for testing with real data)
- Basic knowledge of Python, JavaScript, HTML/CSS

## 🚀 Quick Start

### 1. Fork and Clone
```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/skill-swap-platform.git
cd skill-swap-platform
```

### 2. Set Up Development Environment
```bash
# Backend setup
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Firebase (Optional)
For full functionality, set up Firebase:
1. Create a Firebase project
2. Download service account key
3. Save as `backend/firebase.json`

Or use the template for demo mode:
```bash
cp backend/firebase.json.template backend/firebase.json
```

### 4. Run the Application
```bash
# Terminal 1: Backend
cd backend
python start_server.py

# Terminal 2: Frontend
cd frontend
python -m http.server 3000
```

Visit `http://localhost:3000` to see the application.

## 🏗️ Project Structure

```
skill-swap-platform/
├── backend/                 # FastAPI backend
│   ├── models/             # Data models
│   │   ├── user.py        # User-related models
│   │   └── admin.py       # Admin-related models
│   ├── routers/           # API route handlers
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User management
│   │   ├── swaps.py       # Skill swap logic
│   │   ├── reviews.py     # Rating system
│   │   └── admin.py       # Admin features
│   ├── firebase_init.py   # Firebase connection
│   ├── main.py           # FastAPI application
│   └── start_server.py   # Development server
├── frontend/              # Vanilla JS frontend
│   ├── index.html        # Login page
│   ├── signup.html       # Registration
│   ├── home.html         # Browse users
│   ├── profile.html      # User profiles
│   ├── requests.html     # Skill requests
│   ├── admin.html        # Admin dashboard
│   ├── styles.css        # All styling
│   └── api.js           # API communication
└── docs/                 # Documentation
```

## 🎯 How to Contribute

### 1. Choose an Issue
- Check the [Issues](https://github.com/Cosy-y/skill-swap-platform/issues) page
- Look for labels like `good first issue` or `help wanted`
- Comment on the issue to let others know you're working on it

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Your Changes
Follow the coding standards below and test your changes thoroughly.

### 4. Commit Your Changes
```bash
git add .
git commit -m "Add: feature description"
# or
git commit -m "Fix: bug description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Coding Standards

### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused

Example:
```python
def create_user(user_data: UserCreate) -> UserResponse:
    """
    Create a new user account in the database.
    
    Args:
        user_data: User registration information
        
    Returns:
        UserResponse: Created user data
        
    Raises:
        HTTPException: If email already exists
    """
    # Implementation here...
```

### JavaScript (Frontend)
- Use modern ES6+ features
- Add comments for complex logic
- Keep functions small and focused
- Use descriptive variable names

Example:
```javascript
/**
 * Load and display user profiles from the API
 * @param {string} searchTerm - Optional search filter
 */
async function loadUsers(searchTerm = '') {
    try {
        // Implementation here...
    } catch (error) {
        console.error('Error loading users:', error);
    }
}
```

### CSS
- Use CSS custom properties (variables)
- Mobile-first responsive design
- Follow BEM naming convention when appropriate
- Group related styles together

## 🧪 Testing Guidelines

### Manual Testing
Before submitting a PR, test:
1. User registration and login
2. Profile creation and editing
3. Skill swap request flow
4. Admin features (if applicable)
5. Responsive design on mobile

### API Testing
Use the built-in Swagger UI at `http://localhost:8000/docs` to test API endpoints.

## 🚀 Feature Ideas

### Easy (Good for beginners)
- [ ] Add more skill categories
- [ ] Improve form validation messages
- [ ] Add loading animations
- [ ] Enhance mobile responsiveness
- [ ] Add more user profile fields

### Medium
- [ ] Real-time notifications
- [ ] Advanced search filters
- [ ] User messaging system
- [ ] Skill recommendation engine
- [ ] Export user data feature

### Advanced
- [ ] Video call integration
- [ ] Payment system
- [ ] Multi-language support
- [ ] Progressive Web App (PWA)
- [ ] Machine learning recommendations

## 🐛 Bug Reports

When reporting bugs, please include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Browser/OS information
5. Console error messages (if any)

## 💡 Feature Requests

For new features, please:
1. Check if it already exists in issues
2. Describe the problem it solves
3. Provide mockups or examples if possible
4. Consider the impact on existing users

## 📞 Getting Help

- Check the [documentation](README.md)
- Look through existing [issues](https://github.com/Cosy-y/skill-swap-platform/issues)
- Ask questions in issue comments
- Join discussions in Pull Requests

## 🏆 Recognition

Contributors will be:
- Listed in the project README
- Given credit in release notes
- Invited to become maintainers (for regular contributors)

## 📜 Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Focus on constructive feedback
- Keep discussions relevant to the project

---

**Happy coding! 🎉**
