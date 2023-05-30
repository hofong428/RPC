// ==UserScript==
// @name         crack the code
// @namespace    codebat_raymond
// @version      0.1
// @description  crack the cookie
// @author       Raymond
// @match        http://www.toutiao.com/*
// @grant        none
// @require      https://sekiro.virjar.com/sekiro-doc/assets/sekiro_web_client.js
// ==/UserScript==

(function() {
    'use strict';
    function guid() {
    function S4() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
    }
    var client = new SekiroClient("ws://127.0.0.1:5620/business-demo/register?group=tt-test&clientId="+guid());

    client.registerAction("toutiao",function(request, resolve, reject){

        var oss = request['url']
        resolve(window.byted_acrawler.sign({'url':oss}));
    })

})();