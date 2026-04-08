package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
	"tutoring-api/internal/handlers"

	_ "github.com/lib/pq"
)

func main() {
	// Подключение через переменные окружения из твоего .env
	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASSWORD"),
		os.Getenv("DB_NAME"),
	)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatal("Ошибка подключения к БД:", err)
	}

	// Ждем базу (ретраи), так как Go стартует быстрее Postgres
	for i := 0; i < 10; i++ {
		if err := db.Ping(); err == nil {
			break
		}
		log.Println("Ожидание готовности базы...")
		time.Sleep(2 * time.Second)
	}
	defer db.Close()

	mux := http.NewServeMux()

	// Регистрируем руты (Go 1.22+ роутинг)
	mux.HandleFunc("GET /api/v1/health", handlers.HealthCheck)

	mux.HandleFunc("GET /api/v1/info", handlers.Info)

	// Здесь мы передаем DB в хендлеры (как только ты пришлешь структуру таблиц)
	// mux.HandleFunc("GET /api/v1/profile/{id}", GetProfileHandler(db))

	port := ":8080"
	fmt.Printf("🚀 Go API 1.25 запущен на порту %s\n", port)

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
