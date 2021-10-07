theme: /Подбор/ОсновнойПоток
    state: МинимальнаяЗП
        a: Укажите минимальную заработную плату по данной позиции в рублях.
        buttons:
            "30000"
            "80000"
            "100000"
            "120000"
            "150000"
            "200000"
            "пропустить"
        
        state: Trainee
            q: (пропустить|пропуск|пас)
            q: $NEGATION
            go!: /Подбор/ОсновнойПоток/МинимальнаяЗП/Done
            
        state: Years
            q: * $Number::number *
            script:
                $session.candidate.salaryFrom = $parseTree._number
            go!: /Подбор/ОсновнойПоток/МинимальнаяЗП/Done

        state: Fallback
            event: noMatch
            a: Я не совсем вас понял. Укажите минимальную заработную плату по данной позиции в рублях.
            buttons:
                "30000"
                "80000"
                "100000"
                "120000"
                "150000"
                "200000"
                "пропустить"
            
        state: Done
            if: $session.candidate.experience
                a: Минимальное заработная плата по позиции: {{$session.candidate.salaryFrom}}
            else:
                a: Пропускаем пункт с минимальной заработной платой.
                
            go!: /Подбор/ОсновнойПоток
        
 
    
        
        