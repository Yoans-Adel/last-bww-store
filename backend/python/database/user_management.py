"""User Management"""

class UserManagement:
    def create_user(self, data):
        """Create new user"""
        return {"id": "1", "name": data.get("name")}
