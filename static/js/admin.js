document.addEventListener("DOMContentLoaded", function () {
  var container = document.getElementById("editor-container");
  var hiddenInput = document.getElementById("hidden-content");
  var form = document.getElementById("blog-form");

  if (container && hiddenInput) {
    var quill = new Quill("#editor-container", {
      theme: "snow",
      placeholder: "Write your blog here...",
      modules: {
        toolbar: [
          [{ header: [1, 2, false] }],
          ["bold", "italic", "underline"],
          ["link", "image", "code-block"],
          [{ list: "ordered" }, { list: "bullet" }],
        ],
      },
    });

    // 1. If editing, put existing text into the editor
    if (hiddenInput.value) {
      quill.root.innerHTML = hiddenInput.value;
    }

    // 2. Sync whenever user types
    quill.on("text-change", function () {
      hiddenInput.value = quill.root.innerHTML;
    });

    // 3. Final sync on click
    if (form) {
      form.addEventListener("submit", function (e) {
        // Handle Quill's empty state: <p><br></p>
        if (quill.getText().trim().length === 0) {
          alert("Blog content cannot be empty!");
          e.preventDefault();
          return false;
        }
        hiddenInput.value = quill.root.innerHTML;
      });
    }
  }
});
