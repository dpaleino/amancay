function reload_current_view(evt) {
	var view = document.getElementById("current_view").value;
	load_bugs(evt,"/" + view + "_table/");
}

var items_changed = function(request) {
	var item_type = document.getElementById("item").name;
	var item_list = MochiKit.Async.evalJSONRequest(request)["item_list"];
	if (item_list.length == 0) {
		var dom_form = document.getElementById("item_selection");
		new_span = DIV({'class': 'toolbox_message'}, "No items selected");
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


function loading_bugs() {
		new_span = SPAN({'class': 'loading'}, "Loading...");
		replaceChildNodes(document.getElementById("loading"), new_span);
}
function loading_finished() {
	new_span = SPAN();
	replaceChildNodes(document.getElementById("loading"), new_span);
}

var got_search_results = function(request) {
	place = document.getElementById("search_results");
	replace_content(request, place);
	pagerConnect();
}

var got_bugs = function(request) {
	place = document.getElementById("main_content");
	replace_content(request, place);
}

function replace_content(request, place) {
	if (strip(request.responseText) != "") {
		place.innerHTML = request.responseText;
	} 
	else {
		new_span = SPAN({'class': 'error'}, "No bugs found");
		replaceChildNodes(place, new_span);
	}
	loading_finished();
}

var failed_bugs = function(request) {
	new_span = SPAN({'class': 'error'}, "ERROR: bug list couldn't be loaded");
	replaceChildNodes(document.getElementById("main_content"), new_span);
	loading_finished();
}

var failed_search_results = function(request) {
	new_span = SPAN({'class': 'error'}, "ERROR: search results couldn't be loaded");
	replaceChildNodes(document.getElementById("search_results"), new_span);
	loading_finished();
}

function load_bugs(evt, url) {
	loading_bugs();
	var d = doXHR(url);
	d.addCallbacks(got_bugs, failed_bugs);
	evt.preventDefault();
}

function load_search_results(evt, url) {
	loading_bugs();
	var d = doXHR(url);
	d.addCallbacks(got_search_results, failed_search_results);
	evt.preventDefault();
}

function send_page(evt) {
	url = (evt.src() + "").replace(/search/, "search_table");
	load_search_results(evt,url);
	evt.preventDefault();
}

function pagerConnect() {
	var pager = document.getElementById("pager")
	if (pager) {
		var items = pager.getElementsByTagName("a")
		for (var i = 0; i < items.length; i++) {
			 MochiKit.Signal.connect( items[i], 'onclick', send_page );
		}
	}
}

function myLoadFunction()
{
	pagerConnect();

	if (buglogConnect)
		buglogConnect();

	var link;
	link = document.getElementById("submitted_bugs_link");
	if (link)
	    MochiKit.Signal.connect( link, 'onclick', get_submitted_bugs );

	link = document.getElementById("received_bugs_link");
	if (link)
    	MochiKit.Signal.connect( link, 'onclick', get_received_bugs );

	link = document.getElementById("package_bugs_link");
	if (link)
		MochiKit.Signal.connect( link, 'onclick', get_package_bugs );

	link = document.getElementById("selected_bugs_link");
	if (link)
    	MochiKit.Signal.connect( link, 'onclick', get_selected_bugs );

	link = document.getElementById("tagged_bugs_link");
	if (link)
    	MochiKit.Signal.connect( link, 'onclick', get_tagged_bugs );
}

/*connect our event handlers right off*/
MochiKit.DOM.addLoadEvent(myLoadFunction);
