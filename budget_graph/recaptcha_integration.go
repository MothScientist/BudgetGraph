package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/joho/godotenv"
	recaptcha "cloud.google.com/go/recaptchaenterprise/v2/apiv1"
	recaptchapb "cloud.google.com/go/recaptchaenterprise/v2/apiv1/recaptchaenterprisepb"
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

	http.HandleFunc("/validate-recaptcha", recaptchaHandler)
	log.Println("[SUCCESS] Starting server on :8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("[ERROR] Error starting server: %v", err)
	}
}

// recaptchaHandler processes reCAPTCHA validation request
func recaptchaHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("[INFO] recaptchaHandler init")
	if r.Method != http.MethodPost {
	log.Printf("[ERROR] Unsupported request method: %v", http.StatusMethodNotAllowed)
		http.Error(w, "Unsupported request method", http.StatusMethodNotAllowed)
		return
	}

	var requestData struct {
		RecaptchaToken string `json:"recaptcha_token"`
	}

	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		log.Printf("[ERROR] open log directory: %v", err)
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	projectID := os.Getenv("RECAPTCHA_PROJECT_ID")
	recaptchaKey := os.Getenv("RECAPTCHA_KEY")
	recaptchaAction := "LOGIN"

	// reCAPTCHA token verification
	score, err := createAssessment(projectID, recaptchaKey, requestData.RecaptchaToken, recaptchaAction)
	if err != nil {
		http.Error(w, "reCAPTCHA validation failed", http.StatusForbidden)
		return
	}

	// If everything went well, you can continue processing user data.
	fmt.Fprintf(w, "reCAPTCHA score: %f", score)
}

// createAssessment creates an assessment for the risk analysis of UI action
func createAssessment(projectID string, recaptchaKey string, token string, recaptchaAction string) (float64, error) {
	log.Println("[INFO] createAssessment init")

	ctx := context.Background()
	client, err := recaptcha.NewClient(ctx)
	if err != nil {
		log.Printf("[ERROR] creating reCAPTCHA client: %v", err)
		return 0, fmt.Errorf("error creating reCAPTCHA client: %v", err)
	}
	defer client.Close()

	event := &recaptchapb.Event{
		Token:   token,
		SiteKey: recaptchaKey,
	}

	assessment := &recaptchapb.Assessment{
		Event: event,
	}

	// Building a request for an estimate
	request := &recaptchapb.CreateAssessmentRequest{
		Assessment: assessment,
		Parent:     fmt.Sprintf("projects/%s", projectID),
	}

	response, err := client.CreateAssessment(ctx, request)
	if err != nil {
		log.Printf("[ERROR] calling CreateAssessment: %v", err)
		return 0, fmt.Errorf("error calling CreateAssessment: %v", err)
	}

	// Checking token validity
	if !response.TokenProperties.Valid {
		log.Printf("[ERROR] the token was invalid for the following reasons: %v", response.TokenProperties.InvalidReason)
		return 0, fmt.Errorf("the token was invalid for the following reasons: %v", response.TokenProperties.InvalidReason)
	}

	// Check if the expected action matches the action performed
	if response.TokenProperties.Action != recaptchaAction {
		log.Print("[ERROR] the action attribute does not match the expected action")
		return 0, fmt.Errorf("the action attribute does not match the expected action")
	}

	// Return the risk score by converting float32 to float64
	return float64(response.RiskAnalysis.Score), nil
}
