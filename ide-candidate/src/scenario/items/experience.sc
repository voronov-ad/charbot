theme: /Подбор/ОсновнойПоток
    state: Опыт
        a: Сколько лет опыта считаем минимальным?
        buttons:
            "1"
            "3"
            "5"
            "10"
            "Не имеет значения"
        
        state: Trainee
            q: не имеет значения
            go!: /Подбор/ОсновнойПоток/Опыт/Done
            
        state: Years
            q: * $Number::number *
            script:
                $session.candidate.experience = $parseTree._number
            go!: /Подбор/ОсновнойПоток/Опыт/Done

        state: Fallback
            event: noMatch
            a: Я не совсем вас понял. Уточните, пожалуйста, минимальное количество лет опыт кандидата?
            buttons:
                "1"
                "3"
                "5"
                "10"
                "Не имеет значения"
            go: /Подбор/ОсновнойПоток/Опыт
        
        state: Done
            if: $session.candidate.experience
                a: Минимальное количество лет опыта: {{$session.candidate.experience}}
            else:
                a: Записываю: готовы рассматривать кандидата без опыта.
                
            go!: /Подбор/ОсновнойПоток
        
 
    
        
        