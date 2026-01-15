-- auto_argosy.lua : written by archwizard1204
-- Only on NexusMods, my profile page: https://www.nexusmods.com/users/154089548

local itemBoxId = 65536
local resultAll = 0
local resultSome = 1
local resultFull = 2
local resultMax = 3

local maxTypeOver = 1

local function autoArgosy()
    local tradeFunc = sdk.get_managed_singleton("snow.facility.TradeCenterFacility"):call("get_TradeFunc")
    local tradeOrderList = tradeFunc:call("get_TradeOrderList")
    local dataManager = sdk.get_managed_singleton("snow.data.DataManager")
    local chatManager = sdk.get_managed_singleton("snow.gui.ChatManager")
    local villagePoint = dataManager:call("getVillagePoint")

	if not tradeFunc or not tradeOrderList or not dataManager or not chatManager or not villagePoint then return end

    local argosyItems = {}
    local itemBoxResults = {}
    for i = 0, #tradeOrderList - 1 do
        local tradeOrder = tradeOrderList[i]
        local inventoryList = tradeOrder:call("get_InventoryList")
        local negotiationCount = tradeOrder:call("get_NegotiationCount")

        if negotiationCount == 1 then
            local negotiationData = tradeFunc:call("getNegotiationData", tradeOrder:call("get_NegotiationType"))
            local negotiationCost = negotiationData:call("get_Cost")
            
            if villagePoint:call("get_Point") >= negotiationCost then
                tradeOrder:call("setNegotiationCount", negotiationCount + negotiationData:call("get_Count"))
                villagePoint:call("subPoint", negotiationCost)
            end
        end
    
        for j = 0, #inventoryList - 1 do
            local inventory = inventoryList[j]

            if inventory:call("isEmpty") == false then
                local itemId = inventory:call("get_ItemId")
                local count = inventory:call("get_Count")
                if argosyItems[itemId] ~= nil then
                    argosyItems[itemId] = argosyItems[itemId] + count
                else
                    argosyItems[itemId] = count
                end

                local sendResult = inventory:call("sendInventory(snow.data.ItemInventoryData, snow.data.InventoryData.InventoryType)", inventory, itemBoxId)
                itemBoxResults[itemId] = sendResult

                if sendResult ~= resultAll then
                    dataManager:call("trySellGameItem(snow.data.ItemInventoryData, System.UInt32)", inventory, inventory:call("get_Count"))
                end
            end
        end
        tradeOrder:call("initialize")
    end

    for i, v in pairs(argosyItems) do
        if v ~= 0 then
            local sendResult = itemBoxResults[i]
            local maxType = sendResult
            if sendResult == resultMax or sendResult == resultSome then
                maxType = maxTypeOver
            end
            chatManager:call("reqAddChatItemInfo(snow.data.ContentsIdSystem.ItemId, System.Int32, snow.gui.ChatManager.ItemMaxType, System.Boolean)", i, v, maxType, 0)
        end
    end
end

sdk.hook(sdk.find_type_definition("snow.VillageMapManager"):get_method("getCurrentMapNo"), nil, autoArgosy)
