from abc import ABC, abstractmethod
from typing import Dict, Any

class RecommendationServiceInterface(ABC):
    """Interface for AI-based recommendation service following SOLID principles."""
    
    @abstractmethod
    def get_recommended_products(self, user_id: int, limit: int = 10) -> Dict[str, Any]:
        """
        Get personalized product recommendations for a user based on their chat history.
        
        Args:
            user_id: The user's ID
            limit: Maximum number of products to return per category
            
        Returns:
            Dictionary with categorized recommendations:
            {
                "highly_recommended": [products],
                "recommended": [products], 
                "not_recommended": [products],
                "user_preferences": {preferences},
                "has_chat_history": bool
            }
        """
        pass 