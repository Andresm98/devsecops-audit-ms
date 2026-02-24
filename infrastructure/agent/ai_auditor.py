import os
import sys
from google import genai # Nueva forma de importar

def analyze_infrastructure():
    # Inicializar el cliente con la nueva librería
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model_id = "gemini-flash-latest" # Confirmamos el ID estable

    reports = ""

    # Lectura de archivos (Mantenemos tu lógica que es correcta)
    if os.path.exists("checkov-report.txt"):
        with open("checkov-report.txt", "r") as f:
            reports += "\n--- CHECKOV IAC REPORT ---\n" + f.read()

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
        # Nueva sintaxis para generar contenido
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )

        analysis = response.text
        print("\n=== ANÁLISIS DEL AGENTE AI ===\n")

        # Guardar el análisis en un archivo Markdown para el PR
        with open("ai_report.md", "w") as f:
            f.write("### 🤖 DevSecOps AI Auditor Report\n")
            f.write(analysis)

        print(analysis)

        if "success" in analysis.lower():
            sys.exit(0)
        else:
            print("\n[AI AGENT] Pipeline abortado por riesgos detectados.")
            sys.exit(1)

    except Exception as e:
        print(f"Error crítico en el Agente AI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_infrastructure()