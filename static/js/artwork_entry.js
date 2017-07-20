// The aim of the following Javascript is to allow the addition of a new artist or art discipline
// within the artwork_edit.html or artwork_new.html templates

// Callback funtions
var addNewElement = function(text) {

	var value = $('#select_' + text).val();
	var target = $('#edit_new_' + text)
	var checkvalue = $('#new_' + text)

	if (value === 'new') {
		
		target.removeClass("edit_new_i")
		target.addClass("edit_new_v")
		checkvalue.val('True')

	} else {
		target.removeClass("edit_new_v")
		target.addClass("edit_new_i")
		checkvalue.val('False')
	}

}



// listener

$('#select_art').change(function() {
	addNewElement('art')
});

$('#select_artist').change(function(artist) {
	addNewElement('artist')
});
