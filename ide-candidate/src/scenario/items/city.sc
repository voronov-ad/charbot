theme: /Подбор/ОсновнойПоток
    state: Город
        if: $session.candidate.city
            a: Выбран город: {{$session.candidate.city}}
            buttons: 
                "Оставить, как есть"
                
        a: Из какого города должен быть кандидат?
        buttons:
            "Москва"
            "Санкт-Петербург"
            "Сочи"
            "Пермь"
            "Нижний Новгород"
            "Новосибирск"
            "Екатеринбург"
            "Не имеет значения"
        
        state: НеИмеетЗначения
            q: не имеет значения
            script: 
                $session.candidate.city = null;
            go!: /Подбор/ОсновнойПоток/Город/Done
            
        state: Ввод
            q: * $City *
            script: 
                $session.candidate.city = $parseTree._City;
            go!: /Подбор/ОсновнойПоток/Город/Done

        state: Fallback
            event: noMatch
            a: К сожалению, я не смог вычленить города из вашего запроса. Уточните, пожалуйста, откуда должен быть кандидат?
            buttons:
                "Москва"
                "Санкт-Петербург"
                "Сочи"
                "Пермь"
                "Нижний Новгород"
                "Новосибирск"
                "Екатеринбург"
                "Не имеет значения"
        
            if: $session.candidate.city
                buttons: 
                    "Оставить, как есть"
                    
            go: /Подбор/ОсновнойПоток/Город
        
        state: Done
            q: Оставить, как есть
            if: $session.candidate.city
                a: Город: {{$session.candidate.city.name}}.
            else: 
                a: Записал, что город не важен.
                
            go!: /Подбор/ОсновнойПоток
