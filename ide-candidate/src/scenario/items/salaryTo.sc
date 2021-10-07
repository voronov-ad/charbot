theme: /Подбор/ОсновнойПоток
    state: МаксимальнаяЗП
        a: Укажите максимальную заработную плату по данной позиции
        buttons:
            "50000"
            "100000"
            "120000"
            "150000"
            "200000"
            "250000"
            "пропустить"
        
        state: Пропуск
            q: (пропустить|пропуск|пас)
            q: $NEGATION
            go!: /Подбор/ОсновнойПоток/МаксимальнаяЗП/Done
            
        state: Ввод
            q: * $Number::number *
            script:
                $session.candidate.salaryTo = $parseTree._number
            go!: /Подбор/ОсновнойПоток/МаксимальнаяЗП/Done

        state: Fallback
            event: noMatch
            a: Я не совсем вас понял. Укажите максимальную заработную плату по данной позиции в рублях.
            buttons:
                "50000"
                "100000"
                "120000"
                "150000"
                "200000"
                "250000"
                "пропустить"
            
        state: Done
            if: $session.candidate.experience
                a: Максимальная заработная плата по позиции: {{$session.candidate.salaryTo}}
            else:
                a: Указываем, что нет предела с максимальной зарплатой.
                
            go!: /Подбор/ОсновнойПоток
        
 
    
        
        