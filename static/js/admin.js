document.addEventListener("DOMContentLoaded", function () {
  var container = document.getElementById("editor-container");
  var hiddenInput = document.getElementById("hidden-content");
  var form = document.querySelector("form");

  if (container && hiddenInput) {
    // Initialize Quill
    var quill = new Quill("#editor-container", {
      theme: "snow",
      modules: {
        toolbar: [
          [{ header: [1, 2, false] }],
          ["bold", "italic", "underline"],
          ["link", "image", "code-block"],
          [{ list: "ordered" }, { list: "bullet" }],
        ],
      },
    });

    var existingContent = hiddenInput.value;
    if (existingContent) {
      quill.root.innerHTML = existingContent;
    }

    // CRITICAL: Every time you type, update the hidden field
    quill.on("text-change", function () {
      hiddenInput.value = quill.root.innerHTML;
    });

    // SAFETY: Update one last time when the "Create Blog" button is clicked
    if (form) {
      form.addEventListener("submit", function (e) {
        hiddenInput.value = quill.root.innerHTML;

        // If content is empty, alert the user (common reason for validation fail)
        if (hiddenInput.value === "<p><br></p>" || hiddenInput.value === "") {
          alert("Please enter some content for your blog.");
          e.preventDefault(); // Stop submission
        }
      });
    }
  }
});
