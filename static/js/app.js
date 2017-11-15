$(document).ready(function(){
	$('.form-replies').hide();
	$('.comment-replies').hide();

	console.log('app.js loaded');
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
			let error_message = $this_.closest('div').find('.error-message');
			let urlEndPoint = "/accounts/validate_username/";

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
			if($(this).val() === '')
			{
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
				let urlEndPoint = "/accounts/validate_username/";
				// if($this_.val() !== ''){
				// 	if(!ValidateEmail($this_.val())){
				// 		$this_.closest('div').find('.error-message').show().text('Please enter valid email id.');
				// 	}
				// 	else{
				// 		$this_.closest('div').find('.error-message').hide();
				// 	}
				// }
				// else{

				// 	$this_.closest('div').find('.error-message').show().text('Please enter email id.');		
				// }
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

		// blur:function(event){
		// 	if($(this).val() ==='')
		// 	{
		// 		$(this).closest('div').find('.error-message').show().text('Please enter email id.');				
		// 	}	
			
		// },

		});

	

		$('#id_password1').change(function(event){
			let $this_ = $(this);
			let error_message = $this_.closest('div').find('.error-message');
			if ($this_.val() == '')
			{
				$(error_message).show().text('Please enter password');	
			}
			else{
				$(error_message).hide();		
			}	
		});


		$('#id_password2').change(function(event){
			let $this_ = $(this);
			let id_password1 = $('#id_password1').val();
			//let id_password2 = $(this).val();
			let error_message = $this_.closest('div').find('.error-message');
			if ($this_.val() !== id_password2){
				$(error_message).show().text('password\'s are not matched.');
			}
			else{
				$(error_message).hide();	
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
				// $contact_form.reset();
				console.log($contact_form);
				document.querySelector(".contact-form").reset();
			},
			error: function(xhr, status, error){
				console.log(xhr);
				console.log(status);
				console.log(error);
			},

		});
	});

// New Post and Edit post forms.

	let $new_post_form = $('#new_post_form');
	$new_post_form.submit(function(event){
		event.preventDefault();
		let $formData =$(this).serialize();
		let $thisUrl = window.location.href;
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
				document.querySelector("#new_post_form").reset();
			},
			error: function(data, xhr, status, error){
				console.log(data.message);
				console.log(xhr);
				console.log(status);
				console.log(error);
			},

		});
	});

// Autocomplete for search bar

	// $('#search_posts').change(function(event){
	// 	window.location.href = '/posts/list/?q=' + $(this).val().trim();
	// 	console.log(window.location.href);	
	// });

    $( "#search_posts" ).autocomplete({
      	minLength:3,
      	source: function(req, add){
      		let search = $('#search_posts').val();
			let form_search_post = $('#form_search_post');
			let urlEndPoint = form_search_post.attr('data-url');
			console.log(urlEndPoint);
	      	$.ajax({
	      		url:urlEndPoint,
	      		dataType: 'json',
	      		data: {'term':search},
	      		type: 'GET',
	      		success:function(data){
	      			let suggestions = [];
	      			$.each(data, function(index, objects){
	      				suggestions.push(objects);
	      			});
	      			add(suggestions);
	      		},
	      		error:function(err){
	      			console.log(err);
	      		}
	      	});
      },
    });

// Buttons reply and View Replies hide and show
   $('.button-reply').click(function(e){
   		e.preventDefault();
   		let $this_ = $(this);
   		let $form_replies = $this_.closest('div').find('.form-replies');
   		$($form_replies).toggle();
   });

   $('.button-view-replies').click(function(e){
   		e.preventDefault();
   		let $this_ = $(this);
   		let $form_replies = $this_.closest('div').find('.form-replies');
   		let $comment_replies = $this_.closest('div').find('.comment-replies');
   		$($comment_replies).toggle();
   		$($form_replies).toggle();
   });


// Comment Form

   let $comment_form = $('#comment_form');
	$comment_form.submit(function(event){
		event.preventDefault();
		let $formData =$(this).serialize();
		let $thisUrl = window.location.href;
		let $post_comments = $('#post_comments');
		let $error_message = $(this).find('.error-message');
		$.ajax({
			method: "POST",
			url: $thisUrl,
			data: $formData,
			success: function(data, textStatus, jqxhr){
				$error_message.text('Successfully posted comment');
				// $("#post_comments").load(" #post_comments");
				data = JSON.parse(data);
			 	console.log(data.fields);
			 	let timestamp = data.fields['timestamp'];
			 	let updated = data.fields['updated'];
				let content = data.fields['content'];
				let user = data.fields['user'];

				let output = `<div class="card comment-card">
						<div class="card-header comments-header">
							<h6>By:${user}. <small>on: ${ timestamp }. Last Updated: ${ updated } Replies: 0</small></h6>
						</div>
						<div class="card-block">
							<p class="card-text">${ content } </p>
							<button  class="btn btn-primary btn-sm button-reply" type="button">Reply</button> 
					<button  class="btn btn-primary btn-sm button-view-replies" type="button">0 Replies</button> 
						</div>
					</div>
				`;

				$post_comments.prepend(output);
				
				// console.log(data);
				console.log(textStatus);
				console.log(jqxhr);
				document.querySelector("#comment_form").reset();
			},
			error: function(data, xhr, status, error){
				console.log(data.message);
				console.log(xhr);
				console.log(status);
				console.log(error);
			},

		});
	});

// form replies on Comment Form
	let $form_replies = $('.form-replies');
	$form_replies.submit(function(event){
		event.preventDefault();
		let $formData =$(this).serialize();
		let $thisUrl = window.location.href;
		let $error_message = $(this).find('.error-message');
		let $comment_replies = $(this).prev('.comment-replies');
		let $no_replies_yet = $comment_replies.find('.no-replies-yet');

		$.ajax({
			method: "POST",
			url: $thisUrl,
			data: $formData,
			success: function(data, textStatus, jqxhr){
				data = JSON.parse(data);
				console.log(data["fields"])
				$error_message.text('Successfully replied to comment!');
				let timestamp = data.fields['timestamp'];
				let content = data.fields['content'];
				// let user = $('#userMenu').text();
				let user = data.fields['user']

				$comment_replies.prepend(`<li> replied by: ${user} on:${timestamp} </br> ${content}</li>`);
				// document.querySelector('.form-replies').reset();
				$(".form-replies").trigger("reset");
				$no_replies_yet.hide();
			},
			error: function(data, xhr, textStatus, error){
				console.log(data);
				console.log(xhr);
				console.log(textStatus);
				console.log(error);
			},

		});
	});



});


