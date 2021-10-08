theme: /
    state: НовоеРезюме
        event!: new
        q!: new
            
        a: Привет! Меня зовут Помогатель. Я создан для того, чтоб помочь тебе сделать отличное резюме. Поехали. Из какого Вы города?
        
        go!: /Резюме
        
    state: /Резюме
        script: 
            initResume($session);
            $jsapi.log("INSIDE");
        buttons: 
            "Москва"
            "Санкт-Петербург"
            "Ярославль"

        state: Город
            q: * $City *
            script:
                 $session.resume.city = $parseTree._City.name;
                 $jsapi.log($session.resume.city)
            go!: /Резюме/Город/Уточнение

            state: Уточнение
                a: Ваш город {{ $session.resume.city }}, верно?
                buttons:
                    "да"
                    "нет"

                state: Agree
                    q!: $AGREEMENT
                    go!: /Резюме/ОсновнойПоток

                state: Negation
                    q!: $NEGATION
                    a: Хорошо, из какого Вы города?
                    go!: /Резюме


        state: ОсновнойПоток
            script:
                $jsapi.log("START:");
                $temp.step = getStep();
                $jsapi.log("STATE:" + $temp.step);
                
            if: $temp.step == "STOP"
                go!: /Резюме/Конец
            else:
                go!: {{ $temp.step }}
        
        state: Конец
            script:
                $jsapi.log("OBJ: " + JSON.stringify($session.resume))
                $temp.info = buildSummaryCandidateInfo();
            a: Подведём итог. {{$temp.info}}
            a: Здесь Вы можете исправить данные или же,если все хорошо, то жмите Готово.
            script:
                addSummaryCandidateInfo();
            buttons: 
                "готово"
                
            state: ОтправляемЗапрос
                q: готово
                a: Полетели=)

                
            state: Fallback
                event: noMatch
                script:
                    var stepId = findKeyByValue($request.query, stepNames);
                    if (stepId) {
                        $temp.step = getStepById(stepId);
                    }
                if: $temp.step
                    go!: {{$temp.step}}
                go!: /Резюме/Конец