import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def get_system_prompt(business_type: str = "e-commerce") -> str:
    """Get the system prompt based on business type."""
    return (
        f"You are a helpful sales assistant for a {business_type} store. "
        "Always prioritize the context and products already mentioned in the conversation history if the user refers to 'those products', 'the previous ones', or similar. "
        "Only use the retrieved product list if the user is asking for new or additional options. "
        "Respond in a friendly and professional manner, based solely on the available products. "
        "If there are no relevant products, clearly indicate it. "
        "Always be helpful and provide accurate information about the products."
    )


def build_chat_prompt(
    docs: List[Any],
    user_msg: str,
    history: List[Dict[str, str]] = None,
    business_type: str = "e-commerce"
) -> List[Dict[str, str]]:
    """
    Build the list of messages to send to the LLM:
      1. System message with behavior instructions.
      2. Previous turns (history) to maintain context.
      3. Context block with retrieved documents (text + metadata).
      4. Current user message.

    Args:
        docs: List of document objects, each with:
          - page_content: str (indexed text: name+brand+features)
          - metadata: dict with keys 'price' and 'quantity'
        user_msg: Current user message
        history: List of dicts {'role':'user'|'assistant','content':str}
        business_type: Type of business (e.g., "e-commerce", "clothing store")
    
    Returns:
        List of message dictionaries for the LLM
    """
    try:
        messages = []
        
        system_prompt = get_system_prompt(business_type)
        messages.append({"role": "system", "content": system_prompt})
        
        if history:
            messages.extend(history)
        
        # 3) Add retrieved context
        if docs:
            context_lines = []
            for doc in docs:
                text = doc.page_content
                metadata = doc.metadata
                quantity = metadata.get('quantity', 'N/A')
                price = metadata.get('price', 'N/A')
                context_lines.append(
                    f"- {quantity}x {text} (Price: ${price})"
                )
            context_block = "\n".join(context_lines)
            messages.append({
                "role": "user",
                "content": f"Relevant context:\n{context_block}"
            })
        
        messages.append({
            "role": "user",
            "content": user_msg
        })
        
        logger.info("Built chat prompt with %d documents and %d history messages", len(docs), len(history) if history else 0)
        return messages
        
    except Exception as e:
        logger.error("Error building chat prompt: %s", str(e))
        raise 