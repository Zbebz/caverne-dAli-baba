// https://uploadcare.com/blog/how-to-make-a-drag-and-drop-file-uploader/
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("id_file");

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

dropArea.addEventListener("dragover", preventDefaults);
dropArea.addEventListener("dragenter", preventDefaults);
dropArea.addEventListener("dragleave", preventDefaults);

dropArea.addEventListener("dragover", () => {
    dropArea.classList.add("drag-over");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("drag-over");
});

// For UX
function fileUpload() {
    const otherFields = document.querySelectorAll(".other-field");
    const fileField = document.getElementById("file-field");
    const submitButton = document.getElementById("submit-button");

    otherFields.forEach((f) => {
        f.style.display = "initial";
    });
    submitButton.style.display = "initial";
    fileField.style.display = "none";
}

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();

    // Getting the list of dragged files
    const files = e.dataTransfer.files;

    if (files.length) {
        // Assigning the files to the hidden input
        fileInput.files = files;

        fileUpload();
    }
});

// https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications#using_hidden_file_input_elements_using_the_click_method
dropArea.addEventListener("click", (e) => {
    fileInput.click();
});

fileInput.addEventListener("change", fileUpload);
