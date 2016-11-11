/* site.js */
(function() { //immediate invoked function expression
    'use strict;'
    var map;
    var $sidebarAndWrapper = $('#sidebar,#wrapper');
    $('#sidebarToggle').on("click", function() {
        $sidebarAndWrapper.toggleClass('hide-sidebar');
        map.updateSize();
    });

        $(document).ready(function() {
       
        });
})();