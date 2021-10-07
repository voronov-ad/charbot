theme: /Подбор/ОсновнойПоток
    state: ЯзыкиПрограммирования
        a: Перечислите через запятую (или отдельными сообщениями) основные языки программирования, которыми должен владеть кандидат.
        
        buttons:
            "python"
            "java"
            "C++"
            "Не имеет значения"
            
        if: $session.candidate.devLangs.length
            a: Выбраны языки: {{$session.candidate.devLangs.join(", ")}} 
            buttons: 
                "хватит"
                "очистить"

        
        state: НеИмеетЗначения
            q: Не имеет значения
            script:
                $session.candidate.devLangs = [];
            go!: /Подбор/ОсновнойПоток/ЯзыкиПрограммирования/Done
            

        state: Fallback
            event: noMatch
            script:
                var newLangs = $request.query.split(", ");
                $session.candidate.devLangs = $session.candidate.devLangs.concat(newLangs);
            a: Записал: {{$session.candidate.devLangs.join(", ")}} 
            buttons:
                "очистить"
                "хватит"
            go: /Подбор/ОсновнойПоток/ЯзыкиПрограммирования
        
        state: Очистить
            q: очистить
            script:
                $session.candidate.devLangs = [];
            a: Очистил список компаний.
            go!: /Подбор/ОсновнойПоток/ЯзыкиПрограммирования
            
        state: Done
            q: хватит
            go!: /Подбор/ОсновнойПоток
        
 
    
        
        