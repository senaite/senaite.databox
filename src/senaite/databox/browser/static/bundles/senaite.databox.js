!function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(o,r,function(t){return e[t]}.bind(null,r));return o},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/++plone++senaite.databox.static/bundles",n(n.s=0)}([function(e,t,n){n(1),e.exports=n(3)},function(e,t,n){(function(e){document.addEventListener("DOMContentLoaded",(function(){console.debug("*** SENAITE.DATABOX::DOMContentLoaded: --\x3e Loading JS Controller");var t=document.querySelector("#columns-list"),n=document.querySelectorAll("button.add_column"),o=document.querySelectorAll("button.del_column"),r=document.querySelector("input[name='tab']").value||"query";e("#".concat(r,"-tab")).tab("show"),e(t).sortable();var u=function(e){e.preventDefault(),e.currentTarget.closest("li").remove()},c=function e(n){n.preventDefault();var o=n.currentTarget.closest("li").cloneNode(!0),r=o.querySelector("button.add_column"),c=o.querySelector("button.del_column");r.addEventListener("click",e),c.addEventListener("click",u),t.append(o)};n.forEach((function(e){e.addEventListener("click",c)})),o.forEach((function(e){e.addEventListener("click",u)})),e('a[data-toggle="tab"]').on("shown.bs.tab",(function(e){document.querySelector("input[name='tab']").value=e.target.hash.slice(1)}))}))}).call(this,n(2))},function(e,t){e.exports=jQuery},function(e,t,n){}]);