FROM golang:1.25-alpine AS builder

WORKDIR /build

COPY go.mod go.sum* ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /app_bin ./cmd/server/main.go

FROM alpine:latest
WORKDIR /app

COPY --from=builder /app_bin .

EXPOSE 8080
CMD ["./app_bin"]