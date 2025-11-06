"""Facebook Leads Integration"""

class FacebookLeadsIntegration:
    def __init__(self):
        pass
    
    def verify_webhook(self, request):
        """Verify Facebook webhook"""
        return "OK", 200
    
    def process_message(self, request):
        """Process Facebook message"""
        return {"status": "success"}, 200
