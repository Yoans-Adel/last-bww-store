"""
Enhanced Chatbot Engine
Merged from multiple chatbot implementations
Supports Egyptian Arabic dialect and multiple intents
"""

import os
from typing import Dict, List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class EnhancedChatbotEngine:
    """
    Enhanced chatbot engine with support for:
    - Egyptian Arabic dialect
    - Context-aware responses
    - Multi-turn conversations
    - Intent-based responses
    - Product recommendations
    - Order tracking
    """
    
    def __init__(self):
        self.model_name = os.getenv('CHATBOT_MODEL', 'aubmindlab/bert-base-arabertv2')
        self.conversation_history = {}
        self.max_history = 10
        
        # Intent response templates
        self.response_templates = {
            'greeting': self._handle_greeting,
            'product_inquiry': self._handle_product_inquiry,
            'order_status': self._handle_order_status,
            'complaint': self._handle_complaint,
            'price_inquiry': self._handle_price_inquiry,
            'availability': self._handle_availability,
            'payment': self._handle_payment,
            'shipping': self._handle_shipping,
            'return': self._handle_return,
            'farewell': self._handle_farewell,
        }
        
    def generate_response(
        self,
        message: str,
        user_id: str,
        intent: str = None,
        language: str = 'ar',
        context: Dict = None
    ) -> str:
        """Generate chatbot response based on message and intent"""
        
        # Update conversation history
        self._update_history(user_id, message, 'user')
        
        # Get response based on intent
        if intent and intent in self.response_templates:
            response = self.response_templates[intent](message, user_id, context)
        else:
            response = self._generate_default_response(message, user_id, language)
        
        # Update history with bot response
        self._update_history(user_id, response, 'bot')
        
        return response
    
    def _handle_greeting(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle greeting intents"""
        greetings = [
            "أهلاً وسهلاً! أنا هنا لمساعدتك في BWW Store. إزاي أقدر أساعدك؟",
            "مرحباً بيك في BWW Store! عامل إيه؟ عايز تعرف إيه عن منتجاتنا؟",
            "السلام عليكم! نورت BWW Store. أقدر أساعدك في إيه؟",
        ]
        import random
        return random.choice(greetings)
    
    def _handle_product_inquiry(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle product inquiry intents"""
        return "عندنا مجموعة كبيرة من المنتجات. عايز تعرف عن منتج معين؟ قولي عايز إيه وهقولك كل حاجة عنه."
    
    def _handle_order_status(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle order status intents"""
        return "عشان أتابع طلبك، ممكن تديني رقم الطلب؟ أو لو عارف الإيميل اللي سجلت بيه، هقدر أجيب كل طلباتك."
    
    def _handle_complaint(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle complaint intents"""
        return "أنا آسف جداً للمشكلة اللي حصلت. ممكن تقولي تفاصيل المشكلة عشان أقدر أساعدك؟ راحتك وسعادتك مهمة جداً بالنسبالنا."
    
    def _handle_price_inquiry(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle price inquiry intents"""
        return "أسعارنا تنافسية جداً! قولي على المنتج اللي عايز تعرف سعره وهقولك كل التفاصيل والعروض المتاحة."
    
    def _handle_availability(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle availability intents"""
        return "عشان أتأكد من توفر المنتج، ممكن تقولي اسمه أو رقمه؟ وهشوف ليك المخزون فوراً."
    
    def _handle_payment(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle payment intents"""
        return "عندنا طرق دفع كتير: نقدي عند الاستلام، فيزا، فودافون كاش، وإنستاباي. أي طريقة تريحك؟"
    
    def _handle_shipping(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle shipping intents"""
        return "التوصيل بيكون خلال 2-5 أيام حسب المحافظة. التوصيل مجاني للطلبات فوق 500 جنيه. عايز تعرف المدة لمحافظة معينة؟"
    
    def _handle_return(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle return intents"""
        return "عندك 14 يوم من تاريخ الاستلام للإرجاع أو الاستبدال. المنتج لازم يكون بحالته الأصلية. محتاج تفاصيل أكتر؟"
    
    def _handle_farewell(self, message: str, user_id: str, context: Dict = None) -> str:
        """Handle farewell intents"""
        farewells = [
            "شكراً ليك! لو احتجت أي حاجة تاني أنا موجود دايماً. 😊",
            "العفو! يوم سعيد وإن شاء الله نشوفك تاني قريب!",
            "مع السلامة! BWW Store دايماً موجود لخدمتك.",
        ]
        import random
        return random.choice(farewells)
    
    def _generate_default_response(self, message: str, user_id: str, language: str) -> str:
        """Generate default response when no intent is matched"""
        return "معلش مفهمتش قصدك بالظبط. ممكن توضح أكتر؟ أو ممكن تسأل عن: المنتجات، الأسعار، التوصيل، أو الطلبات."
    
    def _update_history(self, user_id: str, message: str, sender: str):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'sender': sender,
            'message': message,
            'timestamp': None  # Add proper timestamp
        })
        
        # Keep only last N messages
        if len(self.conversation_history[user_id]) > self.max_history:
            self.conversation_history[user_id] = self.conversation_history[user_id][-self.max_history:]
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for a user"""
        return self.conversation_history.get(user_id, [])
    
    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
