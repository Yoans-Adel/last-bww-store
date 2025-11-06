# BWW Store - Unified E-commerce Platform

## 🚀 Overview

BWW Store is a comprehensive e-commerce platform specifically designed for the Egyptian market. It's a unified codebase merging functionality from multiple repositories, featuring:

- **AI-Powered Chatbot** with Egyptian Arabic dialect support
- **Multi-Backend Architecture** (Python Flask + Node.js Express)
- **Modern React Frontend** with Arabic localization
- **Mobile App Support** (React Native)
- **Multi-Platform Integration** (Facebook Messenger, WhatsApp, Telegram)
- **Complete E-commerce Features** (Products, Orders, Payments, Shipping)

## ✨ Features

### 🤖 AI Chatbot
- **Egyptian Arabic NLP**: Native support for Egyptian colloquial dialect
- **Intent Recognition**: Smart detection of user intentions
- **Context-Aware**: Multi-turn conversations with memory
- **Voice Support**: Speech-to-text for Arabic
- **Product Recommendations**: AI-powered product suggestions

### 💬 Multi-Platform Support
- Facebook Messenger integration
- WhatsApp Business API
- Telegram Bot
- Web Chat Widget
- Mobile App Chat

### 🛍️ E-commerce Features
- Product catalog with Arabic support
- Shopping cart and checkout
- Multiple payment methods (Paymob, Fawry, Vodafone Cash, Cash on Delivery)
- Order tracking and management
- User accounts and profiles

## 🛠️ Technology Stack

### Backend
- **Python**: Flask, SQLAlchemy, Transformers, NLTK, spaCy, Celery
- **Node.js**: Express, Mongoose, Socket.io, NLP.js
- **Databases**: MongoDB, Redis

### Frontend
- **React**: 18.x with Hooks
- **State Management**: Redux Toolkit
- **UI Framework**: Material-UI (MUI)
- **Build Tool**: Vite

### Mobile
- **Framework**: React Native
- **Navigation**: React Navigation

### DevOps
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.11+
- Node.js 18+
- MongoDB 7.0+
- Redis 7+

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yoans-Adel/last-bww-store.git
   cd last-bww-store
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the services**
   - Frontend: http://localhost
   - Python API: http://localhost:5000
   - Node.js API: http://localhost:3000

## 📁 Directory Structure

```
last-bww-store/
├── backend/
│   ├── python/              # Python Flask backend
│   │   ├── api/            # Flask API routes
│   │   ├── chatbot/        # Chatbot engines
│   │   ├── nlp/            # Egyptian NLP modules
│   │   ├── integrations/   # Social media integrations
│   │   ├── services/       # Business logic services
│   │   ├── database/       # Database handlers
│   │   └── utils/          # Utilities
│   │
│   └── nodejs/             # Node.js Express backend
│       └── src/            # Source code
│
├── frontend/               # React web application
│   └── src/               # Source code
│
├── mobile-app/             # React Native mobile app
│
├── docker/                 # Docker configurations
├── docs/                   # Documentation
└── scripts/               # Utility scripts
```

## 📚 API Documentation

### Python API Endpoints

- `POST /api/chat` - Process chat messages with Egyptian dialect
- `POST /api/products/recommend` - Get AI-powered recommendations
- `GET /api/orders/track` - Track order status
- `POST /api/speech-to-text` - Convert speech to text

### Node.js API Endpoints

- `GET /api/products` - List all products
- `POST /api/orders` - Create new order
- `POST /api/users/register` - Register new user
- `POST /api/webhooks/facebook` - Facebook webhook
- `POST /api/webhooks/whatsapp` - WhatsApp webhook

## 🌍 Localization

The platform supports Arabic (primary) and English:
- Egyptian Arabic dialect in chatbot
- RTL support for Arabic UI
- Bilingual product information
- Egyptian currency (EGP)

## 🔒 Security

- JWT authentication
- Rate limiting
- Input validation
- CORS configuration
- XSS protection

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project merges and enhances code from multiple BWW Store repositories:
- Bww-store (Python backend)
- Chatbot-E-commerce-Assistance-bot (AI services)
- bww-store (Node.js backend)
- bww-store-looks-like (React frontend)

---

**Made with ❤️ for the Egyptian E-commerce Market**
