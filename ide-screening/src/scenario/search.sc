theme: /
    state: НовыйСкрининг
        event!: new
        q!: new

        a: Сейчас быстренько пройдемся по вопросам и баста! На какую позицию вы записаны?

        go!: /Подбор

    state: Подбор
        script:
            initNewCandidate();

        buttons:
            "Системный аналитик"
            "Разработчик"
            "Менеджер проекта"

        state: Позиция
            event: noMatch
            script:
                updateEntities($context.entities, $session);

            if: (!$session.position)
                script:
                    $session.position = {"text": $request.query}
            go!: /Подбор/ОсновнойПоток


        state: ОсновнойПоток
            script:
                $session.step = getStep();
                $jsapi.log("temp.step:" + $temp.step);
                $jsapi.log("session: " + $session);


            if: $session.step == "STOP"
                go!: /Подбор/Конец
            else:
                go!: /Подбор/ОсновнойПоток/Город

        state: Конец
            script:
                $jsapi.log(JSON.stringify($session.step));