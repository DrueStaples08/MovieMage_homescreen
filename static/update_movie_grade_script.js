console.log("Hello from update_movie_grade_script.js");

$(document).ready(function () {
    $(".confirm-button").on("click", function () {
        var row = $(this).closest("tr");
        var movieId = row.find("button").data("movie-id");

        $.ajax({
            type: "POST",
            url: "/update_grade",
            data: {
                movie_id: movieId,
                grade: row.find(".update_grade").val()
            },
            success: function (response) {
                console.log(response);
                location.reload();
            },
            error: function (error) {
                console.error("Error updating grade:", error);
            }
        });
    });
});
