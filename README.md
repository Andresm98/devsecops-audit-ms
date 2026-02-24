DevSecOps Sovereign: Audit Microservice Infrastructure
======================================================

📌 Visión General
-----------------

Este proyecto demuestra la implementación de un ecosistema **Sovereign DevSecOps** diseñado para el gobierno del ciclo de vida de microservicios. La solución no se limita al despliegue de una aplicación, sino a la creación de una **plataforma automatizada, segura y resiliente** bajo el paradigma de *Infrastructure as Code* (IaC), *GitOps*, y *AI-Ready DevOps Engine* para automatizar el pipelines E2E.

🏗️ Arquitectura del Sistema
----------------------------

La infraestructura ha sido diseñada siguiendo una estrategia **"Local-First, Cloud-Ready"**, permitiendo la validación completa en entornos on-premises antes de la promoción a nubes públicas (AWS/EKS).

-   **Orquestación:** Kubernetes (Kind/EKS).

-   **Provisionamiento:** Terraform (IAAS/PAAS).

-   **Motor de Despliegue:** ArgoCD (GitOps Pattern).

-   **Seguridad:** Shift-Left Security con escaneos estáticos y dinámicos.

* * * * *

🛡️ Implementación de Seguridad (Security-as-Code)
--------------------------------------------------

Se han establecido "Security Gates" en el pipeline de CI/CD para asegurar que ningún artefacto vulnerable alcance el clúster:

1.  **IaC Scanning (Checkov):** Análisis estático de archivos Terraform para prevenir configuraciones inseguras (ej. exposición de secretos, falta de cifrado).

2.  **Container Scanning (Trivy):** Escaneo de vulnerabilidades (CVEs) en imágenes Docker y sistema de archivos.

3.  **Secret Management:** * Limpieza proactiva de `tfstate` en el control de versiones.

    -   Uso de `ImagePullSecrets` con tokens de acceso limitado (PAT).

4.  **Runtime Hardening:** * Imágenes **Distroless** para reducir la superficie de ataque.

    -   Ejecución como usuario `non-root`.

    -   Sistema de archivos de solo lectura (`readOnlyRootFilesystem: true`).

* * * * *

🎡 Flujo de Entrega Continua (GitOps)
-------------------------------------

El proyecto elimina la intervención manual mediante un flujo circular de confianza:

1.  **Code & Push:** El desarrollador envía código al directorio `/src`.

2.  **Automated Build:** GitHub Actions compila el binario en Go, genera la imagen y la firma con el SHA del commit.

3.  **Manifest Update:** El pipeline actualiza automáticamente la etiqueta de la imagen en `k8s/apps/` mediante un bot.

4.  **ArgoCD Sync:** El controlador detecta el desvío en el repositorio y sincroniza el estado deseado en el clúster.

> **Resiliencia Probada:** El sistema cuenta con capacidades de *Self-Healing*. Cualquier modificación manual en el clúster es revertida automáticamente por ArgoCD para coincidir con la "Única Fuente de Verdad" (Git).

* * * * *

🛠️ Stack Tecnológico
---------------------

| **Capa** | **Tecnología** |
| --- | --- |
| **Infraestructura** | Terraform, Kubernetes (Kind) |
| **CI/CD Pipeline** | GitHub Actions |
| **Container Registry** | GitHub Container Registry (GHCR) |
| **GitOps Operator** | ArgoCD |
| **Microservicio** | Golang (Audit API) |
| **Seguridad** | Checkov, Trivy, Gitleaks |

* * * * *

🚀 Ejecución Local
------------------

### Prerrequisitos

-   Docker & Kind

-   Terraform

-   Kubectl

### Despliegue de la Plataforma

Bash

```
# Inicializar infraestructura
cd infrastructure/terraform
terraform init
terraform apply

# Configurar acceso a ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8081:443

```

* * * * *

📈 Valor para el Negocio (TO Perspective)
-----------------------------------------

-   **Gobernanza:** Trazabilidad total de cada cambio en la infraestructura y aplicación.

-   **Eficiencia:** Reducción del *Time-to-Market* mediante automatización del ciclo de vida.

-   **Compliance:** Cumplimiento nativo de estándares de seguridad mediante políticas integradas en el pipeline.

* * * * *

## 🤖 AI-DevOps Sovereign Agent (Gemini 1.5 Flash)

El núcleo de gobernanza de este proyecto evoluciona de un pipeline estático a un **Agente de IA Autónomo**. Este componente actúa como el "Auditor Final" antes de cualquier promoción a entornos productivos.

### 🧠 Capacidades del Agente:
- **Razonamiento Contextual:** A diferencia de los escáneres tradicionales que solo listan errores, el agente analiza la severidad real cruzando los reportes de **Checkov** (IaC) y **Trivy** (App).
- **Decision Making:** El agente tiene la autoridad de ejecutar un `sys.exit(1)`, bloqueando el flujo de CI/CD si detecta riesgos que comprometan la soberanía del dato o la seguridad del clúster.
- **Reporting Ejecutivo:** Genera un análisis técnico detallado, proporcionando la solución exacta y el porqué del bloqueo.

### ⚙️ Lógica de Decisión del Auditor:
1. **Detección:** Recolecta artefactos de escaneo en formato raw.
2. **Evaluación:** Procesa los logs mediante el modelo **Gemini 1.5 Flash**.
3. **Sentencia:** - ✅ `Success`: Si la infraestructura es resiliente, autoriza el despliegue.
    - ❌ `Bloqueado`: Si detecta riesgos (ej. Llaves RSA, S3 Públicos, CVEs Críticos), detiene el ciclo de vida.

* * * * *

**Desarrollado por Andresm98** - *Solutions Architect Project Portfolio*