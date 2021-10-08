theme: /Резюме/ОсновнойПоток
    state: ПоследниеОбязанности
        a: Чем занимались? Чем подробнее расскажите, тем лучше.
        buttons:
            "Разработка"
            "Администрирование"
            "Найм"


        state: Fallback
            event: noMatch
            script:
                $session.resume.last_responsibility = $request.query;
            go!: /Резюме/ОсновнойПоток

 
    
        
        