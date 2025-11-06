"""
Basic Chatbot Engine
Simple implementation for backward compatibility
"""

class ChatbotEngine:
    """Basic chatbot engine"""
    
    def __init__(self):
        self.responses = {}
    
    def process(self, message: str, user_id: str = None) -> str:
        """Process a message and return a response"""
        # This is a placeholder - real implementation would be more complex
        return "مرحباً! كيف يمكنني مساعدتك؟"
    
    def train(self, training_data):
        """Train the chatbot with new data"""
        pass
