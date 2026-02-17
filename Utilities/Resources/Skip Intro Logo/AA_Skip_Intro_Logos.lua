local LOADING_STATES = 
{
	[sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsmManager.GameStartStateType"):get_field("Health_Caution"):get_data()] = true, -- 6
	[sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsmManager.GameStartStateType"):get_field("CAPCOM_Logo"):get_data()] = true, -- 1
	[sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsmManager.GameStartStateType"):get_field("Blank"):get_data()] = true, -- 5
	[sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsmManager.GameStartStateType"):get_field("Re_Logo"):get_data()] = true -- 2
}

local function isLoading()
	local GuiGameStartFsmManager = sdk.get_managed_singleton("snow.gui.fsm.title.GuiGameStartFsmManager")
	if GuiGameStartFsmManager then
		return LOADING_STATES[GuiGameStartFsmManager:call("get_GameStartState")] 
	end
	return false
end

local function isTitleSkip(retval)
	if isLoading() then
		return sdk.to_ptr(1)
	end
	return retval
end

local FINISHED = sdk.find_type_definition("snow.FadeManager.MODE"):get_field("FINISH"):get_data()
local function ClearFadeWithAction(args)
	sdk.to_managed_object(args[3]):call("notifyActionEnd")
	local FadeManager = sdk.get_managed_singleton("snow.FadeManager")
	if FadeManager then 
		FadeManager:call("set_FadeMode", FINISHED)
		FadeManager:set_field("fadeOutInFlag",false)
	end
end
local function ClearFade(args)
	local FadeManager = sdk.get_managed_singleton("snow.FadeManager")
	if FadeManager then 
		FadeManager:call("set_FadeMode", FINISHED)
		FadeManager:set_field("fadeOutInFlag",false)
	end
end

local function skipMovie(movie)
	if isLoading() then
		if movie then
			movie:seek(movie:get_DurationTime())
		end
	end
end

-- Fast forward movies to the end to mute audio
local currentMovie
sdk.hook(sdk.find_type_definition("via.movie.Movie"):get_method("play"), 
	function (args)
		-- playMovie(args)
		currentMovie = sdk.to_managed_object(args[1])
	end, function(ret) 
		skipMovie(currentMovie)
		return ret 
	end)

-- clear fadeout
sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_CautionFadeIn"):get_method("update"), 
	ClearFade, function(ret) return ret end)
sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_CAPCOMLogoFadeIn"):get_method("update"), 
ClearFade, function(ret)return ret end)
sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_RELogoFadeIn"):get_method("update"), 
	ClearFadeWithAction, function(ret)return ret end)

-- sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_HealthCautionFadeIn"):get_method("update"), 
-- 	ClearFade, function(ret)return ret end)

sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_HealthCautionFadeIn"):get_method("start"), function(args)
	local obj = sdk.to_managed_object(args[2]);
	if obj ~= nil then
		sdk.hook_vtable(obj, obj:get_type_definition():get_method("update"), ClearFade);
	end
end);

-- Actual skip actions
-- sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_OtherLogoFadeIn"):get_method("update"), 
-- 	ClearFadeWithAction, function(ret)return ret end)
sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_OtherLogoFadeIn"):get_method("start"), function(args)
    local obj = sdk.to_managed_object(args[2]);
    if obj ~= nil then
        sdk.hook_vtable(obj, obj:get_type_definition():get_method("update"), ClearFadeWithAction);
    end
end);

local function skipAction(action)
	-- Arg: via.behaviortree.ActionArg
	-- sdk.to_managed_object(args[2]):call("notifyEnd")
	if action then
		action:call("notifyActionEnd")
	end
end

local currentAction
sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiGameStartFsm_AutoSaveCaution_Action"):get_method("start"), 
	function (args)
		-- Arg: via.behaviortree.ActionArg
		currentAction = sdk.to_managed_object(args[3])
	end, function(ret) 
		skipAction(currentAction)
		return ret end)
sdk.hook(sdk.find_type_definition("snow.gui.fsm.title.GuiTitleFsm_PressAnyButton_Action"):get_method("start"), 
	function (args)
		currentAction = sdk.to_managed_object(args[3])
	end, function(ret) 
		skipAction(currentAction)
		return ret end)

-- Fake title skip input for HEALTH/Capcom
sdk.hook(sdk.find_type_definition("snow.gui.StmGuiInput"):get_method("getTitleDispSkipTrg"), 
	function(args)end, isTitleSkip)
