 export function getLambdaAPI(){
                var xhttplib = require('xhr2');
                var xhttp = new XMLHttpRequest();

                xhttp.onreadystatechange = function() {
                    if(this.readyState == 4 & this.status == 200){
                        document.getElementById("my-demo").innerHTML = this.responseText;
                    }
                };

                xhttp.open("GET", "{INSERT API GATEWAY ENDPOINT}", true);
                xhttp.send();
            }
