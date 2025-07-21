"""
Seed data for chat history to test the recommendation system.
This creates sample chat messages for different user types.
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.models.user import User

logger = logging.getLogger(__name__)

def seed_chat_history(db: Session):
    """Seed chat history with sample conversations for testing recommendations."""
    
    try:
        # Get existing users
        users = db.query(User).all()
        
        if not users:
            logger.warning("No users found. Please seed users first.")
            return
        
        # Sample conversations for different user types
        conversations = {
            'electronics_enthusiast': [
                "I'm looking for Arduino boards for my robotics project",
                "What's the best 3D printer under $500?",
                "I need sensors for an IoT project",
                "Can you recommend some Raspberry Pi accessories?",
                "I want to build a smart home automation system",
                "What tools do I need for electronics prototyping?",
                "I'm interested in learning about microcontrollers",
                "Do you have any wireless sensors available?"
            ],
            'maker_hobbyist': [
                "I want to start 3D printing as a hobby",
                "What's a good beginner's tool set for DIY projects?",
                "I'm building a custom desk and need some tools",
                "Can you recommend some safety equipment for woodworking?",
                "I want to learn Arduino programming",
                "What's the best way to organize my workshop?",
                "I need some basic hand tools for home repairs",
                "Do you have any project kits for beginners?"
            ],
            'professional_developer': [
                "I need a high-quality development setup",
                "What's the best laptop for software development?",
                "I'm looking for professional-grade tools",
                "Can you recommend some productivity accessories?",
                "I need reliable equipment for client work",
                "What's the best monitor for coding?",
                "I want to set up a home office for remote work",
                "Do you have any ergonomic equipment?"
            ],
            'budget_conscious': [
                "I'm looking for affordable electronics",
                "What's the cheapest way to get started with Arduino?",
                "I need tools but I'm on a tight budget",
                "Can you recommend some budget-friendly 3D printers?",
                "I want to learn but don't want to spend too much",
                "What are some good value-for-money tools?",
                "I need basic equipment for under $200",
                "Do you have any student discounts?"
            ]
        }
        
        # Create chat messages for each user type
        for i, (user_type, messages) in enumerate(conversations.items()):
            if i < len(users):
                user = users[i]
                
                # Create messages with timestamps
                base_time = datetime.now() - timedelta(days=30)
                
                for j, message in enumerate(messages):
                    chat_message = ChatMessage(
                        user_id=user.id,
                        message_type='user',
                        content=message,
                        session_id=f"session_{user.id}_{user_type}",
                        created_at=base_time + timedelta(hours=j*2)
                    )
                    db.add(chat_message)
                
                logger.info(f"Created {len(messages)} chat messages for user {user.id} ({user_type})")
        
        db.commit()
        logger.info("Chat history seeding completed successfully")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding chat history: {str(e)}")
        raise

if __name__ == "__main__":
    from db.session import SessionLocal
    db = SessionLocal()
    try:
        seed_chat_history(db)
    finally:
        db.close() 