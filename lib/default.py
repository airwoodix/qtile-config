class style:
    font = 'Monospace'
    clock_format = '%a %d. %b kw%V %H:%M:%S'
    fontsize = 12
    icon_size = 14
    border_width = 1

    class color:
        black = '#000000'
        blue = '#215578'
        bright_blue = '#18BAEB'
        grey = '#111111'
        red = '#ff0000'


layout_defaults = {
    'margin': 0,
    'border_width': style.border_width,
    'border_normal': style.color.grey,
    'border_focus': style.color.blue,
}

floating_layout_defaults = {
    'margin': 0,
    'border_width': style.border_width,
    'border_normal': style.color.grey,
    'border_focus': style.color.blue,
}

bar_defaults = {
    'size': 24,
    'background': style.color.black,
    'font': style.font,
    'padding': 0,
}

widget_defaults = {
    'font': style.font,
    'fontsize': style.fontsize,
}

widget_graph_defaults = {
    'margin_y': 4,
    'border_width': 1,
    'line_width': 1,
}

widget_sep_defaults = {
    'foreground': style.color.blue,
    'linewidth': 2,
    'height_percent': 55,
    'padding': 14,
}
