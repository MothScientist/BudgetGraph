package main

import (
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/joho/godotenv"
	"path/to/your/project/reCaptchaAPI" // import reCaptchaAPI
)

func main() {
	logDir := filepath.Join("logs", "go") // setting the path for logs

	// Create directory if it does not exist
	if err := os.MkdirAll(logDir, os.ModePerm); err != nil {
		log.Fatalf("[ERROR] creating log directory: %v", err)
	}

	logFile, err := os.OpenFile(filepath.Join(logDir, "recaptcha.log"), os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("[ERROR] open log directory: %v", err)
	}
	defer logFile.Close()

	log.SetOutput(logFile) // redirect logs to a file

	if err := godotenv.Load(); err != nil {
		log.Fatalf("[ERROR] No .env file found")
	} else {
		log.Println("[SUCCESS] .env file found")
	}

	http.HandleFunc("/validate-recaptcha", reCaptchaAPI.RecaptchaHandler) // use the handler from the package
	log.Println("[SUCCESS] Starting server on :8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("[ERROR] Error starting server: %v", err)
	}
}
