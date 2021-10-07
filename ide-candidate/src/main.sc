require: zenflow.sc
  module = sys.zfl-common
  
require: slotfilling/slotFilling.sc
  module = sys.zb-common

require: js/updateEntities.js
require: js/positionsFlow.js
require: js/candidateInfo.js
require: js/utils.js

require: scenario/items/devLevel.sc
require: scenario/items/devLangs.sc
require: scenario/items/experience.sc
require: scenario/items/skills.sc
require: scenario/items/city.sc
require: scenario/items/devLevel.sc
require: scenario/items/education.sc
require: scenario/items/schedule.sc
require: scenario/items/specialization.sc
require: scenario/items/salaryTo.sc
require: scenario/items/salaryFrom.sc
require: scenario/items/companies.sc

require: scenario/search.sc

patterns:
    $AnyText = $nonEmptyGarbage
    
theme: /

    state: Start
        q!: $regex</start>
        a: Начнём.


    state: Список поисков
        event!: get_list
        a: Тут будет список
        
    state: Fallback
        event: noMatch
        a: Я не понял. Вы сказали: {{$request.query}}
