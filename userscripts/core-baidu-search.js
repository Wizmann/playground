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

function remove_search_results() {
    var time = new Date();
    console.log(time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds());
    console.log("removing search results...");
    $("div.result, div.c-container").remove();
}

$(window).bind("load hashchange", remove_search_results);
$("div#wrapper_wrapper").bind("DOMSubtreeModified", remove_search_results);
