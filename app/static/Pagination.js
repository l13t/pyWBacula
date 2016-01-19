/*global require, window, module*/
(function () {
    'use strict';
    var m = window.m || require('mithril/mithril');

    /*
     * Recursively merge properties of two objects
     */
    function mergeRecursive(obj1, obj2) {
        var p;
        for (p in obj2) {
            if (obj2.hasOwnProperty(p)) {
                try {
                    // Property in destination object set; update its value.
                    if (obj2[p].constructor === Object) {
                        obj1[p] = mergeRecursive(obj1[p], obj2[p]);

                    } else {
                        obj1[p] = obj2[p];

                    }

                } catch (e) {
                    // Property in destination object not set; create it and set its value.
                    obj1[p] = obj2[p];

                }
            }
        }

        return obj1;
    }

    function parseViewParameters(pagination, args) {
        var to;
        if (pagination.pages < 2) {
            return m('div', {
                'class': pagination.wrapperclass || 'ui grid'
            }, [
                pagination.pagerender([]),
                m('div')
            ]);
        }
        if (!pagination.started) {
            if (args) {
                pagination.start(args, false);
            }
        }
        pagination.started = false;
        to = (pagination.rowsperpage * pagination.currentpage);
        pagination.latest = (pagination.rowsperpage * pagination.currentpage) - pagination.rowsperpage;
        return to;
    }

    function getCurrentPage(pagination, args) {
        var page;
        pagination.data = args.data;
        if (args.page) {
            page = args.page();
        }
        pagination.currentpage = page || pagination.oldpage || pagination.currentpage || 1;
    }

    function cornerBtn(pagination, pageFlag, iconClass, increment) {
        return m('li', {
            'class': pagination.classes.iconItemClass,
            style: (pageFlag ? '' : 'cursor:pointer;'),
            onclick: pageFlag ? {} : function (e) {
                e.preventDefault();
                pagination.goToPage((pagination.currentpage + increment) || 1);
            }
        }, [
            m('a', [
                m('i', {
                    'class': iconClass + ' ' + (pageFlag ? pagination.classes.disabledClass : '')
                })
            ])
        ]);
    }

    var Pagination = {
        controller: function (cargs) {
            var pagination = this,
                classes;

            classes = {
                leftIconClass: 'left arrow icon',
                rightIconClass: 'right arrow icon',
                iconItemClass: 'icon item',
                disabledClass: 'disabled',
                menuClass: 'ui pagination menu small',
                activeClass: 'active',
                itemClass: 'item',
                wrapperclass: 'ui grid'
            };

            pagination.start = function (args, fromView) {
                getCurrentPage(pagination, args);
                pagination.pages = Math.ceil(args.data.length / args.rowsperpage);
                if (pagination.currentpage > pagination.pages) {
                    pagination.oldpage = pagination.currentpage;
                    pagination.currentpage = pagination.pages;
                } else {
                    pagination.oldpage = null;
                }
                pagination.wrapperclass = args.wrapperclass;
                pagination.classes = mergeRecursive(classes, args.classes || {});
                pagination.latest = (args.rowsperpage * pagination.currentpage) - args.rowsperpage;
                pagination.rowsperpage = args.rowsperpage;
                pagination.pagerender = args.pagerender;
                pagination.started = fromView !== undefined ? fromView : true;
            };

            pagination.start(cargs);

            pagination.goToPage = function (pageNumber) {
                m.startComputation();
                if (cargs.page) {
                    cargs.page(pageNumber);
                } else {
                    this.currentpage = pageNumber;
                }
                this.oldpage = null;
                m.endComputation();
            };
            pagination.buildNumbers = function () {
                var numbers = [],
                    i,
                    activeClass = pagination.classes.activeClass,
                    itemClass = pagination.classes.itemClass;
                //:( super ugly code for pagination
                function renderNumber(next, text, claz, withClick) {
                    return m('li', {
                        'class': itemClass + ' ' + (!withClick ? claz : ''),
                        style: 'cursor:pointer;',
                        onclick: withClick ? function (e) {
                            e.preventDefault();
                            pagination.goToPage(next);
                        } : {}
                    }, [
                        m('a', text)
                    ]);
                }

                function leftButtons() {
                    if (i > 5) {
                        if (i > 7) {
                            return;
                        }
                        numbers.push(renderNumber((i === 6 ? (pagination.currentpage + 4) : pagination.pages), (i === 6 ? '...' : pagination.pages), '', true));
                        return;
                    }
                    numbers.push(renderNumber(i, i, activeClass, pagination.currentpage !== i));
                }

                function centerButtons() {
                    if (i < 3) {
                        if (i === 2) {
                            numbers.push(renderNumber(pagination.currentpage - 4, '...', '', true));
                        } else {
                            numbers.push(renderNumber(i, 1, '', true));
                        }
                        return;
                    }
                    if (i < pagination.currentpage - 1 || (i > pagination.currentpage + 1 && i <= pagination.pages - 2)) {
                        return;
                    }
                    if (i >= pagination.pages - 2) {
                        if (pagination.pages - 1 === i) {
                            numbers.push(renderNumber(pagination.currentpage + 4, '...', '', true));
                        } else {
                            numbers.push(renderNumber(i, i, '', true));
                        }
                        return;
                    }
                    numbers.push(renderNumber(i, i, activeClass, pagination.currentpage !== i));
                }

                function rightButtons() {
                    if (i < 3) {
                        numbers.push(renderNumber((i === 2 ? (pagination.currentpage - 4) : i), (i === 2 ? '...' : 1), '', true));
                        return;
                    }
                    if (i >= pagination.pages - 4) {
                        numbers.push(renderNumber(i, i, activeClass, pagination.currentpage !== i));
                    }
                }

                if (pagination.pages > 7) {
                    for (i = 1; i <= pagination.pages; i += 1) {
                        if (pagination.currentpage < 4) {
                            leftButtons();
                        } else if (pagination.currentpage > 3 && pagination.currentpage <= pagination.pages - 4) {
                            centerButtons();
                        } else if (pagination.currentpage > pagination.pages - 4) {
                            rightButtons();
                        }
                    }
                } else {
                    for (i = 1; i <= pagination.pages; i += 1) {
                        numbers.push(renderNumber(i, i, activeClass, pagination.currentpage !== i));
                    }
                }
                return numbers;
            };
        },
        view: function (ctrl, args) {
            var pagination = ctrl,
                to,
                toRender;
            to = parseViewParameters(pagination, args);
            pagination.start(args);
            toRender = pagination.data.slice(pagination.latest, pagination.rowsperpage * pagination.currentpage);
            return m('div', {
                'class': pagination.wrapperclass
            }, [
                ctrl.pagerender(toRender),
                pagination.pages > 1 ?
                m('p', {
                    style: 'text-align:center;margin-top:10px;'
                }, [
                    m('p', (pagination.latest + 1) +
                        ' - ' +
                        (to <= pagination.data.length ? to : pagination.data.length) +
                        ' of ' + pagination.data.length
                    ),
                    m('ul', {
                        'class': pagination.classes.menuClass,
                        style: 'padding-left:0;'
                    }, [
                        cornerBtn(pagination, pagination.currentpage < 2, pagination.classes.leftIconClass, -1),
                        pagination.buildNumbers(),
                        cornerBtn(pagination, pagination.currentpage >= pagination.pages, pagination.classes.rightIconClass, 1)
                    ])
                ]) : ''
            ]);
        }
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = Pagination;
    } else {
        window.Pagination = Pagination;
    }
}());
