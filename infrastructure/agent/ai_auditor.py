import os
import google.generativeai as genai
import sys

# Configuración de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_infrastructure():
    reports = ""

    # Intentar leer Checkov
    if os.path.exists("checkov-report.txt"):
        with open("checkov-report.txt", "r") as f:
            reports += "\n--- CHECKOV IAC REPORT ---\n" + f.read()

    # Intentar leer Trivy
    if os.path.exists("trivy-report.txt"):
        with open("trivy-report.txt", "r") as f:
            reports += "\n--- TRIVY SECURITY REPORT ---\n" + f.read()

    if not reports.strip():
        reports = "No vulnerability logs found. Everything seems clean."

    prompt = f"""
    Eres un Technical Officer Senior de NTT DATA experto en Ciberseguridad y Cloud.
    Analiza los siguientes reportes de seguridad de infraestructura (IaC) y contenedores:

    {reports}

    TAREA:
    1. Si no hay vulnerabilidades CRITICAL o HIGH, responde exactamente: "success, the workflow is ready to deploy in a cloud provider!! :D"
    2. Si detectas fallos serios (llaves privadas, puertos abiertos, CVEs críticos):
       - Realiza un resumen ejecutivo del riesgo.
       - Da la instrucción técnica exacta para corregirlo.
       - Finaliza con la palabra "BLOQUEADO".
    """

    try:
        response = model.generate_content(prompt)
        analysis = response.text
        print(analysis)

        # Lógica de decisión del Agente
        if "success" in analysis.lower():
            sys.exit(0)
        else:
            print("\n[AI AGENT] Pipeline abortado por riesgos de seguridad detectados.")
            sys.exit(1)

    except Exception as e:
        print(f"Error contactando al Agente AI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_infrastructure()