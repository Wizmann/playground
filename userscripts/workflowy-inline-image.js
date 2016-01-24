// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://workflowy.com/*
// @grant        none
// ==/UserScript==
/* jshint -W097 */
'use strict';

function do_parseImg() {
    $(this).nextAll(".content-img").remove();
    var lines = $(this).text().split("\n");
    var img_re = /^\!\[.*\]\((.+)\)$/;

    for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        var img = line.match(img_re);
        if (img === null) {
            continue;
        }
        console.log(i, img[1]);
        $(this).after('<div class="content-img"><img src="' + img[1] + '"/></div>')
    }
}

function parseImg() {
    $("div.notes div.content").live("click keyup", do_parseImg);
    $("div.notes div.content").each(do_parseImg);
    $("#expandButton").live("click", function() {
        $("div.notes div.content").each(do_parseImg);
    });
};

$(window).bind("load hashchange", parseImg);
