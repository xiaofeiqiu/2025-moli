---�������� for cgmsv 24.9e���ϰ汾
---@class BagSwitch : ModuleType
local BagSwitch = ModuleBase:createModule('bagSwitch');


local MENU = 0;
local BAG_LIST = 1;
local BAG_LIST2 = 2;
local ITEM_MOVE = 1000;
local SHOW_ITEM_LIST = 10;
local ITEM_PAGE_SIZE = 20;
local EQUIP_NUM = 8;
local IPAGE_NUM = 8;

local BAG_PAGE_LIST = {};

--- ����ģ�鹳��
function BagSwitch:onLoad()
    self:logInfo('load')
    self.dummyNPC = self:NPC_createNormal('DummyNPC', 10000, { x = 0, y = 0, map = 777, mapType = 0, direction = 0 });
    self:regCallback('ProtocolOnRecv', Func.bind(self.onProtoHook, self), 'SWITMM');
    self:regCallback('TalkEvent', Func.bind(self.handleTalkEvent, self))
    self:NPC_regWindowTalkedEvent(self.dummyNPC, Func.bind(self.onWindowTalked, self));

    for i = 1, CONST.EXTBAGPAGE + 1 do
        table.insert(BAG_PAGE_LIST, NLG.c(string.format("%d�ű���", i)));
    end
end

--- ж��ģ�鹳��
function BagSwitch:onUnload()
    self:logInfo('unload')
end

function BagSwitch:handleTalkEvent(charIndex, msg)
    if (string.lower(tostring(msg)) == "/itemswitch") then
        self:OpenMenu(charIndex)
        return 0;
    end
    return 1;
end

function BagSwitch:onProtoHook(fd)
    local charIndex = Protocol.GetCharIndexFromFd(fd);
    self:OpenMenu(charIndex);
    return 1;
end

function BagSwitch:OpenMenu(charIndex)
    local ch = self:Chara(charIndex);
    ch[CONST.����_WindowBuffer2] = 1;
    local menu = self:NPC_buildSelectionText("��������", {
        "�л�����",
        "�ƶ���Ʒ"
    })
    NLG.ShowWindowTalked(charIndex, self.dummyNPC,
        CONST.����_ѡ���, CONST.BUTTON_ȷ���ر�,
        0, menu);
end

function BagSwitch:onWindowTalked(npc, player, seqNo, btnClick, line)
    local ch = self:Chara(player);
    line = tonumber(line)
    btnClick = tonumber(btnClick)
    if seqNo == MENU then
        self:onMenu(ch, line, btnClick);
    end
    if seqNo == BAG_LIST then
        self:onSwitchBag(ch, line, btnClick);
    end
    if seqNo == ITEM_MOVE then
        self:onMoveItem(ch, line, btnClick);
    end
    if seqNo == BAG_LIST2 then
        self:onSelectedMoveBag(ch, line, btnClick);
    end
end

---@param ch CharaWrapper
---@param selection number
---@param buttonClick number
function BagSwitch:onMenu(ch, selection, buttonClick)
    if selection == 1 then
        ch:ShowWindowTalked(self.dummyNPC,
            self:NPC_buildSelectionText(
                NLG.c("ѡ�񱳰�"),
                BAG_PAGE_LIST
            ),
            {
                button = CONST.BUTTON_�ر�,
                type = CONST.����_ѡ���,
                seqNo = BAG_LIST,
            })
        return
    end
    if selection == 2 then
        ch[CONST.����_WindowBuffer2] = 0;
        self:onMoveItem(ch, 10, -1);
    end
end

---@param ch CharaWrapper
---@param selection number
---@param buttonClick number
function BagSwitch:onSwitchBag(ch, selection, buttonClick)
    if buttonClick == CONST.BUTTON_�ر� or buttonClick == CONST.BUTTON_�� then
        return
    end
    selection = selection - 1;
    if selection < 0 then
        return
    end
    local cur = Char.GetBagPage(ch.charaIndex);
    if cur == selection then
        NLG.SystemMessage(ch.charaIndex, "�����л�����")
        return
    end
    NLG.SystemMessage(ch.charaIndex, "�л�������" .. (selection + 1))
    Char.SwitchBag(ch.charaIndex, selection)
end

---@param ch CharaWrapper
---@param selection number
---@param buttonClick number
function BagSwitch:onMoveItem(ch, selection, buttonClick)
    local iPage = ch[CONST.����_WindowBuffer2] --[[@as number]];
    if buttonClick == CONST.BUTTON_��һҳ then
        iPage = math.max(0, iPage - 1);
        selection = SHOW_ITEM_LIST;
    elseif buttonClick == CONST.BUTTON_��һҳ then
        iPage = math.min(2, iPage + 1);
        selection = SHOW_ITEM_LIST;
    elseif buttonClick == -1 or selection > 0 then
        -- ignore this
    else
        return
    end

    if selection > 0 and selection ~= SHOW_ITEM_LIST then
        selection = selection - 1;
    end
    if selection < 0 then
        return
    end

    local cur = Char.GetBagPage(ch.charaIndex);

    if selection == SHOW_ITEM_LIST then
        local pageSlotMap = {
            { 1,  2,  3,  4,  5,  6,  7,  8, },
            { 9,  10, 11, 12, 13, 14, 15, 16, },
            { 17, 18, 19, 20, },
        }
        local buttonMap = {
            CONST.BUTTON_��ȡ��,
            CONST.BUTTON_����ȡ��,
            CONST.BUTTON_��ȡ��,
        }
        local menuList = {};
        for _, value in ipairs(pageSlotMap[iPage + 1]) do
            local itemIndex = Char.GetItemIndex(ch.charaIndex, cur * ITEM_PAGE_SIZE + EQUIP_NUM + value - 1);
            local itemName = "- [��] -"
            if itemIndex >= 0 then
                itemName = string.format("%s x %d",
                    Item.GetData(itemIndex, CONST.����_����),
                    Item.GetData(itemIndex, CONST.����_�ѵ���)
                );
            end
            table.insert(menuList, NLG.c(itemName));
        end
        ch:ShowWindowTalked(self.dummyNPC, self:NPC_buildSelectionText(
            NLG.c("ѡ����Ʒ"),
            menuList), {
            type = CONST.����_ѡ���,
            seqNo = ITEM_MOVE,
            windowBuffer2 = iPage,
            button = buttonMap[iPage + 1],
        })
        return
    end
    if selection >= 0 then
        ch:ShowWindowTalked(self.dummyNPC,
            self:NPC_buildSelectionText(
                NLG.c("ѡ�񱳰�"),
                BAG_PAGE_LIST
            ),
            {
                button = CONST.BUTTON_�ر�,
                type = CONST.����_ѡ���,
                seqNo = BAG_LIST2,
                windowBuffer2 = selection + iPage * IPAGE_NUM,
            })
        return
    end
end

---@param ch CharaWrapper
---@param selection number
---@param buttonClick number
function BagSwitch:onSelectedMoveBag(ch, selection, buttonClick)
    if buttonClick == CONST.BUTTON_�ر� or buttonClick == CONST.BUTTON_�� then
        return
    end
    selection = selection - 1;
    if selection < 0 then
        return
    end
    local cur = Char.GetBagPage(ch.charaIndex);
    local itemSelection = ch[CONST.����_WindowBuffer2];

    local ret = Char.ItemMoveBag(ch.charaIndex, EQUIP_NUM + itemSelection, selection, -1);
    if ret ~= 1 then
        NLG.SystemMessage(ch.charaIndex, "�ƶ���Ʒʧ��");
    end
end

return BagSwitch;
