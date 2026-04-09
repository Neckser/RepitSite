package handlers

import (
	"encoding/json"
	"net/http"
	"tutoring-api/iternal/service"
)

type AdminHandler struct {
	statsSvc *service.StatsService
	userSvc  *service.UserService
	homeSvc  *service.HomeworksService
}

func NewAdminHandler(sSvc *service.StatsService, uSvc *service.UserService, hSvc *service.HomeworksService) *AdminHandler {
	return &AdminHandler{statsSvc: sSvc,
		userSvc: uSvc,
		homeSvc: hSvc}
}

func (h *AdminHandler) GetStats(w http.ResponseWriter, r *http.Request) {
	stats, err := h.statsSvc.GetGlobalStats()
	if err != nil {
		http.Error(w, "Failed to fetch stats", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(stats)
}

func (h *AdminHandler) GetUsers(w http.ResponseWriter, r *http.Request) {
	users, err := h.userSvc.GetAllUsers()
	if err != nil {
		http.Error(w, "Failed to fetch users", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(users)
}

func (h *AdminHandler) GetHomeworks(w http.ResponseWriter, r *http.Request) {
	homeworks, err := h.homeSvc.GetAllHomeworks()
	if err != nil {
		http.Error(w, "Failed to fetch homeworks", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(homeworks)
}
