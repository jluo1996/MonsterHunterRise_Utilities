-- loading keycode dicts separate from main logic
local PadKeys = require("bth.PadKeys")
local PlaystationKeys = require("bth.PlaystationKeys")
local XboxKeys = require("bth.XboxKeys")
local NintendoKeys = require("bth.NintendoKeys")
local KeyboardKeys = require("bth.KeyboardKeys")

-- checking if d2d exists
local function loadrequire(module)
    local function requiref(m)
        require(m)
    end
    local res = pcall(requiref, module)
    if not res then
        return false
    end
    return true
end

local d2dEnabled = loadrequire("reframework-d2d")

-- UI drawing state toggles
local drawWin = false
local drawDone = false
local drawSettings = false

-- Settings logic state toggles
local setAnimSkipBtn = false
local setCDSkipBtn = false
local setAnimSkipKey = false
local setCDSkipKey = false
local setWinPos = false

-- Input managers
local hwKB = nil
local hwPad = nil
local padType = 0
local padKeyLUT = XboxKeys -- most probable default

-- Persistent settings (defaults)
local screen_w, screen_h = nil, nil
local settings = { 
    enableWin = true,
    enableMsg = true,
    autoskipCountdown = false,
    autoskipPostAnim = true,
    enableKeyboard = true,
    enableController = true,
    kbCDSkipKey = 36,
    kbAnimSkipKey = 35,
    padCDSkipBtn = 4096,
    padAnimSkipBtn = 8192,
    win_x = 0,
    win_y = 0,
    win_size_x = 0.5,
    win_size_y = 0.5,
    text_x = 50,
    text_y = 50,
    text_size = 16
}

-- Quest manager/actual functionality toggles
local questManager = nil
local skipCountdown = false
local skipPostAnim = false

-- Button code to label decoder
local function pad_btncode_to_label(keycode)
    label = ""

    for k, v in pairs(PadKeys) do
        if keycode & k > 0 and padKeyLUT[PadKeys[k]] ~= nil then
            label = label .. padKeyLUT[PadKeys[k]] .. "+"
        end
    end

    if #label > 0 then
        return label:sub(0, -2)
    end
    return "None"
end

-- Persistence Functions
local function save_settings()
    json.dump_file("bth_settings.json", settings)
end

local function load_settings()
    local loadedTable = json.load_file("bth_settings.json")
    if loadedTable ~= nil then
        for key, val in pairs(loadedTable) do
            settings[key] = loadedTable[key]
        end
        -- the lua equivalent of converting to int
        settings.kbCDSkipKey = math.floor(settings.kbCDSkipKey)
        settings.kbAnimSkipKey = math.floor(settings.kbAnimSkipKey)
        settings.padCDSkipBtn = math.floor(settings.padCDSkipBtn)
        settings.padAnimSkipBtn = math.floor(settings.padAnimSkipBtn)
    end
end

-- Internal Timer Functions
local get_delta_time = sdk.find_type_definition("via.Application"):get_method("get_FrameTimeMillisecond")
local timer = 0
local timerLen = 200 -- timer length in millisecs

local function timer_reset()
    timer = 0
end

local function timer_tick()
    -- timer tick function, returns true if timerLen has been reached
    timer = timer + get_delta_time:call(nil)
    if timer >= timerLen then
        timer_reset()
        return true
    end
    return false
end

-- Strings and update function
local padCDSkipLabel = pad_btncode_to_label(settings.padCDSkipBtn)
local padAnimSkipLabel = pad_btncode_to_label(settings.padAnimSkipBtn)

local carve_str = nil
local anim_str = nil
local autoskip_str = nil
local function update_strings()

    padCDSkipLabel = pad_btncode_to_label(settings.padCDSkipBtn)
    padAnimSkipLabel = pad_btncode_to_label(settings.padAnimSkipBtn)

    carve_str = "Skip Timer: "
    if settings.enableKeyboard or settings.enableController then
        -- carve_str = carve_str.." ("
        if settings.enableKeyboard then
            carve_str = carve_str..KeyboardKeys[settings.kbCDSkipKey]
        end
        
        if settings.enableKeyboard and settings.enableController then
            carve_str = carve_str.."/"
        end

        if settings.enableController then
            carve_str = carve_str..padCDSkipLabel
        end
        
    else
        carve_str = carve_str.."N/A"
    end

    anim_str = "Skip Anim.: "
    if settings.enableKeyboard or settings.enableController then
        -- anim_str = anim_str..": "
        if settings.enableKeyboard then
            anim_str = anim_str..KeyboardKeys[settings.kbAnimSkipKey]
        end
        if settings.enableKeyboard and settings.enableController then
            anim_str = anim_str.."/"
        end
        if settings.enableController then
            anim_str = anim_str..padAnimSkipLabel
        end
        
    else
        anim_str = anim_str.."N/A"
    end

    autoskip_str = "Autoskip: "
    if settings.autoskipCountdown or settings.autoskipPostAnim then
        
        if settings.autoskipCountdown then
            autoskip_str = autoskip_str.."Timer"
        end
        if settings.autoskipCountdown and settings.autoskipPostAnim then
            autoskip_str = autoskip_str.." & "
        end
        if settings.autoskipPostAnim then
            autoskip_str = autoskip_str.."Anim."
        end
    else
        autoskip_str = autoskip_str.."Off"
    end
end

load_settings() -- always try to load settings on start
update_strings() -- settings were loaded, need to update strings

-- chat message on clear
local chatManager = nil
local function push_message()
    if chatManager == nil then
        chatManager = sdk.get_managed_singleton("snow.gui.ChatManager")
    end

    local chat_msg = "<COL RED>    FAST RETURN</COL>" .. '\n' .. carve_str .. '\n' .. anim_str .. '\n' .. autoskip_str
    chatManager:call("reqAddChatInfomation", chat_msg, 2289944406)
end

-- d2d window
if d2dEnabled then
    local screen_w, screen_h = nil, nil
    local font = nil
    local image = nil
    local img_w, img_h = nil, nil
    d2d.register(function()
        font = d2d.Font.new("Tahoma", math.floor(settings.text_size), true)
        image = d2d.Image.new("mhrpopup.png")
        img_w, img_h = image:size()
    end,
    function ()
            if (drawWin and settings.enableWin) or setWinPos then
                local carve_w, carve_h = font:measure(carve_str)
                local anim_w, anim_h = font:measure(anim_str)

                d2d.image(image, settings.win_x, settings.win_y, img_w * settings.win_size_x, img_h*settings.win_size_y)
                
                local t_x, t_y = settings.win_x + settings.text_x, settings.win_y + settings.text_y

                d2d.text(font, carve_str, t_x, t_y, 0xFFFFFFFF)
                d2d.text(font, anim_str, t_x, t_y + carve_h, 0xFFFFFFFF)
                
                d2d.text(font, autoskip_str, t_x, t_y + carve_h + anim_h, 0xFFFFFFFF)
            end
    end
    )
end

-- Quest Clear GUI
re.on_frame(function()
    if drawWin then
        -- Listening for Anim skip key press
        if (hwKB:call("getTrg", settings.kbAnimSkipKey) and settings.enableKeyboard) or (hwPad:call("andOn", settings.padAnimSkipBtn) and settings.enableController) then
            skipPostAnim = true
        end

        -- Listening for CD skip key press
        if (hwKB:call("getTrg", settings.kbCDSkipKey) and settings.enableKeyboard) or (hwPad:call("andOn", settings.padCDSkipBtn) and settings.enableController) then
            skipCountdown = true
        end
    end
end)

-- Event callback hook for behaviour updates
re.on_pre_application_entry("UpdateBehavior", function() -- unnamed/inline function definition
    -- grabbing the quest manager
    if not questManager then
        questManager = sdk.get_managed_singleton("snow.QuestManager")
        if not questManager then -- if still nothing then aborting
            return nil
        end
    end

    if d2dEnabled then
        screen_w, screen_h = d2d.surface_size()
    end
    
    -- grabbing the keyboard manager    
    if not hwKB then
        hwKB = sdk.get_managed_singleton("snow.GameKeyboard"):get_field("hardKeyboard") -- getting hardware keyboard manager
    end
    -- grabbing the gamepad manager
    if not hwPad then
        hwPad = sdk.get_managed_singleton("snow.Pad"):get_field("hard") -- getting hardware keyboard manager
        if hwPad then
            padType = hwPad:call("get_DeviceKindDetails")
            if padType ~= nil then
                if padType < 10 then
                    padKeyLUT = XboxKeys
                elseif padType > 15 then
                    padKeyLUT = NintendoKeys
                else
                    padKeyLUT = PlaystationKeys
                end
            else
                padKeyLUT = XboxKeys -- defaulting to Xbox Keys
            end
        end
    end

    -- getting Quest End state
    -- 0: still in quest, 1: ending countdown, 8: ending animation, 16: quest over
    local endFlow = questManager:get_field("_EndFlow")

    -- getting shared quest end state timer
    -- used for both 60/20sec carve timer and ending animation timing
    local questTimer = questManager:get_field("_QuestEndFlowTimer")

    
    if endFlow > 0 and endFlow < 16 then
        -- enabling main window draw if in the quest ending state
        drawWin = true
        if settings.enableMsg and not drawDone and questTimer < 59 then
            push_message()
            drawDone = true
        end
    else
        -- disabling draw and resetting timer skip otherwise
        -- if skipCountdown is left set to true, every consequent carve timer will be skipped :(
        skipCountdown = false
        skipPostAnim = false
        drawWin = false
    end

    -- Skipping the carve timer if selected
    if endFlow == 1 and (skipCountdown or settings.autoskipCountdown) and questTimer > 1.0 then
        questManager:set_field("_QuestEndFlowTimer", 1)
    end

    -- Skipping the post anim if selected
    if endFlow == 8 and (skipPostAnim or settings.autoskipPostAnim) and questTimer > 1.0 then
        questManager:set_field("_QuestEndFlowTimer", 1)
    end
end)

-- Hook for when the main RE Framework window is being drawn
local padBtnPrev = 0
re.on_draw_ui(function()
   -- Puts a simple confirmation text into the main window
    if imgui.button("Fast Return Settings") then
        drawSettings = true
    end

    if drawSettings then
        local winStr = 'Fast Return Settings'
        if d2dEnabled then
            winStr = winStr .. ' (d2d)'
        end
        if imgui.begin_window(winStr, true, 64) then

            -- settings logic
            -- Keyboard stuff
            
            if setCDSkipKey then
                settings.kbCDSkipKey = 0
                for k, v in pairs(KeyboardKeys) do  -- VERY DIRTY BUT get_trg doesn't work?
                    if hwKB:call("getDown", k) then
                        settings.kbCDSkipKey = k
                        save_settings()
                        update_strings()
                        setCDSkipKey = false
                        break
                    end
                end
            elseif setAnimSkipKey then
                settings.kbAnimSkipKey = 0
                for k, v in pairs(KeyboardKeys) do
                    if hwKB:call("getDown", k) then
                        settings.kbAnimSkipKey = k
                        save_settings()
                        update_strings()
                        setAnimSkipKey = false
                        break
                    end
                end
            -- controller stuff
            elseif setCDSkipBtn then
                settings.padCDSkipBtn = 0
                padCDSkipLabel = pad_btncode_to_label(settings.padCDSkipBtn)
                -- checking if held button changed
                local padBtnPressed = hwPad:call("get_on") -- get held buttons
                if padBtnPressed > 0 then -- if they press anything
                    if padBtnPressed == padBtnPrev then -- is it a new combination?
                        if timer_tick() then -- start timer, wait for it to finish
                            settings.padCDSkipBtn = padBtnPressed -- timer ran out, update settings
                            save_settings()  -- autosave
                            padCDSkipLabel = pad_btncode_to_label(settings.padCDSkipBtn)  -- decoding btn label
                            update_strings()
                            padBtnPrev = 0  -- resetting button 'memory'
                            setCDSkipBtn = false -- done setting this button
                        end
                    else -- not a new combo
                        padBtnPrev = padBtnPressed -- save this combo for a bit
                        timer_reset()
                    end
                end

            elseif setAnimSkipBtn then
                settings.padAnimSkipBtn = 0
                -- checking if held button changed
                local padBtnPressed = hwPad:call("get_on") -- get held buttons
                if padBtnPressed > 0 then -- if they press anything
                    padAnimSkipLabel = pad_btncode_to_label(settings.padAnimSkipBtn)
                    if padBtnPressed == padBtnPrev then -- is it a new combination?
                        if timer_tick() then -- start timer, wait for it to finish
                            settings.padAnimSkipBtn = padBtnPressed -- timer ran out, update settings
                            save_settings()  -- autosave
                            padAnimSkipLabel = pad_btncode_to_label(settings.padAnimSkipBtn)  -- decoding btn label
                            update_strings()
                            padBtnPrev = 0  -- resetting button 'memory'
                            setAnimSkipBtn = false -- done setting this button
                        end
                    else -- not a new combo
                        padBtnPrev = padBtnPressed -- save this combo for a bit
                        timer_reset()
                    end
                end 
            end
            
            if d2dEnabled then
                changed, value = imgui.checkbox('Draw Window on Quest Clear', settings.enableWin)
                if changed then
                    settings.enableWin = value
                    save_settings()
                end
            end

            changed, value = imgui.checkbox('Chat Message on Quest Clear', settings.enableMsg)
            if changed then
                settings.enableMsg = value
                save_settings()
            end
            
            if imgui.tree_node("~~Autoskip Settings~~") then
                changed, value = imgui.checkbox('Autoskip Carve Timer', settings.autoskipCountdown)
                if changed then
                    settings.autoskipCountdown = value
                    save_settings()
                    update_strings()
                end

                changed, value = imgui.checkbox('Autoskip Ending Anim.', settings.autoskipPostAnim)
                if changed then
                    settings.autoskipPostAnim = value
                    save_settings()
                    update_strings()
                end
                imgui.tree_pop()
            end

            if imgui.tree_node("~~Keyboard Settings~~") then

                -- changed, value = imgui.checkbox("Enable Keyboard Controls (" .. KeyboardKeys[settings.kbCDSkipKey] .. "/" .. KeyboardKeys[settings.kbAnimSkipKey] .. ")", settings.enableKeyboard)
                changed, value = imgui.checkbox("Enable Keyboard", settings.enableKeyboard)
                if changed then
                    settings.enableKeyboard = value
                    save_settings()
                    update_strings()
                end

                imgui.text("Timer Skip")
                imgui.same_line()
                if imgui.button(KeyboardKeys[settings.kbCDSkipKey]) then
                    setCDSkipKey = true
                    -- setting other modes to inactive
                    setAnimSkipKey = false
                    setAnimSkipBtn = false
                    setCDSkipBtn = false
                end
                -- imgui.same_line()
                imgui.text("Anim. Skip")
                imgui.same_line()
                if imgui.button(KeyboardKeys[settings.kbAnimSkipKey]) then
                    setAnimSkipKey = true
                    -- setting other modes to inactive
                    setCDSkipKey = false
                    setAnimSkipBtn = false
                    setCDSkipBtn = false
                end
                imgui.tree_pop()
            end

            if imgui.tree_node("~~Controller Settings~~") then
                -- changed, value = imgui.checkbox("Enable Controller Controls (" .. padCDSkipLabel .. "/" .. padAnimSkipLabel .. ")", settings.enableController)
                changed, value = imgui.checkbox("Enable Controller", settings.enableController)
                if changed then
                    settings.enableController = value
                    save_settings()
                    update_strings()
                end

                imgui.text("Timer Skip")
                imgui.same_line()
                if imgui.button(padCDSkipLabel) then
                    setCDSkipBtn = true
                    -- setting other modes to inactive
                    setAnimSkipBtn = false
                    setCDSkipKey = false
                    setAnimSkipKey = false
                end
                -- imgui.same_line()
                imgui.text("Anim. Skip")
                imgui.same_line()
                if imgui.button(padAnimSkipLabel) then
                    setAnimSkipBtn = true
                    -- setting other modes to inactive
                    setCDSkipBtn = false
                    setCDSkipKey = false
                    setAnimSkipKey = false
                end
                imgui.tree_pop()
            end
            
            if d2dEnabled then
                if imgui.tree_node("~~d2d Window Settings~~") then
                    setWinPos = true
                    imgui.text("CTRL+Click sliders for text input")
                    changed, value = imgui.slider_int("X Pos.", settings.win_x, -700, screen_w)
                    if changed then
                        settings.win_x = value
                        save_settings()
                    end
                    changed, value = imgui.slider_int("Y Pos.", settings.win_y, 1, screen_h)
                    if changed then
                        settings.win_y = value
                        save_settings()
                    end
    
                    changed, value = imgui.slider_float("Scale X", settings.win_size_x, 0.25, 1)
                    if changed then
                        settings.win_size_x = value
                        save_settings()
                    end
                    changed, value = imgui.slider_float("Scale Y", settings.win_size_y, 0.25, 1)
                    if changed then
                        settings.win_size_y = value
                        save_settings()
                    end
    
                    changed, value = imgui.slider_int("Text X Pos.", settings.text_x, 0, 500)
                    if changed then
                        settings.text_x = value
                        save_settings()
                    end
                    changed, value = imgui.slider_int("Text Y Pos.", settings.text_y, 0, 500)
                    if changed then
                        settings.text_y = value
                        save_settings()
                    end
    
                    changed, value = imgui.slider_int("Text Size", settings.text_size, 8, 20)
                    if changed then
                        settings.text_size = value
                        save_settings()
                    end
                    imgui.text("Text size requires script reload")
    
                else
                    setWinPos = false
                end
            end
            

            imgui.spacing()
            imgui.end_window()
        else
            drawSettings = false
            setCDSkipBtn = false
            setAnimSkipBtn = false
            setCDSkipKey = false
            setAnimSkipKey = false
            setWinPos = false
        end
    end
end)