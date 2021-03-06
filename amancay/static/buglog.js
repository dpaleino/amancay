/* vim: set sw=4 ts=4 sts=4 noet: */
function hide_all() {
    document.getElementById("add_comment_form").style.display = "none";
    document.getElementById("reassign_form").style.display = "none";
    document.getElementById("close_form").style.display = "none";
    document.getElementById("severity_form").style.display = "none";
    document.getElementById("retitle_form").style.display = "none";
    document.getElementById("owner_form").style.display = "none";
}

function show_block(evt, block) {
    hide_all();
    document.getElementById(block).style.display = "block";
}

/* FIXME: could this be a single function? */
function show_add_comment(evt) {
    show_block(evt, "add_comment_form");
}
function show_reassign(evt) {
    show_block(evt, "reassign_form");
}
function show_close(evt) {
    show_block(evt, "close_form");
}
function show_severity(evt) {
    show_block(evt, "severity_form");
}
function show_retitle(evt) {
    show_block(evt, "retitle_form");
}
function show_owner(evt) {
    show_block(evt, "owner_form");
}
function report_spam(evt) {
    alert("TODO");
}

function show_more_actions(evt) {
    hide_all()
    select = document.getElementById("more_actions");
    index = select.selectedIndex;
    if (select.options[index].value == "reassign")
        show_reassign();
    else if (select.options[index].value == "close")
        show_close();
    else if (select.options[index].value == "severity")
        show_severity();
    else if (select.options[index].value == "retitle")
        show_retitle();
    else if (select.options[index].value == "retitle")
        show_retitle();
    else if (select.options[index].value == "owner")
        show_owner();
}
function subscribe_action(evt) {
    show_block(evt, document.getElementById("subscribe_form"));
}


function buglogConnect() {
    /* Hidden forms */
    var button = document.getElementById("subscribe_button");
    if (button)
        MochiKit.Signal.connect(button, 'onclick', subscribe_action);

    var button = document.getElementById("add_comment_button");
    if (button)
        MochiKit.Signal.connect(button, 'onclick', show_add_comment);

    var button = document.getElementById("report_spam_button");
    if (button)
        MochiKit.Signal.connect(button, 'onclick', report_spam);

    var select = document.getElementById("more_actions");
    if (select)
        MochiKit.Signal.connect(select, 'onchange', show_more_actions);
}

MochiKit.DOM.addLoadEvent(buglogConnect);
