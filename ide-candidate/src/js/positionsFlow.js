var positionsFlow = {
    "common": ["experience", "education", "shedule", "city", "salaryFrom", "salaryTo", "skills", "companies"],
    "dev": ["devLangs", "devLevel", "experience", "education", "shedule", "city", "salaryFrom", "salaryTo", "skills", "companies"],
    "analyst": ["specialization", "devLevel", "experience", "education", "shedule", "city", "salaryFrom", "salaryTo", "skills", "companies"]
}

var steps = {
    "experience": "/Подбор/ОсновнойПоток/Опыт",
    "skills": "/Подбор/ОсновнойПоток/Навыки",
    "devLangs": "/Подбор/ОсновнойПоток/ЯзыкиПрограммирования",
    "devLevel": "/Подбор/ОсновнойПоток/УровеньРазработчика",
    "specialization": "/Подбор/ОсновнойПоток/СпециализациАналитика",
    "city": "/Подбор/ОсновнойПоток/Город",
    "education": "/Подбор/ОсновнойПоток/Образование",
    "shedule": "/Подбор/ОсновнойПоток/ГрафикРаботы",
    "salaryFrom": "/Подбор/ОсновнойПоток/МинимальнаяЗП",
    "salaryTo": "/Подбор/ОсновнойПоток/МаксимальнаяЗП",
    "companies": "/Подбор/ОсновнойПоток/Компании"
}


var stepNames = {
    "experience": "количество лет опыта",
    "skills": "навыки",
    "devLangs": "языки программирования",
    "devLevel": "уровень",
    "specialization": "специализация",
    "city": "город проживания",
    "education": "образование",
    "shedule": "график работы",
    "salaryFrom": "минимальная ЗП",
    "salaryTo": "максимальная ЗП",
    "companies": "список компаний"
}


function getFlow(position){
    var positionId = position.id;
    $jsapi.log(positionId);
    if (positionId && positionId in positionsFlow) {
        return positionsFlow[positionId];
    }
    $jsapi.log("Common positions flow");
    $jsapi.log(positionsFlow["common"]);

    return positionsFlow["common"];
}

function getStep() {
    var ctx = $jsapi.context() || {};
    var session = ctx.session;
    var candidate = session.candidate;
    var step = session.flowStep;
    
    var flow = getFlow(candidate.position);
    session.flowStep = step + 1;
    
    if (step >= flow.length) {
        return "STOP";
    }
    
    if (flow[step] in steps){
        return steps[flow[step]];
    }
    $jsapi.log("Flow step" + step + " not in steps: " + flow[step])
    return getStep();
}

function getStepById(stepId){
    return steps[stepId];
}