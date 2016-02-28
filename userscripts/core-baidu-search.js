// ==UserScript==
// @name         Core Baidu Search
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  remove the search results of baidu, only keep the ads
// @author       You
// @match        https://www.baidu.com/*
// @grant        none
// ==/UserScript==
/* jshint -W097 */
'use strict';

var white_list_regex = /百度|baidu/i;

function remove_search_results() {
    var time = new Date();
    console.log(time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds());
    console.log("removing search results...");
    
    var $suspicious = $("div.result, div.c-container");
    $.each($suspicious, function(i, node) {
        var $node = $(node);
        if (!white_list_regex.test($node.children('h3.t').text())) {
            $node.remove();
        }
    });
}

$(window).bind("load hashchange", remove_search_results);
$("div#wrapper_wrapper").bind("DOMSubtreeModified", remove_search_results);
