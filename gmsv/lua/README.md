# cgmsv lua

## 模块系统
支持动态加载、卸载以及版本升级的数据迁移。其中通过Module注册的回调卸载时自动清理，具体文档：[ModuleSystem.md](docs/ModuleSystem.md)

### 目前能用的模块
1. admin 模块动态管理等
2. ng 内挂相关
3. shop 东门商店NPC配置
4. warp 村落传送
5. warp2 练级点传送
6. welcome 示例模块
7. itemPowerUp.lua 装备强化
8. manaPool 血魔池
9. bag 背包切换
10. autoRegister 自动注册
11. petLottery 宠物抽奖
12. petRebirth 宠物转生
13. autoUnlock 自动解锁崩端导致的卡号
14. charStatusExtend 动态附加属性

## 扩展事件/接口
接口参考 [接口参考](docs/readme.md)

## 版本&下载
### 版本说明:
- 0.3.x: 适配cgmsv24.x, 稳定性较高
- 0.2.x: 适配cgmsv21.2b, 稳定性一般
- 0.1.x: 纯lua版，稳定性极低

### 下载地址:
[releases](https://github.com/Muscipular/cgmsv-lua/releases)

# 玩家命令文档

## 1. 角色管理

| 命令 | 作用 | 用法示例 |
|------|------|---------|
| `/where` | 查询自己或指定玩家的位置信息 | `/where` 或 `/where 目标ID` |
| `/char healthRepair` | 治疗角色受伤状态，消耗金币 | `/char healthRepair` |
| `/char spriteRepair` | 招魂（恢复掉魂），消耗金币 | `/char spriteRepair` |
| `/char addFrame` | 设置角色声望值为200000 | `/char addFrame` |
| `/daka` | 切换角色的卡时状态（挂机模式） | `/daka` |
| `/redoDp` | 重置角色升级点并重新分配 | `/redoDp` |
| `/encount` | 触发随机遭遇战斗 | `/encount` |
| `/noencount` | 切换不遇敌状态 | `/noencount` |
| `/goHome` | 传送回家（固定坐标） | `/goHome` |

---

## 2. 道具管理

| 命令 | 作用 | 用法示例 |
|------|------|---------|
| `/item sort` | 整理背包 | `/item sort` |
| `/item identity` | 鉴定未鉴定的道具（扣除金币） | `/item identity` |
| `/item repair` | 修理装备（恢复耐久，扣除金币） | `/item repair` |

---

## 3. 宠物管理

| 命令 | 作用 | 用法示例 |
|------|------|---------|
| `/pet bp` | 获取宠物成长档案信息 | `/pet bp` |
| `/pet rebirth [宠物栏位]` | 宠物转生，调整成长率 | `/pet rebirth 0` |
| `/md` | 洗档1级宠物，使其成长属性最大化 | `/md` |

---

## 4. 其他功能

| 命令 | 作用 | 用法示例 |
|------|------|---------|
| `/bank` | 打开银行存取界面 | `/bank` |
| `/zl` | 自动整理魔石，将魔石兑换成金币 | `/zl` |

---

## 5. 使用指南

1. **输入方式**：
   - 在聊天窗口输入命令，例如 `/where`，会显示当前角色的地图坐标。
   - 部分命令可以附带参数，例如 `/pet rebirth 0`，表示转生位于第0号位置的宠物。
   
2. **命令格式**：
   - 所有命令均以 `/` 开头。
   - 命令区分大小写，请确保正确输入。
   
3. **注意事项**：
   - 部分命令（如 `/item identity`）需要消耗金币，请确保余额充足。
   - 某些操作（如 `/pet rebirth`）不可逆，使用前请谨慎。

如果有其他问题或需要补充的内容，请联系管理员或开发人员！
