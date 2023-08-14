const paged = document.querySelector("active").textContent

function viewPage (page)
{
    console.log(page);
    fetch('/page/' + page)
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
                paged = page
                window.scrollTo(0, 0);
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

function viewMyPage (page)
{
    console.log(page);
    fetch('/mypage/' + page)
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
                paged = page;
                window.scrollTo(0, 0);
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

function viewPost (postId)
{
    console.log(postId);
    fetch('/viewpost/' + postId)
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