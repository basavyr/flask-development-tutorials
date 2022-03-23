$(document).ready(() => {
  var socket = io();

  sequence_counter = 1;

  socket.on("connect", () => {
    console.log("Connection established...");
  });

  ok = 0;
  socket.on("sequence", (msg) => {
    // console.log("Iteration " + sequence_counter);
    // console.log("Received a new random sequence");
    if (ok == 0) {
      $("#sequence-tile").append("<p> The random sequence</p>");
      ok = 1;
    }
    $("#seq-list").append(
      "<p>" + "Generated a new sequence: #" + sequence_counter + "</p>"
    );
    $("#seq-list").append('<li class="function">' + msg.sequence + "</li>");
    sequence_counter++;
  });

  // generate a console log when a seq-list list element is clicked
  $("#seq-list").on("click", "li", function () {
    console.log("Client requested sequence: " + $(this).text());
    socket.emit("request_sequence_calculation", {
      sequence: $(this).text(),
    });
  });

  $("#stopping_button").click(() => {
    console.log("Will stop the task");
    socket.emit("stop_task");
  });
});
