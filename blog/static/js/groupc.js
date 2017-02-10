$(document).on("click", ".modalcomment", function () {
var myCommentId = $(this).data('id');
 $(".modal-body #mycommentID").val( myCommentId );
});