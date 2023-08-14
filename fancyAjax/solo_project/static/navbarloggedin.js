const darkLayer = document.getElementById("dark");
let darkLayerToggle = false;
const navbarToggler = document.querySelector(".navbar-toggler");
navbarToggler.addEventListener("click", function ()
{
    if (darkLayerToggle == false)
    {
        darkLayer.style.display = "block";
        darkLayerToggle = true;
    } else
    {
        darkLayer.style.display = "none";
        darkLayerToggle = false;
    }
});

function logUserId (userId)
{
    fetch('/theirposts/' + userId)
        .then(response => response.text())
        .then(data =>
        {
            const pages = document.getElementById('pages');
            if (pages)
            {
                while (pages.firstChild)
                {
                    pages.removeChild(pages.firstChild);
                }
                pages.innerHTML = data;
            } else
            {
                console.error("Element 'pages' not found.");
            }
        })
        .catch(error =>
        {
            console.error("Fetch error:", error);
        });
}

const getMyPosts = () =>
{
    fetch('/myposts')
        .then(response => response.text())
        .then(data =>
        {
            const pages = document.getElementById('pages');
            if (pages)
            {
                while (pages.firstChild)
                {
                    pages.removeChild(pages.firstChild);
                }
                pages.innerHTML = data;
            } else
            {
                console.error("Element 'pages' not found.");
            }
        })
        .catch(error =>
        {
            console.error("Fetch error:", error);
        });
};


const newPostRequest = () =>
{
    fetch('/newpostinfo')
        .then(response => response.text())
        .then(data =>
        {
            console.log(data);
            const modalDiv = document.createElement('div');
            modalDiv.id = "newPostDiv";
            modalDiv.innerHTML = data;
            document.body.appendChild(modalDiv);
            $("#newPostModal").modal('show');
            document.getElementById("newPostForm").addEventListener("submit", function (event)
            {
                event.preventDefault();
                const formData = new FormData(event.target);
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const headers = new Headers();
                headers.append('X-CSRFToken', csrfToken);
                fetch("/newpost", {
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
                            $("#newPostModal").modal('hide');
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
            $("#newPostModal").on('hidden.bs.modal', function (e)
            {
                console.log("hello")
                modalDiv.remove();
            });
        });
};

const editRequest = (id) =>
{
    fetch("/editinfo/" + id)
        .then(response => response.text())
        .then(data =>
        {
            console.log(data);
            const modalDiv = document.createElement('div');
            modalDiv.id = "newPostDiv";
            modalDiv.innerHTML = data;
            document.body.appendChild(modalDiv);
            $("#newPostModal").modal('show');
            document.getElementById("newPostForm").addEventListener("submit", function (event)
            {
                event.preventDefault();
                const formData = new FormData(event.target);
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const headers = new Headers();
                headers.append('X-CSRFToken', csrfToken);
                fetch("/editpost/" + id, {
                    method: "POST",
                    body: formData,
                    headers: headers
                })
                    .then(response => response.text())
                    .then(data2 =>
                    {
                        result = data2.split(" ")
                        statuss = result[ 0 ]
                        console.log(statuss)
                        post_id = result[ 1 ]
                        if (statuss === "success")
                        {
                            viewPost(post_id);
                            console.log("hello");
                            $("#newPostModal").modal('hide');
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
            $("#newPostModal").on('hidden.bs.modal', function (e)
            {
                console.log("hello")
                modalDiv.remove();
            });
        });
};

const deleteRequest = (id) =>
{
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const headers = new Headers();
    headers.append('X-CSRFToken', csrfToken);
    fetch("/delete/" + id, {
        method: "DELETE",
        headers: headers
    })
        .then(response => response.text())
        .then(data2 =>
        {
            if (data2 === "success")
            {
                window.location.href = "/";
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

};
$("#newPostModal").on('hidden.bs.modal', function (e)
{
    console.log("hello");
    modalDiv.remove();
});

