local mName = 'warp2'
local Warp = ModuleBase:createModule(mName)

--坐标可以在下面自行添加
local warpPoints = {
  { "熊男", 0, 11004, 20, 22 },
  { "灵堂", 0, 1538, 15, 18 },
  { "雪山", 0, 402, 84, 193 },
  { "噩梦鼠Lv49", 0, 33120, 33, 40 },
  { "水之洞窟Lv65", 0, 15542, 10, 8 },
  { "炎之洞窟Lv40", 0, 15595, 24, 8 },
  { "风之洞窟Lv30", 0, 15564, 23, 5 },
  { "土之洞窟Lv20", 0, 11034, 6, 5 },
  { "树精长老", 0, 15507, 29, 12 },
  { "巴别塔的尽头", 0, 32115, 54, 21 },
  { "神兽", 0, 16511, 26, 68 },
  { "3转双王", 0, 24068, 20, 20 },
  { "犹大", 0, 24001, 15, 8 },
  { "露比", 0, 16508, 24, 12 },
  { "佛利波罗", 0, 20414, 26, 12 },
  { "大风洞", 0, 300, 402, 304 },
  { "库得洞窟", 0, 32222, 30, 35 },
  { "彩叶原-lv60", 0, 32216, 20, 40 },
  { "彩叶原-lv100", 0, 32217, 55, 41 },
  { "彩叶原-lv140", 0, 32215, 36, 19 },
  { "火山", 0, 48008, 50, 23},
  { "红龙boss", 0, 20116, 45, 63},
  { "深渊", 0, 15539, 18, 12},
  { "咨询之塔", 0, 15561, 13, 11},
  { "白龙城1楼", 0, 15579, 25, 35},
  { "白龙城顶楼", 0, 15585, 25, 17},
  { "伊代", 0, 4501, 9, 10},
  { "天空之城", 0, 59519, 26, 17},
  { "牛鬼", 0, 11019, 125, 28},
  { "圣召", 0, 24009, 10, 13},
  { "高塔顶部", 0, 59006, 96, 19},
  { "boss1", 0, 47002, 15, 19},
  { "boss2", 0, 15518, 54, 41},
  { "艾尔巴尼亚", 0, 43000, 290, 438},
  { "不知道", 0, 33232, 6, 13},
  { "森罗万象", 0, 11032, 13, 16},
}

local function calcWarp()
  local page = math.modf(#warpPoints / 8) + 1
  local remainder = math.fmod(#warpPoints, 8)
  return page, remainder
end

function Warp:onLoad()
  self:logInfo('load');
  local warpNPC = self:NPC_createNormal('传送门', 103010, { x = 242, y = 86, mapType = 0, map = 1000, direction = 6 });
  self:NPC_regWindowTalkedEvent(warpNPC, function(npc, player, _seqno, _select, _data)
    local column = tonumber(_data)
    local page = tonumber(_seqno)
    local warpPage = page;
    local winMsg = "1\\n请问你想去哪里\\n"
    local winButton = CONST.BUTTON_关闭;
    local totalPage, remainder = calcWarp()
    --上页16 下页32 关闭/取消2
    if _select > 0 then
      if _select == CONST.BUTTON_下一页 then
        warpPage = warpPage + 1
        if (warpPage == totalPage) or ((warpPage == (totalPage - 1) and remainder == 0)) then
          winButton = CONST.BUTTON_上取消
        else
          winButton = CONST.BUTTON_上下取消
        end
      elseif _select == CONST.BUTTON_上一页 then
        warpPage = warpPage - 1
        if warpPage == 1 then
          winButton = CONST.BUTTON_下取消
        else
          winButton = CONST.BUTTON_下取消
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
      NLG.ShowWindowTalked(player, npc, CONST.窗口_选择框, winButton, warpPage, winMsg);
    else
      local count = 8 * (warpPage - 1) + column
      local short = warpPoints[count]
      Char.Warp(player, short[2], short[3], short[4], short[5])
    end
  end)
  self:NPC_regTalkedEvent(warpNPC, function(npc, player)
    if (NLG.CanTalk(npc, player) == true) then
      local msg = "1\\n请问你想去哪里\\n";
      for i = 1, 8 do
        msg = msg .. warpPoints[i][1] .. "\\n"
      end
      NLG.ShowWindowTalked(player, npc, CONST.窗口_选择框, CONST.BUTTON_下取消, 1, msg);
    end
    return
  end)
end

function Warp:onUnload()
  self:logInfo('unload')
end

return Warp;
