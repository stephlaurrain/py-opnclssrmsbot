function fetchLogin() {
    // on ne peut pas par array car les mandatory sont multiples
    let frmData = new FormData();
    frmData.append("_username", "$login");
    frmData.append("_password", "$password");
    frmData.append("_remember_me", 1);


    frmBody = new URLSearchParams(frmData).toString();
    return fetch("$url", {
        "headers": {
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryxZjg8oiFB9rYd2Ju",
            "sec-ch-ua": "$sec_ch_ua",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        },
        "referrer": "$urlbase",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": frmBody,
        "method": "POST",
        "mode": "cors",
        "credentials": "include"
    });
}

async function login() {
    try {
        const response = await fetchLogin();
        return response;
    }
    catch (err) {
        console.log(err);
    }
    finally {
        console.log('finally')
    }
}

return login();

