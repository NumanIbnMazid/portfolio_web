
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


// jquery ui modal open function
function openJqueryModal(modalId) {

    var dialogElement = $(`#${modalId}`)

    // get the jquery ui dialog class name
    dialogClassName = dialogElement.attr("class").split(" ").filter(function (item) {
        return item.includes("jquery-ui-dialog")
    })[0]

    // get jquery ui dialog options
    var UIoptions = getJqueryUIoption(dialogClassName)

    // open the dialog
    dialogElement.dialog(UIoptions).dialog("open")
}


// jquery ui modal close function 1
function closeJqueryModal(modalId) {

    var dialogElement = $(`#${modalId}`)

    // get the jquery ui dialog class name
    dialogClassName = dialogElement.attr("class").split(" ").filter(function (item) {
        return item.includes("jquery-ui-dialog")
    })[0]

    // get jquery ui dialog options
    var UIoptions = getJqueryUIoption(dialogClassName)

    // close the dialog
    dialogElement.dialog(UIoptions).dialog("close")
}

// jquery ui modal close function 2
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
    // close the dialog
    $(`#${dialog}`).dialog("close")
})
