paragraph = document.getElementById("text_show");
setTimeout(() => {
  const request = new Request("http://127.0.0.1:8000/");

  fetch(request)
    .then((response) => {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Something went wrong on API server!");
      }
    })
    .then((response) => {
      paragraph.innerHTML = `Hello ${response["Hello"]}`;
      console.debug(response);
    })
    .catch((error) => {
      console.error(error);
    });
}, 2000);
