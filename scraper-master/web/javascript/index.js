
API = "http://127.0.0.1:5000/"
page1 = false

async function submitURL() {
    if (page1 === true) { return chooseFolder() }

    URLS = document.getElementById("url-area").value;  // Get list of URLs
    console.log(URLS)

    // Trigger loading animation
    document.getElementById("main-body").className = "main-body-2"
    document.getElementById("url-area").className = "url-area-2"
    document.getElementById("submit-button").className = "submit-button-2"
    document.getElementById("loading").className = "loading-2"
    document.getElementById("title").className = "title-2"
    setTimeout(() => {  document.getElementById("title").innerHTML = "Please Wait" }, 1000);
    setTimeout(() => {  document.getElementById("loading").className = "loader"}, 3000);

    // Send post request to api
    const newTxt = URLS.split(/\r?\n/)
    let toPost = ""

    for (let i = 0; i < newTxt.length; i++) {
        toPost += newTxt[i] + ', '
    }

    let data = `{
        "text" : "${toPost}"
      }`;

    console.log("Starting request ...")
    let request = await makeRequest("POST", "http://127.0.0.1:5000/url", data);
    console.log("status:", request.status)
    console.log("response:", request.response)

    setTimeout(() => { loadPage3(); }, 3500);
    page1 = true
}

const makeRequest = (method, url, data = {}) => {
    const xhr = new XMLHttpRequest();
    return new Promise(resolve => {
      xhr.open(method, url, true);
      xhr.onload = () => resolve({
        status: xhr.status,
        response: xhr.responseText
      });
      xhr.onerror = () => resolve({
        status: xhr.status,
        response: xhr.responseText
      });
      if (method != 'GET') xhr.setRequestHeader('Content-Type', 'application/json');
      data != {} ? xhr.send(data) : xhr.send();
    })
  }

async function loadPage3() {
    // Animations
    document.getElementById("submit-button").innerHTML = "Save File"

    document.getElementById("main-body").className = "main-body-3"
    //document.getElementById("user-input").className = "path-3"
    document.getElementById("path-input").className = "path-3-t"
    document.getElementById("submit-button").className = "submit-button-3"
    document.getElementById("loading").className = "loading-3"
    document.getElementById("title").className = "title-3"
    //document.getElementById("choose-button").className = "choose-button-3"

    setTimeout(() => {  document.getElementById("title").innerHTML = "Please Enter Your Name" }, 1000);
}

async function chooseFolder() {

  let data = `{
    "text" : "${document.getElementById("path-input").value}"
  }`;

  let request = await makeRequest("POST", "http://127.0.0.1:5000/path", data);
  console.log("status:", request.status)
  console.log("response:", request.response)

  document.getElementById("title").innerHTML = "Document Saved, reloading site..."
  setTimeout(() => { location.reload(true) }, 5000);

}

// Code from here: https://developer.mozilla.org/en-US/docs/Web/API/FileSystemDirectoryHandle
async function returnPathDirectories() {

  // Get a file handle by showing a file picker:
  const handle = await self.showDirectoryPicker();
  if (!handle) {
    // User cancelled, or otherwise failed to open a file.
    console.log("User Cancelled")
    return;
  }

  // Check if handle exists inside directory our directory handle
  const relativePaths = await handle.resolve(handle);

  console.log("Part 2")

  if (relativePaths === null) {
    // Not inside directory handle
    console.log("Not inside directory handle")
  } else {
    // relativePath is an array of names, giving the relative path
    console.log(relativePaths)

    // for (let name in relativePaths) {
    //   console.log("name")
    //   // log each entry
    //   console.log(name);
    // }
  }
  }
