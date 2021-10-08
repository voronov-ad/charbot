function updateEntities(entities, session){
    for (var entity_ind = 0; entity_ind < entities.length; entity_ind++){
        var entity = entities[entity_ind];
        var value = JSON.parse(entity["value"]);
        
        if (entity.pattern === "dev_lang"){
            session.candidate.dev_langs.push(value);
        } else {
            if (entity.pattern === "company") {
                session.candidate.companies.push(value);
            } else {
                session.candidate[entity["pattern"]] = JSON.parse(entity["value"]);
            }
        }   
    }
}
