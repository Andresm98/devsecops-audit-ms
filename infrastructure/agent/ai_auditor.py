import os
import google.generativeai as genai
import sys

# Configuración de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_infrastructure():
    # Intentar leer reportes de seguridad generados en pasos previos
    try:
        with open("trivy-results.txt", "r") as f:
            security_logs = f.read()
    except FileNotFoundError:
        security_logs = "No se encontraron vulnerabilidades críticas detectadas por Trivy."

    prompt = f"""
    Eres un Technical Officer experto en DevSecOps. 
    Analiza los siguientes logs de seguridad de una infraestructura de microservicios:
    
    {security_logs}
    
    Instrucciones:
    1. Si no hay vulnerabilidades críticas, responde únicamente: "success, the workflow is ready to deploy in a cloud provider!! :D"
    2. Si hay fallos, realiza un informe detallado con:
       - Riesgo detectado.
       - Solución técnica inmediata.
       - Por qué este fallo bloquea el despliegue a la nube.
    """

    response = model.generate_content(prompt)
    print(response.text)

    if "success" in response.text.lower():
        sys.exit(0) # Todo bien, el pipeline continúa
    else:
        sys.exit(1) # Hay fallos, el pipeline se detiene

if __name__ == "__main__":
    analyze_infrastructure()