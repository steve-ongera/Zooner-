# Zooner - Local Business Discovery & Social Platform

A comprehensive business directory and social media platform that connects local businesses with customers through an engaging, location-based community experience.

## 🎯 Overview

Zooner is a modern business discovery platform designed to help users find and connect with local businesses while providing businesses with powerful tools to engage their community. The platform combines business directory functionality with social media features, creating a unique ecosystem for local commerce.

## ✨ Key Features

### For Users
- **Business Discovery**: Find local businesses by category, location, and services
- **Social Feed**: Follow businesses and stay updated with their latest posts
- **Interactive Engagement**: Like, comment, and share business content
- **Direct Messaging**: Chat directly with business owners
- **Location-based Search**: Discover businesses in your area
- **User Reviews & Ratings**: Share experiences and read community feedback

### For Businesses
- **Business Profiles**: Create comprehensive business listings with photos, hours, and contact info
- **Content Publishing**: Share updates, promotions, events, and product showcases
- **Customer Engagement**: Respond to comments and messages from customers
- **Analytics Dashboard**: Track profile views, engagement, and follower growth
- **Verification System**: Get verified status for increased credibility
- **Multi-media Posts**: Share images and videos to showcase products/services

### For Administrators
- **Content Moderation**: Review and manage reported content
- **Business Verification**: Approve and verify business listings
- **User Management**: Manage user accounts and roles
- **Analytics & Insights**: Platform-wide analytics and business intelligence
- **Notification System**: Send system-wide announcements

## 🏗 Architecture

### Technology Stack

#### Backend
- **Framework**: Django 4.x with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT Token Authentication
- **File Storage**: Django File Storage (configurable for cloud storage)
- **API Documentation**: OpenAPI/Swagger

#### Frontend (Web)
- **Framework**: React.js
- **State Management**: Redux/Context API
- **UI Framework**: Material-UI / Tailwind CSS
- **HTTP Client**: Axios
- **Real-time**: WebSocket connections

#### Mobile (Android)
- **Language**: Kotlin
- **Architecture**: MVVM with Repository Pattern
- **HTTP Client**: Retrofit2
- **Image Loading**: Glide/Coil
- **Database**: Room (local caching)
- **Navigation**: Navigation Component

#### Infrastructure
- **API**: RESTful API with Django REST Framework
- **Real-time**: WebSocket for chat and notifications
- **Media Storage**: Configurable (local, AWS S3, CloudFlare)
- **Caching**: Redis (optional)
- **Search**: PostgreSQL Full-text Search

## 📊 Data Models

### Core Models

#### User Management
- **User**: Extended Django user with roles (user, business, admin)
- **Town**: Location-based filtering and business organization
- **Category**: Business categorization system

#### Business Management
- **Business**: Business profiles with location, contact, and media
- **Post**: Social media-style content from businesses
- **BusinessAnalytics**: Performance metrics and insights

#### Social Features
- **Follow**: User-business relationships
- **Like**: Post engagement tracking
- **Comment**: Threaded comments on posts
- **Chat/Message**: Direct messaging system

#### Platform Management
- **Notification**: System and user notifications
- **UserEngagement**: Analytics and user behavior tracking
- **ReportedContent**: Content moderation system

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Android Studio (for mobile development)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-org/zooner.git
cd zooner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
createdb zooner_db
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py loaddata initial_data.json

# Run development server
python manage.py runserver
```

### Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Mobile Setup (Android)

```bash
# Open Android Studio
# Import the android/ directory as a new project
# Sync project with Gradle files
# Update API_BASE_URL in Constants.kt
# Run on emulator or device
```

## 📡 API Documentation

### Authentication Endpoints
```
POST /api/auth/login/          # User login
POST /api/auth/register/       # User registration
POST /api/auth/refresh/        # Token refresh
POST /api/auth/logout/         # User logout
```

### Business Endpoints
```
GET    /api/businesses/        # List businesses
POST   /api/businesses/        # Create business
GET    /api/businesses/{id}/   # Business details
PUT    /api/businesses/{id}/   # Update business
DELETE /api/businesses/{id}/   # Delete business
```

### Post Endpoints
```
GET    /api/posts/             # List posts (feed)
POST   /api/posts/             # Create post
GET    /api/posts/{id}/        # Post details
PUT    /api/posts/{id}/        # Update post
DELETE /api/posts/{id}/        # Delete post
POST   /api/posts/{id}/like/   # Like/unlike post
```

### Social Endpoints
```
POST   /api/follow/            # Follow/unfollow business
GET    /api/comments/          # List comments
POST   /api/comments/          # Create comment
GET    /api/notifications/     # User notifications
```

### Chat Endpoints
```
GET    /api/chats/             # List user chats
POST   /api/chats/             # Create chat
GET    /api/chats/{id}/messages/ # Chat messages
POST   /api/messages/          # Send message
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/zooner_db

# Media Storage
MEDIA_ROOT=/path/to/media/files
STATIC_ROOT=/path/to/static/files

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# API Keys
GOOGLE_MAPS_API_KEY=your-google-maps-key
PUSH_NOTIFICATION_KEY=your-fcm-key
```

## 📱 Mobile App Features

### User Experience
- **Onboarding**: Smooth registration and location setup
- **Business Discovery**: Location-based business search with map integration
- **Social Feed**: Instagram-like feed with business posts
- **Profile Management**: User and business profile customization
- **Real-time Chat**: Instant messaging with businesses
- **Push Notifications**: Real-time updates and engagement alerts

### Technical Features
- **Offline Support**: Cache critical data for offline viewing
- **Image Optimization**: Automatic image compression and caching
- **Location Services**: GPS integration for location-based features
- **Deep Linking**: Direct links to businesses and posts
- **Analytics Integration**: User behavior tracking and analytics

## 🌐 Web Application Features

### Responsive Design
- **Mobile-first**: Optimized for mobile devices
- **Progressive Web App**: PWA capabilities for app-like experience
- **Cross-browser**: Support for all modern browsers

### Advanced Features
- **Real-time Updates**: WebSocket integration for live updates
- **Advanced Search**: Full-text search with filters
- **SEO Optimized**: Server-side rendering for better search visibility
- **Analytics Dashboard**: Comprehensive business analytics

## 🚦 Development Workflow

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
git commit -m "Add new feature"
git push origin feature/new-feature

# Create pull request for review
# Merge to main after approval
```

### Code Quality
```bash
# Backend linting
flake8 .
black .
isort .

# Frontend linting
npm run lint
npm run format

# Run tests
python manage.py test
npm test
```

## 🧪 Testing

### Backend Testing
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test zooner.tests.test_models

# Coverage report
coverage run --source='.' manage.py test
coverage report
```

### Frontend Testing
```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# E2E tests
npm run e2e
```

## 📊 Monitoring & Analytics

### Key Metrics
- **User Engagement**: Daily/Monthly Active Users
- **Business Growth**: New business registrations
- **Content Metrics**: Post engagement rates
- **Platform Health**: API response times, error rates

### Analytics Tools
- **User Analytics**: Track user behavior and engagement
- **Business Analytics**: Provide insights to business owners
- **Platform Analytics**: Monitor overall platform performance

## 🔐 Security

### Authentication & Authorization
- **JWT Tokens**: Secure API authentication
- **Role-based Access**: User, Business, Admin roles
- **Permission System**: Granular permission control

### Data Security
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Protection**: ORM-based database queries
- **File Upload Security**: Secure file handling and validation
- **Rate Limiting**: API rate limiting for abuse prevention

## 🚀 Deployment

### Production Deployment

#### Backend (Django)
```bash
# Install production dependencies
pip install -r requirements/production.txt

# Collect static files
python manage.py collectstatic

# Run database migrations
python manage.py migrate

# Start with Gunicorn
gunicorn zooner.wsgi:application
```

#### Frontend (React)
```bash
# Build for production
npm run build

# Serve with nginx or deploy to CDN
```

#### Database Migration
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Data migration (if needed)
python manage.py migrate_data
```

## 📈 Roadmap

### Phase 1 (Current)
- [x] Core business directory functionality
- [x] User authentication and profiles
- [x] Basic social features (posts, likes, comments)
- [x] Mobile app MVP

### Phase 2 (Next)
- [ ] Advanced search and filtering
- [ ] Business verification system
- [ ] Enhanced analytics dashboard
- [ ] Push notification system

### Phase 3 (Future)
- [ ] E-commerce integration
- [ ] Event management system
- [ ] Review and rating system
- [ ] Multi-language support

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and development process.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Backend Team**: Django/Python developers
- **Frontend Team**: React.js developers  
- **Mobile Team**: Android/Kotlin developers
- **DevOps Team**: Infrastructure and deployment
- **Product Team**: Product management and design

## 📞 Support

- **Documentation**: [docs.zooner.app](https://docs.zooner.app)
- **API Reference**: [api.zooner.app](https://api.zooner.app)
- **Community**: [community.zooner.app](https://community.zooner.app)
- **Email**: support@zooner.app

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- React.js community
- Android development community
- Open source contributors
- Local business community for feedback and support

---

steve ongera - Backend Developer