$(document).ready(() => {
  console.log("Connection is OK");

  // console log the text from the dropdown list
  $("#topic").change(() => {
    // console.log($("#topic").val());
    var element_text = $("#topic option:selected").text();
    var element_value = $("#topic option:selected").val();
    console.log("{ " + element_value + " }" + " -> " + element_text);
  });

  $("#client-submit").click(() => {
    var sub_value = $("#topic option:selected").val();
    console.log("submitted the client: " + sub_value);
  });
});
