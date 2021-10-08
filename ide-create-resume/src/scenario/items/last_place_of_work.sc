theme: /Резюме/ОсновнойПоток
    state: ПоследнееМестоРаботы
        a: Укажите последнее место работы?
        buttons:
            "Сбер"
            "Озон"
            "Тензор"


        state: Fallback
            event: noMatch
            script:
                $session.resume.last_place_of_work = $request.query;
            go!: /Резюме/ОсновнойПоток

 
    
        
        