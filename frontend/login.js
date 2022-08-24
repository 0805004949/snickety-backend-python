function parseJwt (token) { // user_id 가져오는 함수
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
};

function createCookie(value) {
  var now = new Date();
  var expirationDate = new Date(now.getFullYear(), now.getMonth(), now.getDate()+7, 0, 0, 0);

  document.cookie = 'token='+value+'; expires='+expirationDate+'; path=/';
};

$(document).ready(function() {
  $("#loginForm").submit(function(e) {
    e.preventDefault();

    var id = $("#id").val();
    var password = $("#password").val();

    $.ajax({
      method: "POST",
      url: "http://localhost:5000/login",
      data: JSON.stringify({
        "email"    : id,
        "password" : password
      }),
      contentType: 'application/json'
    })
    .done(function(msg) {
      if (msg.access_token) {
        createCookie(msg.access_token);
        var user_id = parseJwt(msg.access_token).user_id; 
        console.log(user_id)
        window.location.href = './tweets.html?user_id='+user_id;
      }
    });
  });
});
