package handlers

import (
	"encoding/json"
	"net/http"
)

func (h *AdminHandler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	response := map[string]string{
		"status": "active",
	}

	json.NewEncoder(w).Encode(response)
}
