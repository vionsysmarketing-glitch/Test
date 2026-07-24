document.addEventListener('DOMContentLoaded', function () {
  var menuToggle = document.getElementById('MenuToggle');
  var mobileMenu = document.getElementById('MobileMenu');
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', function () {
      var isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
      mobileMenu.hidden = isOpen;
    });
  }

  var searchToggle = document.getElementById('SearchToggle');
  var searchDrawer = document.getElementById('SearchDrawer');
  if (searchToggle && searchDrawer) {
    searchToggle.addEventListener('click', function () {
      searchDrawer.hidden = !searchDrawer.hidden;
      if (!searchDrawer.hidden) {
        var input = searchDrawer.querySelector('input[name="q"]');
        if (input) input.focus();
      }
    });
  }
});
