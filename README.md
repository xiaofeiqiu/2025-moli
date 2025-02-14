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
| `/module reload {module_name}` | 重新加载指定模块, 模块可以在lua/Modules找到，每个lua脚本都会定义模块名字 |`/module reload bag`|


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

# 常用命令
| 命令                        | 解释 |
|----------------------------|------------------------------------------------|
|[nr makepet {宠物id}]|宠物id可以在[GMSV/data/enemy_cn.txt](gmsv/data/enemy_cn.txt)找到 905 是圣龙|
|[nr setpettech 0 3 8659]|设置第0个宠物的第三个技能为8659 (超强即死)， 技能编号在[text](gmsv/data/tech.txt)|
| [nr setpettech 0 3 8659]   | 设置第 0 个宠物的第 3 个技能为 **8659（超强即死）** |
| [nr setpettech 0 3 451]    | 设置第 0 个宠物的第 3 个技能为 **451（气功蛋 EX）** |
| [nr checkoinum]          | 查看当前形象 ID |
| [nr metamo {形象ID}]      | 更改角色形象 ID |
| [nr setallskilllv 2]      | 将所有技能等级设置为 **2** |
| [nr setskillslot xxx]     | 扩展技能栏，默认 10 个栏位，可扩展至 15 个。参数范围 `11-15`，如 `nr setskillslot 13` 增加 3 个栏位 |
| [nr warp 0 11011 23 17] | 传送到地图11011，0楼，坐标23，17，地图id可以在data/MapTransName.txt 找到|


# Quick start
1. 下载台服客户端 https://cg.softstar.com.tw/
2. 下载本repo
3. 把所有登陆器下面的文件复制到游戏客户端目录下
4. 启动服务端.bat
5. 启动游戏客户端目录下面的登陆器
6. 到127.0.0.1 注册游戏账号密码
7. 登入游戏