package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
	"tutoring-api/iternal/handlers"
	"tutoring-api/iternal/service"

	_ "github.com/lib/pq"
)

func main() {
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

	statsService := service.NewStatsService(db)
	usersService := service.NewUserService(db)
	homeService := service.NewHomeworksService(db)

	adminHandler := handlers.NewAdminHandler(statsService, usersService, homeService)

	mux.HandleFunc("GET /api/v1/health", handlers.HealthCheck)

	mux.HandleFunc("GET /api/v1/info", handlers.Info)

	mux.HandleFunc("GET /api/v1/admin/stats", adminHandler.GetStats)

	mux.HandleFunc("GET /api/v1/admin/users", adminHandler.GetUsers)

	mux.HandleFunc("GET /api/v1/admin/homeworks", adminHandler.GetHomeworks)

	port := ":8080"
	fmt.Printf("🚀 Go API 1.25 запущен на порту %s\n", port)

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
