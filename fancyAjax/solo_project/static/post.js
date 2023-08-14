const commentRequest = (id) =>
{
    fetch('/commentinfo')
        .then(response => response.text())
        .then(data =>
        {
            console.log(data);
            const modalDiv = document.createElement('div');
            modalDiv.id = "commentDiv";
            modalDiv.innerHTML = data;
            document.body.appendChild(modalDiv);
            $("#commentModal").modal('show');
            document.getElementById("commentForm").addEventListener("submit", function (event)
            {
                event.preventDefault();
                const formData = new FormData(event.target);
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const headers = new Headers();
                headers.append('X-CSRFToken', csrfToken);
                fetch("/comment/" + id, {
                    method: "POST",
                    body: formData,
                    headers: headers
                })
                    .then(response => response.text())
                    .then(data2 =>
                    {
                        result = data2.split(" ");
                        statuss = result[ 0 ];
                        console.log(statuss);
                        post_id = result[ 1 ];
                        if (statuss === "success")
                        {
                            viewPost(post_id);
                            console.log("hello");
                            $("#commentModal").modal('hide');
                            modalDiv.remove();
                        } else
                        {
                            const modalDiv2 = document.createElement('div');
                            modalDiv2.id = "logginDiv2";
                            modalDiv2.innerHTML = data2;
                            document.body.appendChild(modalDiv2);
                            $("#errorModal").modal('show');
                            $("#errorModal").on('hidden.bs.modal', function (e)
                            {
                                modalDiv2.remove();
                            });
                        };
                    })
                    .catch(error =>
                    {
                        console.error("Error submitting form:", error);
                    });
            });
            $("#commentModal").on('hidden.bs.modal', function (e)
            {
                console.log("hello");
                modalDiv.remove();
            });
        });
};