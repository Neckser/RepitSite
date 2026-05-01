package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
	"tutoring-api/iternal/handlers"
	"tutoring-api/iternal/middleware"
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
	gradeService := service.NewGradeService(db)
	lessonService := service.NewLessonService(db)
	tutorService := service.NewTutorService(db)
	studentService := service.NewStudentService(db)
	testService := service.NewTestService(db)
	chatService := service.NewChatService(db)

	adminHandler := handlers.NewAdminHandler(
		statsService,
		usersService,
		homeService,
		gradeService,
		lessonService,
		tutorService,
		studentService,
		testService,
		chatService,
	)

	adminJwtProtector := func(h http.HandlerFunc) http.Handler {
		return middleware.AdminAuth(h)
	}

	mux.Handle("GET /api/v1/admin/health", adminJwtProtector(adminHandler.HealthCheck))

	mux.Handle("GET /api/v1/admin/stats", adminJwtProtector(adminHandler.GetStats))

	mux.Handle("GET /api/v1/admin/users", adminJwtProtector(adminHandler.GetUsers))

	mux.Handle("GET /api/v1/admin/homeworks", adminJwtProtector(adminHandler.GetHomeworks))

	mux.Handle("GET /api/v1/admin/grades", adminJwtProtector(adminHandler.GetGrades))

	mux.Handle("GET /api/v1/admin/lessons", adminJwtProtector(adminHandler.GetLessons))

	mux.Handle("GET /api/v1/admin/tutors", adminJwtProtector(adminHandler.GetTutors))

	mux.Handle("GET /api/v1/admin/students", adminJwtProtector(adminHandler.GetStudents))

	mux.Handle("POST /api/v1/admin/tutor/create", adminJwtProtector(adminHandler.CreateTutor))

	mux.Handle("POST /api/v1/admin/student/create", adminJwtProtector(adminHandler.CreateStudent))

	mux.Handle("POST /api/v1/admin/tutor-students/create", adminJwtProtector(adminHandler.LinkStudentToTutor))

	mux.Handle("GET /api/v1/admin/links", adminJwtProtector(adminHandler.GetLinks))

	mux.Handle("GET /api/v1/admin/tests", adminJwtProtector(adminHandler.GetAllTests))

	mux.Handle("GET /api/v1/admin/tutor/{uuid}/info", adminJwtProtector(adminHandler.GetTutorInfo))

	mux.Handle("GET /api/v1/admin/student/{uuid}/info", adminJwtProtector(adminHandler.GetStudentInfo))

	mux.Handle("GET /api/v1/admin/chats", adminJwtProtector(adminHandler.GetAllChats))

	mux.Handle("GET /api/v1/admin/chats/messages", adminJwtProtector(adminHandler.GetAllMessages))

	port := ":8080"
	fmt.Printf("🚀 Go API 1.25 запущен на порту %s\n", port)

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
