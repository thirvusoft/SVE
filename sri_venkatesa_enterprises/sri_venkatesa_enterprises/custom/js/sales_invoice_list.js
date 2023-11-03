frappe.listview_settings['Sales Invoice'] = {
    onload: function(list_view) {
        list_view.$page.find(`div[data-fieldname='title']`).addClass('hide');
      }
    
  };
