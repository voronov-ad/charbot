var positionsFlow = {
    "common": [
        {q: "Что такое ПК?", a: ""},
        {q: "Что такое процессор?", a: ""},
        {q: "Почему небо голубое?", a: ""}],
    "dev": [
        {q: "Что такое стек?", a: ""},
        {q: "Что такое solid?", a: ""},
        {q: "Что такое асинхронность?", a: ""}],
    "analyst": [{q: "Что входит в обязанности Аналитика?", a: ""}]
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
    var pos = session.position;
    var flow = getFlow(pos);
    session.flowStep += 1

    if (session.flowStep > flow.length) {
        return "STOP";
    }

    return flow[session.flowStep - 1];

}


