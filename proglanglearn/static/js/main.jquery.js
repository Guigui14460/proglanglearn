$(function () {
    // Hide loader
    $('.loader').addClass('hidden');

    // Scroll top button and scroll progress
    $('#btnScrollToTop').hide().click(function () { $('html, body').animate({ scrollTop: 0, scrollLeft: 0 }, 500) });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 700) {
            $('#btnScrollToTop').show();
        } else {
            $('#btnScrollToTop').hide();
        }

        let scroll = $(this).scrollTop(),
            dh = $(document).height(),
            wh = $(window).height(),
            value = (scroll / (dh - wh)) * 100;
        $('#page-scroll-progress').css('width', value + '%');
    });

    // Themes (dark and light)
    if (localStorage.getItem('theme')) {
        $('html').attr('data-theme', localStorage.getItem('theme'));
    };
    if ($('html').data('theme') === 'dark') {
        $('input[name=theme]').prop('checked', true);
    } else {
        $('input[name=theme]').prop('checked', false);
    }
    $('input[name=theme]').change(function () {
        if ($(this).is(':checked')) {
            $('html').attr('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            $('html').attr('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
        $('html').addClass('transition');
    });

    // Language switcher
    $('#version-switcher').click(function () { $(this).toggleClass('show-languages') });

    // Smooth animation on link
    $('a').click(function (event) {
        if ($(this).attr('href') == "#") {
            $('html, body').animate({ scrollTop: 0, scrollLeft: 0 }, 500);
        } else if (this.hash !== "") {
            var hash = this.hash;
            $('html, body').animate({ scrollTop: $(hash).offset().top, scrollLeft: 0 }, 500, function () { window.location.hash = hash; });
        }
    });

    // Navbar search
    const expandSearchBar = () => {
        $('#main-navbar').toggleClass('search-expanded');
        closeAllDropdown();
    }
    if ($('#search') !== null) {
        $('#search').focusin(expandSearchBar).focusout(expandSearchBar);
    }
    if ($('#expand-search i.fa-search') !== null) {
        $('#expand-search i.fa-search').click(function () {
            $('#search').off('focusin');
            expandSearchBar();
            $('#search').focus();
            $('#search').focusin(expandSearchBar);
        });
    }

    // Navbars toggle
    $('.burger').each(function (index) {
        $(this).click(function () {
            closeAllDropdown();
            $($('.navbar-links')[index]).toggleClass('navbar-active');
            if (index === 0) {
                let links = $($('.navbar-links')[index].children);
                links.each(function (index2) {
                    if (this.style.animation == '') {
                        this.style.animation = "NavLinkFade 0.5s ease forwards " + (index2 * 0.125 + 0.5) + "s";
                    } else {
                        this.style.animation = '';
                    }
                });
            }
        });
    });

    // Dropdowns
    function closeAllDropdown() {
        $('.dropdown-toggle').each(function (index) {
            if ($(this).hasClass('show-dropdown')) {
                $(this).removeClass('show-dropdown');
            }
        });
    };
    $('.dropdown-toggle').click(function () { $(this).toggleClass('show-dropdown') });

    // Alerts
    $('.alert__dismissable').each(function (index) {
        let close = $('<i class="closebtn"</i>').html('&times;');
        close.click(function () {
            $($('.alert__dismissable')[index]).fadeOut(400);
        });
        let currentAlertText = $(this).text();
        $(this).html(close).append(currentAlertText);
    });

    // Show password
    $('label.eye').each(function (index) {
        let input = $('#' + $(this).attr('for') + 'Input');
        $(this).click(function () {
            if (input.attr('type') === 'password') {
                input.attr('type', 'text');
            } else {
                input.attr('type', 'password');
            }
        });
    });

    // Accordions
    $('.accordion-panel').hide();
    $('.collapsible-btn').addClass('active');
    $('.accordion-btn, .collapsible-btn').click(function () {
        $(this).toggleClass('active');
        $(this).next().slideToggle();
    });

    // Toasts
    $('.toast').css({ 'visibility': 'visible' }).delay(3000).fadeOut('fast');

    // Custom select
    let customSelect = document.getElementsByClassName("custom-select");
    for (let i = 0; i < customSelect.length; i++) {
        let selectElmnt = customSelect[i].getElementsByTagName('select')[0];
        let a = document.createElement('div');
        a.setAttribute("class", "select-selected");
        a.innerHTML = selectElmnt.options[selectElmnt.selectedIndex].innerHTML;
        customSelect[i].appendChild(a);

        let b = document.createElement('div');
        b.setAttribute('class', 'select-items select-hide');
        for (let j = 1; j < selectElmnt.length; j++) {
            let c = document.createElement('div');
            c.innerHTML = selectElmnt.options[j].innerHTML;
            c.addEventListener('click', function (e) {
                let selectParent = this.parentNode.parentNode.getElementsByTagName("select")[0];
                let prev = this.parentNode.previousSibling;
                for (let k = 0; k < selectParent.length; k++) {
                    if (selectParent.options[k].innerHTML == this.innerHTML) {
                        selectParent.selectedIndex = k;
                        prev.innerHTML = this.innerHTML;
                        let sameAsSelected = this.parentNode.getElementsByClassName('same-as-selected');
                        for (let l = 0; l < sameAsSelected.length; l++) {
                            sameAsSelected[l].removeAttribute('class');
                        }
                        this.setAttribute('class', 'same-as-selected');
                        break;
                    }
                }
                prev.click();
            });
            b.appendChild(c);
        }
        customSelect[i].appendChild(b);
        a.addEventListener('click', function (e) {
            e.stopPropagation();
            closeAllSelect(this);
            this.nextSibling.classList.toggle("select-hide");
            this.classList.toggle('select-arrow-active');
        });
    }
    function closeAllSelect(elmnt) {
        let arrNo = [];
        let selectItems = document.getElementsByClassName('select-items');
        let selectSelected = document.getElementsByClassName('select-selected');
        for (let i = 0; i < selectSelected.length; i++) {
            if (elmnt == selectSelected[i]) {
                arrNo.push(i);
            } else {
                selectSelected[i].classList.remove('select-arrow-active');
            }
        }
        for (let i = 0; i < selectItems.length; i++) {
            if (arrNo.indexOf(i)) {
                selectItems[i].classList.add('select-hide');
            }
        }
    }
    document.addEventListener('click', closeAllSelect);
});