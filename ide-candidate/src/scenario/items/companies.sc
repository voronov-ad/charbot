theme: /Подбор/ОсновнойПоток
    state: Компании
        a: Важно ли вам, в какой компании до этого работал кандидат?
        buttons:
            "да"
            "нет"
            
        state: КомпанияВажна
            q: $AGREEMENT
            a: Хорошо.
            go!: /Подбор/ОсновнойПоток/Компании/Ввод
            
        state: КомпанияНеВажна
            q: $NEGATION
            q: пропустить
            q: Не имеет значения
            script: 
                $session.candidate.companies = [];
            go!: /Подбор/ОсновнойПоток/Компании/Done
        
        state: Ввод
            a: Укажите названия компаний по одному или через запятую. 
            buttons: 
                "Сбер"
                "Яндекс"
                "Mail.ru Group"
                "Google"
                "Facebook"
                "Apple"
                "пропустить"
                
            if: $session.candidate.companies.length
                a: Выбраны компании: {{$session.candidate.companies.join(", ")}}. 
                buttons: 
                    "хватит"
                    "очистить"
                    
            state: Fallback
                event: noMatch
                script:
                    var companies = $request.query.split(", ");
                    $session.candidate.companies = $session.candidate.companies.concat(companies);
                a: Записал: {{$session.candidate.companies.join(", ")}} 
                buttons:
                    "Сбер"
                    "Яндекс"
                    "Mail.ru Group"
                    "Google"
                    "Facebook"
                    "Apple"
                    "хватит"
                    "очистить"
                go: /Подбор/ОсновнойПоток/Компании/Ввод
                
            state: Очистить
                q: очистить
                script:
                    $session.candidate.companies = [];
                a: Очистил список компаний.
                go!: /Подбор/ОсновнойПоток/Компании/Ввод
                
        
        state: Fallback
            event: noMatch
            a: Не совсем понял, что Вы хотели сказать.
            go!: /Подбор/ОсновнойПоток/Компании
        
        
        state: Done
            q: хватит
            q: пропустить
            if: $session.candidate.companies
                a: Список компаний, из которых кандидаты наиболее интересны: {{$session.candidate.companies.join(", ")}}
            else:
                a: Указал, что предыдущее место работы не играет роли.
            go!: /Подбор/ОсновнойПоток
        
 
    
        
        