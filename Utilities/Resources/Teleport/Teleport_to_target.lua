local GuiManager
local PlayerManager
local EnemyManager
local masterPlayer
local masterPlayerQuest
local mBehaviortree
local get_UpTimeSecond = sdk.find_type_definition("via.Application"):get_method("get_UpTimeSecond")


local targetEnemyID = -1
local preNodeID = -1
local startTime = 0
local tpFlag = false
local effectFlag = false
local arriveFlag = false
local targetEnemyList = {}


local function TpToTarget()

	local targetEnemy = targetEnemyList[targetEnemyID]
	if not targetEnemy then return end
	local targetPos = targetEnemy:call("get_Pos")

	targetPos.y = targetPos.y + 10
	masterPlayer:call("setPosWarp(via.vec3, System.Int32)", targetPos, 0)
	masterPlayerQuest:set_field("_MutekiTime", 180.0)

end

local function GetTime()
	return get_UpTimeSecond:call(nil)
end

re.on_frame(
	function()

		if not PlayerManager then
			PlayerManager = sdk.get_managed_singleton("snow.player.PlayerManager")
		end
		if not PlayerManager then return end
		masterPlayer = PlayerManager:call("findMasterPlayer")
		if not masterPlayer then return end

		if not EnemyManager then
			EnemyManager = sdk.get_managed_singleton("snow.enemy.EnemyManager")
		end
		if not EnemyManager then return end

		if not GuiManager then
			GuiManager = sdk.get_managed_singleton("snow.gui.GuiManager")
		end
		if not GuiManager then return end

		local tgCam = GuiManager:call("get_refGuiHud_TgCamera")
		if not tgCam then return end
		targetEnemyID = tgCam:get_field("OldTargetingEmIndex")
		if targetEnemyID < 0 then return end

		local offset = 0
		for i = 0, EnemyManager:call("getBossEnemyCount") do
			local enemy = EnemyManager:call("getBossEnemy(System.Int32)", i)
			if enemy and enemy:call("checkDie") then
				offset = offset + 1
			else
				targetEnemyList[i - offset] = enemy
			end
		end
		
		mBehaviortree = masterPlayer:call("get_GameObject"):call("getComponent(System.Type)",
		sdk.typeof("via.behaviortree.BehaviorTree"))

		local curNodeID = mBehaviortree:call("getCurrentNodeID", 0)
		if curNodeID ~= preNodeID then
			startTime = GetTime()
			preNodeID = curNodeID
		end

		if GetTime() - startTime > 0.2 and curNodeID == 690136471 and not effectFlag then
			masterPlayerQuest:call("setItemEffect", 100, 800)
			effectFlag = true
		end
		if GetTime() - startTime > 1.2 and curNodeID == 690136471 and not tpFlag then
			TpToTarget()
			tpFlag = true
			arriveFlag = true
		end
		if curNodeID ~= 690136471 then
			tpFlag = false
			effectFlag = false
			if arriveFlag then
				arriveFlag = false
				masterPlayerQuest:call("setItemEffect", 100, 4030)
				mBehaviortree:call("setCurrentNode(System.UInt64, System.UInt32, via.behaviortree.SetNodeInfo)", 2454004072, nil,
                nil)
			end
		end


	end
)

sdk.hook(sdk.find_type_definition("snow.player.PlayerQuestBase"):get_method("update"),
	function(args)
		local manager = sdk.to_managed_object(args[2])

		if masterPlayer and manager:get_field("_PlayerIndex") == masterPlayer:get_field("_PlayerIndex") then
			masterPlayerQuest = manager
		end

	end,
	function(retval)

		return retval
	end
)
