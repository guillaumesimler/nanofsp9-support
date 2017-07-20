/*	Picturehandler

	The aim of the following Javascript is to simplify the picture handling using JS
 	to manage the action mostly in the frontend and only secondly in the backend

*/


/* 1. Helper functions */
var createUrl = function() {

	var index = window.location.pathname.split('/')[2];
	var url = 'http://localhost:8000/artworks/' + index + '/pictures/JSON';
	
	return url;
};

var html_insert = function(pictures) {
	var i= 1;

	if (pictures.length > 0) {
		pictures.forEach(function(picture) {
			var html_insert = '<tr class="container">';
		
			html_insert += '<td class="col-md-5">%data%</td>';
			html_insert += '<td class="col-md-4" id="status-%ind%">Stored</td>';
			html_insert += '<td class="col-md-3"><button id="deleteButton-%ind%" value="%nb%" type="button">Delete</button></td>';
			html_insert += '</tr>';
		
			html_insert = html_insert.replace(/%ind%/g, i);
			html_insert = html_insert.replace('%nb%', picture.id);
			html_insert = html_insert.replace('%data%', picture.filename);
		
			$('#pictures_list').append(html_insert);
			i += 1;
		});
	} else {
		$('#pictures_header').text('No Related Pictures');

	}
};

var collect_id = function(id){
	var value = JSON.parse($("#delete_picture").val());
	value.push(id);
	value = '[' + value + ']'
	$("#delete_picture").val(value);
};

var remove_id = function(id){
	var values = JSON.parse($("#delete_picture").val());
	var newvalues = []

	values.forEach(function(value){
		if (value !== Number(id)) {
			newvalues.push(value)
		}
	})
	
	value = '[' + newvalues + ']'
	$("#delete_picture").val(value);
};


/* 2. Eventlistener  */
var deleteButtons = function(pictures) {
	var i = 1;

	pictures.forEach(function(picture){
		var target = "#deleteButton-" + i,
			status = "#status-" + i;
		var	id = $(target).val();

		$(target).click(function() {

			if ($(status).text() === 'Stored') {
				$(status).text('to be deleted');
				$(target).text('Cancel');

				collect_id(id);

			} else {
				$(status).text('Stored');
				$(target).text('Delete');

				remove_id(id);

			}
		});
		
		i += 1 ;
	})	
};

var loadNewPicture = function() {
	var origin = $("#new_picture"),
		target = $("#upload_picture");

	origin.change(function(event) {
		console.log('starting ...')
		var tmppath = URL.createObjectURL(event.target.files[0]);
		
		target.val(tmppath)
		console.log('finished: ' +tmppath)


	})

}


/* 3. Ajax request */



var getpictures = function() {

	// correct later
	var url = createUrl();

	$.ajax({
		url: url,
		datatype: 'json'
	})
	.done(function(responses) {
		console.log('AJAX request worked !');
		console.log(responses);

		var pictures = responses.pictures;

		// Start the functions
		html_insert(pictures);
		
		deleteButtons(pictures);
		loadNewPicture();

	})
	.fail(function(responses){
		console.log('Ajax failed!');
	});
}();






// var loadNewPicture = function(){

// 	var loader = $('#new_picture');

// 	loader.change(function(){
// 		console.log('Listener triggered, value =' + loader.val() );

// 		if (loader.val()) {
// 			var html_insert = '<tr class="container">';
		
// 			html_insert += '<td class="col-md-6">%data%</td>';
// 			html_insert += '<td class="col-md-3">will be added</td>';
// 			html_insert += '<td class="col-md-3">Delete</td>';
// 			html_insert += '</tr>';
		
// 			html_insert = html_insert.replace('%data%', loader.val());
		
// 			$('#pictures_list').append(html_insert);

// 			loader.val('');
// 		} 

// 	});
// }();






