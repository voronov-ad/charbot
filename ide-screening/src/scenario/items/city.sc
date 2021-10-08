theme: /Подбор/ОсновнойПоток
    state: Город
        a: {{$session.step.q}}
        buttons:
            "LOL"

        state: Fallback
            event: noMatch
            script:
                $jsapi.log("++++:" +JSON.stringify($session.step));
                $session.step.a = $request.query;
                $session.answers.push($session.step)
               
                    
            go!: /Подбор/ОсновнойПоток/
