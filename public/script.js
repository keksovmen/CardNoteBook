function loaded(){
    function addCaretListeners(){
        var toggler = document.getElementsByClassName("caret");
        for (var i = 0; i < toggler.length; i++) {
          toggler[i].addEventListener("click", function() {
            this.parentElement.querySelector(".child_node").classList.toggle("active");
            this.classList.toggle("caret-down");
          });
        }
    }

    function openCurrentTree(){
        var current = document.getElementById("current_dir");
        if (current == null){
            return;
        }
        while (current.tagName != "LI"){
            current = current.parentNode
        }
        var children = current.querySelector(".child_node");
        if (children != null){
            children.classList.toggle("active");
            current.getElementsByClassName("caret")[0].classList.toggle("caret-down")
        }
        var p = current.parentNode;
        while (p.className != "tree"){
            if (p.className == "child_node"){
                p.classList.toggle("active");
            }
            if (p.tagName == "LI"){
                p.getElementsByClassName("caret")[0].classList.toggle("caret-down")
            }
            p = p.parentNode;
        }
    }

    function resizeTreeView(){
        var view = document.getElementsByClassName("tree_view")[0];
        if (view == null){
            return;
        }
        view.style["height"] = (window.innerHeight - 130) + "px";
    }

    addCaretListeners();
    openCurrentTree();
    resizeTreeView();
}