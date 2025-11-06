"""
Egyptian Intent Handler
Detects user intents from Egyptian Arabic messages
"""

from typing import Dict, Optional
import re


class EgyptianIntentHandler:
    """Handle intent detection for Egyptian Arabic"""
    
    def __init__(self):
        self.intent_patterns = {
            'greeting': [
                r'(السلام|مرحبا|أهلا|صباح|مساء|ازيك|عامل|ايه|إيه)',
            ],
            'product_inquiry': [
                r'(عايز|محتاج|عاوز|بدور على|ابحث عن|منتج|حاجة)',
            ],
            'order_status': [
                r'(طلب|أوردر|شحنة|وين|فين|وصل|متى يصل)',
            ],
            'price_inquiry': [
                r'(سعر|بكام|كام|تمن|ثمن|قد ايه)',
            ],
            'availability': [
                r'(متوفر|موجود|عندكم|في المخزون)',
            ],
            'complaint': [
                r'(مشكلة|شكوى|غلط|خطأ|زعلان|مش راضي)',
            ],
            'payment': [
                r'(دفع|الدفع|كاش|فيزا|فودافون كاش|انستاباي)',
            ],
            'shipping': [
                r'(توصيل|شحن|التوصيل|الشحن|يوصل|متى يصل)',
            ],
            'return': [
                r'(ارجاع|استرجاع|استبدال|رجوع)',
            ],
            'farewell': [
                r'(شكرا|مع السلامة|باي|وداعا|تمام كده)',
            ],
        }
    
    def detect_intent(self, text: str) -> Optional[str]:
        """Detect intent from text"""
        if not text:
            return None
        
        text = text.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return intent
        
        return None
    
    def extract_intent_params(self, text: str, intent: str) -> Dict:
        """Extract parameters based on detected intent"""
        params = {}
        
        if intent == 'order_status':
            # Extract order ID
            order_id_pattern = r'#?(\d+)'
            match = re.search(order_id_pattern, text)
            if match:
                params['order_id'] = match.group(1)
        
        elif intent == 'product_inquiry':
            # Extract product name (simplified)
            params['query'] = text
        
        return params
