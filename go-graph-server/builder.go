package main

import (
	"os"
	"fmt"

	"github.com/go-echarts/go-echarts/v2/charts"
	"github.com/go-echarts/go-echarts/v2/opts"
)

func createReport(data map[string][2]float32, uuid string, ch chan string) {

	bar := charts.NewBar()

	bar.SetGlobalOptions(
		charts.WithTitleOpts(opts.Title{
			Title:    "Income/Expense Report",
			Subtitle: "Made with BudgetGraph",
		}),
		charts.WithColorsOpts(opts.Colors{"red", "black"}),
	)

	var names []string
	var incomeElements []float32
	var expenseElements []float32

	for person := range data {
		names = append(names, person)
	}

	// Plot values along the X axis. In our case, these are usernames.
	bar.SetXAxis(names)

	for person := range data {
		names = append(names, person)
		incomeElements = append(incomeElements, data[person][0])
		expenseElements = append(expenseElements, data[person][1])
	}

	// Each AddSeries method applied adds 1 column to each value on the X-axis interval [0; count]
	// Each user will have 2 columns, but they will be laid out in 2 cycles, going from the first to the last user on the X axis.
	bar.AddSeries("Income", compositionDataColumns(incomeElements)).
		AddSeries("Expense", compositionDataColumns(expenseElements))

	PathFilename := fmt.Sprintf("../budget_graph/graphs/%s.html", uuid)
	f, err := os.Create(PathFilename)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	bar.Render(f)
	ch <- uuid
}

func compositionDataColumns(salary []float32) []opts.BarData {
	items := make([]opts.BarData, len(salary))
	for i := range len(salary) {
		items[i] = opts.BarData{Value: salary[i]}
	}
	return items
}
