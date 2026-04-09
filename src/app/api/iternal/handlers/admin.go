package handlers

import (
	"encoding/json"
	"net/http"
	"tutoring-api/iternal/service"
)

type AdminHandler struct {
	statsSvc *service.StatsService
}

func NewAdminHandler(svc *service.StatsService) *AdminHandler {
	return &AdminHandler{statsSvc: svc}
}

func (h *AdminHandler) GetStats(w http.ResponseWriter, r *http.Request) {
	stats, err := h.statsSvc.GetGlobalStats()
	if err != nil {
		http.Error(w, "Failed to fetch stats", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(stats)
}
