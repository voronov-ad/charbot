require: zenflow.sc
  module = sys.zfl-common
  
require: slotfilling/slotFilling.sc
  module = sys.zb-common

require: script.js
require: js/positionsFlow.js
require: js/candidateInfo.js


require: scenario/items/post.sc
require: scenario/items/salary.sc
require: scenario/items/full_employment.sc
require: scenario/items/schedule.sc
require: scenario/items/last_place_of_work.sc
require: scenario/items/last_post.sc
require: scenario/items/last_work_experience.sc
require: scenario/items/last_responsibility.sc
require: scenario/resume.sc

patterns:
    $AnyText = $nonEmptyGarbage
    
theme: /

    state: Start
        q!: $regex</start>
        a: Начнём.


        
    state: Fallback
        event: noMatch
        a: Я не понял. Вы сказали: {{$request.query}}
