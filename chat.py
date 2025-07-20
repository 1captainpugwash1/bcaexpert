from flask import Blueprint, request, jsonify
import requests
import os
import json
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

# Building Code knowledge base - simplified version for demo
BCA_KNOWLEDGE_BASE = {
    "fire_safety": {
        "section": "Section C",
        "content": "Fire safety requirements in the Building Code of Australia are primarily covered in Section C of the NCC. Buildings must comply with fire resistance levels (FRL) appropriate for their classification and use. Class 2 buildings (apartments) require specific fire separation between units and common areas.",
        "sources": [
            {
                "section": "Section C1.1",
                "title": "Fire Resistance",
                "excerpt": "An element is to have an FRL appropriate for its intended purpose, which shall be verified by testing, or calculation based on testing, in accordance with C1.2, C1.3 and C1.5."
            },
            {
                "section": "Section C2.2", 
                "title": "Fire Separation",
                "excerpt": "Fire separation must be provided between different fire compartments to prevent the spread of fire."
            }
        ]
    },
    "energy_efficiency": {
        "section": "Section J",
        "content": "Energy efficiency requirements are detailed in Section J of the NCC. The 2022 edition introduced stricter thermal performance standards, requiring buildings to achieve higher star ratings. New homes must now meet 7-star energy efficiency, up from the previous 6-star requirement.",
        "sources": [
            {
                "section": "Section J1.2",
                "title": "Energy Efficiency",
                "excerpt": "Buildings must achieve the energy efficiency requirements specified in this section."
            },
            {
                "section": "Section J1.5",
                "title": "Building Fabric", 
                "excerpt": "The building fabric must comply with thermal performance requirements to achieve the required energy efficiency."
            }
        ]
    },
    "structural": {
        "section": "Section B",
        "content": "Structural requirements are covered in Section B of the NCC. All structural elements must be designed to withstand the loads and forces they may reasonably be expected to experience during construction and use. This includes dead loads, live loads, wind loads, and seismic forces where applicable.",
        "sources": [
            {
                "section": "Section B1.2",
                "title": "Structural Provisions",
                "excerpt": "A building or structure must have structural integrity during construction and use."
            },
            {
                "section": "Section B1.4",
                "title": "Loads and Forces",
                "excerpt": "Structural elements must be designed for appropriate loads and forces as specified in the relevant Australian Standards."
            }
        ]
    },
    "accessibility": {
        "section": "Section D",
        "content": "Accessibility requirements are outlined in Section D of the NCC. Buildings must provide appropriate access and facilities for people with disabilities, including accessible paths of travel, doorways, ramps, and sanitary facilities.",
        "sources": [
            {
                "section": "Section D3.1",
                "title": "Access for People with Disabilities",
                "excerpt": "Buildings must provide access and facilities for people with disabilities in accordance with the Disability Discrimination Act."
            }
        ]
    }
}

def get_relevant_knowledge(query):
    """Simple keyword matching to find relevant BCA knowledge"""
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in ['fire', 'safety', 'flame', 'smoke']):
        return BCA_KNOWLEDGE_BASE['fire_safety']
    elif any(keyword in query_lower for keyword in ['energy', 'efficiency', 'thermal', 'star', 'rating']):
        return BCA_KNOWLEDGE_BASE['energy_efficiency']
    elif any(keyword in query_lower for keyword in ['structural', 'structure', 'load', 'force', 'beam', 'column']):
        return BCA_KNOWLEDGE_BASE['structural']
    elif any(keyword in query_lower for keyword in ['access', 'accessibility', 'disability', 'disabled']):
        return BCA_KNOWLEDGE_BASE['accessibility']
    else:
        return None

def call_gemini_api(system_prompt, user_message):
    """Call Gemini AI API using requests"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        api_base = os.getenv('OPENAI_API_BASE')
        
        if not api_key or not api_base:
            return "I'm sorry, the AI service is not properly configured. Please provide the API keys."
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gemini-2.5-flash',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            'max_tokens': 500,
            'temperature': 0.3
        }
        
        response = requests.post(
            f'{api_base}/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "I'm sorry, I'm having trouble processing your request right now."
            
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return "I'm sorry, I'm having trouble connecting to the AI service."

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get relevant BCA knowledge
        relevant_knowledge = get_relevant_knowledge(user_message)
        
        # Prepare system prompt with BCA context
        system_prompt = """You are BCA Expert, a specialized AI assistant for the Building Code of Australia (National Construction Code - NCC 2022). 

Your role is to provide accurate, helpful information about Australian building codes, regulations, and construction standards. Always:

1. Base your responses on the NCC 2022 and related Australian Standards
2. Provide specific section references when possible
3. Explain technical concepts in clear, professional language
4. Mention compliance pathways (deemed-to-satisfy vs alternative solutions)
5. Include relevant building classifications when applicable
6. Suggest consulting with building professionals for complex matters

If you don't have specific information about a query, acknowledge this and suggest where the user might find authoritative information."""

        # Add relevant knowledge to the context if found
        if relevant_knowledge:
            context = f"\nRelevant BCA Information:\n{relevant_knowledge['content']}\n\nSources:\n"
            for source in relevant_knowledge['sources']:
                context += f"- {source['section']}: {source['title']} - {source['excerpt']}\n"
            system_prompt += context

        # Generate response using Gemini AI
        bot_response = call_gemini_api(system_prompt, user_message)
        
        # Prepare response with sources
        response_data = {
            'response': bot_response,
            'sources': relevant_knowledge['sources'] if relevant_knowledge else [],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'BCA Expert Chat API'})

