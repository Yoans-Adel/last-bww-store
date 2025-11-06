"""
Egyptian NLP Module
Handles Egyptian Arabic dialect processing
"""

import re
from typing import Dict, List
import nltk


class EgyptianNLP:
    """
    Natural Language Processing for Egyptian Arabic dialect
    Handles colloquial Egyptian expressions and transforms them
    """
    
    def __init__(self):
        # Egyptian dialect to MSA mappings
        self.dialect_mappings = {
            # Greetings
            'ازيك': 'كيف حالك',
            'ازاي': 'كيف',
            'إزاي': 'كيف',
            'إيه': 'ماذا',
            'ايه': 'ماذا',
            'عامل ايه': 'كيف حالك',
            'عامل إيه': 'كيف حالك',
            
            # Questions
            'فين': 'أين',
            'منين': 'من أين',
            'امتى': 'متى',
            'ليه': 'لماذا',
            
            # Common words
            'عايز': 'أريد',
            'عاوز': 'أريد',
            'محتاج': 'أحتاج',
            'بدي': 'أريد',
            'ممكن': 'هل يمكن',
            'ينفع': 'هل يمكن',
            
            # Products
            'حاجة': 'شيء',
            'حاجه': 'شيء',
            'هدوم': 'ملابس',
            
            # Prices
            'بكام': 'بكم',
            'بقد ايه': 'بكم',
            'سعر': 'سعر',
            
            # Affirmatives
            'اه': 'نعم',
            'آه': 'نعم',
            'ايوه': 'نعم',
            'أيوة': 'نعم',
            'تمام': 'نعم',
            'ماشي': 'نعم',
            
            # Negatives
            'لا': 'لا',
            'لأ': 'لا',
            'مش': 'ليس',
            'ما': 'لا',
        }
        
        # Common Egyptian expressions
        self.expressions = {
            'يا سلام': 'رائع',
            'يا نهار': 'يا للعجب',
            'الله': 'حسناً',
            'ربنا يخليك': 'شكراً',
            'جزاك الله خيراً': 'شكراً',
        }
        
    def process(self, text: str) -> str:
        """
        Process Egyptian Arabic text and normalize it
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.strip()
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Apply dialect mappings
        processed_text = self._apply_mappings(text)
        
        # Normalize Arabic characters
        processed_text = self._normalize_arabic(processed_text)
        
        return processed_text
    
    def _apply_mappings(self, text: str) -> str:
        """Apply Egyptian dialect to MSA mappings"""
        words = text.split()
        processed_words = []
        
        for word in words:
            # Check if word exists in mappings
            if word in self.dialect_mappings:
                processed_words.append(self.dialect_mappings[word])
            else:
                processed_words.append(word)
        
        return ' '.join(processed_words)
    
    def _normalize_arabic(self, text: str) -> str:
        """Normalize Arabic text"""
        # Normalize alef variations
        text = re.sub('[إأٱآا]', 'ا', text)
        
        # Normalize teh marbuta
        text = re.sub('ة', 'ه', text)
        
        # Remove diacritics
        text = re.sub(r'[\u064B-\u065F]', '', text)
        
        return text
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        entities = {
            'products': [],
            'prices': [],
            'locations': [],
            'dates': []
        }
        
        # Extract price mentions
        price_pattern = r'\d+\s*(جنيه|ج\.م|pounds?|EGP)'
        prices = re.findall(price_pattern, text, re.IGNORECASE)
        entities['prices'] = prices
        
        return entities
    
    def detect_intent_keywords(self, text: str) -> List[str]:
        """Detect intent keywords in text"""
        intent_keywords = {
            'greeting': ['مرحبا', 'أهلا', 'السلام', 'صباح', 'مساء'],
            'product': ['منتج', 'حاجة', 'عايز', 'محتاج', 'بدور'],
            'price': ['سعر', 'بكام', 'تمن', 'كام'],
            'order': ['طلب', 'أوردر', 'شحنة'],
            'complaint': ['مشكلة', 'شكوى', 'زعلان', 'غلط'],
        }
        
        detected = []
        text_lower = text.lower()
        
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected.append(intent)
                    break
        
        return detected
