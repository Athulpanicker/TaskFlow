document.addEventListener("DOMContentLoaded", function () {

    console.log("TaskFlow JavaScript loaded.");


    // =========================================
    // DELETE CONFIRMATION
    // =========================================

    const deleteButtons =
        document.querySelectorAll(".delete-task-btn");


    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const taskTitle =
                button.dataset.taskTitle;


            const confirmed = confirm(
                `Are you sure you want to delete "${taskTitle}"?`
            );


            if (!confirmed) {

                event.preventDefault();

            }

        });

    });


    // =========================================
    // AUTO-HIDE DJANGO MESSAGES
    // =========================================

    const messageElements =
        document.querySelectorAll(".js-message");


    messageElements.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";


            setTimeout(function () {

                message.remove();

            }, 500);

        }, 3000);

    });


    // =========================================
    // DISABLE SUBMIT BUTTON AFTER SUBMISSION
    // =========================================

    const forms =
        document.querySelectorAll("form");


    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton =
                form.querySelector(".form-submit-btn");


            if (submitButton) {

                submitButton.disabled = true;

                submitButton.textContent = "Saving...";

            }

        });

    });

});