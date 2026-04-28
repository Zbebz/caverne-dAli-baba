// https://uploadcare.com/blog/how-to-make-a-drag-and-drop-file-uploader/
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("id_file");
const submitButton = document.getElementById("submit-button");

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
    const field1 = document.getElementById("field-1");
    const fileField = document.getElementById("file-field");

    field1.style.display = "initial";
    submitButton.style.display = "initial";
    fileField.style.display = "none";
}

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();

    // Getting the list of dragged files
    const files = e.dataTransfer.files;
    const acceptedFileTypes = fileInput.accept.split(",");
    if (files.length && acceptedFileTypes.includes(files[0].type)) {
        // Assigning the files to the hidden input
        fileInput.files = files;

        fileUpload();
    } else {
        const errorMessage = document.querySelector(".files-accepted");
        errorMessage.style.color = "red";
        dropArea.classList.remove("drag-over");
    }
});

// https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications#using_hidden_file_input_elements_using_the_click_method
dropArea.addEventListener("click", (e) => {
    fileInput.click();
});

fileInput.addEventListener("change", fileUpload);

const selectDropdowns = document.querySelectorAll("select");

selectDropdowns.forEach((s) => {
    const selectPlaceholder = s.firstElementChild;
    selectPlaceholder.selected = true;
    selectPlaceholder.disabled = true;
});

submitButton.addEventListener("click", () => {
    const field2 = document.getElementById("field-2");
    const fields1inputs = document.querySelectorAll(
        "#field-1 input, #field-1 select",
    );

    let exit = false;
    let skip = false;
    fields1inputs.forEach((f) => {
        if (skip) {
            return;
        }
        if (!f.reportValidity()) {
            exit = true;
            skip = true;
            return;
        }
    });

    if (exit) {
        return;
    }

    field2.style.display = "initial";

    submitButton.innerText = "Partager";
    submitButton.type = "submit";
});
