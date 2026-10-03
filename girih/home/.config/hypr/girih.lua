-- Girih look and feel.
-- Loaded after futuwwa.lua so these values win; behaviour and binds stay there.
--
-- Chamfer: rounding_power = 1 turns the corner curve into a straight 45° cut,
-- so no corner shader is needed.

local C = {
    obsidian = "0B0E14",
    slate    = "121826",
    raised   = "1A2233",
    emerald  = "0F6B4F",
    lapis    = "1F4E9C",
    brass    = "C9A24A",
    gold     = "E6C36A",
    ivory    = "F2EAD8",
}

hl.config({
    general = {
        gaps_in     = 4,   -- 8px between windows
        gaps_out    = 14,
        border_size = 2,
        col = {
            active_border   = {
                colors = { "rgb(" .. C.gold .. ")", "rgb(" .. C.brass .. ")", "rgb(" .. C.emerald .. ")" },
                angle  = 135,
            },
            inactive_border = "rgba(" .. C.brass .. "4d)",
        },
    },

    decoration = {
        rounding       = 10,
        rounding_power = 1.0,

        active_opacity   = 0.86,
        inactive_opacity = 0.74,

        blur = {
            enabled           = true,
            size              = 8,
            passes            = 3,
            vibrancy          = 0.18,
            new_optimizations = true,
            popups            = true,
        },

        shadow = {
            enabled      = true,
            range        = 28,
            render_power = 3,
            offset       = { 0, 10 },
            color        = "rgba(1C1406B0)",
        },
    },

    group = {
        col = {
            border_active   = "rgb(" .. C.gold .. ")",
            border_inactive = "rgba(" .. C.brass .. "4d)",
        },
    },

    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        background_color         = "rgb(" .. C.obsidian .. ")",
    },
})

-- Terminals draw their own 84% glass so text stays fully opaque.
hl.window_rule({
    name    = "girih-terminal-opaque",
    match   = { class = "^(foot|footclient|Alacritty|com.mitchellh.ghostty)$" },
    opacity = "1.0 override 1.0 override",
})

-- Glass for layer surfaces: waybar lintels, launcher, notifications.
-- ignore_alpha keeps the fully transparent gaps between lintels unblurred.
hl.layer_rule({
    name         = "girih-bar-glass",
    match        = { namespace = "^hattin-" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "girih-launcher-glass",
    match        = { namespace = "^launcher$" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "girih-notify-glass",
    match        = { namespace = "^swaync" },
    blur         = true,
    ignore_alpha = 0.1,
})

-- Launcher: floating foot + fzf (~/.local/bin/girih-launcher). As a real
-- window it gets the chamfer, gradient frame and blur; 12px chamfer.
hl.window_rule({
    name     = "girih-launcher",
    match    = { class = "^girih-launcher$" },
    float    = true,
    size     = "780 470",
    center   = true,
    pin      = true,
    rounding = 12,
    opacity  = "1.0 override 1.0 override",
})

-- Taskwarrior popups from the waybar "yawm" module (~/.local/bin/girih-yawm):
-- task list on click, one-line quick add on right-click.
hl.window_rule({
    name     = "girih-yawm",
    match    = { class = "^girih-yawm$" },
    float    = true,
    size     = "820 600",
    center   = true,
    pin      = true,
    rounding = 12,
    opacity  = "1.0 override 1.0 override",
})

hl.window_rule({
    name     = "girih-yawm-add",
    match    = { class = "^girih-yawm-add$" },
    float    = true,
    size     = "720 240",
    center   = true,
    pin      = true,
    rounding = 12,
    opacity  = "1.0 override 1.0 override",
})

local girih_popups = { "girih-launcher", "girih-yawm", "girih-yawm-add" }

-- Close every popup window except those of class `keep`.
-- hl.get_windows matches `class` exactly (no regex), so pass the plain name.
function girih_close_popups(keep)
    for _, class in ipairs(girih_popups) do
        if class ~= keep then
            for _, w in ipairs(hl.get_windows({ class = class })) do
                hl.dispatch(hl.dsp.window.close({ window = "address:" .. w.address }))
            end
        end
    end
end

function girih_close_launcher()
    girih_close_popups()
end

-- Close popups as soon as focus moves elsewhere.
hl.on("window.active", function(win)
    girih_close_popups(win and win.class)
end)
