### mainly the same screen as for the default bubbles

screen dynamic_bubble(who, what):
    style_prefix "bubble"
    key "shift_K_b" action dynamic_bubble.ToggleShown()
    window:
        id "window"

        text what:
            id "what"

define dynamic_bubble.frame = bubble.frame
define dynamic_bubble.thoughtframe = bubble.thoughtframe

define dynamic_bubble.properties = bubble.properties

define dynamic_bubble.expand_area = bubble.expand_area