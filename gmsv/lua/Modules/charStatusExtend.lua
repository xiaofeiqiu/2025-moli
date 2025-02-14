---@class CharStatusExtend : ModuleType

local CharStatusExtend = ModuleBase:createModule('charStatusExtend')

local Allow = {
  ['' .. CONST.CHAR_���Ѫ] = 1,
  ['' .. CONST.CHAR_���ħ] = 1,
  ['' .. CONST.CHAR_������] = 1,
  ['' .. CONST.CHAR_������] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_�ظ�] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_��ɱ] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_����] = 1,
  ['' .. CONST.CHAR_��˯] = 1,
  ['' .. CONST.CHAR_��ʯ] = 1,
  ['' .. CONST.CHAR_����] = 1,
};

function CharStatusExtend:onLoad()
  self:logInfo('load');
  self:regCallback('AfterCalcCharaStatusEvent', Func.bind(self.onStatusUpdate, self));
end

function CharStatusExtend:addCharStatus(charIndex, t, val)
  if (Allow[t .. ''] ~= 1) then
    return false;
  end
  Char.SetTempData(charIndex, 'CSE:Enable', 1);
  Char.SetTempData(charIndex, "CSE:" .. t, tonumber(val));
  if (t == CONST.CHAR_���Ѫ or t == CONST.CHAR_���ħ) then
    Char.SetTempData(charIndex, "CSE:L" .. t, Char.GetData(charIndex, t));
  end
  return true;
end

function CharStatusExtend:clearCharStatus(charIndex)
  Char.SetTempData(charIndex, 'CSE:Enable', nil);
  for i, v in pairs(Allow) do
    Char.SetTempData(charIndex, 'CSE:' .. i, nil);
    if (tonumber(i) == CONST.CHAR_���Ѫ or tonumber(i) == CONST.CHAR_���ħ) then
      Char.SetTempData(charIndex, "CSE:L" .. i, nil);
    end
  end
end

function CharStatusExtend:onStatusUpdate(charIndex)
  if (Char.GetTempData(charIndex, "CSE:Enable") == 1) then
    local t = { CONST.CHAR_������, CONST.CHAR_������, CONST.CHAR_����, CONST.CHAR_����, CONST.CHAR_�ظ�,
      CONST.CHAR_����, CONST.CHAR_��ɱ, CONST.CHAR_����, CONST.CHAR_����, CONST.CHAR_����, CONST.CHAR_����,
      CONST.CHAR_����, CONST.CHAR_��˯, CONST.CHAR_��ʯ, CONST.CHAR_���� };
    for i, v in ipairs(t) do
      local vx = tonumber(Char.GetTempData(charIndex, "CSE:" .. v)) or 0;
      if (vx ~= 0 and vx ~= nil) then
        Char.SetData(charIndex, v, Char.GetData(charIndex, v) + vx);
      end
    end
    local t2 = { { CONST.CHAR_���Ѫ, CONST.CHAR_Ѫ }, { CONST.CHAR_���ħ, CONST.CHAR_ħ } }
    for i, v in ipairs(t2) do
      local vx = tonumber(Char.GetTempData(charIndex, "CSE:" .. v[1])) or 0;
      if (vx ~= 0 and vx ~= nil) then
        local vxL = tonumber(Char.GetTempData(charIndex, "CSE:L" .. v[1])) or -1;
        Char.SetTempData(charIndex, "CSE:L" .. v[1], nil);
        local vo = Char.GetData(charIndex, v[1]);
        local full = vo == Char.GetData(charIndex, v[2]) and vo == vxL;
        Char.SetData(charIndex, v[1], vo + vx);
        if full then
          Char.GetData(charIndex, v[2], vo + vx);
        end
      end
    end
  end
end

function CharStatusExtend:onUnload()
  self:logInfo('unload');
end

return CharStatusExtend;
