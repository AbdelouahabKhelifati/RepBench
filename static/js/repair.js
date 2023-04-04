let createRepairRequestFormData = function (alg) {
    const form = document.getElementById(alg)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)
    repairFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))
    return repairFormData
}

let repairResult = null
let repair = (alg) => {
    createScoreBoard()

    fetch(repair_url, {
        method: 'POST',
        body: createRepairRequestFormData(alg),
    }).then(response => response.json()).then(responseJson => {
        const repSeries = responseJson.repaired_series
        const scores = responseJson.scores
        repairResult = repSeries
        let color = null
        repairedSeries.length  = 0
        const chartRepairSeries = Object.keys(repSeries).map(key => {
            let repair = repSeries[key]
            return addRepairedSeries(repair,color)
        })
        updateScoreBoard(scores)

        resetSeries(true)
        scores["color"] = mainChart.series[mainChart.series.length-2].color


    })
}
