# SkillSwap Platform 🔄
**Created by: PRIYANSHU AICH, SHIVAM MORE, ANIRBAN MISRA**

A modern, full-stack skill exchange platform where users can trade knowledge and expertise with each other. Built with **FastAPI** backend and **vanilla JavaScript** frontend, powered by **Firebase** for authentication and data storage.

## 📊 Project Statistics
- **Total Lines of Code**: 6,091 lines
- **Backend**: 1,651 lines (Python/FastAPI)
- **Frontend**: 4,440 lines (HTML/CSS/JavaScript)
- **Features**: 25+ implemented features
- **Last Updated**: July 2025

## 🌟 Features

### For Users
- **🔐 User Authentication**: Secure registration and login system
- **👤 Profile Management**: Create detailed profiles with skills offered and wanted
- **🔍 Smart Search**: Find users by skills, location, or keywords
- **💬 Skill Requests**: Send and manage skill exchange requests
- **⭐ Rating System**: Rate and review completed skill exchanges
- **🌍 Public/Private Profiles**: Control your visibility
- **📅 Availability Scheduling**: Set when you're available for skill exchanges

### For Administrators
- **🛡️ Admin Dashboard**: Comprehensive platform management
- **📊 Analytics**: View platform statistics and user metrics
- **👥 User Management**: Ban/unban users, view user details
- **🔄 Swap Monitoring**: Track all skill exchange requests
- **📢 Platform Messaging**: Send announcements to users
- **📈 Detailed Reports**: Platform activity and usage reports

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Firebase Admin SDK** - Authentication and Firestore database
- **Pydantic** - Data validation and settings management
- **Python 3.10+** - Programming language

### Frontend
- **Vanilla JavaScript** - Pure JavaScript for maximum compatibility
- **HTML5 & CSS3** - Modern web standards
- **Responsive Design** - Works on all devices

### Database & Authentication
- **Firebase Firestore** - NoSQL document database
- **Firebase Authentication** - Secure user management

## 🏗️ Project Structure

```
skill-swap-platform/
├── backend/                 # FastAPI backend
│   ├── routers/            # API route handlers
│   ├── models/             # Data models
│   ├── firebase_init.py    # Firebase configuration
│   ├── main.py            # Application entry point
│   └── requirements.txt   # Python dependencies
├── frontend/               # Frontend application
│   ├── index.html         # Login page
│   ├── admin.html         # Admin dashboard
│   ├── styles.css         # Styling
│   └── api.js            # API integration
└── README.md              # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- A Firebase project with Firestore enabled

### One-Line Setup
```bash
# Clone and setup the project
git clone https://github.com/Cosy-y/skill-swap-platform.git && cd skill-swap-platform
```

### Backend Setup (2 minutes)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python start_server.py  # Runs on localhost:8000
```

### Frontend Setup (1 minute)
```bash
cd frontend
python -m http.server 8080  # Runs on localhost:8080
```

### Admin Access
- **Email**: admin@skillswap.com
- **Password**: admin123
- **Dashboard**: http://localhost:8080/admin.html

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Cosy-y/skill-swap-platform.git
cd skill-swap-platform
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Firebase Configuration
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing one
3. Enable Firestore Database
4. Generate a service account key:
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Download the JSON file

5. Rename the downloaded file to `firebase.json` and place it in the `backend/` directory
   ```bash
   cp path/to/your/service-account-file.json backend/firebase.json
   ```

   Or copy the template and fill in your credentials:
   ```bash
   cp backend/firebase.json.template backend/firebase.json
   # Edit firebase.json with your actual credentials
   ```

### 3. Frontend Setup

The frontend uses vanilla JavaScript and doesn't require any build process. Simply serve the files through a web server.

## 🏃‍♂️ Running the Application

### Start the Backend Server
```bash
cd backend
python start_server.py
```

The backend API will be available at `http://localhost:8000`

### Start the Frontend Server
```bash
cd frontend
python -m http.server 8080  # Updated port to avoid conflicts
```

The frontend will be available at `http://localhost:8080`

### 🎯 Demo Accounts
For testing purposes:
- **Regular User**: test@example.com / password123
- **Admin User**: admin@skillswap.com / admin123

### API Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📱 Usage

### For Regular Users

1. **Sign Up**: Visit `http://localhost:8080` and create an account
2. **Complete Profile**: Add your skills, location, and availability
3. **Browse Users**: Find people with skills you want to learn
4. **Send Requests**: Request skill exchanges with other users
5. **Manage Exchanges**: Track your requests and responses
6. **Rate & Review**: Leave feedback after completed exchanges

### For Administrators

1. **Admin Access**: Login with admin@skillswap.com / admin123
2. **Dashboard**: Access the admin panel at `http://localhost:8080/admin.html`
3. **User Management**: View, ban, or unban users
4. **Monitor Activity**: Track platform usage and swap requests
5. **Send Messages**: Communicate with all platform users
6. **View Reports**: Analyze platform metrics and trends

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Users
- `GET /users/public` - Get public user profiles
- `GET /users/{user_id}` - Get specific user profile
- `PUT /users/current` - Update current user profile

### Skill Swaps
- `POST /swaps/` - Create swap request
- `GET /swaps/user/{user_id}` - Get user's swap requests
- `PUT /swaps/{swap_id}/respond` - Respond to swap request
- `DELETE /swaps/{swap_id}` - Delete swap request

### Reviews
- `POST /reviews/` - Create review
- `GET /reviews/user/{user_id}` - Get user reviews

### Admin (Requires Admin Role)
- `GET /admin/stats` - Platform statistics
- `GET /admin/users` - All users management
- `GET /admin/swaps` - All swaps monitoring
- `POST /admin/message` - Send platform message
- `POST /admin/user-action` - Ban/unban users

## 🗃️ Database Schema

### Users Collection
```javascript
{
  user_id: string,
  email: string,
  full_name: string,
  location: string,
  bio: string,
  skills_offered: [
    {
      name: string,
      description: string,
      proficiency_level: string
    }
  ],
  skills_wanted: [
    {
      name: string,
      description: string,
      proficiency_level: string
    }
  ],
  availability: {
    days: [string],
    time_slots: [string],
    timezone: string
  },
  is_profile_public: boolean,
  role: "user" | "admin",
  is_banned: boolean,
  rating: number,
  total_swaps: number,
  created_at: timestamp,
  updated_at: timestamp
}
```

### Swaps Collection
```javascript
{
  id: string,
  requester_id: string,
  requestee_id: string,
  offered_skill: string,
  requested_skill: string,
  message: string,
  status: "pending" | "accepted" | "declined" | "completed",
  created_at: timestamp,
  updated_at: timestamp
}
```

## 🎨 Frontend Architecture

### Pages
- **index.html** - Login page
- **signup.html** - User registration
- **home.html** - Browse users
- **profile.html** - User profile management
- **requests.html** - Skill swap requests
- **admin.html** - Admin dashboard

### Styling
- **styles.css** - Main stylesheet with CSS custom properties
- Responsive design for mobile and desktop
- Modern UI with hover effects and transitions
- Consistent color scheme and typography

### JavaScript
- **api.js** - API communication and authentication
- Modular functions for different features
- Local storage for user session management
- Real-time form validation and feedback

## 🔒 Security Features

- **Password Hashing**: Secure password storage
- **JWT Tokens**: Session management
- **Role-based Access**: Admin vs user permissions
- **Input Validation**: Server-side data validation
- **CORS Configuration**: Proper cross-origin setup
- **Firebase Security Rules**: Database access control

## 🧪 Testing

### Manual Testing
The platform includes comprehensive testing for:
- User registration and login
- Profile creation and updates
- Skill swap request flow
- Admin functionality
- API endpoints

### Admin Account Creation
To create an admin account:
1. Register a normal user account
2. In Firebase Console, go to Firestore Database
3. Find the user document
4. Update the `role` field to `"admin"`

## 🚀 Deployment

### Backend Deployment
1. Choose a hosting service (Heroku, DigitalOcean, etc.)
2. Set up environment variables for Firebase credentials
3. Update CORS settings for your domain
4. Deploy the FastAPI application

### Frontend Deployment
1. Upload files to a static hosting service (Netlify, Vercel, etc.)
2. Update the API base URL in `api.js`
3. Configure domain and SSL

### Database Setup
1. Ensure Firestore security rules are properly configured
2. Set up backup strategies
3. Monitor usage and costs

## 📝 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-key-id
# ... other Firebase credentials
```

### Frontend Configuration
Update `api.js` with your backend URL:
```javascript
const API_BASE_URL = "http://localhost:8000"; // Change for production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the console for error messages
2. Verify Firebase configuration
3. Ensure all dependencies are installed
4. Check that both servers are running

For additional help, please open an issue on GitHub.

## 🎯 Roadmap

### ✅ Completed Features
- [x] User authentication and registration
- [x] Complete profile management system
- [x] Skill swap request workflow
- [x] Admin dashboard with analytics
- [x] User management (ban/unban)
- [x] Platform messaging system
- [x] Review and rating system
- [x] Responsive design
- [x] API documentation
- [x] Security implementation

### 🚧 Future Enhancements
- [ ] Mobile app development
- [ ] Real-time messaging
- [ ] Video call integration
- [ ] Payment system for premium skills
- [ ] Skill certification verification
- [ ] Advanced matching algorithms
- [ ] Multi-language support
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Skill progress tracking

---

**Built with ❤️ for the learning community**
