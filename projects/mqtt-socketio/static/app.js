$(document).ready(() => {
  var socketio = io();

  socketio.on("connect", () => {
    console.log("Connection established");
  });

  // console log the text from the dropdown list
  $("#client").change(() => {
    var element_text = $("#topic option:selected").text();
    var element_value = $("#topic option:selected").val();
    console.log("CLIENT: { " + element_value + " }" + " -> " + element_text);
  });

  //get the information from the message dropdown list
  $("#message").change(() => {
    var element_text = $("#message option:selected").text();
    var element_value = $("#message option:selected").val();
    console.log("MSG: { " + element_value + " }" + " -> " + element_text);
  });

  //get the information from the topic dropdown list
  $("#topic").change(() => {
    var element_text = $("#topic option:selected").text();
    var element_value = $("#topic option:selected").val();
    console.log("TOPIC: { " + element_value + " }" + " -> " + element_text);
  });

  $("#client-submit").click(() => {
    var client = $("#client option:selected").val();
    var msg = $("#message option:selected").text();
    var topic = $("#topic option:selected").val();

    $("#client-show").html(
      "<p> Client <strong>" +
        client +
        "</strong> will publish message: <strong>" +
        msg +
        " </strong>" +
        "on topic <strong>" +
        topic +
        "</strong>.</p>"
    );
    socketio.emit("client-request", { client: client, topic: topic, msg: msg });
  });
});
