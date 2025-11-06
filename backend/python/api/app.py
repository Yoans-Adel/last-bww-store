"""
Flask API Application
Main entry point for the Python backend API
Merged from Chatbot-E-commerce-Assistance-bot
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Import modules from different services
from chatbot.chatbot_engine import ChatbotEngine
from chatbot.enhanced_chatbot_engine import EnhancedChatbotEngine
from nlp.egyptian_nlp import EgyptianNLP
from nlp.egyptian_intent_handler import EgyptianIntentHandler
from integrations.facebook_leads_integration import FacebookLeadsIntegration
from integrations.whatsapp_handler import WhatsAppHandler
from integrations.social_media_integration import SocialMediaIntegration
from services.recommendation_engine import RecommendationEngine
from services.order_tracker import OrderTracker
from services.order_collection_system import OrderCollectionSystem
from services.speech_to_text import SpeechToText
from services.faq_system import FAQSystem
from database.database_handler import DatabaseHandler
from database.user_management import UserManagement
from database.sync_products import sync_products
from utils.config import Config
from utils.logging_setup import setup_logging
from utils.notification import NotificationService
from utils.analytics import Analytics
from utils.monitoring import Monitoring

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
jwt = JWTManager(app)

# Setup logging
logger = setup_logging()

# Initialize services
chatbot_engine = EnhancedChatbotEngine()
egyptian_nlp = EgyptianNLP()
intent_handler = EgyptianIntentHandler()
recommendation_engine = RecommendationEngine()
order_tracker = OrderTracker()
faq_system = FAQSystem()
db_handler = DatabaseHandler()
user_management = UserManagement()
notification_service = NotificationService()
analytics = Analytics()
monitoring = Monitoring()

# Social media integrations
facebook_integration = FacebookLeadsIntegration()
whatsapp_handler = WhatsAppHandler()
social_media = SocialMediaIntegration()

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'BWW Store Python API',
        'version': '1.0.0',
        'features': [
            'Egyptian Arabic NLP',
            'AI Chatbot',
            'Multi-platform Integration',
            'Order Management',
            'Product Recommendations'
        ]
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', '')
        language = data.get('language', 'ar')  # Arabic by default
        
        # Process Egyptian dialect
        processed_message = egyptian_nlp.process(message)
        intent = intent_handler.detect_intent(processed_message)
        
        # Get chatbot response
        response = chatbot_engine.generate_response(
            message=processed_message,
            user_id=user_id,
            intent=intent,
            language=language
        )
        
        # Log analytics
        analytics.track_message(user_id, message, response)
        
        return jsonify({
            'success': True,
            'response': response,
            'intent': intent,
            'language': language
        })
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        monitoring.log_error('chat', str(e))
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/recommend', methods=['POST'])
def recommend_products():
    """Get product recommendations"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', '')
        preferences = data.get('preferences', {})
        
        recommendations = recommendation_engine.get_recommendations(
            user_id=user_id,
            preferences=preferences
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/track', methods=['GET'])
def track_order():
    """Track order status"""
    try:
        order_id = request.args.get('order_id', '')
        
        if not order_id:
            return jsonify({'success': False, 'error': 'Order ID required'}), 400
        
        status = order_tracker.track(order_id)
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'status': status
        })
    except Exception as e:
        logger.error(f"Error tracking order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/faq', methods=['POST'])
def get_faq():
    """Get FAQ answers"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        answer = faq_system.get_answer(question)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer
        })
    except Exception as e:
        logger.error(f"Error processing FAQ: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'ar-EG')
        
        speech_service = SpeechToText()
        text = speech_service.transcribe(audio_file, language)
        
        return jsonify({
            'success': True,
            'text': text,
            'language': language
        })
    except Exception as e:
        logger.error(f"Error in speech-to-text: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/webhook/facebook', methods=['GET', 'POST'])
def facebook_webhook():
    """Facebook Messenger webhook"""
    if request.method == 'GET':
        # Verification
        return facebook_integration.verify_webhook(request)
    else:
        # Process incoming message
        return facebook_integration.process_message(request)

@app.route('/api/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """WhatsApp webhook"""
    return whatsapp_handler.process_message(request)

@app.route('/api/products/sync', methods=['POST'])
def sync_products_route():
    """Sync products from external sources"""
    try:
        result = sync_products()
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        logger.error(f"Error syncing products: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    try:
        data = request.get_json()
        user = user_management.create_user(data)
        return jsonify({
            'success': True,
            'user': user
        })
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/report', methods=['GET'])
def get_analytics():
    """Get analytics report"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        report = analytics.get_report(start_date, end_date)
        
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
