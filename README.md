# RPC
use rpc as complement tool
if the encrypt method is sign = vx('123123123')
export window.xx = vx
use the rpc resolve(window.xx('123123123'))
1. console injection
   http://q.10jqka.com.cn/
   interface: 1/
   cookie1: v=A8yDfEzLxG5WEdCSoed6pOSJnSH7BXH1cquEcyaM2Zcbe2KfThVAP8K5VAp1
   cookie2: v=AxhXULjPyIr63eQOdV7mAJj16U2vAX1g3mZQD1IIZSMHJ7bz-hFMGy51IJGh
   console: output document.cookie, then we use the hook cookie output on console:
   follow the stack:
   set -> o L cookie formed
   o -> D return Qn.setCookie(Fn, n, o[248], A, t[215])
        Qn: from document, Fn = 'v', n = 'A-eoLUOiT49x-MsD0Q8BZaPwdhC0bLmLFUM_wrlVAoacYglOwTxLniUQzzHK'(cookie value)
        o[248] = time, A = domain name, t[215] = '/'
   Hook catch the cookie-> v=A-eoLUOiT49x-MsD0Q8BZaPwdhC0bLmLFUM_wrlVAoacYglOwTxLniUQzzHK; domain=10jqka.com.cn; path=/; expires=Fri, 01 Feb 2050 00:00:00 GMT
   test: Qn.setCookie('ps', '123123123123', o[248], A, t[215]) then output
        Hook catch the cookie-> ps=123123123; domain=10jqka.com.cn; path=/; expires=Fri, 01 Feb 2050 00:00:00 GMT
    reload and hook cookie again, we find
     rt.update() and output:
     'A2wjXKwrJE66yTByCtzaRETpPUGbJRA2EsgklcateC67FwL_7jXgX2LZ9CoV'
     hover on it then link to functionD(){}
     D() output:
     'A3Q7RHQDrNbyETiawxJCLBxBRTnjTZjO2nAsfQ7VAEaDvxrnNl1oxyqB_Add'
     input sss = D
     then output sss()
     'AzN8Aa-mU6sJXB9_qxiNwVc8wjxYaMfTgf0LWOXQj2uIIl2ibThXepHMm6P2'
     means we call call it, deactive breakpoints we still can call it.
     Next, we will transfer it to the RPC:
     set the pn = D(), output pn:
     'A4_ANWvaN_cVSDML7lfp7duIHiictOMvfQnnzKGcK0cEtqFWqYRzJo3YdxWy'
     -- console export
        --- find the encrypt location, export the core encrypt spot
        --- RPC connection inject console (inject web client connection)
            ### note: if the status still under debugging, it will not execute the injection
            inject RPC client connection and release all the breakpoints first:
            ---- click the Deactivate breakpoints, then click the debugger to resume, make sure the hook still works
            ---- copy the sekiro web client (inject console)
            ---- use sss() to make sure cookie value extraction works
            ---- we write forwarding scripts:(uuid template)
                function guid() {
                    function S4() {
                        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
                    }
                    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
                }
                // connect server
                var client = new SekiroClient("ws://127.0.0.1:5620/business-demo/register?group=ws-group&clientId="+guid());
                // business api
                client.registerAction("10jqka",function(request, resolve, reject){
                    resolve(sss());
                })
        --- then we go to the 02-index.js (forwarding api):
                import uuid
                import requests

                data = {
                    "group": "ws-group",
                    "action": "sign",
                    "sig": '123123123'
                    }
                pwd = requests.get("http://127.0.0.1:5620/business-demo/invoke",params=data )
                print(pwd.json().get('data'))

                data = {
                    "group": "ws-group",
                    "action": "10jqka"
                    }
                sign = requests.get("http://127.0.0.1:5620/business-demo/invoke",params=data )
                print(sign.json().get('data'))
                then run it, get the cookie value
        --- but the shortcoming is it must restart after reload page

2. Tampermonkey injection
   -- create new scripts
      can reload page, but cannot close the webpage
Crack the tautiao.com:
https://www.toutiao.com/
interface: feed?offset=0...
Headers >> copy Request URL to url to output
so we must crack and manage the _signature:
1. position first:
   -- hook url
   -- search '_signature'
      we find _signature: n
      we debug on var n = u(p.getUri(e), e);
      _signature = u(p.getUri(e), e);
      change the tag to break
2. If we can inject RPC or not rely on the p.getUri(e), output it then we get the cleartext:
   '/hot-event/hot-board/?origin=toutiao_pc'
   lets hover on u : index.js then go to function u(e, t), debug on:
   var n, a, r = "".concat(location.protocol, "//").concat(location.host);
   output u(p.getUri(e), e) get the result(ciphertext)
   we also debug on return t.data && (o.body = t.data) after var n, a, r = ,
3. lets decompose the ternary equation:
    t.data && (o.body = t.data),
            (null === (a = null === (n = window.byted_acrawler) || void 0 === n ? void 0 : n.sign) || void 0 === a ? void 0 : a.call(n, o)) || ""
        o: object and a dictionary, so we rewrite the equation: a request address
        window.byted_acrawler.sign(o) and output:'_02B4Z6wo00101u1ciNgAAIDDMyrQfRQhM3bteIxAAN80Hn6w4lhDSX-enuimwrnSZ-c6kh8gFoq0ZjHZGeATAcKefC9hEiKTKs-ibS2BZR86xS748KcIsYyq7-7-Px4nNlHTcEIodnBTK1w78c'
        (encrypt successfully!)
    n = window.byted_acralwer
    a = n.sign
    a.call(n ,a)
    a(o) transmit the params :  '_02B4Z6wo001015aCu4AAAIDCSPTjJsJkffuWpr8AAIHZHn6w4lhDSX-enuimwrnSZ-c6kh8gFoq0ZjHZGeATAcKefC9hEiKTKs-ibS2BZR86xS748KcIsYyq7-7-Px4nNlHTcEIodnBTK1w7a7'
    aa && bb return: bb
    aa || bb return: aa
    window.byted_acrawler.sign(o) == a(o)
    o = request address
    _signature = window.byted_acrawler.sign{}
    window.xx = parameters


    How we use the tampermonkey?
    rewrite the tampermonkey:
    resolve("window.byted_acrawler.sign(o)"):

        (function() {
        'use strict';
        function guid() {
        function S4() {
            return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
        }
        return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
        }
        var client = new SekiroClient("ws://127.0.0.1:5620/business-demo/register?group=ws-group&clientId="+guid());

        client.registerAction("登陆",function(request, resolve, reject){
           var o = {
                 "url": "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
            }
            resolve("window.byted_acrawler.sign(o)");
        })

    })();
4. JS override and injection:
   -- use the hook cookie
   -- follow the stack: --> D:
        var n = rt.update(); we output it and get the cookie value:
        'A5vUSReee0bLXoekqEuViY-0KvQAcK-xqYRzIo3YdxqxbLVqFUA_wrlUAwKe'
   -- let sss = D and output the function and sss() >>> cookie value

   https://ygp.gdzwfw.gov.cn/#/44/jygg
   X-Dgi-Req-Nonce:
    1mF3LwCG4JjmYMR8
   X-Dgi-Req-Signature:
    3593cbb408131ccf1ea2d25ec78fad5f910509142ae11bdf28a3bc0ac1c2b55f >> 64 bits
    whatever which one, it is hard to global search the long syntax
    maybe the SHA256 encryption
    search for sha256, then debug on o.SHA256 = s._createHelper(f),
    or we can search for headers[.... too many and too complex, so we use the headers hook method.
        --- we can see the hint after breaking, the value is from grouping encryption
            value:
            H.toString() = 'e3b8f706cbff2fef17296abbd30025ab13942f0c5cbc352c77d94109ef27bfc8'
            Y = 'X-Dgi-Req-Signature'
            if we copy the H
            {
            ""words": [
            1435919254,
            -1145603836,
            1235977018,
            -1902055636,
            1616363873,
            193491043,
            -864698542,
            1404369800
        ],
        "sigBytes": 32
        }
            }to toll libs then it will shows the result of encryption method:
            ex.'X-Dgi-Req-Signature'= "645df3d840ff4f205ef4491e0d35724d3e4c7586332a43183cd3f6616f7997cb"

            follow the stack: (anonymous)
            let look at the   "setRequestHeader"in F && e.forEach(m, function(H, Y)

        --- follow stack to lm ..... it is very time costing
        so we click the window.XMLHttpRequest(the hook location...then stepping till we reach
         toString: function(E) {
                        return (E || p).stringify(this)
                    }, we can find the cleartext here, debug on it
         it is the algorithm inside, keep stepping, debug on return F.join(""),
         we also debug on return new d.init(v,y / 2) and return F.join(""), return new d.init(v,y) then change tag
         it stops at return new d.init(v,y)
         output E; it is the cleartext what we encrypt for:

         lets follow stack
        --- parse > parse >a_append>>>Ov
        it stops at return tJ(r + o + decodeURIComponent(u) + n), output it, it is the result of initialization:
            {
        "words": [
            1435919254,
            -1145603836,
            1235977018,
            -1902055636,
            1616363873,
            193491043,
            -864698542,
            1404369800
        ],
        "sigBytes": 32
        }
        debug on it and run it (cleartext compositions analysis)
        r + o + decodeURIComponent(u) + n = 'jkAGisItYdDViPJB k8tUyS$m dateType=&openConvert=false&pageNo=2&pageSize=10&projectType=&publishEndTime=&publishStartTime=&secondType=A&siteCode=44&thirdType=&total=248657&type=trading-type 1685281221742'
        r = 'jkAGisItYdDViPJB' : JS inside algorithm
        o = 'k8tUyS$m': JS inside algorithm
        u = param
        n = timestamp
        decodeURIComponent(u) = 'dateType=&openConvert=false&pageNo=2&pageSize=10&projectType=&publishEndTime=&publishStartTime=&secondType=A&siteCode=44&thirdType=&total=248657&type=trading-type'
        n = 1685281221742
        Keep following stacks downward: r
        look up then we find:
        l = cue(16) = 'jkAGisItYdDViPJB', there is a concatenation: const f
        lets hover on cue then link in, copy the function and paste to new opened js:
            ---- function cue(e) {
                    return [...Array(e)].map(()=>m2[aue(0, 61)]).join("")
                }
                console.log(cue(16));
                 ReferenceError: m2 is not defined
                 const m2 = "zxcvbnmlkjhgfdsaqwertyuiop0987654321QWERTYUIOPLKJHGFDSAZXCVBNM"
                ReferenceError: aue is not defined
                hover on aue:
                copy and paste
                function aue(e, t) {
                switch (arguments.length) {
                case 1:
                    return parseInt(Math.random() * e + 1, 10);
                case 2:
                    return parseInt(Math.random() * (t - e + 1) + e, 10);
                default:
                    return 0
                }
                }
        then we restore 1st param successfully.

        o = c
        c = Bu([8, 28, 20, 42, 21, 53, 65, 6]), hover on Bu and link to:
                function Bu(e=[]) {
            return e.map(t=>lue[t]).join("")
        }
        complement the lue: var lue = m2 + "-@#$%^&*+!";
        then we restore 2nd param successfully.
How to change the string to the following:
        dateType=&openConvert=false&pageNo=2&pageSize=10&projectType=&publishEndTime=&publishStartTime=&secondType=A&siteCode=44&thirdType=&total=248657&type=trading-type compares to the payload (Request Payload):
 source:{
            "type": "trading-type",
            "publishStartTime": "",
            "publishEndTime": "",
            "siteCode": "44",
            "secondType": "A",
            "projectType": "",
            "thirdType": "",
            "dateType": "",
            "total": 248657,
            "pageNo": 3,
            "pageSize": 10,
            "openConvert": false
        }
        how to change the syntax?
 import json

data = '{"type":"trading-type","publishStartTime":"","publishEndTime":"","siteCode":"44","secondType":"A","projectType":"","thirdType":"","dateType":"","total":248657,"pageNo":3,"pageSize":10,"openConvert":true}'
# dataType= &openConvert = True
'''
key = value & key = value
aa =

'''

# for key in sorted(data.keys()):

data = '{"type":"trading-type","publishStartTime":"","publishEndTime":"","siteCode":"44","secondType":"A","projectType":"","thirdType":"","dateType":"","total":248657,"pageNo":3,"pageSize":10,"openConvert":true}'
# dataType= &openConvert = True
'''
key = value & key = value
aa =

'''

# for key in sorted(data.keys()):

data_it = json.loads(data)
datas = '&'.join(['{}={}'.format(key,data_it[key]) for key in sorted(data_it.keys())])
xxx = datas.replace('True','true')
print(xxx)

r = 'jkAGisItYdDViPJB'
o = 'k8tUyS$m'
import time
params = r + o + xxx + str(int(time.time())*1000)
sign = hashlib.sha256(params.encode()).hexdigest()
print(sign)
print(str(int(time.time())*1000)))

zhipin.com
1. global search for __zp_stoken__:
    interface: main.js
     GATEWAY_TOKEN_NAME = "__zp_stoken__"
    search for GATEWAY_TOKEN_NAME
    debug on  n = (new a).z(e, parseInt(t) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3) ...under the try
    output (new a).z(e, parseInt(t) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3):
    '72fdeUC0wczQMAW1jEyosNV4wYm4jbXFFZCN6XW15RlQ7ABZ4OX8gMnkyQFV1dThceSptKX9ubT9ZN2lMAVBNV2tjISRYND4mYEs7eH91JiFhBQVGLzURUgwBO0c2ZEdEKB15RSVxEmcJXzIFJnt7e0lyUwY4cX8oOCAjfhYDA3wRCAE5CRQwXAZmEQx0XXU/LRsNQG00YQ=='
        >>> this is the encrypt result
            here comes the encrypt method : a js file changed weekly. but can br executed under browser environment
        -- lets use RPC:
            input parameters: e, t  : from background data
            function s(e, t) {
            var i = (new Date).getTime() + 2304e5
              , n = "";
            e = 'JExF04lhTh8KXCL/fX7IC8Ww5IJXoOmlRVMTq5BoccA6tPloX5Jmgr9wRrmbirT5j1CtQnjqLvDfulkCGJmI2Q=='
            t = '1685292596373'
 2. we override the main.js:
    insert the following scripts after     n = (new a).z(e, parseInt(t) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3)
        } catch (e) {}:
        --- console.log(n) ## test first
    start the RPC:
    -- inject socket connection
    -- inject interface
    inject the following scripts:
            (function () {
            var newElement = document.createElement("script");
            newElement.setAttribute("type", "text/javascript");
            newElement.setAttribute("src", "https://sekiro.virjar.com/sekiro-doc/assets/sekiro_web_client.js");
            document.body.appendChild(newElement);
            function guid() {
                function S4() {
                    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
                }
                return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
            }
            function startSekiro() {
                var client = new SekiroClient("ws://127.0.0.1:5620/business-demo/register?group=rpc-boss&clientId=" + guid());

                client.registerAction("des", function (request, resolve, reject) {

                    resolve(n);
                })
            }
            setTimeout(startSekiro, 1000)
        })();

        -- open the webclient connection
        -- create a python file:
        import requests

        data= {
            "group": "rpc-boss",
            "action": "des"
            }
        sign = requests.get("http://127.0.0.1:5620/business-demo/invoke",params=data )
        print(sign.text)

        then we get the signature value

        but we still do not solve the input param problem yet: there are tow params here:
        e, t

        lets look up the scripts, we see the  n = (new a).z(e, parseInt(t) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3)
        } catch (e) {}

        so we rewrite the js as follows:
        client.registerAction("des", function (request, resolve, reject) {

            // resolve(n);
            var _e = request['e']
            var _t = request['t']
            var _n = (new a).z(_e, parseInt(_t) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3)
            resolve(_n)
        })
        we can try to use fixed e & t input the py file, we can get result, so

        let debug on n = (new a).z(e, parseInt(t) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3)
        output e :
        'JExF04lhTh8KXCL/fX7IC8Ww5IJXoOmlRVMTq5BoccAno7xRtvNWtWltN1J3hoJUlsE7S0yRLZe+lIC2rW4Gaw=='
        and compare it with the value in cookie:
        it is the same as __zp_sseed__
        output t :
        '1685297514372'
        it is the sames as __zp_sts__
        they possibly exists in the headers (set-cookie: without http-only)

        notice: if we use RPC to import parameters, we should use different name for var

        














