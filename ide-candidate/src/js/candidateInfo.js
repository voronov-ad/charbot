function initNewCandidate() {
    var ctx = $jsapi.context() || {};
    ctx.session.candidate = {
        "position": null,
        "devLangs": [],
        "specialization": null,
        "education": null,
        "experience": 0,
        "devLevel": null,
        "skills": [],
        "schedule": null,
        "city": null,
        "salaryFrom": null,
        "salaryTo": null,
        "comment": null,
        "companies": []
    };
    ctx.session.flowStep = 0;
}


function buildSummaryCandidateInfo(){
    var ctx = $jsapi.context() || {};
    var candidate = ctx.session.candidate;
    var info = "Позиция: " + candidate.position.text;
    if (candidate.devLangs.length) {
        info += "; Языки: " + candidate.devLangs.join(", ");
    }
    if (candidate.specialization) {
        info += "; Специализация: " + candidate.specialization;
    }
    if (candidate.devLevel) {
        info += "; Уровень: " + candidate.devLevel;
    } 
    
    var education = candidate.education || "не имеет значения";
    info += "; Образование: " + education;
    
    var experience = candidate.experience || "не имеет значения";
    info += "; Количество лет опыта: " + experience;
    
    var city = candidate.city ? candidate.city.name : "не имеет значения";
    info += "; Место проживания: " + city;
    
    if (candidate.schedule) {
        info += "; График работы: " + candidate.schedule;
    } 
    
    if (candidate.skills.length) {
        info += "; Основные навыки: " + candidate.skills.join(", ");
    } 
    
    if (candidate.salaryFrom && candidate.salaryTo) {
        info += "; Зарплатная вилка: " + candidate.salaryFrom + " - " + candidate.salaryTo;
    } else {
        if (candidate.salaryFrom) {
            info += "; Минимальная зарплата: " + candidate.salaryFrom;
        } 
        if (candidate.salaryTo) {
            info += "; Максимальная зарплата: " + candidate.salaryTo;
        } 
    }
    
    if (candidate.companies.length) {
        info += "; Будет плюсом, если кандидат до этого работал в одной из следующих компаний: " + candidate.companies.join(", ");
    }
    
    if (candidate.comment) {
        info += "; Дополнительно: " + candidate.comment;
    } 
    
    info += ".";
    return info;
}



function addSummaryCandidateInfo(){
    var ctx = $jsapi.context() || {};
    var session = ctx.session;
    var candidate = session.candidate;
    var flow = getFlow(candidate.position);
    for (var stepInd = 0; stepInd < flow.length; stepInd += 1) {
        var step = flow[stepInd];
        $reactions.buttons(stepNames[step]);
    }
}