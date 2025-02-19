---原地登陆
---@class LoginModule: ModuleType
local LoginModule = ModuleBase:createModule('loginGate')
---是否启用lua自定义登陆点
local customLoginPoints = false;
local LoginPoints = {};
-- 出生点
LoginPoints[-1] = {
  { 0, 1530, 15, 6 },
  { 0, 1530, 15, 6 },
  { 0, 1530, 15, 6 },
  { 0, 1530, 15, 6 },
  { 0, 1530, 15, 6 },
  { 0, 1530, 15, 6 },
}
-- 法兰城登陆点设置 LoginPoint = 0
LoginPoints[0] = {
  { 0, 1000, 233, 78 },
  { 0, 1000, 233, 78 },
  { 0, 1000, 233, 78 },
  { 0, 1000, 233, 78 },
  { 0, 1000, 233, 78 },
  { 0, 1000, 233, 78 },
};
-- 阿凯鲁法村登录点设置 LoginPoint = 1
LoginPoints[1] = {
  { 0, 33200, 99, 165 },
};
-- 哥拉尔登陆点设置 LoginPoint = 2
LoginPoints[2] = {
  { 0, 43100, 120, 107 },
};
-- 新城登陆点设置 LoginPoint = 3
LoginPoints[3] = {
  { 0, 59520, 140, 105 },
};

function LoginModule:GetLoginPointEvent(charIndex, mapID, floorID, x, y)
  if Char.EndEvent(charIndex, 0) ~= 1 then
    return
  end
  ---@type number|string|number[]|nil
  local lastPoint = Char.GetExtData(charIndex, "LastLogoutPoint");
  if type(lastPoint) == "string" then
    local ret;
    ret, lastPoint = pcall(JSON.decode, lastPoint);
    if ret and lastPoint then
      if (lastPoint[1] == 1) then
        local expire = Map.GetDungeonExpireAt(lastPoint[2]);
        local dungeonId = Map.GetDungeonId(lastPoint[2]);
        if expire ~= lastPoint[5] or lastPoint[6] ~= dungeonId then
          mapID, floorID, x, y = Map.FindDungeonEntry(lastPoint[6]);
          if mapID >= 0 and floorID > 0 then
            lastPoint = { mapID, floorID, x, y };
          else
            lastPoint = nil;
          end
        end
      end
    else
      self:logError('decode json failed:', json, lastPoint);
      lastPoint = nil;
    end
  end
  Char.SetExtData(charIndex, 'LastLogoutPoint', nil);
  --self:logDebug('LoginPoint', Char.GetData(charIndex, CONST.CHAR_登陆点), table.unpack(lastPoint or {}))
  if lastPoint == nil or lastPoint[1] == 0 and lastPoint[2] == 0 then
    if customLoginPoints == false then
      return
    end
    lastPoint = LoginPoints[Char.GetData(charIndex, CONST.CHAR_登陆点)] or LoginPoints[0];
    lastPoint = lastPoint[math.random(1, #lastPoint)]
  end
  Char.SetData(charIndex, CONST.CHAR_地图类型, lastPoint[1]);
  Char.SetData(charIndex, CONST.CHAR_地图, lastPoint[2]);
  Char.SetData(charIndex, CONST.CHAR_X, lastPoint[3]);
  Char.SetData(charIndex, CONST.CHAR_Y, lastPoint[4]);
end

function LoginModule:LogoutEvent(charIndex)
  local lastPoint = {
    Char.GetData(charIndex, CONST.CHAR_地图类型),
    Char.GetData(charIndex, CONST.CHAR_地图),
    Char.GetData(charIndex, CONST.CHAR_X),
    Char.GetData(charIndex, CONST.CHAR_Y),
  };
  if lastPoint[1] == 0 and lastPoint[2] == 0 then
    lastPoint = nil;
    goto END;
  end
  if lastPoint[1] == 1 then
    local expire = Map.GetDungeonExpireAt(lastPoint[2])
    lastPoint[5] = expire;
    lastPoint[6] = Map.GetDungeonId(lastPoint[2]);
    goto END;
  end
  if lastPoint[1] > 1 then
    lastPoint = nil
    goto END;
  end
  ::END::
  if lastPoint then
    Char.SetExtData(charIndex, 'LastLogoutPoint', JSON.encode(lastPoint));
  else
    Char.SetExtData(charIndex, 'LastLogoutPoint', nil);
  end
  return 0;
end

--- 加载模块钩子
function LoginModule:onLoad()
  self:logInfo('load')
  self:regCallback('GetLoginPointEvent', Func.bind(self.GetLoginPointEvent, self));
  self:regCallback('LogoutEvent', Func.bind(self.LogoutEvent, self))
  self:regCallback('DropEvent', Func.bind(self.LogoutEvent, self))
end

--- 卸载模块钩子
function LoginModule:onUnload()
  self:logInfo('unload')
end

return LoginModule;
