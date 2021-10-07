function updateEntities(entities, session){
    $jsapi.log(JSON.stringify(entities));
    for (var entity_ind = 0; entity_ind < entities.length; entity_ind++){
        var entity = entities[entity_ind];

        if (entity.pattern === "position"){
            $jsapi.log(JSON.stringify(entity));
            session.candidate.position = JSON.parse(entity["value"]);
            return;
        } 
    }
}
