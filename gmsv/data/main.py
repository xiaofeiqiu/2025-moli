import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from enum import Enum
import os

# 枚举定义
class SkillType(Enum):
    Passive = 0         # 被动技能
    PhysicalAttack = 1  # 物理攻击
    Production = 2      # 生产技能
    Magic = 3           # 魔法技能
    Other = 6           # 其他类技能

class WeaponRestriction(Enum):
    NoLimit = 255       # 无限制
    Melee = 143         # 近战武器
    MeleeOrBow = 159    # 近战武器或弓
    Boomerang = 64      # 回力镖
    Barehand = 128      # 空手

class JobType(Enum):
    Combat = 1          # 战斗职业
    Production = 2      # 生产职业
    Other = 3           # 其他

# 数据管理器：负责加载、保存各个配置文件，并提供联合视图
class DataManager:
    def __init__(self):
        self.skills = []    # 来自 skill.txt
        self.techs = []     # 来自 tech.txt
        self.skilllvs = []  # 来自 skilllv.txt
        self.jobs = []      # 来自 jobs.txt

    def load_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='gb18030', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []
        data = []
        for line in lines:
            if line.strip() == '':
                continue
            tokens = line.strip().split()
            data.append(tokens)
        return data

    def load_skills(self, filepath):
        self.skills = self.load_file(filepath)

    def load_techs(self, filepath):
        # 先加载原始数据
        raw_data = self.load_file(filepath)
        processed_data = []
        # 对每一行预处理：查找第一个以 "TECH_" 开头的列
        for row in raw_data:
            index = None
            for i, token in enumerate(row):
                if token.startswith("TECH_"):
                    index = i
                    break
            if index is not None and index > 0:
                # 合并该列之前的所有token为技能名称
                merged = " ".join(row[:index])
                new_row = [merged] + row[index:]
            else:
                new_row = row
            processed_data.append(new_row)
        self.techs = processed_data

    def load_skilllvs(self, filepath):
        self.skilllvs = self.load_file(filepath)

    def load_jobs(self, filepath):
        self.jobs = self.load_file(filepath)

    def save_file(self, filepath, data):
        """Overwrite file while ensuring all data is written line by line."""
        if not data:  # 🚨 Prevent overwriting with empty data
            print(f"⚠️ Warning: Attempted to save empty file {filepath}, operation aborted.")
            return

        try:
            with open(filepath, 'w', encoding='gb18030') as f:  # ✅ Overwrite the file
                for row in data:
                    row_str = '\t'.join(map(str, row))  # ✅ Convert each item to a string
                    f.write(row_str + '\n')  # ✅ Ensure each row is on a new line
        except Exception as e:
            print(f"Error writing file {filepath}: {e}")


    def save_skills(self, filepath):
        self.save_file(filepath, self.skills)

    def save_techs(self, filepath):
        self.save_file(filepath, self.techs)

    def save_skilllvs(self, filepath):
        self.save_file(filepath, self.skilllvs)

    def save_jobs(self, filepath):
        self.save_file(filepath, self.jobs)

    # join_all() 将 skilllv.txt 为基础，联合 skill.txt、tech.txt、jobs.txt 成一个完整的配置表
    # 每行 join 后的字段为：
    # [职业名称, 职业编号, 技能名称, 技能代号, 技能种类, 学习费用, 武器限制, 最高可学等级, 技能效果名称, 技能效果参数, 技能效果等级]
    def join_all(self):
        joined = []
        for lvl in self.skilllvs:
            if len(lvl) < 4:
                continue
            skill_id = lvl[1]
            job_id = lvl[2]
            max_level = lvl[3]
            
            skill = next((s for s in self.skills if len(s) > 1 and s[1] == skill_id), None)
            job = next((j for j in self.jobs if len(j) > 1 and j[1] == job_id), None)
            
            job_name = job[0] if job else ""
            job_no = job[1] if job else ""
            skill_name = skill[0] if skill else ""
            skill_code = skill[1] if skill else ""
            skill_type = skill[3] if skill and len(skill) > 3 else ""
            learn_cost = skill[6] if skill and len(skill) > 6 else ""
            weapon_limit = skill[8] if skill and len(skill) > 8 else ""
            
            joined.append([
                job_name,
                job_no,
                skill_name,
                skill_code,
                skill_type,
                learn_cost,
                weapon_limit,
                max_level
            ])
        return joined


# 编辑窗口，编辑和添加时字段前显示列名称
class RecordEditor(tk.Toplevel):
    def __init__(self, master, record, col_names, callback):
        super().__init__(master)
        self.title("编辑记录")
        self.record = record.copy()
        self.col_names = col_names  # 预设的列名称
        self.callback = callback
        self.entries = []
        # 为每个字段添加标签，标签内容与表格中的列名一致
        for i, col in enumerate(col_names):
            tk.Label(self, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = tk.Entry(self, width=50)
            entry.insert(0, record[i] if i < len(record) else "")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)
        btn_save = tk.Button(self, text="保存", command=self.save)
        btn_save.grid(row=len(col_names), column=0, columnspan=2, pady=10)
    
    def save(self):
        new_record = [e.get() for e in self.entries]
        self.callback(new_record)
        self.destroy()

# 主应用程序
class SkillManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("技能配置管理")
        self.geometry("1200x700")
        self.data_manager = DataManager()
        # 预设各表的列名称
        self.col_names = {
            "skills": ["技能名称", "技能代号", "技能解释", "技能种类", "非本职等级", "技能类别", "学习费用", "未知", "武器限制", "经验关联", "技能栏", "未知", "职业经验"],
            "techs": ["技能名称", "技能性质", "技能效果", "未知", "图挡代码", "关联技能代号", "技能等级", "技能种类", "技能范围", "耗魔量", "使用者"],
            "skilllvs": ["唯一ID", "技能代号", "职业代号", "最高等级"],
            "jobs": ["职业名称", "职业编号", "类型", "转职金钱", "转职声望"],
            "config": ["职业名称", "职业编号", "技能名称", "技能代号", "技能种类", "学习费用", "武器限制", "最高等级"]
        }
        self.create_menu()
        self.create_widgets()
        self.auto_load_default_files()
    
    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="加载 Skills", command=self.load_skills_dialog)
        filemenu.add_command(label="加载 Techs", command=self.load_techs_dialog)
        filemenu.add_command(label="加载 SkillLv", command=self.load_skilllvs_dialog)
        filemenu.add_command(label="加载 Jobs", command=self.load_jobs_dialog)
        filemenu.add_separator()
        filemenu.add_command(label="保存 Skills", command=self.save_skills)
        filemenu.add_command(label="保存 Techs", command=self.save_techs)
        filemenu.add_command(label="保存 SkillLv", command=self.save_skilllvs)
        filemenu.add_command(label="保存 Jobs", command=self.save_jobs)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.quit)
        menubar.add_cascade(label="文件", menu=filemenu)
        self.config(menu=menubar)
    
    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        
        # 分别显示原始数据表
        self.tab_skills = ttk.Frame(self.notebook)
        self.tab_techs = ttk.Frame(self.notebook)
        self.tab_skilllvs = ttk.Frame(self.notebook)
        self.tab_jobs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text="Skills")
        self.notebook.add(self.tab_techs, text="Techs")
        self.notebook.add(self.tab_skilllvs, text="SkillLv")
        self.notebook.add(self.tab_jobs, text="Jobs")
        
        # 配置详情页（join 四个表后的数据）
        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="配置详情")
        
        # 为各表创建 Treeview，并设置预设列名
        self.tree_skills = self.create_treeview(self.tab_skills, self.col_names["skills"], "skills")
        self.tree_techs = self.create_treeview(self.tab_techs, self.col_names["techs"], "techs")
        self.tree_skilllvs = self.create_treeview(self.tab_skilllvs, self.col_names["skilllvs"], "skilllvs")
        self.tree_jobs = self.create_treeview(self.tab_jobs, self.col_names["jobs"], "jobs")

        
        # 配置详情页顶部增加职业选择区域
        top_frame = tk.Frame(self.tab_config)
        top_frame.pack(fill='x', pady=5)
        tk.Label(top_frame, text="选择职业:").pack(side='left', padx=5)
        self.job_combobox = ttk.Combobox(top_frame, state="readonly", width=30)
        self.job_combobox.pack(side='left', padx=5)
        btn_query = tk.Button(top_frame, text="查询", command=self.refresh_config_details)
        btn_query.pack(side='left', padx=5)
        self.tree_config = self.create_treeview_no_search(self.tab_config, self.col_names["config"])

        
        self.create_buttons(self.tab_skills, self.tree_skills, "skills")
        self.create_buttons(self.tab_techs, self.tree_techs, "techs")
        self.create_buttons(self.tab_skilllvs, self.tree_skilllvs, "skilllvs")
        self.create_buttons(self.tab_jobs, self.tree_jobs, "jobs")
    
    def create_treeview(self, parent, col_names, data_type):
        """创建表格视图，并在顶部添加搜索框"""
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True)
        
        # 搜索框
        search_frame = tk.Frame(frame)
        search_frame.pack(fill='x', padx=5, pady=2)
        tk.Label(search_frame, text="搜索:").pack(side="left")
        
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True)
        
        # Treeview 表格
        tree = ttk.Treeview(frame, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')

        # 配置表头
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # 绑定搜索框事件
        search_entry.bind("<KeyRelease>", lambda event: self.search_tree(tree, search_entry.get(), data_type))

        return tree
    
    def create_treeview_no_search(self, parent, col_names):
        """创建不带搜索框的表格视图"""
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True)

        # Treeview 表格
        tree = ttk.Treeview(frame, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')

        # 配置表头
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # 滚动条
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        return tree

    
    def search_tree(self, tree, query, data_type):
        """根据查询内容搜索并更新表格"""
        query = query.lower()  # 统一转换为小写，支持大小写不敏感搜索

        # 获取原始数据和对应的列
        if data_type == "skills":
            data = self.data_manager.skills
        elif data_type == "techs":
            data = self.data_manager.techs
        elif data_type == "skilllvs":
            data = self.data_manager.skilllvs
        elif data_type == "jobs":
            data = self.data_manager.jobs
        else:
            return

        # 针对 SkillLv 进行名称映射，同时保留原始索引
        filtered_data = []
        if data_type == "skilllvs":
            # 创建 技能代号 -> 技能名称 映射
            skill_mapping = {t[1]: t[0] for t in self.data_manager.skills if len(t) > 5}
            # 创建 职业代号 -> 职业名称 映射
            job_mapping = {j[1]: j[0] for j in self.data_manager.jobs if len(j) > 1}
            for i, row in enumerate(data):
                if len(row) < 3:
                    continue
                # 原始代号
                skill_id = row[1]
                job_id = row[2]
                # 映射为名称（找不到时保留原值）
                skill_name = skill_mapping.get(skill_id, skill_id)
                job_name = job_mapping.get(job_id, job_id)
                # 构造显示行，同时保留原始索引 i
                processed_row = [row[0], skill_name, job_name] + row[3:]
                if any(query in str(cell).lower() for cell in processed_row):
                    filtered_data.append((i, processed_row))
        else:
            # 其它数据类型，遍历原始数据时记录原始索引
            for i, row in enumerate(data):
                if any(query in str(cell).lower() for cell in row):
                    filtered_data.append((i, row))

        # 清空表格
        for item in tree.get_children():
            tree.delete(item)

        # 插入过滤后的数据，并设置 iid 为原始数据的索引（转换为字符串）
        for original_index, row in filtered_data:
            tree.insert("", "end", iid=str(original_index), values=row)


    def create_buttons(self, parent, tree, data_type):
        frame = tk.Frame(parent)
        frame.pack(side='bottom', fill='x')

        btn_add = tk.Button(frame, text="添加", command=lambda: self.add_record(data_type))
        btn_edit = tk.Button(frame, text="编辑", command=lambda: self.edit_record(tree, data_type))
        btn_delete = tk.Button(frame, text="删除", command=lambda: self.delete_record(tree, data_type))
        btn_refresh = tk.Button(frame, text="刷新", command=lambda: self.refresh_tree(data_type))
        btn_save = tk.Button(frame, text="保存", command=lambda: self.save_data(data_type))  # 添加保存按钮

        btn_add.pack(side='left', padx=5, pady=5)
        btn_edit.pack(side='left', padx=5, pady=5)
        btn_delete.pack(side='left', padx=5, pady=5)
        btn_refresh.pack(side='left', padx=5, pady=5)
        btn_save.pack(side='left', padx=5, pady=5)  # 显示保存按钮


    def save_data(self, data_type):
        """根据数据类型保存更改到文件，SkillLv 需要转换回代号"""
        if data_type == "skilllvs" and hasattr(self, 'skilllv_file'):
            # 1️⃣ 创建 技能名称 -> 技能代号 映射
            skill_name_to_id = {t[0]: t[1] for t in self.data_manager.skills if len(t) > 5}

            # 2️⃣ 创建 职业名称 -> 职业代号 映射
            job_name_to_id = {j[0]: j[1] for j in self.data_manager.jobs if len(j) > 1}

            # 3️⃣ 还原 SkillLv 表中的名称 -> 代号
            processed_data = []
            for row in self.data_manager.skilllvs:
                if len(row) < 3:
                    continue

                skill_name = row[1]
                job_name = row[2]

                # 用映射找到代号，找不到就保留原值
                skill_id = skill_name_to_id.get(skill_name, skill_name)
                job_id = job_name_to_id.get(job_name, job_name)

                # 还原为 [唯一ID, 技能代号, 职业代号, 最高等级]
                processed_data.append([row[0], skill_id, job_id] + row[3:])

            # 4️⃣ 存储 SkillLv 数据
            self.data_manager.skilllvs = processed_data
            self.data_manager.save_skilllvs(self.skilllv_file)
            messagebox.showinfo("保存", "SkillLv 保存成功")

        elif data_type == "skills" and hasattr(self, 'skill_file'):
            self.data_manager.save_skills(self.skill_file)
            messagebox.showinfo("保存", "Skills 保存成功")
        elif data_type == "techs" and hasattr(self, 'tech_file'):
            self.data_manager.save_techs(self.tech_file)
            messagebox.showinfo("保存", "Techs 保存成功")
        elif data_type == "jobs" and hasattr(self, 'job_file'):
            self.data_manager.save_jobs(self.job_file)
            messagebox.showinfo("保存", "Jobs 保存成功")
        else:
            messagebox.showwarning("保存失败", f"{data_type} 文件未加载，无法保存！")


    def auto_load_default_files(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        skill_path = os.path.join(cur_dir, "skill.txt")
        tech_path = os.path.join(cur_dir, "tech.txt")
        skilllv_path = os.path.join(cur_dir, "skilllv.txt")
        jobs_path = os.path.join(cur_dir, "jobs.txt")
        if os.path.exists(skill_path):
            self.data_manager.load_skills(skill_path)
            self.skill_file = skill_path
            self.refresh_tree("skills")
        if os.path.exists(jobs_path):
            self.data_manager.load_jobs(jobs_path)
            self.job_file = jobs_path
            self.refresh_tree("jobs")
            self.update_job_combobox()
        if os.path.exists(tech_path):
            self.data_manager.load_techs(tech_path)
            self.tech_file = tech_path
            self.refresh_tree("techs")
        if os.path.exists(skilllv_path):
            self.data_manager.load_skilllvs(skilllv_path)
            self.skilllv_file = skilllv_path
            self.refresh_tree("skilllvs")
        
        else:
            print(f"jobs.txt not found in {cur_dir}")
    
    def load_skills_dialog(self):
        path = filedialog.askopenfilename(title="选择 skill.txt", filetypes=[("Text Files", "*.txt")])
        if path:
            self.data_manager.load_skills(path)
            self.skill_file = path
            self.refresh_tree("skills")
    
    def load_techs_dialog(self):
        path = filedialog.askopenfilename(title="选择 tech.txt", filetypes=[("Text Files", "*.txt")])
        if path:
            self.data_manager.load_techs(path)
            self.tech_file = path
            self.refresh_tree("techs")
    
    def load_skilllvs_dialog(self):
        path = filedialog.askopenfilename(title="选择 skilllv.txt", filetypes=[("Text Files", "*.txt")])
        if path:
            self.data_manager.load_skilllvs(path)
            self.skilllv_file = path
            self.refresh_tree("skilllvs")
    
    def load_jobs_dialog(self):
        path = filedialog.askopenfilename(title="选择 jobs.txt", filetypes=[("Text Files", "*.txt")])
        if path:
            self.data_manager.load_jobs(path)
            self.job_file = path
            self.refresh_tree("jobs")
            self.update_job_combobox()
    
    def save_skills(self):
        if hasattr(self, 'skill_file'):
            self.data_manager.save_skills(self.skill_file)
            messagebox.showinfo("保存", "Skills 保存成功")
    
    def save_techs(self):
        if hasattr(self, 'tech_file'):
            self.data_manager.save_techs(self.tech_file)
            messagebox.showinfo("保存", "Techs 保存成功")
    
    def save_skilllvs(self):
        if hasattr(self, 'skilllv_file'):
            self.data_manager.save_skilllvs(self.skilllv_file)
            messagebox.showinfo("保存", "SkillLv 保存成功")
    
    def save_jobs(self):
        if hasattr(self, 'job_file'):
            self.data_manager.save_jobs(self.job_file)
            messagebox.showinfo("保存", "Jobs 保存成功")
    
    def refresh_tree(self, data_type):
        if data_type == "skills":
            tree = self.tree_skills
            data = self.data_manager.skills
            cols = self.col_names["skills"]
        elif data_type == "jobs":
            tree = self.tree_jobs
            data = self.data_manager.jobs
            cols = self.col_names["jobs"]
        elif data_type == "techs":
            tree = self.tree_techs
            data = self.data_manager.techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            data = self.data_manager.skilllvs
            cols = self.col_names["skilllvs"]

            # 创建一个职业编号 -> 职业名称的映射表
            job_mapping = {j[1]: j[0] for j in self.data_manager.jobs if len(j) > 1}
            # 创建一个技能代号 -> 技能名称的映射表
            tech_mapping = {t[1]: t[0] for t in self.data_manager.skills if len(t) > 5}
            
            processed_data = []
            for row in data:
                if len(row) < 3:
                    continue

                skill_id = row[1]  # 获取技能代号
                job_id = row[2]  # 获取职业代号

                # 查找技能名称，如果找不到就显示原技能代号
                skill_name = tech_mapping.get(skill_id, skill_id)
                # 查找职业名称，如果找不到就显示原职业代号
                job_name = job_mapping.get(job_id, job_id)

                processed_row = [row[0], skill_name, job_name] + row[3:]  # 替换技能代号和职业代号
                processed_data.append(processed_row)

            data = processed_data  # 只影响显示

        else:
            return

        # 清空 TreeView
        for item in tree.get_children():
            tree.delete(item)

        # 重新插入处理后的数据，同时指定 iid 为原始数据的索引
        for idx, row in enumerate(data):
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", iid=str(idx), values=row_extended)



    
    def update_job_combobox(self):
        """更新职业下拉框，允许用户输入并支持过滤"""
        self.job_list = [f"{job[1]}: {job[0]}" for job in self.data_manager.jobs if len(job) >= 2]
        
        # 允许输入
        self.job_combobox.config(state="normal")
        self.job_combobox['values'] = self.job_list
        
        if self.job_list:
            self.job_combobox.set(self.job_list[0])  # 设置默认值
        
        # 绑定输入事件以支持过滤
        self.job_combobox.bind("<KeyRelease>", self.filter_combobox)

    def filter_combobox(self, event):
        """根据用户输入动态过滤职业选项"""
        value = self.job_combobox.get().lower()
        
        # 筛选包含用户输入的选项
        filtered = [job for job in self.job_list if value in job.lower()]
        
        # 更新下拉框选项
        self.job_combobox['values'] = filtered

    
    def refresh_config_details(self):
        all_joined = self.data_manager.join_all()
        selected = self.job_combobox.get()
        if not selected:
            filtered = all_joined
        else:
            job_no = selected.split(":")[0].strip()
            filtered = [row for row in all_joined if row[1] == job_no]
        tree = self.tree_config
        for item in tree.get_children():
            tree.delete(item)
        for row in filtered:
            tree.insert("", "end", values=row)
    
    def get_data_list(self, data_type):
        if data_type == "skills":
            return self.data_manager.skills
        elif data_type == "techs":
            return self.data_manager.techs
        elif data_type == "skilllvs":
            return self.data_manager.skilllvs
        elif data_type == "jobs":
            return self.data_manager.jobs
        else:
            return []
    
    def set_data_list(self, data_type, data):
        if data_type == "skills":
            self.data_manager.skills = data
        elif data_type == "techs":
            self.data_manager.techs = data
        elif data_type == "skilllvs":
            self.data_manager.skilllvs = data
        elif data_type == "jobs":
            self.data_manager.jobs = data
    
    def add_record(self, data_type):
        data = self.get_data_list(data_type)
        cols = self.col_names[data_type]
        num_cols = len(cols)
        new_record = [""] * num_cols
        def callback(rec):
            data.append(rec)
            self.refresh_tree(data_type)
        RecordEditor(self, new_record, cols, callback)
    
    def edit_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("编辑", "请选择一行")
            return
        # 直接使用 iid 作为索引（这里 iid 是字符串，需要转换成整数）
        index = int(selected[0])
        values = list(tree.item(selected[0])['values'])
        data = self.get_data_list(data_type)
        cols = self.col_names[data_type]
        def callback(rec):
            data[index] = rec
            self.refresh_tree(data_type)
        RecordEditor(self, values, cols, callback)

    
    def delete_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("删除", "请选择一行")
            return
        index = tree.index(selected[0])
        data = self.get_data_list(data_type)
        del data[index]
        self.refresh_tree(data_type)

if __name__ == "__main__":
    app = SkillManagerApp()
    app.mainloop()