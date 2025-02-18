local mName = 'warp2'
local Warp = ModuleBase:createModule(mName)

--��������������������
local warpPoints = {
  { "����", 0, 11004, 20, 22 },
  { "����", 0, 1538, 15, 18 },
  { "ѩɽ", 0, 402, 84, 193 },
  { "ج����Lv49", 0, 33120, 33, 40 },
  { "ˮ֮����Lv65", 0, 15542, 10, 8 },
  { "��֮����Lv40", 0, 15595, 24, 8 },
  { "��֮����Lv30", 0, 15564, 23, 5 },
  { "��֮����Lv20", 0, 11034, 6, 5 },
  { "��������", 0, 15507, 29, 12 },
  { "�ͱ����ľ�ͷ", 0, 32115, 54, 21 },
  { "����", 0, 16511, 26, 68 },
  { "3ת˫��", 0, 24068, 20, 20 },
  { "�̴�", 0, 24001, 15, 8 },
  { "¶��", 0, 16508, 24, 12 },
  { "��������", 0, 20414, 26, 12 },
  { "��綴", 0, 300, 402, 304 },
  { "��ö���", 0, 32222, 30, 35 },
  { "��Ҷԭ-lv60", 0, 32216, 20, 40 },
  { "��Ҷԭ-lv100", 0, 32217, 55, 41 },
  { "��Ҷԭ-lv140", 0, 32215, 36, 19 },
  { "����boss", 0, 20116, 45, 63},
  { "��Ԩ", 0, 15539, 18, 12},
  { "��ѯ֮��", 0, 15561, 13, 11},
  { "������1¥", 0, 15579, 25, 35},
  { "�����Ƕ�¥", 0, 15585, 25, 17},
  { "����", 0, 4501, 9, 10},
  { "���֮��", 0, 59519, 26, 17},
  { "ţ��", 0, 11019, 125, 28},
  { "ʥ��", 0, 24009, 10, 13},
  { "��������", 0, 59006, 96, 19},
  { "boss1", 0, 47002, 15, 19},
  { "boss2", 0, 15518, 54, 41},
  { "����������", 0, 43000, 290, 438},
  { "��֪��", 0, 33232, 6, 13},
  { "ɭ������", 0, 11032, 13, 16},
}

local function calcWarp()
  local page = math.modf(#warpPoints / 8) + 1
  local remainder = math.fmod(#warpPoints, 8)
  return page, remainder
end

function Warp:onLoad()
  self:logInfo('load');
  local warpNPC = self:NPC_createNormal('������', 103010, { x = 242, y = 86, mapType = 0, map = 1000, direction = 6 });
  self:NPC_regWindowTalkedEvent(warpNPC, function(npc, player, _seqno, _select, _data)
    local column = tonumber(_data)
    local page = tonumber(_seqno)
    local warpPage = page;
    local winMsg = "1\\n��������ȥ����\\n"
    local winButton = CONST.BUTTON_�ر�;
    local totalPage, remainder = calcWarp()
    --��ҳ16 ��ҳ32 �ر�/ȡ��2
    if _select > 0 then
      if _select == CONST.BUTTON_��һҳ then
        warpPage = warpPage + 1
        if (warpPage == totalPage) or ((warpPage == (totalPage - 1) and remainder == 0)) then
          winButton = CONST.BUTTON_��ȡ��
        else
          winButton = CONST.BUTTON_����ȡ��
        end
      elseif _select == CONST.BUTTON_��һҳ then
        warpPage = warpPage - 1
        if warpPage == 1 then
          winButton = CONST.BUTTON_��ȡ��
        else
          winButton = CONST.BUTTON_��ȡ��
        end
      elseif _select == 2 then
        warpPage = 1
        return
      end
      local count = 8 * (warpPage - 1)
      if warpPage == totalPage then
        for i = 1 + count, remainder + count do
          winMsg = winMsg .. warpPoints[i][1] .. "\\n"
        end
      else
        for i = 1 + count, 8 + count do
          winMsg = winMsg .. warpPoints[i][1] .. "\\n"
        end
      end
      NLG.ShowWindowTalked(player, npc, CONST.����_ѡ���, winButton, warpPage, winMsg);
    else
      local count = 8 * (warpPage - 1) + column
      local short = warpPoints[count]
      Char.Warp(player, short[2], short[3], short[4], short[5])
    end
  end)
  self:NPC_regTalkedEvent(warpNPC, function(npc, player)
    if (NLG.CanTalk(npc, player) == true) then
      local msg = "1\\n��������ȥ����\\n";
      for i = 1, 8 do
        msg = msg .. warpPoints[i][1] .. "\\n"
      end
      NLG.ShowWindowTalked(player, npc, CONST.����_ѡ���, CONST.BUTTON_��ȡ��, 1, msg);
    end
    return
  end)
end

function Warp:onUnload()
  self:logInfo('unload')
end

return Warp;
