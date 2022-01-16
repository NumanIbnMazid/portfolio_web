// standard
$(".jquery-ui-dialog").dialog(
    jQueryUIdialogOptions
)
// default
$(".jquery-ui-dialog-default").dialog(
    jQueryUIdialogDefaultOptions
)
// small
$(".jquery-ui-dialog-sm").dialog(
    jQueryUIdialogSmOptions
)
// medium
$(".jquery-ui-dialog-md").dialog(
    jQueryUIdialogMdOptions
)
// large
$(".jquery-ui-dialog-lg").dialog(
    jQueryUIdialogLgOptions
)
// full
$(".jquery-ui-dialog-full").dialog(
    jQueryUIdialogFullOptions
)

$(".jquery-ui-dialog-opener").click(function () {
    let dialog = $(this).attr('data-dialog')
    $(`#${dialog}`).dialog("open")
})


$(".jquery-ui-dialog-closer").click(function (e) {
    e.preventDefault()

    let dialog = null

    if ($(this).parents('.jquery-ui-dialog-sm').first().length > 0) {
        dialog = $(this).parents('.jquery-ui-dialog-sm').first().attr('id')
    }
    else if ($(this).parents('.jquery-ui-dialog-md').first().length > 0) {
        dialog = $(this).parents('.jquery-ui-dialog-md').first().attr('id')
    }
    else if ($(this).parents('.jquery-ui-dialog-lg').first().length > 0) {
        dialog = $(this).parents('.jquery-ui-dialog-lg').first().attr('id')
    }
    else if ($(this).parents('.jquery-ui-dialog-full').first().length > 0) {
        dialog = $(this).parents('.jquery-ui-dialog-full').first().attr('id')
    }
    else if ($(this).parents('.jquery-ui-dialog-default').first().length > 0) {
        dialog = $(this).parents('.jquery-ui-dialog-default').first().attr('id')
    }
    else {
        dialog = $(this).parents('.jquery-ui-dialog').first().attr('id')
    }

    $(`#${dialog}`).dialog("close")
})


// get jquery ui options from class name

function getJqueryUIoption(className) {
    let optionMap = {
        "jquery-ui-dialog-sm": jQueryUIdialogSmOptions,
        "jquery-ui-dialog-md": jQueryUIdialogMdOptions,
        "jquery-ui-dialog-lg": jQueryUIdialogLgOptions,
        "jquery-ui-dialog-full": jQueryUIdialogFullOptions,
        "jquery-ui-dialog-default": jQueryUIdialogDefaultOptions,
        "jquery-ui-dialog": jQueryUIdialogOptions
    }

    // check if class name is in optionMap
    if (optionMap[className]) {
        return optionMap[className]
    }
    else {
        return jQueryUIdialogOptions
    }
}
