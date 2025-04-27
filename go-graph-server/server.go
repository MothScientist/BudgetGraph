package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"fmt"

	"github.com/joho/godotenv"
)

type RequestData struct {
	Data map[string][2]float32 `json:"data"`
	UUID string                `json:"uuid"`
}

type Task struct {
	UUID string
	Data map[string][2]float32
}

var taskQueue = make(chan Task, 10)   // Channel where we store data for unprocessed requests
var taskReady = make(chan string, 10) // Channel where UUIDs of processed requests are stored

func requestProcessing(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		log.Println("Method not allowed")
		return
	}

	var requestData RequestData
	err := json.NewDecoder(r.Body).Decode(&requestData)
	if err != nil {
		http.Error(w, "Error reading data: "+err.Error(), http.StatusBadRequest)
		log.Printf("Error reading data: %v\n", err.Error())
		return
	}

	log.Printf("Received data: %v, UUID: %s\n", requestData.Data, requestData.UUID)

	task := Task{
		UUID: requestData.UUID,
		Data: requestData.Data,
	}
	taskQueue <- task
}

func processTasks() {
	for task := range taskQueue {
		go func(t Task) {
			createReport(t.Data, t.UUID, taskReady)
		}(task)
	}
}

func logNotification() {
	for task := range taskReady {
		go func(uuid string) {
			log.Printf("Task completed. UUID: %s", uuid)
		}(task)
	}
}

func main() {
	go processTasks()
	go logNotification()

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	logFile, err := os.OpenFile("../budget_graph/logs/goPlotBuilderServer.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0222)
	if err != nil {
		log.Fatalf("Error opening log file: %v", err)
	}
	defer logFile.Close()

	log.SetOutput(logFile)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	log.Println("The server is running")

	http.HandleFunc("/api/report/generate", requestProcessing)

  port := os.Getenv("PLOT_BUILDER_PORT")

	portFormat := fmt.Sprintf(":%s", port)
	if err := http.ListenAndServe(portFormat, nil); err != nil {
		log.Fatalf("Error starting server: %v", err)
	}
}
