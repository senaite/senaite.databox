/* SENAITE DATABOX JS */

document.addEventListener("DOMContentLoaded", () => {
  console.debug("*** SENAITE.DATABOX::DOMContentLoaded: --> Loading JS Controller");

  let columns = document.querySelector("#columns");
  let add_btns = document.querySelectorAll("button.add_column");
  let del_btns = document.querySelectorAll("button.del_column");

  add_btns.forEach((item )=> {
    item.addEventListener("click", (event) => {
      event.preventDefault();
      let target = event.currentTarget;
      let node = target.closest("li");
      let new_node = node.cloneNode(true);
      let add_btn = new_node.querySelector("button.add_column");
      add_btn.style.display = "none";
      columns.append(new_node);
    });
  });

  del_btns.forEach((item )=> {
    item.addEventListener("click", (event) => {
      event.preventDefault();
      let target = event.currentTarget;
      target.closest("li").remove();
    });
  });
  $(columns).sortable();

  // https://getbootstrap.com/docs/4.5/components/navs/#events
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    location.hash = e.target.hash;
    let el = document.querySelector("input[name='hash']");
    el.value = e.target.hash;
  })

  let hash = location.hash || "#query";
  $(hash + '-tab').tab("show");
});
