// aHR0cHM6Ly9naXRodWIuY29tL2x1b3N0MjYvYWNhZGVtaWMtaG9tZXBhZ2U=
$(function () {
    var themeStorageKey = 'theme';
    var $html = $('html');

    function updateThemeToggle(theme) {
        var $button = $('#theme-toggle');
        if (!$button.length) {
            return;
        }

        var isDark = theme === 'dark';
        var nextTitle = isDark ? 'Switch to light mode' : 'Switch to dark mode';

        $button.attr('aria-checked', isDark ? 'true' : 'false');
        $button.attr('title', nextTitle);
    }

    function applyTheme(theme) {
        $html.attr('data-theme', theme);
        updateThemeToggle(theme);
    }

    function getPreferredTheme() {
        var storedTheme = localStorage.getItem(themeStorageKey);
        if (storedTheme) {
            return storedTheme;
        }

        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }

        return 'light';
    }

    var initialTheme = getPreferredTheme();
    applyTheme(initialTheme);

    $('#theme-toggle').on('click', function () {
        var nextTheme = $html.attr('data-theme') === 'dark' ? 'light' : 'dark';
        localStorage.setItem(themeStorageKey, nextTheme);
        applyTheme(nextTheme);
    });

    $('img.lazy').each(function () {
        var $img = $(this);
        var src = $img.data('src');
        if (src) {
            $img.attr('src', src);
            $img.removeAttr('data-src');
        }
        $img.removeClass('lazy');
    });

    $('div.lazy').each(function () {
        var $div = $(this);
        var src = $div.data('src');
        if (src) {
            $div.css({
                'background-image': 'url(' + src + ')',
                'background-size': 'cover',
                'background-position': 'center'
            });
            $div.removeAttr('data-src');
        }
        $div.removeClass('lazy');
    });

    $('[data-toggle="tooltip"]').tooltip()

    var $grid = $('.grid').masonry({
        "percentPosition": true,
        "itemSelector": ".grid-item",
        "columnWidth": ".grid-sizer"
    });
    // layout Masonry after each image loads
    $grid.imagesLoaded()
        .progress(function () {
            $grid.masonry('layout');
        })
        .always(function () {
            $grid.addClass('is-ready');
            $grid.masonry('layout');
        });

    $grid.find('img').on('load', function () {
        $grid.masonry('layout');
    });

    requestAnimationFrame(function () {
        $('.page-transition').addClass('is-visible');
    });
})
