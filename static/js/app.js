$(document).ready(function(){

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

	$('#id_username').on({
		change:function(event){
			let $this_ = $(this);
			let error_message = $this_.next('#errorMessage');
			let urlEndPoint = "/accounts/validate_username/";

			$.ajax({
				url :urlEndPoint,
				method:'GET',
				data: {
					'username': $this_.val(),
				},
				dataType:'json',
				success: function(data){
					if(!data.username_error_message){
						$this_.closest('div').find('.error-message').show().html('username available');						
					}

					$this_.closest('div').find('.error-message').show().html(data.username_error_message);
					
				},
				error:function(xhr,status,error){
					console.log(error);
				}
			});
		},

		// focus:function(event){
		// 	$(this).closest('div').find('.error-message').hide();
		// },

		blur:function(event){
			if($(this).val() === '')
			{
				$(this).closest('div').find('.error-message').show().text('Please enter username id.');
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
					$this_.closest('div').find('.error-message').show().html(data.email_error_message);
				},
				error:function(xhr,status,error){
					console.log(error);
				}
			});

		},

		focus:function(event){
			$(this).closest('div').find('.error-message').hide();
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
		let error_message = $this_.next('#errorMessage');
		if ($this_.val() == '')
		{
			$($this_).next('#errorMessage').show().text('Please enter password');	
		}
		else{
			$($this_).next('#errorMessage').hide();		
		}	
	});


	$('#id_password2').change(function(event){
		let id_password1 = $('#id_password1').val();
		//let id_password2 = $(this).val();
		let $this_ = $(this);
		let error_message = $this_.next('#errorMessage');
		if ($this_.val() !== id_password2){
			error_message.show().text('password are not matched.');
			console.log('password\'s are not matched.');
		}
		else{
			error_message.hide();	
		}	
		
	});

});


