terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.23.0"
    }
  }
}

provider "kind" {}

# Definición del Cluster Local "Audit-Cluster"
resource "kind_cluster" "audit_cluster" {
  name            = "devsecops-audit-cluster"
  node_image      = "kindest/node:v1.27.3"
  wait_for_ready  = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
    }
    node {
      role = "worker"
    }
  }
}

# 1. Configurar el Provider de Kubernetes con la salida del Cluster de Kind
provider "kubernetes" {
  host                   = kind_cluster.audit_cluster.endpoint
  client_certificate     = kind_cluster.audit_cluster.client_certificate
  client_key             = kind_cluster.audit_cluster.client_key
  cluster_ca_certificate = kind_cluster.audit_cluster.cluster_ca_certificate
}

# 2. Namespace para ArgoCD
resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
  # IMPORTANTE: Dependencia explícita para asegurar que el cluster exista antes
  depends_on = [kind_cluster.audit_cluster]
}

# 3. Instalación de ArgoCD con Server-Side Apply
resource "null_resource" "install_argocd" {
  provisioner "local-exec" {
    # Añadimos --server-side para evitar el error de límite de anotaciones (262144 bytes)
    command = "kubectl apply --server-side -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --context kind-${kind_cluster.audit_cluster.name}"
  }
  depends_on = [kubernetes_namespace.argocd]
}