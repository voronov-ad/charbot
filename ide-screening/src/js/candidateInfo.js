function initNewCandidate() {
    var ctx = $jsapi.context() || {};
    ctx.session.position = null;
    ctx.session.answers = [];
    ctx.session.flowStep = 0;
}


