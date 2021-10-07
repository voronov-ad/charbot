theme: /Подбор/ОсновнойПоток
    state: УровеньРазработчика
        a: Укажите, какого уровня кандидат вас интересует?
        buttons:
            "trainee"
            "junior"
            "middle"
            "senior"
        
        state: Trainee
            q: (стажёр|стажер|начинающий|новчичок|trainee)
            script:
                $session.candidate.devLevel = "trainee"
            go!: /Подбор/ОсновнойПоток/УровеньРазработчика/Done
            
        state: Junior
            q: (джун|джуниор|junior|jun)
            script:
                $session.candidate.devLevel = "junior"
            go!: /Подбор/ОсновнойПоток/УровеньРазработчика/Done

        state: Middle
            q: (mid|middle|мид|миддл)
            script:
                $session.candidate.devLevel = "middle"
            go!: /Подбор/ОсновнойПоток/УровеньРазработчика/Done

        state: Senior
            q: (сеньор|синьор|сеньёр|синьёр|senior)
            script:
                $session.candidate.devLevel = "senior"
            go!: /Подбор/ОсновнойПоток/УровеньРазработчика/Done
                
        state: Fallback
            event: noMatch
            a: Я не совсем вас понял. Уточните, пожалуйста, минимальный уровень кандидат, с которым вы готовы общаться?
            buttons:
                "trainee"
                "junior"
                "middle"
                "senior"
            go: /Подбор/ОсновнойПоток/УровеньРазработчика
            
        state: Done
            a: Интересуемый уровень кандидата: {{$session.candidate.devLevel}} 
            go!: /Подбор/ОсновнойПоток
         
 
    
        
        