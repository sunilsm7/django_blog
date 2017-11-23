$(document).ready(function(){
	// $('.comment-replies').hide();
	console.log('app.js loaded');
	// $('.comment-replies').hide();

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




	let $api_post_comments_list_url = $("#post_title_id").attr('data-api_post_comments_list_url');
	let $post_comment_list = function(api_post_comments_list_url){
		let $post_comments = $('#post_comments');
		console.log($api_post_comments_list_url);
		$.getJSON(api_post_comments_list_url, function(data) {	
			comment_list = data.results
			let items = []
			if (comment_list == 0){
				$post_comments.html("<strong> No comments yet.</strong>");
			}
			else{
				$.each(comment_list, function(key, val){
					let timestamp = comment_list[key]['timestamp'];
					let updated = comment_list[key]['updated'];
					let content = comment_list[key]['content'];
					let user = comment_list[key]['user'];
					let replies = comment_list[key]['replies_count'];
					let comment_id = comment_list[key]['id'];

					let output = `<div class="card comment-card">
							<div class="card-header comments-header">
								<h6>By:${user}. <small>on: ${ timestamp }. Last Updated: ${ updated } Replies: ${replies}</small></h6>
							</div>
							<div class="card-block">
								<p class="card-text">${ content } </p>
								<button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}">Reply</button> 
								<button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/posts/comments/${comment_id}/detail/">View Replies</button> 
								<ul class="comment-replies mt-2">
								</ul>
							</div>
						</div>
					`;
					// output.appendTo($post_comments);
					items.push(output);
				});	 
				$post_comments.html(items);
			}
			 
		});
	};

	// $post_comment_list($api_post_comments_list_url);

	let $api_post_detail_url = $("#post_title_id").attr('data-api_post_detail_url');
	let $post_single_comment = function(api_post_detail_url){
		let $post_comments = $('#post_comments');
		var items = []

		$.getJSON(api_post_detail_url, function(data){
			comment_list = data.comments;
			$.each(comment_list, function(key, val){
				if (comment_list[key].parent == null){
					let timestamp = comment_list[key]['timestamp'];
					let updated = comment_list[key]['updated'];
					let content = comment_list[key]['content'];
					let user = comment_list[key]['user'];
					let replies = comment_list[key]['replies_count'];
					let comment_id = comment_list[key]['id'];

					let output = `<div class="card comment-card">
							<div class="card-header comments-header">
								<h6>By:${user}. <small>on: ${ timestamp }. Last Updated: ${ updated } Replies: ${replies}</small></h6>
							</div>
							<div class="card-block">
								<p class="card-text" data-user="${ user }">${ content } </p>
								<button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}">Reply</button> 
								<button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/posts/comments/${comment_id}/detail/">View Replies</button> 
								<ul class="comment-replies mt-2">
								</ul>
							</div>
						</div>
					`;
					items.push(output);			
				}
				
			});
			return $post_comments.prepend(items);
			
		});
		
	};

$post_single_comment($api_post_detail_url);


// Sign up form validations

	let $signUpForm = $('#signUpForm');
	if ($signUpForm.attr("id") === 'signUpForm'){

		$('#id_username').on({
		change:function(event){
			let $this_ = $(this);
			let error_message = $this_.closest('div').find('.error-message');
			let urlEndPoint = $signUpForm.attr('data-url');
			console.log(urlEndPoint);

			$.ajax({
				url :urlEndPoint,
				method:'GET',
				data: {
					'username': $this_.val(),
				},
				dataType:'json',
				success: function(data){
					if($($this_).val() !== '' && !data.username_error_message){
						$(error_message).show().html('username available');						
					}

					$(error_message).show().html(data.username_error_message);
					
				},
				error:function(xhr,status,error){
					console.log(error);
				}
			});
		},

		focus:function(event){
			$(this).closest('div').find('.error-message').hide();
		},

		blur:function(event){
			let $this_ = $(this);
			let error_message = $this_.closest('div').find('.error-message');
			if($(this).val() === ''){
				$(error_message).show().text('Please enter username id.');
			}
			
		},

		});

	

		// for email validations
		let ValidateEmail= function(email) {
		    var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
		    return expr.test(email);
		};


		$('#id_email').on({
			change:function(event){
				let $this_ = $(this);
				let error_message = $this_.closest('div').find('.error-message');
				let urlEndPoint = $signUpForm.attr('data-url');
				if($this_.val() !== ''){
					if(!ValidateEmail($this_.val())){
						$this_.closest('div').find('.error-message').show().text('Please enter valid email id.');
					}
					else{
						$this_.closest('div').find('.error-message').hide();
					}
				}
				else{

					$this_.closest('div').find('.error-message').show().text('Please enter email id.');		
				}

				$.ajax({
					url :urlEndPoint,
					method:'GET',
					data: {
						'email': $this_.val(),
					},
					dataType:'json',
					success: function(data){
						$(error_message).show().html(data.email_error_message);
					},
					error:function(xhr,status,error){
						console.log(error);
					}
				});

		},

		focus:function(event){
			let $this_ = $(this);
			let error_message = $this_.closest('div').find('.error-message');
			$(error_message).hide();
		},

		blur:function(event){
			let $this_ = $(this);
			let error_message = $this_.closest('div').find('.error-message');
			if($(this).val() ===''){
				error_message.show().text('Please enter email id.');				
			}	
		},
		});

		$('#id_password1').change(function(event){
			let $this_ = $(this);
			let error_message = $this_.closest('div').find('.error-message');
			if ($this_.val() == ''){
				error_message.show().text('Please enter password');	
			}
			else{
				error_message.hide();		
			}	
		});


		$('#id_password2').change(function(event){
			let $this_ = $(this);
			let id_password1 = $('#id_password1').val();
			let error_message = $this_.closest('div').find('.error-message');
			if ($this_.val() !== id_password2){
				error_message.show().text('password\'s are not matched.');
			}
			else{
				error_message.hide();	
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
				console.log(data.message);
				console.log(textStatus);
				console.log(jqxhr);
				document.querySelector(".contact-form").reset();
			},
			error: function(xhr, status, error){
				console.log(xhr);
				console.log(status);
				console.log(error);
			},

		});
	});


// Autocomplete for search bar

	// $('#search_posts').change(function(event){
	// 	window.location.href = '/posts/list/?q=' + $(this).val().trim();
	// });

    $( "#search_posts" ).autocomplete({
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
	      		console.log(err);
	      	});	
      },
    });

  

// Comment Form
   let $comment_form = $('#comment_form');
	$comment_form.submit(function(event){
		event.preventDefault();
		let $formData =$(this).serialize();
		let $post_comments = $('#post_comments');
		let $api_post_comments_list_url = $("#post_title_id").attr('data-api_post_comments_list_url');
		let $api_post_detail_url = $("#post_title_id").attr('data-api_post_detail_url');
		let urlEndPoint = $(this).attr('data-comment_post_url');
		console.log
		let $error_message = $(this).find('.error-message');
		let ajaxCall = $.ajax({
			method: "POST",
			url: urlEndPoint,
			data: $formData,
		 });

		ajaxCall.done(function(data, textStatus, jqxhr){
			$error_message.text('Successfully posted comment');
                $post_single_comment($api_post_detail_url);
                
                
                // console.log(data.message)
				console.log(textStatus);
				console.log(jqxhr);
				document.querySelector("#comment_form").reset();
		});

		ajaxCall.fail(function(data, jqXHR, textStatus, errorThrown){
			console.log(data.message);
			console.log(xhr);
			console.log(status);
			console.log(error);
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
		   				let output = `<li> replied by: ${user} on:${timestamp} </br> content: ${content}</li>`;
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
		$("#replyModal #comment_text_content").text(comment_text);
    	let parentId = $this_.attr("data-parent_id")
		$("#replyModal textarea").after("<input type='hidden' value='" + parentId + "' name='parent_id' />")
	});


// form replies on Comment Form
	let $form_replies = $('.form-replies');
	$form_replies.submit(function(event){
		event.preventDefault();
		let $formData =$(this).serialize();
		let urlEndPoint = $(this).attr('data-comment_post_url');
		// let $thisUrl = window.location.href;

		let $error_message = $(this).find('.error-message');

		let ajaxCall = $.ajax({
			method: "POST",
			url: urlEndPoint,
			data: $formData,
		});

		ajaxCall.done(function(data, textStatus, jqxhr){
			console.log(data)
			$error_message.text('Successfully replied to comment!').fadeOut('slow');
			// document.querySelector('.form-replies').reset();
			$('#replyModal').modal('hide');
			$(".form-replies").trigger("reset");
		});

		ajaxCall.fail(function(xhr, textStatus, error){
			console.log(xhr);
			console.log(textStatus);
			console.log(error);
		});
		
	});

});


