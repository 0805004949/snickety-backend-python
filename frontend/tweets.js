
function getCookie(name) {
  return document.cookie.split(';').filter(function(item) {
    return item.indexOf(name) !== -1;
  })[0];
};

function parseJwt (token) { // user_id 가져오는 함수
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
};


$(document).ready(function() {
  var accessToken = (getCookie('token') || '').split('=')[1];
  var current_user_id = parseJwt(accessToken).user_id; // 현재 로그인된 user_id
  var paramArr = (window.location.search.split('?')[1] || '').split('&'); // 현재 보고있는 페이지 user_id
  var userId = '';
  paramArr.forEach(function (param) {
    if (param.indexOf('user_id') !== -1) {
      userId = param.split('=')[1];
    }
  })

  if (userId) {

    $('.userId')
      .append(userId);
  }

  if (accessToken) {
    
    $.ajax({
      method: 'GET',
      url: 'http://localhost:5000/timeline',
      headers: {
        'Authorization': accessToken
      }, 
      data : {
        'user_id' : userId // 주소에 있는 user_id  타임라인 가져옴
      }
    },
  
    )
    .done(function(msg) {
      var timeline = msg.timeline;

      if (timeline) {
        timeline.forEach(function (item) {
          $('.timeline-container')
            .append('<div class="card">' +
              '<div class="card-body">' +
              '<h5 class="card-title">'+item.user_id+'</h5>' +
              '<p class="card-text">'+item.tweet+'</p></div>' +
              '</div>')
        })
      }
    });
  } else {
    alert('로그인이 필요합니다.');
    window.location.href = './login.html';
    return;
  }

  $('#tweetForm').submit(function(e) {
    e.preventDefault();

    // if (!myId) {
    if (!accessToken) {
      alert('로그인이 필요합니다.');
      window.location.href = './login.html';
      return;
    }

    var tweet = $('#tweet').val();

    $.ajax({
      method: 'POST',
      url: 'http://localhost:5000/tweet',
      headers: {
        'Authorization': accessToken
      },
      data: JSON.stringify({
        "tweet" : tweet
      }),
      contentType: 'application/json'
    })
    .done(function(msg) {
    });
  });

  $('#follow').on('click', function () {
    if (current_user_id == userId) {
      alert("나 자신을 팔로우,언팔로우 할 수 없어요!")
    }else {
      $.ajax({
        method: 'POST',
        url: 'http://localhost:5000/follow',
        headers: {
          'Authorization': accessToken
        },
        data: JSON.stringify({
          "follow" : userId
        }),
        contentType: 'application/json'
      })
        .done(function(msg) {
        });
    }


  });

  $('#unfollow').on('click', function () {
    if (current_user_id == userId) {
      alert("나 자신을 팔로우,언팔로우 할 수 없어요!")
    }else{
      $.ajax({
        method: 'POST',
        url: 'http://localhost:5000/unfollow',
        headers: {
          'Authorization': accessToken
        },
        data: JSON.stringify({
          "unfollow" : userId
        }),
        contentType: 'application/json'
      })
        .done(function(msg) {
        });

    }

  });
});
