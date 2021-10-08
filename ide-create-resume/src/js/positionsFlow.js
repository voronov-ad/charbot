var positionsFlow = {
    "common": ["experience", "skills"],
    "dev": ["dev_langs", "dev_level", "experience", "skills"],
    "analyst": ["analyst_spec", "dev_level", "experience", "skills"]
}

var steps = {
    1: "/Резюме/ОсновнойПоток/Должность",
    2: "/Резюме/ОсновнойПоток/Зарплата",
    3: "/Резюме/ОсновнойПоток/ПолнаяЗанятность",
    4: "/Резюме/ОсновнойПоток/ГрафикРаботы",
    5: "/Резюме/ОсновнойПоток/ПоследнееМестоРаботы",
    6: "/Резюме/ОсновнойПоток/ПоследняяДолжность",
    7: "/Резюме/ОсновнойПоток/ПоследнийОпыт",
    8: "/Резюме/ОсновнойПоток/ПоследниеОбязанности"
}

var stepNames = {
    1: "Желаемая Должность",
    2: "Зарплата",
    3: "Тип занятости",
    4: "График работы",
    5: "Последнее место работы",
    6: "Последняя Должность",
    7: "Последний Опыт",
    8: "Текущие обязанности"
}

function getFlow(position) {
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
    session.flowStep += 1;

    $jsapi.log("session.flowStep:" + session.flowStep);
    $jsapi.log("steps.length: " + Object.keys(steps).length);

    // if (session.flowStep > steps.length + 1) {
    //     $jsapi.log("return STOP");
    //     return "STOP";
    // }

    if (session.flowStep in steps) {
        return steps[session.flowStep];
    } else {
        return "STOP";
    }
}

function findKeyByValue(value, obj) {
    for (var prop in obj) {
        if (obj[prop] === value) {
            return prop;
        }
    }
}

function getStepById(stepId) {
    return steps[stepId];
}