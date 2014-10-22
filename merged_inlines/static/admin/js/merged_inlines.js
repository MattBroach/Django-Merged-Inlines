    /**
     * based off of django admin inlines by Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
     *
     * modifies the formset method to insert the inline rows at the bottom of the table instead of above the template form.
     */
(function($) {
    $.fn.merged_formset = function (opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts);
        var $this = $(this);
        var $parent = $this.parent();
        var updateElementIndex = function (el, prefix, ndx) {
            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            var replacement = prefix + "-" + ndx;
            if ($(el).prop("for")) {
                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
            }
            if (el.id) {
                el.id = el.id.replace(id_regex, replacement);
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
        };
        var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
        var nextIndex = parseInt(totalForms.val(), 10);
        var maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
        // only show the add button if we are allowed to add more items,
        // note that max_num = None translates to a blank string.
        var showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0;
        $this.each(function (i) {
            $(this).not("." + options.emptyCssClass).addClass(options.formCssClass);
        });
        if ($this.length && showAddButton) {
            var addButton;
            if ($this.prop("tagName") == "TR") {
                // If forms are laid out as table rows, insert the
                // "add" button in a new table row:
                var numCols = this.eq(-1).children().length;
                $parent.prepend('<tr class="' + options.addCssClass + '"><td colspan="100"><a href="javascript:void(0)">' + options.addText + "</a></tr>");
                addButton = $parent.find("tr:first a");
            } else {
                // Otherwise, insert it immediately after the last form:
                $this.filter(":last").after('<div class="' + options.addCssClass + '"><a href="javascript:void(0)">' + options.addText + "</a></div>");
                addButton = $this.filter(":last").next().find("a");
            }
            addButton.click(function (e) {
                e.preventDefault();
                var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS");
                var template = $("#" + options.prefix + "-empty");
                var row = template.clone(true);
                row.removeClass(options.emptyCssClass)
                        .addClass(options.formCssClass)
                        .attr("id", options.prefix + "-" + nextIndex);
                if (row.is("tr")) {
                    // If the forms are laid out in table rows, insert
                    // the remove button into the last table cell:
                    row.children(":last").append('<div><a class="' + options.deleteCssClass + '" href="javascript:void(0)">' + options.deleteText + "</a></div>");
                } else if (row.is("ul") || row.is("ol")) {
                    // If they're laid out as an ordered/unordered list,
                    // insert an <li> after the last list item:
                    row.append('<li><a class="' + options.deleteCssClass + '" href="javascript:void(0)">' + options.deleteText + "</a></li>");
                } else {
                    // Otherwise, just insert the remove button as the
                    // last child element of the form's container:
                    row.children(":first").append('<span><a class="' + options.deleteCssClass + '" href="javascript:void(0)">' + options.deleteText + "</a></span>");
                }
                row.find("*").each(function () {
                    updateElementIndex(this, options.prefix, totalForms.val());
                });

                $(template).closest('tbody').append(row);
                // Update number of total forms
                $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
                nextIndex += 1;
                // Hide add button in case we've hit the max, except we want to add infinitely
                if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
                    addButton.parent().hide();
                }
                // The delete button of each row triggers a bunch of other things
                row.find("a." + options.deleteCssClass).click(function (e) {
                    e.preventDefault();
                    // Remove the parent form containing this button:
                    var row = $(this).parents("." + options.formCssClass);
                    row.remove();
                    nextIndex -= 1;
                    // If a post-delete callback was provided, call it with the deleted form:
                    if (options.removed) {
                        options.removed(row);
                    }
                    // Update the TOTAL_FORMS form count.
                    var forms = $("." + options.formCssClass);
                    $("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
                    // Show add button again once we drop below max
                    if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
                        addButton.parent().show();
                    }
                    // Also, update names and ids for all remaining form controls
                    // so they remain in sequence:
                    for (var i = 0, formCount = forms.length; i < formCount; i++) {
                        updateElementIndex($(forms).get(i), options.prefix, i);
                        $(forms.get(i)).find("*").each(function () {
                            updateElementIndex(this, options.prefix, i);
                        });
                    }
                });
                // If a post-add callback was supplied, call it with the added form:
                if (options.added) {
                    options.added(row);
                }
                $('tr:not(.empty-form, .add-row)', $(this).closest('tbody')).each(function(i, elem) {
                    $(elem).find('.field-' + opts.sortField + ' > input').val(i);
                });
            });
        }
        return this;
    };

  $.fn.mergedTabularFormset = function(options) {
    var $rows = $(this);
    var alternatingRows = function(row) {
      $($rows.selector).not(".add-row, .empty-form").removeClass("row1 row2")
        .filter(":odd").addClass("row2").end()
        .filter(":even").addClass("row1");
    };

    var reinitDateTimeShortCuts = function() {
      // Reinitialize the calendar and clock widgets by force
      if (typeof DateTimeShortcuts != "undefined") {
        $(".datetimeshortcuts").remove();
        DateTimeShortcuts.init();
      }
    };

    var updateSelectFilter = function() {
      // If any SelectFilter widgets are a part of the new form,
      // instantiate a new SelectFilter instance for it.
      if (typeof SelectFilter != 'undefined'){
        $('.selectfilter').each(function(index, value){
          var namearr = value.name.split('-');
          SelectFilter.init(value.id, namearr[namearr.length-1], false, options.adminStaticPrefix );
        });
        $('.selectfilterstacked').each(function(index, value){
          var namearr = value.name.split('-');
          SelectFilter.init(value.id, namearr[namearr.length-1], true, options.adminStaticPrefix );
        });
      }
    };

    var initPrepopulatedFields = function(row) {
      row.find('.prepopulated_field').each(function() {
        var field = $(this),
            input = field.find('input, select, textarea'),
            dependency_list = input.data('dependency_list') || [],
            dependencies = [];
        $.each(dependency_list, function(i, field_name) {
          dependencies.push('#' + row.find('.field-' + field_name).find('input, select, textarea').attr('id'));
        });
        if (dependencies.length) {
          input.prepopulate(dependencies, input.attr('maxlength'));
        }
      });
    };

    $rows.merged_formset({
      prefix: options.prefix,
      addText: options.addText,
      formCssClass: "dynamic-" + options.prefix,
      deleteCssClass: "inline-deletelink",
      deleteText: options.deleteText,
      emptyCssClass: "empty-form",
      removed: alternatingRows,
      sortField: 'index',
      added: function(row) {
        initPrepopulatedFields(row);
        reinitDateTimeShortCuts();
        updateSelectFilter();
        alternatingRows(row);
      }
    });

    return $rows;
  };
})(django.jQuery);