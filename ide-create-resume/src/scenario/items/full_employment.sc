theme: /Резюме/ОсновнойПоток
    state: ПолнаяЗанятность
        a: Полная занятость?
        buttons:
            "да"
            "нет"

        state: Agree
            q!: $AGREEMENT
            script:
                $session.resume.full_employment = true;
            go!: /Резюме/ОсновнойПоток

        state: Negation
            q!: $NEGATION
            script:
                $session.resume.full_employment = false;
            go!: /Резюме/ОсновнойПоток

 
    
        
        