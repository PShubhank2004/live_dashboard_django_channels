console.log('hello world')
const dashboardSlug = document.getElementById('dashboard-slug').textContent.trim()
const user = document.getElementById('user').textContent.trim()
const submitBtn = document.getElementById('submit-btn')
const dataInput = document.getElementById('data-input')
const dataBox = document.getElementById('data-box')

const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}/`);
console.log(socket)

socket.onmessage = function(e){
    console.log('server: '+ e.data);
    const{sender, message} = JSON.parse(e.data)
    console.log(sender)
    console.log(message)

    dataBox.innerHTML += `<p>${sender}: ${message}</p>`
    updateCharts()
};

submitBtn.addEventListener('click', ()=>{
    const dataValue = dataInput.value
    socket.send(JSON.stringify({
        'message':dataValue,
        'sender': user,

    }))
})






const ctxPie = document.getElementById('myChartPie').getContext("2d");
const ctxBar = document.getElementById('myChartBar').getContext("2d");
const ctxLine = document.getElementById('myChartLine').getContext("2d");

let chartPie, chartBar, chartLine;

const fetchChartData = async () => {
    const response = await fetch(window.location.href + 'chart/');
    const data = await response.json();
    console.log(data);
    return data;
};

const drawCharts = async () => {
    const data = await fetchChartData();
    const { chartData, chartLabels } = data;

    const colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"];

    if (chartPie) chartPie.destroy();
    if (chartBar) chartBar.destroy();
    if (chartLine) chartLine.destroy();

    chartPie = new Chart(ctxPie, {
        type: "pie",
        data: {
            labels: chartLabels,
            datasets: [{
                label: '% of Contribution',
                data: chartData,
                backgroundColor: colors,
                borderWidth: 1
            }]
        }
    });

    chartBar = new Chart(ctxBar, {
        type: "bar",
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Data Contribution',
                data: chartData,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    chartLine = new Chart(ctxLine, {
        type: "line",
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Trend Over Time',
                data: chartData,
                borderColor: "#FF6384",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
};

const updateCharts = async () => {
    if (chartPie) chartPie.destroy();
    if (chartBar) chartBar.destroy();
    if (chartLine) chartLine.destroy();
    
    await drawCharts();
};


drawCharts();