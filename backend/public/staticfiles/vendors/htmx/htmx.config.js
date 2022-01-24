document.body.addEventListener(

    // handle htmx response error
    'htmx:responseError', (event) => {
        if (event.detail.successful === false) {

            // TODO: This URLs are defined in `admin-panel/components/hidden-components.html`

            // var url_400 = $("#400URL").attr("data-url")
            // var url_403 = $("#403URL").attr("data-url")
            // var url_404 = $("#404URL").attr("data-url")
            // var url_500 = $("#500URL").attr("data-url")

            if (event.detail.xhr.status != null) {
                toastr.error(event.detail.xhr.status + ": " +
                    event.detail.xhr.statusText).css("min-width", "200px").css("width", "350px").css("max-width", "100%")
            } else {
                toastr.error(event.detail.error).css("min-width", "200px").css("width", "350px").css("max-width", "100%")
            }

            // TODO: redirect urls
            // if (event.detail.xhr.status == 400) {
            //     window.location.replace(url_400)
            // }
            // else if (event.detail.xhr.status == 403) {
            //     window.location.replace(url_403)
            // }
            // else if (event.detail.xhr.status == 404) {
            //     window.location.replace(url_404)
            // }
            // else if (event.detail.xhr.status == 500) {
            //     window.location.replace(url_500)
            // }
            // else {
            //     console.log(event.detail.error)
            // }
        }
    },

    // manage csrf token for htmx request
    'htmx:configRequest', (event) => {
        event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}'
    }
)
