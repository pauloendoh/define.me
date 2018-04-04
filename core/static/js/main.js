$(document).ready(function(){

    console.log('Sanity check #1');

    $('.update-question-form').submit(function(event){
        event.preventDefault();
        console.log('Form submitted'); //sanity check
        var question_id = $(this).find("input[type=submit]").val();
        console.log(question_id);
        update_question(this, question_id);
    });

});

function update_question(event, question_id){
    console.log('Starting update_question() function, question id = ' + question_id); //sanity check
    question_q = $(event).find("input[type=text]").val(); //sanity check
    console.log("The new question is: "+ question_q); // Sanity check

     $.ajax({
        url: "/ajax/update_question",
        type: "POST",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            question_id: question_id,
            question_q: question_q,
        } ,

        dataType: 'json',

        success : function(data){
            console.log(data.teste);
            console.log("Question updated");

        }
    });
};