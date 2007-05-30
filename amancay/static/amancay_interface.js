
var packages_changed = function(request) {
	var package_list = MochiKit.Async.evalJSONRequest(request)["package_list"];
	var cells = new Array(package_list.length);
	for (var i=0; i < package_list.length; i++) {
		cells[i] = [ TD(null, INPUT({"type":"checkbox",
		"name":"package_select", "id":"package_select", "value":
		package_list[i]}, null)), TD(null, package_list[i]) ];
	}
	var rows = map(partial(TR, null), cells);
	var dom_package_list = document.getElementById("package_list");
	if (! dom_package_list) {
		dom_package_list = TABLE({"id":"package_list"})
		var dom_form = document.getElementById("package_selection");
		var dom_remove = INPUT({"type":"submit", "value": "Remove"})
    	MochiKit.Signal.connect( dom_form, 'onsubmit', send_package_selected );
		replaceChildNodes(dom_form, dom_package_list, dom_remove)
	}
	replaceChildNodes(dom_package_list, rows);
	get_package_bugs();
}

var package_remove_failed = function (err) {
  alert("The package/s could not be removed");
  alert(err);
};

var package_add_failed = function (err) {
  alert("The package could not be added");
  alert(err);
};

var send_add_package = function (ev) {
	ev.preventDefault();
	var content = queryString(["package_name"], 
                  [document.getElementById("package_name").value]);
	var d = doXHR("/index/?xhr=1", {"method": "post", "sendContent": content});
	d.addCallbacks(packages_changed, package_add_failed);
	document.getElementById("package_name").value = "";
}

var send_package_selected = function (ev) {
	ev.preventDefault();
	table = document.getElementById("package_list");
	boxes = table.getElementsByTagName("input");

	var selected_packages = Array();
	for (var i=0; i < boxes.length; i++) {
		if (boxes[i].checked == true) {
			selected_packages[i] = boxes[i].value;
		}
	}
	var content = queryString({"package_select": filter(null,selected_packages)});
	var d = doXHR("/index/?xhr=1", {"method": "post", "sendContent": content});
	d.addCallbacks(packages_changed, package_remove_failed);
}

var bugs_changed = function(request) {
	var bug_list = MochiKit.Async.evalJSONRequest(request)["bug_list"];
	var cells = new Array(bug_list.length);
	for (var i=0; i < bug_list.length; i++) {
		cells[i] = [ TD(null, INPUT({"type":"checkbox",
		"name":"bug_select", "id":"bug_select", "value":
		bug_list[i]}, null)), TD(null, bug_list[i]) ];
	}
	var rows = map(partial(TR, null), cells);
	var dom_bug_list = document.getElementById("bug_list");
	if (! dom_bug_list) {
		dom_bug_list = TABLE({"id": "bug_list"})
		var dom_form = document.getElementById("bug_selection");
		var dom_remove = INPUT({"type":"submit", "value": "Remove"})
    	MochiKit.Signal.connect( dom_form, 'onsubmit', send_bug_selected );
		replaceChildNodes(dom_form, dom_bug_list, dom_remove)
	}
	replaceChildNodes(dom_bug_list, rows);
	get_selected_bugs();
}

var bug_remove_failed = function (err) {
  alert("The bug/s could not be removed");
  alert(err);
};

var bug_add_failed = function (err) {
  alert("The bug could not be added");
  alert(err);
};

var send_add_bug = function (ev) {
	ev.preventDefault();
	var content = queryString(["bug_number"], 
                  [document.getElementById("bug_number").value]);
	var d = doXHR("/index/?xhr=1", {"method": "post", "sendContent": content});
	d.addCallbacks(bugs_changed, bug_add_failed);
	document.getElementById("bug_number").value = "";
}

var send_bug_selected = function (ev) {
	ev.preventDefault();
	table = document.getElementById("bug_list");
	boxes = table.getElementsByTagName("input");

	var selected_bugs = Array();
	for (var i=0; i < boxes.length; i++) {
		if (boxes[i].checked == true) {
			selected_bugs[i] = boxes[i].value;
		}
	}
	var content = queryString(["bug_select"], filter(null, selected_bugs));
	var d = doXHR("/index/?xhr=1", {"method": "post", "sendContent": content});
	d.addCallbacks(bugs_changed, bug_remove_failed);
}

function place_bug_table(place, request) {
	if (strip(request.responseText) != "") {
		new_table = TABLE();
		new_table.innerHTML = request.responseText;
		replaceChildNodes(place, new_table);
	} 
	else {
		new_span = SPAN({'class': 'loading'}, "No bugs found");
		replaceChildNodes(place, new_span);
	}
}

function failed_bug_table(place, request) {
	new_span = SPAN({'class': 'loading'}, "ERROR: bug list couldn't be loaded");
	replaceChildNodes(place, new_span);
};

var got_submitted_bugs = function(request) {
	place_bug_table(document.getElementById("submitted_bugs"), request);
}
var got_received_bugs = function(request) {
	place_bug_table(document.getElementById("received_bugs"), request);
}
var got_package_bugs = function(request) {
	place_bug_table(document.getElementById("package_bugs"), request);
}
var got_selected_bugs = function(request) {
	place_bug_table(document.getElementById("selected_bugs"), request);
}
var failed_submitted_bugs = function(request) {
	failed_bug_table(document.getElementById("submitted_bugs"), request);
}
var failed_received_bugs = function(request) {
	failed_bug_table(document.getElementById("received_bugs"), request);
}
var failed_package_bugs = function(request) {
	failed_bug_table(document.getElementById("package_bugs"), request);
}
var failed_selected_bugs = function(request) {
	failed_bug_table(document.getElementById("selected_bugs"), request);
}
function get_submitted_bugs() {
	var d = doXHR("/submitted_bugs/");
	d.addCallbacks(got_submitted_bugs, failed_submitted_bugs);
}
function get_received_bugs() {
	var d = doXHR("/received_bugs/");
	d.addCallbacks(got_received_bugs, failed_received_bugs);
}
function get_package_bugs() {
	var d = doXHR("/package_bugs/");
	d.addCallbacks(got_package_bugs, failed_package_bugs);
}
function get_selected_bugs() {
	var d = doXHR("/selected_bugs/");
	d.addCallbacks(got_selected_bugs, failed_selected_bugs);
}
function myLoadFunction()
{
	get_submitted_bugs();
	get_received_bugs();
	get_package_bugs();
	get_selected_bugs();

	/* Signal connection */
	var add_package = document.getElementById("add_package");
    MochiKit.Signal.connect( add_package, 'onsubmit', send_add_package );

	var package_selection = document.getElementById("package_selection");
    MochiKit.Signal.connect( package_selection, 'onsubmit', send_package_selected );

	var add_bug = document.getElementById("add_bug");
    MochiKit.Signal.connect( add_bug, 'onsubmit', send_add_bug );

	var bug_selection = document.getElementById("bug_selection");
    MochiKit.Signal.connect( bug_selection, 'onsubmit', send_bug_selected );
}

/*connect our event handlers right off*/
MochiKit.Signal.connect(window, "onload", myLoadFunction);
