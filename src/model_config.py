from google import genai
from google.genai import types
import os

def get_client():
    """Configura o cliente unificado para Vertex AI."""
    return genai.Client(
        vertexai=True,
        project="llm-studies",
        location="us-central1"
    )

def call_model(client, model_name, temp, prompt, content):
    """Chama o Gemini usando o novo SDK google-genai."""
    
    # Configuração de Geração
    generate_content_config = types.GenerateContentConfig(
        temperature=temp,
        response_mime_type="application/json",
        # ThinkingConfig é opcional, use apenas se precisar de raciocínio profundo
        # thinking_config=types.ThinkingConfig(include_thoughts=True) if "pro" in model_name else None,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
        ],
    )

    # Chamada do Modelo
    response = client.models.generate_content(
        model=model_name,
        contents=[content, prompt],
        config=generate_content_config,
    )

    return ModelResp(response)

class ModelResp:
    def __init__(self, response):
        # No novo SDK, os metadados são mais acessíveis
        self.modelVersion = response.model_version or "gemini-3.1-pro"
        self.totalTokenCount = response.usage_metadata.total_token_count or 0
        
        candidate = response.candidates[0]
        self.finish_reason = str(candidate.finish_reason)
        
        # Mapeamento de Safety Ratings para o seu BigQuery
        self.safetyRatings = []
        if candidate.safety_ratings:
            for sr in candidate.safety_ratings:
                self.safetyRatings.append({
                    "category": sr.category,
                    "probability": sr.probability,
                    "blocked": sr.blocked or False,
                    "probability_score": sr.probability_score or 0.0,
                    "severity": sr.severity or "NEUTRAL",
                    "severity_score": sr.severity_score or 0.0
                })

        # Conteúdo Final (JSON)
        if self.finish_reason == "FinishReason.STOP" or self.finish_reason == "STOP":
            self.text = candidate.content.parts[0].text
        else:
            self.text = '{"authors": [{"author": "CENSURADO"}]}'