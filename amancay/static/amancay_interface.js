
function reload_current_view(evt) {
	var view = document.getElementById("current_view").value;
	load_bugs(evt,"/"+view+"_table/");
}

var items_changed = function(request) {
	var item_type = document.getElementById("item").name;
	var item_list = MochiKit.Async.evalJSONRequest(request)["item_list"];
	if (item_list.length == 0) {
		var dom_form = document.getElementById("item_selection");
		new_span = SPAN({'class': 'toolbox_message'}, "No items selected");
		replaceChildNodes(dom_form, new_span);
	} else {
		var cells = new Array(item_list.length);
		for (var i=0; i < item_list.length; i++) {
			cells[i] = [ TD({"class":"item_select"}, INPUT({"type":"checkbox",
			"name":item_type+"_select", "id":"item_select", "value":
			item_list[i]}, null)), TD({"class":"item_name"}, item_list[i]) ];
		}
		var rows = map(partial(TR, null), cells);
		var dom_item_table = document.getElementById("item_list");
		if (! dom_item_table) {
			dom_item_table = TABLE({"id":"item_list"})
			dom_item_list = TBODY(null, null)
			replaceChildNodes(dom_item_table, dom_item_list);
			var dom_form = document.getElementById("item_selection");
			var dom_remove = DIV({"class":"toolbox_remove"},
			INPUT({"type":"submit", "value": "Remove", "class": "toolbox_remove"}))
	    	MochiKit.Signal.connect( dom_form, 'onsubmit', send_item_selected );
			replaceChildNodes(dom_form, dom_item_table, dom_remove)
		} else {
			dom_item_list = dom_item_table.getElementsByTagName("tbody")[0];
		}
		replaceChildNodes(dom_item_list, rows);
	}
	reload_current_view();
}

var item_remove_failed = function (err) {
  alert("The item/s could not be removed");
  alert(err);
};

var item_add_failed = function (err) {
  alert("The item could not be added");
  alert(err);
};

var send_item_add = function (ev) {
	ev.preventDefault();
	var content = queryString([document.getElementById("item").name],
	                          [document.getElementById("item").value]);
	var d = doXHR("/index/?xhr=1", {"method": "post", "sendContent": content});
	d.addCallbacks(items_changed, item_add_failed);
	document.getElementById("item").value = "";
}

var send_item_selected = function (ev) {
	ev.preventDefault();
	item_name = document.getElementById("item").name+"_select";
	table = document.getElementById("item_list");
	var content = queryString(table);
	var d = doXHR("/index/?xhr=1", {"method": "post", "sendContent": content});
	d.addCallbacks(items_changed, item_remove_failed);
}

function loading_bugs() {
		new_span = SPAN({'class': 'loading'}, "Loading...");
		replaceChildNodes(document.getElementById("loading"), new_span);
}
function loading_finished() {
	new_span = SPAN();
	replaceChildNodes(document.getElementById("loading"), new_span);
}


var got_bugs = function(request) {
	place = document.getElementById("bug_list");
	if (strip(request.responseText) != "") {
		new_table = TABLE();
		new_table.innerHTML = request.responseText;
		replaceChildNodes(place, new_table);
	} 
	else {
		new_span = SPAN({'class': 'error'}, "No bugs found");
		replaceChildNodes(place, new_span);
	}
	loading_finished();
}
var failed_bugs = function(request) {
	new_span = SPAN({'class': 'error'}, "ERROR: bug list couldn't be loaded");
	replaceChildNodes(document.getElementById("bug_list"), new_span);
	loading_finished();
}

var got_toolbox = function(request) {
	place = document.getElementById("toolbox");
	if (strip(request.responseText) != "") {
		new_div = DIV();
		new_div.innerHTML = request.responseText;
		replaceChildNodes(place, new_div);
		toolboxConnect();
	} 
	else {
		new_span = SPAN({'class': 'error'}, "No toolbox");
		replaceChildNodes(place, new_span);
	}
}
var failed_toolbox = function(request) {
	new_span = SPAN({'class': 'error'}, "ERROR: Unable to load toolbox");
	replaceChildNodes(document.getElementById("toolbox"), new_span);
}

function load_bugs(evt, url) {
	loading_bugs();
	var d = doXHR(url);
	d.addCallbacks(got_bugs, failed_bugs);
	evt.preventDefault();
}

function load_toolbox(url) {
	var d = doXHR(url);
	d.addCallbacks(got_toolbox, failed_toolbox);
}

function get_submitted_bugs(evt) {
	load_bugs(evt,"/submitted_bugs_table/");
	load_toolbox("/submitted_bugs_toolbox/");
}
function get_received_bugs(evt) {
	load_bugs(evt,"/received_bugs_table/");
	load_toolbox("/received_bugs_toolbox/");
}
function get_package_bugs(evt) {
	load_bugs(evt,"/package_bugs_table/");
	load_toolbox("/package_bugs_toolbox/");
}
function get_selected_bugs(evt) {
	load_bugs(evt,"/selected_bugs_table/");
	load_toolbox("/selected_bugs_toolbox/");
}
function get_tagged_bugs(evt) {
	load_bugs(evt,"/tagged_bugs_table/");
	load_toolbox("/tagged_bugs_toolbox/");
}
function get_search_form(evt) {
	load_bugs(evt,"/search_form/");
	load_toolbox("/search_form_toolbox/");
}

function toolboxConnect() {
	var item_add = document.getElementById("add_item");
    MochiKit.Signal.connect( item_add, 'onsubmit', send_item_add );
	var item_selection = document.getElementById("item_selection");
    MochiKit.Signal.connect( item_selection, 'onsubmit', send_item_selected );
}

function myLoadFunction()
{
	toolboxConnect();

	var link;
	link = document.getElementById("submitted_bugs_link");
    MochiKit.Signal.connect( link, 'onclick', get_submitted_bugs );

	link = document.getElementById("received_bugs_link");
    MochiKit.Signal.connect( link, 'onclick', get_received_bugs );

	link = document.getElementById("package_bugs_link");
    MochiKit.Signal.connect( link, 'onclick', get_package_bugs );

	link = document.getElementById("selected_bugs_link");
    MochiKit.Signal.connect( link, 'onclick', get_selected_bugs );

	link = document.getElementById("tagged_bugs_link");
    MochiKit.Signal.connect( link, 'onclick', get_tagged_bugs );

	link = document.getElementById("search_link");
    MochiKit.Signal.connect( link, 'onclick', get_search_form );
}

/*connect our event handlers right off*/
MochiKit.Signal.connect(window, "onload", myLoadFunction);
