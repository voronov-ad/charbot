theme: /Подбор/ОсновнойПоток
    state: Навыки
        a: Перечислите через запятую (или отдельными сообщениями) основные навыки, которыми должен обладать кандидат.
        
        buttons:
            "Не имеет значения"
            
        if: $session.candidate.skills.length
            a: Сейчас выбраны: {{$session.candidate.skills.join(", ")}} 
            buttons:
                "хватит"
                "очистить"
        
        state: НеИмеетЗначения
            q: Не имеет значения
            script:
                $session.candidate.skills = [];
            go!: /Подбор/ОсновнойПоток/Навыки/Done
            

        state: Fallback
            event: noMatch
            script:
                var new_skills = $request.query.split(", ");
                $session.candidate.skills = $session.candidate.skills.concat(new_skills);
            a: Записал: {{$session.candidate.skills.join(", ")}} 
            buttons:
                "очистить"
                "хватит"
            go: /Подбор/ОсновнойПоток/Навыки
        
        state: Очистить
            q: очистить
            script:
                $session.candidate.skills = [];
            a: Очистил список компаний.
            go!: /Подбор/ОсновнойПоток/Навыки
            
        state: Done
            q: хватит
            go!: /Подбор/ОсновнойПоток
        
 
    
        
        