theme: /Резюме/ОсновнойПоток
    state: ПоследняяДолжность
        a: Укажите должность на последнем месте работы?
        buttons:
            "Python-разработчик"
            "Аналитик"
            "Тестировщик"


        state: Fallback
            event: noMatch
            script:
                $session.resume.last_post = $request.query;
            go!: /Резюме/ОсновнойПоток

        
 
    
        
        