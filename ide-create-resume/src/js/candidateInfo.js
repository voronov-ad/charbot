function initResume() {
    var ctx = $jsapi.context() || {};
    ctx.session.resume = {
        "city": null,
        "post": null,
        "salary": null,
        "full_employment": null,
        "schedule": null,
        "last_place_of_work": null,
        "last_post": null,
        "last_work_experience": null,
        "last_responsibility": null,
    };
    ctx.session.flowStep = 0;
}


function buildSummaryCandidateInfo() {
    var ctx = $jsapi.context() || {};
    var resume = ctx.session.resume;
    var info = "Должность: " + resume.post;
    info += "; Город: " + resume.city;
    info += "; Зарплата: " + resume.salary;
    info += "; Занятость: " + (resume.full_employment ? "полная" : "частичная");
    info += "; График: " + resume.schedule;
    info += "; Последнее место работы: " + resume.last_place_of_work;
    info += "; Последняя занимаемая должность: " + resume.last_post;
    info += "; Последний опыт в месяцах: " + resume.last_work_experience;
    info += "; Обязанности на текущем месте: " + resume.last_responsibility;
    info += ".";
    return info;
}

function addSummaryCandidateInfo() {
    var ctx = $jsapi.context() || {};
    for (var stepInd = 0; stepInd < Object.keys(steps).length; stepInd += 1) {
        // var step = flow[stepInd];
        $reactions.buttons(stepNames[stepInd+1]);
    }
}