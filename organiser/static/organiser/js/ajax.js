$(function() {
    setTimeout(runAjax, 3000);
    function runAjax() {
        var req = $.ajax({
            url: "http://127.0.0.1:8000/sample.json",
            type: "get",
            dataType: "json",
        });
        req.done(function(response, status, jqXHR) {
            console.log(response);
            createElement(response);
        });
        req.fail(function(jqXHR, status, errorType) {
            console.log(errorType)
        });
    }
    function createElement(response) {
        var x = document.createElement("div");
        x.setAttribute("id", "content");
        for (var i = 0; i < response['people'].length; i++) {
            var el = document.createElement("p");
            el.textContent = response['people'][i]['name'] + ": " + 
                response['people'][i]['age'];
            x.appendChild(el);
        }
        document.body.appendChild(x)
        setTimeout(redirect, 2000, ["http://127.0.0.1:8000/tag/"])
    }
    function redirect(path) {
        location.href = path
    }
});
