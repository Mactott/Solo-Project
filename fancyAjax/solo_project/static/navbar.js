const logginButton = document.getElementById("logginButton");
logginButton.style.cursor = 'pointer';

const addUserButton = document.getElementById("addUserButton");
addUserButton.style.cursor = 'pointer';

function logUserId (userId)
{   
    console.log(userId)
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

const logginRequest = () => {
    fetch('/loggininfo')
        .then(response => response.text())
        .then(data => {
            console.log(data)
            const modalDiv = document.createElement('div');
            modalDiv.id="logginDiv";
            modalDiv.innerHTML=data;
            document.body.appendChild(modalDiv);
            $("#logginModal").modal('show');
            document.getElementById("logginForm").addEventListener("submit", function (event)
            {
                event.preventDefault();
                const formData = new FormData(event.target);
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const headers = new Headers();
                headers.append('X-CSRFToken', csrfToken);
                fetch("/loggin", {
                    method: "POST",
                    body: formData,
                    headers: headers
                })
                    .then(response => response.text())
                    .then(data2 => {
                        if (data2 === "success")
                        {
                            window.location.href = "/";
                        } else
                        {
                        console.log(data2)
                        const modalDiv2 = document.createElement('div');
                        modalDiv2.id = "logginDiv2";
                        modalDiv2.innerHTML = data2;
                        document.body.appendChild(modalDiv2);
                        $("#errorModal").modal('show');
                        $("#errorModal").on('hidden.bs.modal', function (e)
                        {
                            modalDiv2.remove();
                        })};
                    })
                    .catch(error =>
                    {
                        console.error("Error submitting form:", error);
                    });
            });
            $("#logginModal").on('hidden.bs.modal', function (e)
            {
                modalDiv.remove();
            });
        })
}

const addUserRequest = () =>
{
    fetch('/adduserinfo')
        .then(response => response.text())
        .then(data =>
        {
            console.log(data);
            const modalDivs = document.createElement('div');
            modalDivs.id = "addUserDiv";
            modalDivs.innerHTML = data;
            document.body.appendChild(modalDivs);
            $("#addUserModal").modal('show');
            document.getElementById("addUserForm").addEventListener("submit", function (event)
            {
                event.preventDefault();
                const formData = new FormData(event.target);
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const headers = new Headers();
                headers.append('X-CSRFToken', csrfToken);
                fetch("/adduser", {
                    method: "POST",
                    body: formData,
                    headers: headers
                })
                    .then(response => response.text())
                    .then(data2 =>
                    {
                        if(data2 === "success"){
                            window.location.href = "/"
                        } else {
                        const modalDiv2 = document.createElement('div');
                        modalDiv2.id = "logginDiv2";
                        modalDiv2.innerHTML = data2;
                        document.body.appendChild(modalDiv2);
                        $("#errorModal").modal('show');
                        $("#errorModal").on('hidden.bs.modal', function (e)
                        {
                            modalDiv2.remove();
                        })};
                    })
                    .catch(error =>
                    {
                        console.error("Error submitting form:", error);
                    });
            });
            $("#addUserModal").on('hidden.bs.modal', function (e)
            {
                modalDivs.remove();
            });
        });
}

const darkLayer = document.getElementById("dark")
let darkLayerToggle = false;
const navbarToggler = document.querySelector(".navbar-toggler");
navbarToggler.addEventListener("click", function ()
{
    if(darkLayerToggle == false){
        darkLayer.style.display = "block";
        darkLayerToggle = true;
    } else {
        darkLayer.style.display = "none";
        darkLayerToggle = false;
    }
});
