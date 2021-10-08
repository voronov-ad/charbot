theme: /Резюме/ОсновнойПоток
    state: Должность
        a: На какую должность создаем вакансию?
        buttons:
            "Python-разработчик"
            "Аналитик"
            "Тестировщик"


        state: Fallback
            event: noMatch
            script:
                $session.resume.post = $request.query;
            go!: /Резюме/ОсновнойПоток
 
    
        
        