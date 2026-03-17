local sdk = sdk;
local json = json;
local re = re;
local imgui = imgui;
local thread = thread;
-- Config
local SendType = {"Good", "NotGood"};
local config = json.load_file("AutoLikes.json") or {enable = true, autosend = true, sendtype = SendType[1]};
if config.enable == nil then
	config.enable = true;
end
if config.autosend == nil then
	config.autosend = true;
end
if config.sendtype == nil then
	config.sendtype = SendType[1];
end
-- Cache
local GoodRelationship_type_def = sdk.find_type_definition("snow.gui.GuiHud_GoodRelationship");
local OtherPlayerInfos_field = GoodRelationship_type_def:get_field("_OtherPlayerInfos");
local gaugeAngleY_field = GoodRelationship_type_def:get_field("_gaugeAngleY");
local WaitTime_field = GoodRelationship_type_def:get_field("WaitTime");

local Enable_field = sdk.find_type_definition("snow.gui.GuiHud_GoodRelationship.PlInfo"):get_field("_Enable");
-- Main
local MAX_ANGLE_Y = 360.0;
local NO_WAIT_TIME = 0.0;
local TRUE_POINTER = sdk.to_ptr(true);

local sendReady = false;
local playerInfoUpdated = false;

local function PreHook_updatePlayerInfo(args)
	if config.enable == true then
		local storage = thread.get_hook_storage();
		storage["this"] = sdk.to_managed_object(args[2]);

		if gaugeAngleY_field:get_data(storage["this"]) ~= MAX_ANGLE_Y then
			storage["this"]:set_field("_gaugeAngleY", MAX_ANGLE_Y);
		end

		if WaitTime_field:get_data(storage["this"]) ~= NO_WAIT_TIME then
			storage["this"]:set_field("WaitTime", NO_WAIT_TIME);
		end

		if config.autosend == true and sendReady ~= false then
			sendReady = false;
		end
	end
end
local function PostHook_updatePlayerInfo()
	local GoodRelationshipHud = thread.get_hook_storage()["this"];
	if GoodRelationshipHud ~= nil then
		if config.sendtype == SendType[1] and playerInfoUpdated == false then
			local OtherPlayerInfos = OtherPlayerInfos_field:get_data(GoodRelationshipHud);
			if OtherPlayerInfos ~= nil then
				for i = 0, OtherPlayerInfos:get_size() - 1, 1 do
					local OtherPlayerInfo = OtherPlayerInfos:get_element(i);
					if OtherPlayerInfo ~= nil and Enable_field:get_data(OtherPlayerInfo) == true then
						OtherPlayerInfo:set_field("_good", true);
						OtherPlayerInfos[i] = OtherPlayerInfo;
					end
				end
				playerInfoUpdated = true;
			end
		end

		if config.autosend == true and sendReady ~= true then
			sendReady = true;
		end
	end
end

local function PostHook_isOperationOn(retval)
	return sendReady == true and TRUE_POINTER or retval;
end

local function PreHook_sendGood()
	sendReady = false;
	playerInfoUpdated = false;
end
-- Hook
sdk.hook(GoodRelationship_type_def:get_method("updatePlayerInfo"), PreHook_updatePlayerInfo, PostHook_updatePlayerInfo);
sdk.hook(sdk.find_type_definition("snow.gui.StmGuiInput"):get_method("isOperationOn(snow.StmInputManager.UI_INPUT, snow.StmInputManager.UI_INPUT)"), nil, PostHook_isOperationOn);
sdk.hook(GoodRelationship_type_def:get_method("sendGood"), PreHook_sendGood);
--
local function table_find_index(table, value, nullable)
	for index, sendType in ipairs(table) do
		if sendType == value then
			return index;
		end
	end

	if not nullable then
		return 1;
	end

	return nil;
end

local function SaveConfig()
	json.dump_file("AutoLikes.json", config);
end

re.on_config_save(SaveConfig);
re.on_draw_ui(function()
	if imgui.tree_node("AutoLikes") == true then
		local config_changed = false;
		config_changed, config.enable = imgui.checkbox("Enable", config.enable);
		if config.enable == true then
			local changed = false;
			changed, config.autosend = imgui.checkbox("Auto Send", config.autosend);
			config_changed = config_changed or changed;
			local indexChanged, index = imgui.combo("Send Type", table_find_index(SendType, config.sendtype, false), SendType);
			config_changed = config_changed or indexChanged;
			if indexChanged == true then
				config.sendtype = SendType[index];
			end
		end
		if config_changed == true then
			SaveConfig();
			if config.enable ~= true then
				sendReady = false;
				playerInfoUpdated = false;
			end
		end
		imgui.tree_pop();
	end
end);