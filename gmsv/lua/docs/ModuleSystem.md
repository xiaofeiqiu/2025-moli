## ģ��ϵͳ

֧�ֶ�̬���ء�ж���Լ��汾����������Ǩ�ơ�����ͨ��Moduleע��Ļص�ж��ʱ�Զ�����

### ModuleBase��

#### ����

1. `name` ��ǰģ������, string����
2. `migrations` ����Ǩ���б� �������ͣ� ÿ��Ԫ����Ҫ��`version`��`name`��`value` ��������
    - `version` �汾�� number����
    - `name` ���� string����
    - `value` sql���߾��巽�� string��function����

#### ����

1. `ModuleBase:regCallback(eventNameOrCallbackKeyOrFn, fn)`  ע��ص�
    - ���� `eventNameOrCallbackKeyOrFn`
      - ���Դ���NL.Reg*��Ӧ���¼����ƣ���NL.RegLoginEvent ���� `LoginEvent`
      - �Զ�����������ڷ�ȫ�ֻص�����NPC�����ص���
      - �����ص�����NPC�����ص���

    - ���� `fn`
      - �ص����������eventNameOrCallbackKeyOrFn�������ص���fn���Դ�nil

    - ����ֵ `eventNameOrCallbackKeyOrFn`, `lastIx`, `fnIndex`
      - `eventNameOrCallbackKeyOrFn` ������ȫ��Key�����ڴ���NL.Reg*
      - `lastIx` ��ǰģ���µ�ע������
      - `fnIndex` ȫ��ע������

2. `ModuleBase:unRegCallback(eventNameOrCallbackKey, fnOrFnIndex)`  ��ע��ص�
    - ���� `eventNameOrCallbackKey`
      - ���Դ���NL.Reg*��Ӧ���¼����ƣ���NL.RegLoginEvent ���� `LoginEvent`
      - �Զ�����������ڷ�ȫ�ֻص�����NPC�����ص���

    - ���� `fnOrFnIndex`
      - ���봫��ע���õĻص�����
      - Ҳ����fnIndex ȫ��ע������
3. `ModuleBase:onLoad()`  ģ��ע�ṳ�ӣ��ɾ���ʵ��ģ��ʵ��
4. `ModuleBase:onUnload()`  ģ��ж�ع��ӣ��ɾ���ʵ��ģ��ʵ��
5. `ModuleBase:logInfo(msg, ...)`  ��ӡ��־
6. `ModuleBase:logDebug(msg, ...)`  ��ӡ��־
7. `ModuleBase:logWarn(msg, ...)`  ��ӡ��־
8. `ModuleBase:logError(msg, ...)`  ��ӡ��־
9. `ModuleBase:log(level, msg, ...)`  ��ӡ��־
10. `ModuleBase:addMigration(version, name, sqlOrFunction)` ����һ����Ǩ��

## ģ�����
����ģ�������ModuleConfig.lua
### loadModule 
����`Modules`�µ�Module��Module���������໥�����������ֶ�ָ��ȫ�ֱ��������򲻻�Ӱ������Module�������������Module��ͨ��getModule��ȡ
```
loadModule('admin') --����adminģ��
```
### useModule 
����`Module`Ŀ¼�µ���ͨlua, ��ͨlua������һ����������������ִ�С������ֶ�ָ��Ϊȫ�ֱ���������ֻ��Ӱ����ͨlua��module���ܷ�����ر���/����
```
useModule('Welcome') --����Welcome
```
### getModule
��ȡ��Ӧ��Module

### unloadModule
ж��Module

### reloadModule
���¼���Module

�����ĵ�: [�����](readme.md)