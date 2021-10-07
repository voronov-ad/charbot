
function findKeyByValue(value, obj) {
  for (var prop in obj){
      if (obj[prop] === value){
          return prop;
      }
  }
}