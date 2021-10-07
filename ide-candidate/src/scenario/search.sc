theme: /
    state: НовыйПодборКандидата
        event!: new
        q!: new

        a: Сейчас быстренько подберём интересных кандидатов! Для начала: на какую позицию нам нужен человек?

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

            if: (!$session.candidate.position)
                script:
                    $session.candidate.position = {"text": $request.query}
            go!: /Подбор/Позиция/Проверка

            state: Проверка
                a: Будем искать кандидата на позицию {{ $session.candidate.position.text }}, верно?
                buttons:
                    "да"
                    "нет"

                state: Agree
                    q!: $AGREEMENT
                    go!: /Подбор/ОсновнойПоток

                state: Negation
                    q!: $NEGATION
                    a: Хорошо, кого будем искать?
                    go!: /Подбор


        state: ОсновнойПоток
            script:
                $temp.step = getStep();
                $jsapi.log($temp.step);

            if: $temp.step == "STOP"
                go!: /Подбор/Конец
            else:
                go!: {{ $temp.step }}

        state: Конец
            script:
                $temp.info = buildSummaryCandidateInfo();
            a: Подведём итог. {{$temp.info}}
            a: Если мы указали все интересующие вас параметры, скажите "готово". Если что-то необходимо поменять, укажите соответствующий пункт. Если хотите добавить комментарий - просто скажите его :)
            script:
                addSummaryCandidateInfo();
            buttons:
                "готово"

            state: ОтправляемЗапрос
                q: готово
                a: Супер, начинаю искать. Скоро вернусь :)

            state: ПользовательХочетДобавитьИнфо
                q: $AGREEMENT
                a: Что добавим?
                buttons:
                    "хватит"
                go: /Подбор/Конец

            state: Добавляем комментарий
                event: noMatch
                script:
                    var stepId = findKeyByValue($request.query, stepNames);
                    if (stepId) {
                        $temp.step = getStepById(stepId);
                    }
                if: $temp.step
                    go!: {{$temp.step}}
                else:
                    script:
                        if ($session.candidate.comment) {
                            $session.candidate.comment += "; " + $request.query;
                        } else {
                            $session.candidate.comment = $request.query;
                        }

                go!: /Подбор/Конец
