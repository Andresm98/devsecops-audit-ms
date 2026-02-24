package main

import (
        "fmt"
        "log"
        "net/http"
)

func main() {
        // Endpoint de Salud (Liveness/Readiness para K8s)
        http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
                w.WriteHeader(http.StatusOK)
                fmt.Fprint(w, "OK")
        })

        // Endpoint de Auditoría
        http.HandleFunc("/audit", func(w http.ResponseWriter, r *http.Request) {
                log.Println("Audit Event Received: Action log processed safely.")
                fmt.Fprint(w, "Event Logged")
        })

        fmt.Println("Audit Service running on port 8080...")
        log.Fatal(http.ListenAndServe(":8080", nil))
        log.Println("AI-Agent Status: Monitoring security logs.....!!!")
}