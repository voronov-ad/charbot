theme: /Подбор/ОсновнойПоток
    # TODO: Сделать общую специализацию, вынести в json позицию и её специализации
    state: СпециализациАналитика
        a: Укажите, какая специализация должна быть у аналитика?
        buttons:
            "бизнес"
            "системный"
            "не важно"

        state: НеВажно
            q: не важно
            q: $NEGATION
            go!: /Подбор/ОсновнойПоток/СпециализациАналитика/Done
            
        state: Системный
            q: системный
            script:
                $session.candidate.specialization = "системный"
            go!: /Подбор/ОсновнойПоток/СпециализациАналитика/Done

        state: Бизнес
            q: бизнес
            script:
                $session.candidate.specialization = "бизнес"
            go!: /Подбор/ОсновнойПоток/СпециализациАналитика/Done

        state: Fallback
            event: noMatch
            a: Я не совсем вас понял. Уточните, пожалуйста, какая специализация должна быть у аналитика?
            buttons:
                "бизнес"
                "системный"
                "не важно"
            go: /Подбор/ОсновнойПоток/СпециализациАналитика
            
        state: Done
            if: $session.candidate.specialization
                a: Специализация: {{$session.candidate.specialization}} аналитик
            else: Записал, что специализация не важна.
            go!: /Подбор/ОсновнойПоток
         
 
    
        
        