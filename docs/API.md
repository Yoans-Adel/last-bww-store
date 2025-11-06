# BWW Store API Documentation

## Base URLs

- **Python Backend**: `http://localhost:5000/api`
- **Node.js Backend**: `http://localhost:3000/api`

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Python Backend Endpoints

### Chat API

#### POST /api/chat
Process chat messages with Egyptian dialect support.

**Request:**
```json
{
  "message": "عايز أشتري تيشرت",
  "user_id": "user123",
  "language": "ar"
}
```

**Response:**
```json
{
  "success": true,
  "response": "عندنا مجموعة كبيرة من التيشرتات. عايز تشوف إيه بالظبط؟",
  "intent": "product_inquiry",
  "language": "ar"
}
```

#### POST /api/products/recommend
Get AI-powered product recommendations.

**Request:**
```json
{
  "user_id": "user123",
  "preferences": {
    "category": "clothing",
    "price_range": [100, 500]
  }
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "id": "prod123",
      "name": "تيشرت قطن",
      "price": 250,
      "image": "https://..."
    }
  ]
}
```

#### GET /api/orders/track
Track order status.

**Query Parameters:**
- `order_id`: Order ID to track

**Response:**
```json
{
  "success": true,
  "order_id": "ORD123",
  "status": {
    "current": "in_transit",
    "updated_at": "2024-01-20T10:30:00Z",
    "estimated_delivery": "2024-01-22"
  }
}
```

#### POST /api/speech-to-text
Convert Arabic speech to text.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` file (mp3, wav, m4a)
- Form field: `language` (default: "ar-EG")

**Response:**
```json
{
  "success": true,
  "text": "عايز أشتري تيشرت",
  "language": "ar-EG"
}
```

#### POST /api/faq
Get FAQ answers.

**Request:**
```json
{
  "question": "إيه طرق الدفع المتاحة؟"
}
```

**Response:**
```json
{
  "success": true,
  "question": "إيه طرق الدفع المتاحة؟",
  "answer": "عندنا طرق دفع كتير: نقدي، فيزا، فودافون كاش، وإنستاباي"
}
```

### Webhooks

#### GET /api/webhook/facebook
Facebook webhook verification.

#### POST /api/webhook/facebook
Receive Facebook Messenger messages.

#### POST /api/webhook/whatsapp
Receive WhatsApp messages.

## Node.js Backend Endpoints

### Products

#### GET /api/products
List all products with pagination.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `category`: Filter by category
- `min_price`: Minimum price
- `max_price`: Maximum price

**Response:**
```json
{
  "success": true,
  "products": [
    {
      "_id": "prod123",
      "name": "T-Shirt",
      "nameAr": "تيشرت",
      "price": 250,
      "category": "clothing",
      "stock": 100,
      "images": ["url1", "url2"]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

#### GET /api/products/:id
Get single product details.

#### POST /api/products
Create new product (Admin only).

**Request:**
```json
{
  "name": "T-Shirt",
  "nameAr": "تيشرت",
  "description": "Cotton t-shirt",
  "descriptionAr": "تيشرت قطن",
  "price": 250,
  "category": "clothing",
  "stock": 100,
  "images": ["url1"]
}
```

### Orders

#### GET /api/orders
List user's orders.

#### POST /api/orders
Create new order.

**Request:**
```json
{
  "items": [
    {
      "productId": "prod123",
      "quantity": 2,
      "price": 250
    }
  ],
  "total": 500,
  "shipping_address": {
    "street": "123 Main St",
    "city": "Cairo",
    "governorate": "Cairo",
    "postal_code": "11511"
  },
  "payment_method": "cash_on_delivery"
}
```

### Users

#### POST /api/users/register
Register new user.

**Request:**
```json
{
  "name": "Ahmed Hassan",
  "email": "ahmed@example.com",
  "phone": "+201234567890",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "user123",
    "name": "Ahmed Hassan",
    "email": "ahmed@example.com"
  }
}
```

#### POST /api/users/login
User login.

**Request:**
```json
{
  "email": "ahmed@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user123",
    "name": "Ahmed Hassan",
    "email": "ahmed@example.com"
  }
}
```

### Chat

#### POST /api/chat/message
Send chat message.

**Request:**
```json
{
  "message": "مرحباً",
  "userId": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "response": "مرحباً! كيف يمكنني مساعدتك؟"
}
```

## Error Responses

All endpoints return errors in the following format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

API requests are limited to 100 requests per 15 minutes per IP address.

## Pagination

Endpoints that return lists support pagination:

```
GET /api/products?page=2&limit=20
```

Response includes pagination info:

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

## Localization

Include `Accept-Language` header for localized responses:

```
Accept-Language: ar
```

Supported languages:
- `ar`: Arabic (العربية)
- `en`: English
