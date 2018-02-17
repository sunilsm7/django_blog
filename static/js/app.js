$(document).ready(function(){

  Notification.requestPermission().then(function(result) {
  });


  function notifyMe() {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
  alert("This browser does not support system notifications");
  }

  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
  // If it's okay let's create a notification
  var notification = new Notification("Hi there!");
  }

  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== 'denied') {
  Notification.requestPermission(function (permission) {
    // If the user accepts, let's create a notification
    if (permission === "granted") {

      var notification = new Notification("Hi there!");
    }
  });
  }

  // Finally, if the user has denied notifications and you 
  // want to be respectful there is no need to bother them any more.
  }

 

  // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');
  


  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });


 

// Sign up form validations
  let $signUpForm = $('#signUpForm');
  if ($signUpForm.attr("id") === 'signUpForm'){

    $('#id_username').on({
    change:function(event){
      let $this_ = $(this);
      let $error_message = $this_.closest('div').find('.error-message');
      let urlEndPoint = $signUpForm.attr('data-url');

      $.ajax({
          url :urlEndPoint,
          method:'GET',
          data: {
              'username': $this_.val(),
          },
          dataType:'json',
          success: function(data){
              if($($this_).val() !== '' && !data.username_error_message){
                  $error_message.show().html('username available');                     
              }

              $error_message.show().html(data.username_error_message);
              
          },
          error:function(xhr,status,error){
              
          }
      });
    },

    focus:function(event){
      $(this).closest('div').find('.error-message').hide();
    },

    blur:function(event){
      let $this_ = $(this);
      let $error_message = $this_.closest('div').find('.error-message');
      if($(this).val() === ''){
        $error_message.show().text('Please enter username id.');
      }     
    },

    });

    // for email validations
    let ValidateEmail= function(email) {
        let expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        return expr.test(email);
    };


    $('#id_email').on({
      change:function(event){
        let $this_ = $(this);
        let $error_message = $this_.closest('div').find('.error-message');
        let urlEndPoint = $signUpForm.attr('data-url');
        if($this_.val() !== ''){
          if(!ValidateEmail($this_.val())){
            // $this_.closest('div').find('.error-message').show().text('Please enter valid email id.');
            $error_message.show().text('Please enter valid email id.');
          }
          else{
            // $this_.closest('div').find('.error-message').hide();
            $error_message.hide();
          }
        }
        else{
          // $this_.closest('div').find('.error-message').show().text('Please enter email id.');     
          $error_message.show().text('Please enter email id.');     
        }

        $.ajax({
          url :urlEndPoint,
          method:'GET',
          data: {
            'email': $this_.val(),
          },
          dataType:'json',
          success: function(data){
            $error_message.show().html(data.email_error_message);
          },
          error:function(xhr,status,error){
          }
        });
    },

    focus:function(event){
      let $this_ = $(this);
      let $error_message = $this_.closest('div').find('.error-message');
      $error_message.hide();
    },

    blur:function(event){
      let $this_ = $(this);
      let $error_message = $this_.closest('div').find('.error-message');
      if($(this).val() ===''){
        $error_message.show().text('Please enter email id.');                
      }   
    },
    });

      $('#id_password1').change(function(event){
        let $this_ = $(this);
        let $error_message = $this_.closest('div').find('.error-message');
        if ($this_.val() == ''){
          $error_message.show().text('Please enter password'); 
        }
        else{
          $error_message.hide();       
        }   
      });


      $('#id_password2').change(function(event){
        let $this_ = $(this);
        let id_password1 = $('#id_password1').val();
        let $error_message = $this_.closest('div').find('.error-message');
        if ($this_.val() !== id_password2){
          $error_message.show().text('password\'s are not matched.');
        }
        else{
          $error_message.hide();   
        }       
      });
  }

// Contact us form.
  let $contact_form = $('.contact-form');
  $contact_form.submit(function(event){
    event.preventDefault();
    let $formData =$(this).serialize();
    let $thisUrl = $contact_form.attr('data-url') || window.location.href;
    let $error_message = $('#error');
    $.ajax({
      method: "POST",
      url: $thisUrl,
      data: $formData,
      success: function(data, textStatus, jqxhr){
          $error_message.text(data.message);
          document.querySelector(".contact-form").reset();
      },
      error: function(xhr, status, error){
      },
    });
  });


// Autocomplete for search bar

  // $('#search_posts').change(function(event){
  //  window.location.href = '/posts/list/?q=' + $(this).val().trim();
  // });

  $("#search_posts").autocomplete({
      minLength:3,
      source: function(req, add){
        let search = $('#search_posts').val();
        let form_search_post = $('#form_search_post');
        let urlEndPoint = form_search_post.attr('data-url');
        let ajaxCall = $.ajax({
          url:urlEndPoint,
          dataType: 'json',
          data: {'term':search},
          type: 'GET',
        });
        
        ajaxCall.done(function(data){
          let suggestions = [];
          $.each(data, function(index, objects){
              suggestions.push(objects);
          });
          add(suggestions);
        });

        ajaxCall.fail(function(error){
          
        }); 
    },
  });

  

// Comment Form
  let $comment_form = $('#comment_form');
  $comment_form.submit(function(event){
    event.preventDefault();
    let $this_ = $(this);
    let $formData =$this_.serialize();
    let $post_comments = $('#post_comments');
    // let $api_post_comments_list_url = $("#post_title_id").attr('data-api_post_comments_list_url');
    let $api_post_detail_url = $("#post_title_id").attr('data-api_post_detail_url');
    let urlEndPoint = $this_.attr('data-comment_post_url');
    let api_comment_create_url = $this_.attr('data-api_comment_create_url');

    let $error_message = $this_.find('.error-message');

    let ajaxCall = $.ajax({
      method: "POST",
      url: api_comment_create_url,
      data: $formData,
     });

    ajaxCall.done(function(data, textStatus, jqxhr){
      $error_message.text('Successfully posted comment');
      let user = data.user;
      let content = data.content;
      let timestamp = data.timestamp;
      let comment_id = data.id;
      let replies = data.replies_count;
      
      let output = `<div class="card comment-card" data-comment_id="${comment_id}" id="comment_id_${comment_id}">
                  <div class="card-block">
                      <h5 class="card-title">By:${user}. <small class="text-muted">on: ${ timestamp }.  Replies: <span>${replies}</span></small></h6>
                      <p class="card-text" data-user="${ user }">${ content } </p>
                      <button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}">Reply</button> 
                      <button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/posts/comments/${comment_id}/detail/">View Replies</button> 
                      <ul class="comment-replies mt-2">
                      </ul>
                  </div>
              </div>
          `;
      $post_comments.prepend(output);
      document.querySelector("#comment_form").reset();
    });

    ajaxCall.fail(function(jqXHR, textStatus, errorThrown){
    });

  });

// button view replies
  $(document.body).on("click", ".button-view-replies", function(e){

    e.preventDefault();
    let $this_ = $(this);
    let comment_detail_url = $this_.attr('data-comment_detail_url');
    let $replies_list_ul = $this_.next('.comment-replies');
    $view_btn_replies_text = $this_.text();

    if ($this_.text() == 'View Replies'){
      $this_.text('Hide Replies');
      $replies_list_ul.show();

      $.getJSON(comment_detail_url, function(data) {

        let replies_list = data.replies;
        var items = [];
        if (replies_list == 0){
          $replies_list_ul.html('<strong> no replies yet!.</strong>');
        }
        else{
          $.each(replies_list, function(key, val) {
            let content = replies_list[key].content;
            let user = replies_list[key].user;
            let timestamp = replies_list[key].timestamp;
            let output=`<div class="card">
                            <div class="card-block">
                                <h6 class = "card-title">replied by: ${user} <small class="text-muted">on:${timestamp}</small></h6>
                                <p class="card-text"> content: ${content} </p>
                            </div>
                        </div>`; 
            items.push(output);
          });
          $replies_list_ul.html(items);
        }
      });
    }
    else{
      $this_.text('View Replies');
      $replies_list_ul.hide('slow');
    }
  });


  // reply button
  $(document.body).on("click", ".comment-reply", function(event){
    event.preventDefault();
    let $this_ = $(this);
    let comment_text = $this_.prev('p').attr('data-user');
    let post_id  = $('#post_title_id').attr('data-post_id');

    $("#replyModal #comment_text_content").text(comment_text);
    let parentId = $this_.attr("data-parent_id")
    $("#replyModal textarea").after("<input type='hidden' value='" + parentId + "' name='parent' />")
    $("#replyModal textarea").after("<input type='hidden' value='" + post_id + "' name='post' />")
  });


// form replies on Comment Form
  let $form_replies = $('.form-replies');
  $form_replies.submit(function(event){
    event.preventDefault();
    let $this_ = $(this);
    let $formData = $this_.serialize();
    let urlEndPoint = $this_.attr('data-comment_post_url'); // regular django views url
    let $error_message = $this_.find('.error-message');
    let api_replies_create_url = $this_.attr('data-api_replies_create_url'); // api views url
 
    let ajaxCall = $.ajax({
      method: "POST",
      url: api_replies_create_url,
      data: $formData,
    });

    ajaxCall.done(function(data, textStatus, jqxhr){
      $error_message.text('Successfully replied to comment!');
      // $('#replyModal').modal('hide');
       $this_.trigger("reset");
    });

    ajaxCall.fail(function(xhr, textStatus, error){
    });
      
  });


  let $posts_status = $('.posts-status');
  $posts_status.change(function(event){
    let $this_ = $(this);
    let post_id = $this_.attr('data-post_id');
    let $form = $this_.closest('.form-post-status_update');
    let $td_approved = $this_.closest('td').prev('td');

    let post_update_url = $form.attr('data-post_update_url');
    let post_approved_change_url = $form.attr('data-post_approved_change_url');
    let $formData = $form.serialize();

    if($this_.prop("checked")){
      let ajaxCall = $.ajax({
        method: "POST",
        url:post_approved_change_url ,
        data: {
          "post_id":post_id,
          "approved":"True",
        },
      });
      ajaxCall.done(function(data, textStatus, jqxhr){
        
        // $td_approved.text(data.approved);
        $td_approved.text('True');
        
      });
      ajaxCall.fail(function(xhr, textStatus, error){
        
      });
    }
    else{
      
      let ajaxCall = $.ajax({
        method: "POST",
        url:post_approved_change_url ,
        data: {
          "post_id":post_id,
          "approved":"False"
        },
      });

      ajaxCall.done(function(data, textStatus, jqxhr){
        // $td_approved.text(data.approved);
        $td_approved.text("False");
      });
      ajaxCall.fail(function(xhr, textStatus, error){
      });
    }
  });


  let $author_status = $('.author-status');
  $author_status.change(function(event){
    let $this_ = $(this);
    let user = $this_.attr('data-user');
    let $td_author = $this_.closest('td').prev('td');
    let $form = $this_.closest('.form-author-status_update');
    let $formData = $form.serialize();
    let author_add_remove_url = $form.attr('data-author_add_remove_url');

    if($this_.prop("checked")){
      $this_.prop("unchecked");
      
      let ajaxCall = $.ajax({
        method: "POST",
        url:author_add_remove_url ,
        data: {
          "username":user,
          "author_status":"True"
        },
      });
      ajaxCall.done(function(data, textStatus, jqxhr){
        $td_author.text("True");
      });
      ajaxCall.fail(function(xhr, textStatus, error){
      });

    }
    else{
      let ajaxCall = $.ajax({
        method: "POST",
        url:author_add_remove_url ,
        data: {
          "username":user,
          "author_status":"False"
        },
      });
      ajaxCall.done(function(data, textStatus, jqxhr){
        $td_author.text("False");
      });
      ajaxCall.fail(function(xhr, textStatus, error){
      });
    }
  });


  // let $api_post_list_url = $("#post_title_id").attr('data-api_post_list_url');
  let $api_post_list_url = '/api/posts/';
  let $post_list = (api_post_list_url) => {
    let $post_container = $('#container_post_list');

    $.getJSON(api_post_list_url, function(data) {   
      let post_list = data.results;
      let items = []

      if (post_list == 0){
        $post_container.html("<strong> No comments yet.</strong>");
      }
      else{
        $.each(post_list, function(key, val){
          // let timestamp = post_list[key]['timestamp'];
          // let updated = post_list[key]['updated'];
          // let content = post_list[key]['content'];
          // let user = post_list[key]['user'];
          // let replies = post_list[key]['replies_count'];
          // let comment_id = post_list[key]['id'];

          // let output = `<div class="card comment-card" data-comment_id="${comment_id}" id="comment_id_${comment_id}">
          //           <div class="card-block">
          //               <h5 class="card-title">By:${user}. <small class="text-muted">on: ${ timestamp }.  Replies: <span>${replies}</span></small></h6>
          //               <p class="card-text" data-user="${ user }">${ content } </p>
          //               <button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}">Reply</button> 
          //               <button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/posts/comments/${comment_id}/detail/">View Replies</button> 
          //               <ul class="comment-replies mt-2">
          //               </ul>
          //           </div>
          //       </div>
          //   `;
          let output = `post list`;
          // output.appendTo($post_container);
          items.push(output);
        });  
        // $post_container.html(items);
      }  
    });
  };

  $post_list($api_post_list_url);

});