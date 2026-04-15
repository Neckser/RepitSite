package handlers

import (
	"encoding/json"
	"net/http"
	"tutoring-api/iternal/models"
	"tutoring-api/iternal/service"
)

type AdminHandler struct {
	statsSvc   *service.StatsService
	userSvc    *service.UserService
	homeSvc    *service.HomeworksService
	gradeSvc   *service.GradeService
	lessonSvc  *service.LessonsService
	tutorSvc   *service.TutorService
	studentSvc *service.StudentService
}

func NewAdminHandler(
	sSvc *service.StatsService,
	uSvc *service.UserService,
	hSvc *service.HomeworksService,
	gSvc *service.GradeService,
	lSvc *service.LessonsService,
	tSvc *service.TutorService,
	studSvc *service.StudentService,
) *AdminHandler {

	return &AdminHandler{statsSvc: sSvc,
		userSvc:    uSvc,
		homeSvc:    hSvc,
		gradeSvc:   gSvc,
		lessonSvc:  lSvc,
		tutorSvc:   tSvc,
		studentSvc: studSvc,
	}
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

func (h *AdminHandler) GetGrades(w http.ResponseWriter, r *http.Request) {
	homeworks, err := h.gradeSvc.GetAllGrades()
	if err != nil {
		http.Error(w, "Failed to fetch grades", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(homeworks)
}

func (h *AdminHandler) GetLessons(w http.ResponseWriter, r *http.Request) {
	lessons, err := h.lessonSvc.GetAllLessons()
	if err != nil {
		http.Error(w, "Failed to fetch lessons", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(lessons)
}

func (h *AdminHandler) GetTutors(w http.ResponseWriter, r *http.Request) {
	tutors, err := h.tutorSvc.GetAllTutors()
	if err != nil {
		http.Error(w, "Failed to fetch tutors", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(tutors)
}

func (h *AdminHandler) GetStudents(w http.ResponseWriter, r *http.Request) {
	students, err := h.studentSvc.GetAllStudents()
	if err != nil {
		http.Error(w, "Failed to fetch students", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(students)
}

func (h *AdminHandler) CreateTutor(w http.ResponseWriter, r *http.Request) {
	var req models.TutorCreateBadRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if err := req.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	id, err := h.tutorSvc.CreateTutor(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(map[string]string{
		"id":     id,
		"status": "created",
	})
}

func (h *AdminHandler) CreateStudent(w http.ResponseWriter, r *http.Request) {
	var req models.StudentCreateRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if err := req.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	id, err := h.studentSvc.CreateStudent(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(map[string]string{
		"id":     id,
		"status": "created",
	})
}

func (h *AdminHandler) LinkStudentToTutor(w http.ResponseWriter, r *http.Request) {
	var req models.AddRelationRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	isCreated, err := h.tutorSvc.LinkStudent(req)
	if err != nil {
		http.Error(w, "Database error: "+err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	if !isCreated {
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{
			"status":  "exists",
			"message": "Такая связь уже существует",
		})
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "created",
		"message": "Связь успешно создана",
	})
}

func (h *AdminHandler) CreateHomework(w http.ResponseWriter, r *http.Request) {
	var req models.HomeworkCreateRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid json", http.StatusBadRequest)
		return
	}

	if err := req.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	isCreated, err := h.homeSvc.CreateHomework(req)
	if err != nil {
		http.Error(w, "Database error"+err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-type", "application/json")

	if !isCreated {
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{
			"status":  "exists",
			"message": "Такая связь уже существует",
		})
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "created",
		"message": "Связь успешно создана",
	})

}

func (h *AdminHandler) GetLinks(w http.ResponseWriter, r *http.Request) {
	links, err := h.tutorSvc.GetAllLinks()
	if err != nil {
		http.Error(w, "Failed to fetch links", http.StatusInternalServerError)
	}
	w.Header().Set("Content-type", "application/json")
	json.NewEncoder(w).Encode(links)
}
