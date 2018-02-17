
let $sign_up_form = document.querySelector("#signUpForm");
let $email_id = document.querySelector('#id_email');
let $id_username = document.querySelector('#id_username');
let $id_password1 = document.querySelector('#id_password1');
let $id_password2 = document.querySelector('#id_password2');
let error = document.querySelector('#error');


// for email validations
let ValidateEmail= function(email) {
    var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    return expr.test(email);
};

$sign_up_form.addEventListener("focus", function( event ) {
  // event.target.style.background = "pink";    
  	$id_username.onfocus = function(e) {
	  if (this.classList.contains('invalid-feedback')) {
	    this.classList.remove('invalid-feedback');
	    let error_message = this.parentElement.children.errorMessage;
	    error_message.textContent = "";
	  }
	};

  	$id_username.onblur = function(e) {
		let error_message = this.parentElement.children.errorMessage;
	  	if (this.value == '') { 
	    	this.classList.add('invalid-feedback');
	    	error_message.textContent = 'Please enter username.';
	  	}
	  	else{
	  		error_message.textContent = '';
	  	}
	};

	$email_id.onblur = function(e) {
	  if (!ValidateEmail(this.value)) { 
	    this.classList.add('invalid-feedback');
	    let error_message = this.parentElement.children.errorMessage;
	    error_message.textContent = 'Please enter a correct email.';
	  }
	};

	$email_id.onfocus = function(e) {
	  if (this.classList.contains('invalid-feedback')) {
	    // remove the "error" indication, because the user wants to re-enter something
	    this.classList.remove('invalid-feedback');
	    let error_message = this.parentElement.children.errorMessage;
	    error_message.textContent = "";
	  }
	};

	$id_password1.onblur = function(e) {
		let error_message = this.parentElement.children.errorMessage;
	  	if (this.value == '') { 
	    	this.classList.add('invalid-feedback');
	    	error_message.textContent = 'Please enter password.';
	  	}
	  	else if($id_password2.value!==''){
	  		if(this.value !== $id_password2.value)
	  		{
	  			error_message.textContent = 'The two password fields didn\'t match.';;
	  		}
	  	}
	  	else{
	  		error_message.textContent = '';
	  	}
	};

	$id_password1.onfocus = function(e) {
	  if (this.classList.contains('invalid-feedback')) {
	    // remove the "error" indication, because the user wants to re-enter something
	    this.classList.remove('invalid-feedback');
	    let error_message = this.parentElement.children.errorMessage;
	    error_message.textContent = "";
	  }
	};


	$id_password2.onblur = function(e) {
		let error_message = this.parentElement.children.errorMessage;
	  	if (this.value == '') { 
	    	this.classList.add('invalid-feedback');
	    	error_message.textContent = 'Please enter password confirmation.';
	  	}
	  	else if(this.value !== $id_password1.value){
	  		error_message.textContent = 'The two password fields didn\'t match.';	
	  	}
	  	else{
	  		error_message.textContent = '';
	  	}
	};

	$id_password2.onfocus = function(e) {
	  if (this.classList.contains('invalid-feedback')) {
	    // remove the "error" indication, because the user wants to re-enter something
	    this.classList.remove('invalid-feedback');
	    let error_message = this.parentElement.children.errorMessage;
	    error_message.textContent = "";
	  }
	};
	



	// $id_password2.onchange = function(){
	// 	let error_message = this.parentElement.children.errorMessage;
	// 	if (this.value !== $id_password1.value)
	// 	{
	// 		error_message.textContent = 'The two password fields didn\'t match.'
	// 	}
	// 	else{
	// 		error_message.textContent = ''
	// 	}	
		
	// };

	// $id_username.oninput = function(){
	// 	let error_message = this.parentElement.children.errorMessage;
	// 	errorMessage.textContent = this.value;
	// };

	// $id_username.onchange = function(){
	// 	let error_message = this.parentElement.children.errorMessage;
	// 	error_message.textContent = this.value;
	// };

	// $id_username.addEventListener('input', function (e) {
	// 	let error_message = this.parentElement.children.errorMessage;
	// 	error_message.textContent = e.target.value;
	// }, false);

}, true);

$sign_up_form.addEventListener("blur", function( event ) {
  // event.target.style.background = "";    
}, true);
