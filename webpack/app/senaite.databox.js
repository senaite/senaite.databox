/* SENAITE DATABOX JS */

document.addEventListener("DOMContentLoaded", () => {
  console.debug("*** SENAITE.DATABOX::DOMContentLoaded: --> Loading JS Controller");

  let columns = document.querySelector("#columns-list");
  let add_btns = document.querySelectorAll("button.add_column");
  let del_btns = document.querySelectorAll("button.del_column");

  // Handle active tab
  let el = document.querySelector("input[name='tab']");
  let tab = el.value || "query"
  $(`#${tab}-tab`).tab("show");

  // make columns sortable by drag&drop
  $(columns).sortable();

  let on_del = (event) => {
    event.preventDefault();
    let target = event.currentTarget;
    target.closest("li").remove();
  }

  let on_add = (event) => {
    event.preventDefault();
    let target = event.currentTarget;
    let node = target.closest("li");
    let new_node = node.cloneNode(true);
    let add_btn = new_node.querySelector("button.add_column");
    let del_btn = new_node.querySelector("button.del_column");
    add_btn.addEventListener("click", on_add);
    del_btn.addEventListener("click", on_del);
    columns.append(new_node);
  }

  add_btns.forEach((item )=> {
    item.addEventListener("click", on_add);
  });

  del_btns.forEach((item )=> {
    item.addEventListener("click", on_del);
  });

  // https://getbootstrap.com/docs/4.5/components/navs/#events
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    let tab = document.querySelector("input[name='tab']");
    // omit the `#` symbol
    tab.value = e.target.hash.slice(1);
  })

});
