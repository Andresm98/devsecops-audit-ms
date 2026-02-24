# Etapa 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go mod init audit-service && go build -o audit-service main.go

# Etapa 2: Runtime (Seguridad Máxima)
FROM gcr.io/distroless/static-debian11
COPY --from=builder /app/audit-service /
USER nonroot:nonroot
EXPOSE 8080
CMD ["/audit-service"]