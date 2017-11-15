let $id_title = document.querySelector('#id_title');
let $id_content = document.querySelector('#id_content');
let $id_read_time = document.querySelector('#id_read_time');

$id_title.addEventListener('input', function (e) {
		let $preview_post_title = document.querySelector('#preview_post_title');
		$preview_post_title.textContent = e.target.value;
	}, false);

$id_content.addEventListener('input', function (e) {
		let $preview_content = document.querySelector('#preview_content');
		$preview_content.innerHTML = e.target.value;
	}, false);

$id_read_time.addEventListener('input', function (e) {
		let $preview_read_time = document.querySelector('#preview_read_time');
		$preview_read_time.textContent = 'Read Time: ' + e.target.value + ' min.';
	}, false);
