function fetchEvents(){
                
    let token = localStorage.getItem("$tokenkey");    
    let myHeaders = new Headers();
    myHeaders.append ("accept", "application/json;version=0.1");
    myHeaders.append ("accept-language", "fr");
    myHeaders.append ("authorization", "Bearer "+token);
    myHeaders.append ("content-type", "application/json");
    myHeaders.append ("sec-ch-ua", "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"");
    myHeaders.append ("sec-ch-ua-mobile", "?0");
    myHeaders.append ("sec-ch-ua-platform", "\"Linux\"");
    myHeaders.append ("sec-fetch-dest", "empty");
    myHeaders.append ("sec-fetch-mode", "cors");
    myHeaders.append ("sec-fetch-site", "same-site");
    myHeaders.append ("x-requested-with", "XMLHttpRequest");

    let myInit = { method: 'GET', headers: myHeaders, mode: 'cors', cache: 'default' };
    let myRequest = new Request("$url", myInit);
    return fetch(myRequest,myInit)
        .then(function(response) {  return response.json(); }); 
}

async function getEvents(){
    try{
          const response = await fetchEvents();
          return response;
      }
    catch (err){
          console.log(err);
    } 
    finally{
          console.log('finally')
    } 
  }
  return getEvents();
  