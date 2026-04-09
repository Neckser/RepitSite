package handlers

import (
	"encoding/json"
	"net/http"
)

func HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	response := map[string]string{
		"status": "active",
		"engine": "go1.25",
		"path":   "src/app/api",
	}

	json.NewEncoder(w).Encode(response)
}

func Info(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	response := map[string]string{
		"status": "asd",
		"":       "",
	}
	json.NewEncoder(w).Encode(response)
}
