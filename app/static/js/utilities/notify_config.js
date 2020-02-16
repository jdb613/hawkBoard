function toasta(response) {
  for(var A=0;A<response.length;A++) {
    console.log("Notify Test: ", response[A]);
    toastr.info(response[A]);
}
}
