package middleware

import (
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/golang-jwt/jwt/v5"
)

func AdminAuth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if !strings.HasPrefix(authHeader, "Bearer ") {
			http.Error(w, "Access Denied: No token", http.StatusUnauthorized)
			return
		}
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")

		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			return []byte(os.Getenv("GO_API_ADMIN_SECRET")), nil
		})
		fmt.Println("DEBUG: Secret is:", os.Getenv("GO_API_ADMIN_SECRET"))

		if err != nil || !token.Valid {
			http.Error(w, "Access token: Invalid token", http.StatusUnauthorized)
			return
		}

		deviceSig := r.Header.Get("X-Device-Signature")
		if deviceSig == "" || deviceSig != os.Getenv("MY_ONLY_DEVICE_KEY") {
			http.Error(w, "Access Denied: Hardware mismatch", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)

	})
}
