theme: /Резюме/ОсновнойПоток
    state: ПоследнийОпыт
        a: Сколько месяцев проработали на последнем месте работы?
        buttons:
            "12"
            "24"
            "36"


       state: Месяцы
           q: * $Number::number *
           script:
               $session.resume.last_work_experience = $parseTree._number
           go!: /Резюме/ОсновнойПоток


        state: Fallback
            event: noMatch
            a: Я не совсем вас понял. Уточните, пожалуйста, сколько вы проработали на последнем месте работы?
            buttons:
                "12"
                "24"
                "36"
            go: /Резюме/ОсновнойПоток/ПоследнийОпыт

 
    
        
        