import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re

class DataManager:
    def __init__(self):
        self.skills = []
        self.techs = []
        self.skilllvs = []
        self.jobs = []

    def load_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='gb18030', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []
        data = []
        for line in lines:
            if not line.strip():
                continue
            tokens = re.split(r'\s+', line.strip())
            data.append(tokens)
        return data

    def load_skills(self, filepath):
        self.skills = self.load_file(filepath)

    def load_techs(self, filepath):
        raw_data = self.load_file(filepath)
        processed = []
        expected_cols = 11
        # 先收集所有技能种类出现的值（原始数据中技能种类位于索引7）
        skilltype_values = set()
        for row in raw_data:
            if len(row) > 7:
                skilltype_values.add(row[7])
        # 已知映射
        known_mapping = {"1": "战斗技能", "2": "生产技能", "3": "治疗/急救/变装技能"}
        # 对于未知的数值，自动命名为“未知技能类型(值)”
        mapping = {}
        for val in skilltype_values:
            if val in known_mapping:
                mapping[val] = known_mapping[val]
            else:
                mapping[val] = f"未知技能类型({val})"
        map_user = {"0": "宠物", "1": "人类"}
        for row in raw_data:
            idx = None
            for i, token in enumerate(row):
                if token.startswith("TECH_"):
                    idx = i
                    break
            if idx is not None and idx > 0:
                merged = " ".join(row[:idx])
                new_row = [merged] + row[idx:]
            else:
                new_row = row
            if len(new_row) < expected_cols:
                new_row += [""] * (expected_cols - len(new_row))
            elif len(new_row) > expected_cols:
                new_row = new_row[:expected_cols]
            if len(new_row) > 7:
                new_row[7] = mapping.get(new_row[7], new_row[7])
            if len(new_row) > 10:
                new_row[10] = map_user.get(new_row[10], new_row[10])
            processed.append(new_row)
        self.techs = processed

    def load_skilllvs(self, filepath):
        self.skilllvs = self.load_file(filepath)

    def load_jobs(self, filepath):
        self.jobs = self.load_file(filepath)

    def save_file(self, filepath, data):
        try:
            with open(filepath, 'w', encoding='gb18030') as f:
                for row in data:
                    f.write('\t'.join(row) + '\n')
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

    # 用 skilllv 做主表进行关联，修改后SkillLv的技能代号用Tech中对应的技能名称显示
    def join_all(self):
        joined = []
        for lvl in self.skilllvs:
            if len(lvl) < 4:
                continue
            skill_id = lvl[1]
            job_id = lvl[2]
            max_level = lvl[3]
            # 优先在 techs 中查找对应记录（关联技能代号在索引5，且技能等级== "1"）
            tech = next((t for t in self.techs if len(t) > 6 and t[5] == skill_id and t[6] == "1"), None)
            if tech:
                display_skill_name = tech[0]
            else:
                skill = next((s for s in self.skills if len(s) > 1 and s[1] == skill_id), None)
                display_skill_name = skill[0] if skill else ""
            joined.append([
                self.transform_jobid(job_id),  # 职业名称
                job_id,                        # 职业编号
                display_skill_name,            # 技能名称（显示为Tech中的技能名称）
                display_skill_name,            # 技能代号显示为技能名称
                (skill[3] if (not tech and skill and len(skill) > 3) else (tech[7] if tech and len(tech) > 7 else "")),
                (skill[6] if (not tech and skill and len(skill) > 6) else ""),
                (skill[8] if (not tech and skill and len(skill) > 8) else ""),
                max_level,
                (tech[0] if tech else ""),
                (tech[2] if tech and len(tech) > 2 else ""),
                (tech[6] if tech and len(tech) > 6 else "")
            ])
        return joined

    def transform_jobid(self, job_id):
        # 从 jobs.txt 中查找：如果第二列等于 job_id，则返回第一列（职业名称）
        for row in self.jobs:
            if len(row) >= 2 and row[1] == job_id:
                return row[0]
        return job_id

class RecordEditor(tk.Toplevel):
    def __init__(self, master, record, col_names, callback):
        super().__init__(master)
        self.title("编辑记录")
        self.record = record.copy()
        self.col_names = col_names
        self.callback = callback
        self.entries = []
        # 获取jobs映射 {职业名称: 职业编号}
        job_map = master.get_job_map()
        for i, col in enumerate(col_names):
            tk.Label(self, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='w')
            if col == "职业代号":
                # 使用下拉列表显示所有职业名称
                combo = ttk.Combobox(self, values=list(job_map.keys()), state="normal")
                # 如果原记录为数字，则转换成对应名称
                val = record[i]
                for job_name, job_no in job_map.items():
                    if job_no == val:
                        val = job_name
                        break
                combo.set(val)
                combo.grid(row=i, column=1, padx=5, pady=5)
                self.entries.append(combo)
            else:
                e = tk.Entry(self, width=50)
                e.insert(0, record[i] if i < len(record) else "")
                e.grid(row=i, column=1, padx=5, pady=5)
                self.entries.append(e)
        btn_save = tk.Button(self, text="保存", command=self.save)
        btn_save.grid(row=len(col_names), column=0, columnspan=2, pady=10)

    def save(self):
        new_record = []
        job_map = self.master.get_job_map()
        for i, col in enumerate(self.col_names):
            val = self.entries[i].get()
            if col == "职业代号":
                if val in job_map:
                    new_record.append(job_map[val])
                else:
                    new_record.append(val)
            else:
                new_record.append(val)
        self.callback(new_record)
        self.destroy()

class SkillManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("技能配置管理")
        self.geometry("1200x700")
        self.data_manager = DataManager()
        self.col_names = {
            "skills": ["技能名称", "技能代号", "技能解释", "技能种类", "非本职等级", "技能类别", "学习费用", "????", "武器限制", "经验关联", "技能栏", "未知", "职业经验"],
            "techs": ["技能名称", "技能性质", "技能效果", "唯一ID", "图挡代码", "关联技能代号", "技能等级", "技能种类", "技能范围", "耗魔量", "使用者"],
            "skilllvs": ["唯一ID", "技能代号", "职业代号", "最高等级"],
            "jobs": ["职业名称", "职业编号", "类型", "转职金钱", "转职声望"],
            "config": ["职业名称", "职业编号", "技能名称", "技能代号", "技能种类", "学习费用", "武器限制", "最高等级", "技能效果名称", "技能效果参数", "技能效果等级"]
        }
        self.search_keys = {
            "skills": 0,
            "techs": 0,
            "skilllvs": 1,
            "jobs": 0,
            "config": 0
        }
        self.search_entries = {}
        self.create_menu()
        self.create_widgets()
        self.auto_load_default_files()

    def get_job_map(self):
        mapping = {}
        for row in self.data_manager.jobs:
            if len(row) >= 2:
                mapping[row[0]] = row[1]
        return mapping

    def add_search_bar(self, parent, data_type):
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=5)
        tk.Label(frame, text="搜索:").pack(side='left', padx=5)
        entry = tk.Entry(frame)
        entry.pack(side='left', padx=5)
        btn_search = tk.Button(frame, text="搜索", command=lambda: self.search_data(data_type, entry.get()))
        btn_search.pack(side='left', padx=5)
        btn_reset = tk.Button(frame, text="重置", command=lambda: self.refresh_tree(data_type))
        btn_reset.pack(side='left', padx=5)
        self.search_entries[data_type] = entry

    def search_data(self, data_type, keyword):
        # 根据预设的搜索关键字索引，过滤数据（不区分大小写）
        if data_type == "skills":
            full_data = self.data_manager.skills
            key_idx = self.search_keys["skills"]
        elif data_type == "techs":
            full_data = self.data_manager.techs
            key_idx = self.search_keys["techs"]
        elif data_type == "skilllvs":
            full_data = self.data_manager.skilllvs
            key_idx = self.search_keys["skilllvs"]
        elif data_type == "jobs":
            full_data = self.data_manager.jobs
            key_idx = self.search_keys["jobs"]
        elif data_type == "config":
            full_data = self.data_manager.join_all()
            key_idx = self.search_keys["config"]
        else:
            return

        filtered = [row for row in full_data if len(row) > key_idx and keyword.lower() in row[key_idx].lower()]
        # 更新 tree view 显示 filtered 数据
        if data_type == "skills":
            tree = self.tree_skills
            cols = self.col_names["skills"]
        elif data_type == "techs":
            tree = self.tree_techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            cols = self.col_names["skilllvs"]
        elif data_type == "jobs":
            tree = self.tree_jobs
            cols = self.col_names["jobs"]
        elif data_type == "config":
            tree = self.tree_config
            cols = self.col_names["config"]
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in filtered:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

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

        self.tab_skills = ttk.Frame(self.notebook)
        self.tab_techs = ttk.Frame(self.notebook)
        self.tab_skilllvs = ttk.Frame(self.notebook)
        self.tab_jobs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text="Skills")
        self.notebook.add(self.tab_techs, text="Techs")
        self.notebook.add(self.tab_skilllvs, text="SkillLv")
        self.notebook.add(self.tab_jobs, text="Jobs")

        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="配置详情")

        # 为每个 tab 添加搜索栏
        self.add_search_bar(self.tab_skills, "skills")
        self.add_search_bar(self.tab_techs, "techs")
        self.add_search_bar(self.tab_skilllvs, "skilllvs")
        self.add_search_bar(self.tab_jobs, "jobs")
        self.add_search_bar(self.tab_config, "config")

        self.tree_skills = self.create_treeview(self.tab_skills, self.col_names["skills"])
        self.tree_techs = self.create_treeview(self.tab_techs, self.col_names["techs"])
        self.tree_skilllvs = self.create_treeview(self.tab_skilllvs, self.col_names["skilllvs"])
        self.tree_jobs = self.create_treeview(self.tab_jobs, self.col_names["jobs"])

        top_frame = tk.Frame(self.tab_config)
        top_frame.pack(fill='x', pady=5)
        tk.Label(top_frame, text="选择职业:").pack(side='left', padx=5)
        self.job_combobox = ttk.Combobox(top_frame, state="readonly", width=30)
        self.job_combobox.pack(side='left', padx=5)
        btn_query = tk.Button(top_frame, text="查询", command=self.refresh_config_details)
        btn_query.pack(side='left', padx=5)
        self.tree_config = self.create_treeview(self.tab_config, self.col_names["config"])

        self.create_buttons(self.tab_skills, self.tree_skills, "skills")
        self.create_buttons(self.tab_techs, self.tree_techs, "techs")
        self.create_buttons(self.tab_skilllvs, self.tree_skilllvs, "skilllvs")
        self.create_buttons(self.tab_jobs, self.tree_jobs, "jobs")

    def create_treeview(self, parent, col_names):
        tree = ttk.Treeview(parent, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        return tree

    def create_buttons(self, parent, tree, data_type):
        frame = tk.Frame(parent)
        frame.pack(side='bottom', fill='x')
        btn_add = tk.Button(frame, text="添加", command=lambda: self.add_record(data_type))
        btn_edit = tk.Button(frame, text="编辑", command=lambda: self.edit_record(tree, data_type))
        btn_delete = tk.Button(frame, text="删除", command=lambda: self.delete_record(tree, data_type))
        btn_refresh = tk.Button(frame, text="刷新", command=lambda: self.refresh_tree(data_type))
        btn_add.pack(side='left', padx=5, pady=5)
        btn_edit.pack(side='left', padx=5, pady=5)
        btn_delete.pack(side='left', padx=5, pady=5)
        btn_refresh.pack(side='left', padx=5, pady=5)

    def auto_load_default_files(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        skill_path = os.path.join(cur_dir, "skill.txt")
        tech_path = os.path.join(cur_dir, "tech.txt")
        skilllv_path = os.path.join(cur_dir, "skilllv.txt")
        jobs_path = os.path.join(cur_dir, "jobs.txt")
        if os.path.exists(jobs_path):
            self.data_manager.load_jobs(jobs_path)
            self.job_file = jobs_path
            self.refresh_tree("jobs")
            self.update_job_combobox()
        if os.path.exists(skill_path):
            self.data_manager.load_skills(skill_path)
            self.skill_file = skill_path
            self.refresh_tree("skills")
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
        elif data_type == "techs":
            tree = self.tree_techs
            data = self.data_manager.techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            data = self.data_manager.skilllvs
            cols = self.col_names["skilllvs"]
            # 将 SkillLv 表中的职业代号列 (下标2) 转换为对应名称
            for i, row in enumerate(data):
                if len(row) > 2:
                    data[i][2] = self.data_manager.transform_jobid(row[2])
            # 同时，用技能代号去Tech中查找对应的技能名称，替换掉技能代号
            for i, row in enumerate(data):
                if len(row) > 1:
                    skill_id = row[1]
                    tech = next((t for t in self.data_manager.techs if len(t) > 6 and t[5] == skill_id and t[6] == "1"), None)
                    if tech:
                        data[i][1] = tech[0]
        elif data_type == "jobs":
            tree = self.tree_jobs
            data = self.data_manager.jobs
            cols = self.col_names["jobs"]
        elif data_type == "config":
            tree = self.tree_config
            data = self.data_manager.join_all()
            cols = self.col_names["config"]
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    def update_job_combobox(self):
        job_list = []
        for job in self.data_manager.jobs:
            if len(job) >= 2:
                job_list.append(f"{job[1]}: {job[0]}")
        self.job_combobox['values'] = job_list
        if job_list:
            self.job_combobox.current(0)

    def refresh_config_details(self):
        all_joined = self.data_manager.join_all()
        selected = self.job_combobox.get()
        if not selected:
            filtered = all_joined
        else:
            # 提取下拉框中“:”前面的职业编号
            parts = selected.split(":")
            if parts:
                job_id = parts[0].strip()
            else:
                job_id = ""
            # 利用第二列（职业编号）进行过滤
            filtered = [row for row in all_joined if row[1] == job_id]
            # 若过滤结果为空，则显示所有记录，便于调试
            if not filtered:
                filtered = all_joined
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
        new_record = [""] * len(cols)
        def callback(rec):
            data.append(rec)
            self.refresh_tree(data_type)
        RecordEditor(self, new_record, cols, callback)

    def edit_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("编辑", "请选择一行")
            return
        index = tree.index(selected[0])
        item = tree.item(selected[0])
        values = list(item['values'])
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

    def search_data(self, data_type, keyword):
        if data_type == "skills":
            full_data = self.data_manager.skills
            key_idx = self.search_keys["skills"]
            cols = self.col_names["skills"]
        elif data_type == "techs":
            full_data = self.data_manager.techs
            key_idx = self.search_keys["techs"]
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            full_data = self.data_manager.skilllvs
            key_idx = self.search_keys["skilllvs"]
            cols = self.col_names["skilllvs"]
        elif data_type == "jobs":
            full_data = self.data_manager.jobs
            key_idx = self.search_keys["jobs"]
            cols = self.col_names["jobs"]
        elif data_type == "config":
            full_data = self.data_manager.join_all()
            key_idx = self.search_keys["config"]
            cols = self.col_names["config"]
        else:
            return

        filtered = [row for row in full_data if len(row) > key_idx and keyword.lower() in row[key_idx].lower()]
        # 更新对应treeview
        if data_type == "skills":
            tree = self.tree_skills
        elif data_type == "techs":
            tree = self.tree_techs
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
        elif data_type == "jobs":
            tree = self.tree_jobs
        elif data_type == "config":
            tree = self.tree_config
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in filtered:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    # 预设每个表搜索关键字所在列
    search_keys = {
        "skills": 0,
        "techs": 0,
        "skilllvs": 1,
        "jobs": 0,
        "config": 0
    }

    def add_search_bar(self, parent, data_type):
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=5)
        tk.Label(frame, text="搜索:").pack(side='left', padx=5)
        entry = tk.Entry(frame)
        entry.pack(side='left', padx=5)
        btn_search = tk.Button(frame, text="搜索", command=lambda: self.search_data(data_type, entry.get()))
        btn_search.pack(side='left', padx=5)
        btn_reset = tk.Button(frame, text="重置", command=lambda: self.refresh_tree(data_type))
        btn_reset.pack(side='left', padx=5)
        return entry

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab_skills = ttk.Frame(self.notebook)
        self.tab_techs = ttk.Frame(self.notebook)
        self.tab_skilllvs = ttk.Frame(self.notebook)
        self.tab_jobs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text="Skills")
        self.notebook.add(self.tab_techs, text="Techs")
        self.notebook.add(self.tab_skilllvs, text="SkillLv")
        self.notebook.add(self.tab_jobs, text="Jobs")

        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="配置详情")

        # 为每个tab增加搜索栏
        self.add_search_bar(self.tab_skills, "skills")
        self.add_search_bar(self.tab_techs, "techs")
        self.add_search_bar(self.tab_skilllvs, "skilllvs")
        self.add_search_bar(self.tab_jobs, "jobs")
        self.add_search_bar(self.tab_config, "config")

        self.tree_skills = self.create_treeview(self.tab_skills, self.col_names["skills"])
        self.tree_techs = self.create_treeview(self.tab_techs, self.col_names["techs"])
        self.tree_skilllvs = self.create_treeview(self.tab_skilllvs, self.col_names["skilllvs"])
        self.tree_jobs = self.create_treeview(self.tab_jobs, self.col_names["jobs"])

        top_frame = tk.Frame(self.tab_config)
        top_frame.pack(fill='x', pady=5)
        tk.Label(top_frame, text="选择职业:").pack(side='left', padx=5)
        self.job_combobox = ttk.Combobox(top_frame, state="readonly", width=30)
        self.job_combobox.pack(side='left', padx=5)
        btn_query = tk.Button(top_frame, text="查询", command=self.refresh_config_details)
        btn_query.pack(side='left', padx=5)
        self.tree_config = self.create_treeview(self.tab_config, self.col_names["config"])

        self.create_buttons(self.tab_skills, self.tree_skills, "skills")
        self.create_buttons(self.tab_techs, self.tree_techs, "techs")
        self.create_buttons(self.tab_skilllvs, self.tree_skilllvs, "skilllvs")
        self.create_buttons(self.tab_jobs, self.tree_jobs, "jobs")

    def create_treeview(self, parent, col_names):
        tree = ttk.Treeview(parent, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        return tree

    def create_buttons(self, parent, tree, data_type):
        frame = tk.Frame(parent)
        frame.pack(side='bottom', fill='x')
        btn_add = tk.Button(frame, text="添加", command=lambda: self.add_record(data_type))
        btn_edit = tk.Button(frame, text="编辑", command=lambda: self.edit_record(tree, data_type))
        btn_delete = tk.Button(frame, text="删除", command=lambda: self.delete_record(tree, data_type))
        btn_refresh = tk.Button(frame, text="刷新", command=lambda: self.refresh_tree(data_type))
        btn_add.pack(side='left', padx=5, pady=5)
        btn_edit.pack(side='left', padx=5, pady=5)
        btn_delete.pack(side='left', padx=5, pady=5)
        btn_refresh.pack(side='left', padx=5, pady=5)

    def auto_load_default_files(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        skill_path = os.path.join(cur_dir, "skill.txt")
        tech_path = os.path.join(cur_dir, "tech.txt")
        skilllv_path = os.path.join(cur_dir, "skilllv.txt")
        jobs_path = os.path.join(cur_dir, "jobs.txt")
        if os.path.exists(jobs_path):
            self.data_manager.load_jobs(jobs_path)
            self.job_file = jobs_path
            self.refresh_tree("jobs")
            self.update_job_combobox()
        if os.path.exists(skill_path):
            self.data_manager.load_skills(skill_path)
            self.skill_file = skill_path
            self.refresh_tree("skills")
        if os.path.exists(tech_path):
            self.data_manager.load_techs(tech_path)
            self.tech_file = tech_path
            self.refresh_tree("techs")
        if os.path.exists(skilllv_path):
            self.data_manager.load_skilllvs(skilllv_path)
            self.skilllv_file = skilllv_path
            self.refresh_tree("skilllvs")
        else:
            print("jobs.txt not found")

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
        elif data_type == "techs":
            tree = self.tree_techs
            data = self.data_manager.techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            data = self.data_manager.skilllvs
            cols = self.col_names["skilllvs"]
            for i, row in enumerate(data):
                if len(row) > 2:
                    data[i][2] = self.data_manager.transform_jobid(row[2])
            for i, row in enumerate(data):
                if len(row) > 1:
                    skill_id = row[1]
                    tech = next((t for t in self.data_manager.techs if len(t) > 6 and t[5] == skill_id and t[6] == "1"), None)
                    if tech:
                        data[i][1] = tech[0]
        elif data_type == "jobs":
            tree = self.tree_jobs
            data = self.data_manager.jobs
            cols = self.col_names["jobs"]
        elif data_type == "config":
            tree = self.tree_config
            data = self.data_manager.join_all()
            cols = self.col_names["config"]
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    def update_job_combobox(self):
        job_list = []
        for job in self.data_manager.jobs:
            if len(job) >= 2:
                job_list.append(f"{job[1]}: {job[0]}")
        self.job_combobox['values'] = job_list
        if job_list:
            self.job_combobox.current(0)

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
        new_record = [""] * len(cols)
        def callback(rec):
            data.append(rec)
            self.refresh_tree(data_type)
        RecordEditor(self, new_record, cols, callback)

    def edit_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("编辑", "请选择一行")
            return
        index = tree.index(selected[0])
        item = tree.item(selected[0])
        values = list(item['values'])
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

    def search_data(self, data_type, keyword):
        if data_type == "skills":
            full_data = self.data_manager.skills
            key_idx = self.search_keys["skills"]
            cols = self.col_names["skills"]
        elif data_type == "techs":
            full_data = self.data_manager.techs
            key_idx = self.search_keys["techs"]
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            full_data = self.data_manager.skilllvs
            key_idx = self.search_keys["skilllvs"]
            cols = self.col_names["skilllvs"]
        elif data_type == "jobs":
            full_data = self.data_manager.jobs
            key_idx = self.search_keys["jobs"]
            cols = self.col_names["jobs"]
        elif data_type == "config":
            full_data = self.data_manager.join_all()
            key_idx = self.search_keys["config"]
            cols = self.col_names["config"]
        else:
            return

        filtered = [row for row in full_data if len(row) > key_idx and keyword.lower() in row[key_idx].lower()]
        if data_type == "skills":
            tree = self.tree_skills
        elif data_type == "techs":
            tree = self.tree_techs
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
        elif data_type == "jobs":
            tree = self.tree_jobs
        elif data_type == "config":
            tree = self.tree_config
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in filtered:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    search_keys = {
        "skills": 0,
        "techs": 0,
        "skilllvs": 1,
        "jobs": 0,
        "config": 0
    }

    def add_search_bar(self, parent, data_type):
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=5)
        tk.Label(frame, text="搜索:").pack(side='left', padx=5)
        entry = tk.Entry(frame)
        entry.pack(side='left', padx=5)
        btn_search = tk.Button(frame, text="搜索", command=lambda: self.search_data(data_type, entry.get()))
        btn_search.pack(side='left', padx=5)
        btn_reset = tk.Button(frame, text="重置", command=lambda: self.refresh_tree(data_type))
        btn_reset.pack(side='left', padx=5)
        return entry

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab_skills = ttk.Frame(self.notebook)
        self.tab_techs = ttk.Frame(self.notebook)
        self.tab_skilllvs = ttk.Frame(self.notebook)
        self.tab_jobs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text="Skills")
        self.notebook.add(self.tab_techs, text="Techs")
        self.notebook.add(self.tab_skilllvs, text="SkillLv")
        self.notebook.add(self.tab_jobs, text="Jobs")

        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="配置详情")

        # 为每个tab增加搜索栏
        self.add_search_bar(self.tab_skills, "skills")
        self.add_search_bar(self.tab_techs, "techs")
        self.add_search_bar(self.tab_skilllvs, "skilllvs")
        self.add_search_bar(self.tab_jobs, "jobs")
        self.add_search_bar(self.tab_config, "config")

        self.tree_skills = self.create_treeview(self.tab_skills, self.col_names["skills"])
        self.tree_techs = self.create_treeview(self.tab_techs, self.col_names["techs"])
        self.tree_skilllvs = self.create_treeview(self.tab_skilllvs, self.col_names["skilllvs"])
        self.tree_jobs = self.create_treeview(self.tab_jobs, self.col_names["jobs"])

        top_frame = tk.Frame(self.tab_config)
        top_frame.pack(fill='x', pady=5)
        tk.Label(top_frame, text="选择职业:").pack(side='left', padx=5)
        self.job_combobox = ttk.Combobox(top_frame, state="readonly", width=30)
        self.job_combobox.pack(side='left', padx=5)
        btn_query = tk.Button(top_frame, text="查询", command=self.refresh_config_details)
        btn_query.pack(side='left', padx=5)
        self.tree_config = self.create_treeview(self.tab_config, self.col_names["config"])

        self.create_buttons(self.tab_skills, self.tree_skills, "skills")
        self.create_buttons(self.tab_techs, self.tree_techs, "techs")
        self.create_buttons(self.tab_skilllvs, self.tree_skilllvs, "skilllvs")
        self.create_buttons(self.tab_jobs, self.tree_jobs, "jobs")

    def create_treeview(self, parent, col_names):
        tree = ttk.Treeview(parent, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        return tree

    def create_buttons(self, parent, tree, data_type):
        frame = tk.Frame(parent)
        frame.pack(side='bottom', fill='x')
        btn_add = tk.Button(frame, text="添加", command=lambda: self.add_record(data_type))
        btn_edit = tk.Button(frame, text="编辑", command=lambda: self.edit_record(tree, data_type))
        btn_delete = tk.Button(frame, text="删除", command=lambda: self.delete_record(tree, data_type))
        btn_refresh = tk.Button(frame, text="刷新", command=lambda: self.refresh_tree(data_type))
        btn_add.pack(side='left', padx=5, pady=5)
        btn_edit.pack(side='left', padx=5, pady=5)
        btn_delete.pack(side='left', padx=5, pady=5)
        btn_refresh.pack(side='left', padx=5, pady=5)

    def auto_load_default_files(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        skill_path = os.path.join(cur_dir, "skill.txt")
        tech_path = os.path.join(cur_dir, "tech.txt")
        skilllv_path = os.path.join(cur_dir, "skilllv.txt")
        jobs_path = os.path.join(cur_dir, "jobs.txt")
        if os.path.exists(jobs_path):
            self.data_manager.load_jobs(jobs_path)
            self.job_file = jobs_path
            self.refresh_tree("jobs")
            self.update_job_combobox()
        if os.path.exists(skill_path):
            self.data_manager.load_skills(skill_path)
            self.skill_file = skill_path
            self.refresh_tree("skills")
        if os.path.exists(tech_path):
            self.data_manager.load_techs(tech_path)
            self.tech_file = tech_path
            self.refresh_tree("techs")
        if os.path.exists(skilllv_path):
            self.data_manager.load_skilllvs(skilllv_path)
            self.skilllv_file = skilllv_path
            self.refresh_tree("skilllvs")
        else:
            print("jobs.txt not found")

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
        elif data_type == "techs":
            tree = self.tree_techs
            data = self.data_manager.techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            data = self.data_manager.skilllvs
            cols = self.col_names["skilllvs"]
            for i, row in enumerate(data):
                if len(row) > 2:
                    data[i][2] = self.data_manager.transform_jobid(row[2])
            for i, row in enumerate(data):
                if len(row) > 1:
                    skill_id = row[1]
                    tech = next((t for t in self.data_manager.techs if len(t) > 6 and t[5] == skill_id and t[6] == "1"), None)
                    if tech:
                        data[i][1] = tech[0]
        elif data_type == "jobs":
            tree = self.tree_jobs
            data = self.data_manager.jobs
            cols = self.col_names["jobs"]
        elif data_type == "config":
            tree = self.tree_config
            data = self.data_manager.join_all()
            cols = self.col_names["config"]
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    def update_job_combobox(self):
        job_list = []
        for job in self.data_manager.jobs:
            if len(job) >= 2:
                job_list.append(f"{job[1]}: {job[0]}")
        self.job_combobox['values'] = job_list
        if job_list:
            self.job_combobox.current(0)

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
        new_record = [""] * len(cols)
        def callback(rec):
            data.append(rec)
            self.refresh_tree(data_type)
        RecordEditor(self, new_record, cols, callback)

    def edit_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("编辑", "请选择一行")
            return
        index = tree.index(selected[0])
        item = tree.item(selected[0])
        values = list(item['values'])
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

    def search_data(self, data_type, keyword):
        if data_type == "skills":
            full_data = self.data_manager.skills
            key_idx = self.search_keys["skills"]
            cols = self.col_names["skills"]
        elif data_type == "techs":
            full_data = self.data_manager.techs
            key_idx = self.search_keys["techs"]
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            full_data = self.data_manager.skilllvs
            key_idx = self.search_keys["skilllvs"]
            cols = self.col_names["skilllvs"]
        elif data_type == "jobs":
            full_data = self.data_manager.jobs
            key_idx = self.search_keys["jobs"]
            cols = self.col_names["jobs"]
        elif data_type == "config":
            full_data = self.data_manager.join_all()
            key_idx = self.search_keys["config"]
            cols = self.col_names["config"]
        else:
            return

        filtered = [row for row in full_data if len(row) > key_idx and keyword.lower() in row[key_idx].lower()]
        if data_type == "skills":
            tree = self.tree_skills
        elif data_type == "techs":
            tree = self.tree_techs
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
        elif data_type == "jobs":
            tree = self.tree_jobs
        elif data_type == "config":
            tree = self.tree_config
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in filtered:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    search_keys = {
        "skills": 0,
        "techs": 0,
        "skilllvs": 1,
        "jobs": 0,
        "config": 0
    }

    def add_search_bar(self, parent, data_type):
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=5)
        tk.Label(frame, text="搜索:").pack(side='left', padx=5)
        entry = tk.Entry(frame)
        entry.pack(side='left', padx=5)
        btn_search = tk.Button(frame, text="搜索", command=lambda: self.search_data(data_type, entry.get()))
        btn_search.pack(side='left', padx=5)
        btn_reset = tk.Button(frame, text="重置", command=lambda: self.refresh_tree(data_type))
        btn_reset.pack(side='left', padx=5)
        return entry

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab_skills = ttk.Frame(self.notebook)
        self.tab_techs = ttk.Frame(self.notebook)
        self.tab_skilllvs = ttk.Frame(self.notebook)
        self.tab_jobs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text="Skills")
        self.notebook.add(self.tab_techs, text="Techs")
        self.notebook.add(self.tab_skilllvs, text="SkillLv")
        self.notebook.add(self.tab_jobs, text="Jobs")

        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="配置详情")

        # 为每个tab增加搜索栏
        self.add_search_bar(self.tab_skills, "skills")
        self.add_search_bar(self.tab_techs, "techs")
        self.add_search_bar(self.tab_skilllvs, "skilllvs")
        self.add_search_bar(self.tab_jobs, "jobs")
        self.add_search_bar(self.tab_config, "config")

        self.tree_skills = self.create_treeview(self.tab_skills, self.col_names["skills"])
        self.tree_techs = self.create_treeview(self.tab_techs, self.col_names["techs"])
        self.tree_skilllvs = self.create_treeview(self.tab_skilllvs, self.col_names["skilllvs"])
        self.tree_jobs = self.create_treeview(self.tab_jobs, self.col_names["jobs"])

        top_frame = tk.Frame(self.tab_config)
        top_frame.pack(fill='x', pady=5)
        tk.Label(top_frame, text="选择职业:").pack(side='left', padx=5)
        self.job_combobox = ttk.Combobox(top_frame, state="readonly", width=30)
        self.job_combobox.pack(side='left', padx=5)
        btn_query = tk.Button(top_frame, text="查询", command=self.refresh_config_details)
        btn_query.pack(side='left', padx=5)
        self.tree_config = self.create_treeview(self.tab_config, self.col_names["config"])

        self.create_buttons(self.tab_skills, self.tree_skills, "skills")
        self.create_buttons(self.tab_techs, self.tree_techs, "techs")
        self.create_buttons(self.tab_skilllvs, self.tree_skilllvs, "skilllvs")
        self.create_buttons(self.tab_jobs, self.tree_jobs, "jobs")

    def create_treeview(self, parent, col_names):
        tree = ttk.Treeview(parent, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        return tree

    def create_buttons(self, parent, tree, data_type):
        frame = tk.Frame(parent)
        frame.pack(side='bottom', fill='x')
        btn_add = tk.Button(frame, text="添加", command=lambda: self.add_record(data_type))
        btn_edit = tk.Button(frame, text="编辑", command=lambda: self.edit_record(tree, data_type))
        btn_delete = tk.Button(frame, text="删除", command=lambda: self.delete_record(tree, data_type))
        btn_refresh = tk.Button(frame, text="刷新", command=lambda: self.refresh_tree(data_type))
        btn_add.pack(side='left', padx=5, pady=5)
        btn_edit.pack(side='left', padx=5, pady=5)
        btn_delete.pack(side='left', padx=5, pady=5)
        btn_refresh.pack(side='left', padx=5, pady=5)

    def auto_load_default_files(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        skill_path = os.path.join(cur_dir, "skill.txt")
        tech_path = os.path.join(cur_dir, "tech.txt")
        skilllv_path = os.path.join(cur_dir, "skilllv.txt")
        jobs_path = os.path.join(cur_dir, "jobs.txt")
        if os.path.exists(jobs_path):
            self.data_manager.load_jobs(jobs_path)
            self.job_file = jobs_path
            self.refresh_tree("jobs")
            self.update_job_combobox()
        if os.path.exists(skill_path):
            self.data_manager.load_skills(skill_path)
            self.skill_file = skill_path
            self.refresh_tree("skills")
        if os.path.exists(tech_path):
            self.data_manager.load_techs(tech_path)
            self.tech_file = tech_path
            self.refresh_tree("techs")
        if os.path.exists(skilllv_path):
            self.data_manager.load_skilllvs(skilllv_path)
            self.skilllv_file = skilllv_path
            self.refresh_tree("skilllvs")
        else:
            print("jobs.txt not found")

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
        elif data_type == "techs":
            tree = self.tree_techs
            data = self.data_manager.techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            data = self.data_manager.skilllvs
            cols = self.col_names["skilllvs"]
            for i, row in enumerate(data):
                if len(row) > 2:
                    data[i][2] = self.data_manager.transform_jobid(row[2])
            for i, row in enumerate(data):
                if len(row) > 1:
                    skill_id = row[1]
                    tech = next((t for t in self.data_manager.techs if len(t) > 6 and t[5] == skill_id and t[6] == "1"), None)
                    if tech:
                        data[i][1] = tech[0]
        elif data_type == "jobs":
            tree = self.tree_jobs
            data = self.data_manager.jobs
            cols = self.col_names["jobs"]
        elif data_type == "config":
            tree = self.tree_config
            data = self.data_manager.join_all()
            cols = self.col_names["config"]
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    def update_job_combobox(self):
        job_list = []
        for job in self.data_manager.jobs:
            if len(job) >= 2:
                job_list.append(f"{job[1]}: {job[0]}")
        self.job_combobox['values'] = job_list
        if job_list:
            self.job_combobox.current(0)

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
        new_record = [""] * len(cols)
        def callback(rec):
            data.append(rec)
            self.refresh_tree(data_type)
        RecordEditor(self, new_record, cols, callback)

    def edit_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("编辑", "请选择一行")
            return
        index = tree.index(selected[0])
        item = tree.item(selected[0])
        values = list(item['values'])
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

    def search_data(self, data_type, keyword):
        if data_type == "skills":
            full_data = self.data_manager.skills
            key_idx = self.search_keys["skills"]
            cols = self.col_names["skills"]
        elif data_type == "techs":
            full_data = self.data_manager.techs
            key_idx = self.search_keys["techs"]
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            full_data = self.data_manager.skilllvs
            key_idx = self.search_keys["skilllvs"]
            cols = self.col_names["skilllvs"]
        elif data_type == "jobs":
            full_data = self.data_manager.jobs
            key_idx = self.search_keys["jobs"]
            cols = self.col_names["jobs"]
        elif data_type == "config":
            full_data = self.data_manager.join_all()
            key_idx = self.search_keys["config"]
            cols = self.col_names["config"]
        else:
            return

        filtered = [row for row in full_data if len(row) > key_idx and keyword.lower() in row[key_idx].lower()]
        if data_type == "skills":
            tree = self.tree_skills
        elif data_type == "techs":
            tree = self.tree_techs
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
        elif data_type == "jobs":
            tree = self.tree_jobs
        elif data_type == "config":
            tree = self.tree_config
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in filtered:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    search_keys = {
        "skills": 0,
        "techs": 0,
        "skilllvs": 1,
        "jobs": 0,
        "config": 0
    }

    def add_search_bar(self, parent, data_type):
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=5)
        tk.Label(frame, text="搜索:").pack(side='left', padx=5)
        entry = tk.Entry(frame)
        entry.pack(side='left', padx=5)
        btn_search = tk.Button(frame, text="搜索", command=lambda: self.search_data(data_type, entry.get()))
        btn_search.pack(side='left', padx=5)
        btn_reset = tk.Button(frame, text="重置", command=lambda: self.refresh_tree(data_type))
        btn_reset.pack(side='left', padx=5)
        return entry

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab_skills = ttk.Frame(self.notebook)
        self.tab_techs = ttk.Frame(self.notebook)
        self.tab_skilllvs = ttk.Frame(self.notebook)
        self.tab_jobs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text="Skills")
        self.notebook.add(self.tab_techs, text="Techs")
        self.notebook.add(self.tab_skilllvs, text="SkillLv")
        self.notebook.add(self.tab_jobs, text="Jobs")

        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="配置详情")

        self.add_search_bar(self.tab_skills, "skills")
        self.add_search_bar(self.tab_techs, "techs")
        self.add_search_bar(self.tab_skilllvs, "skilllvs")
        self.add_search_bar(self.tab_jobs, "jobs")
        self.add_search_bar(self.tab_config, "config")

        self.tree_skills = self.create_treeview(self.tab_skills, self.col_names["skills"])
        self.tree_techs = self.create_treeview(self.tab_techs, self.col_names["techs"])
        self.tree_skilllvs = self.create_treeview(self.tab_skilllvs, self.col_names["skilllvs"])
        self.tree_jobs = self.create_treeview(self.tab_jobs, self.col_names["jobs"])

        top_frame = tk.Frame(self.tab_config)
        top_frame.pack(fill='x', pady=5)
        tk.Label(top_frame, text="选择职业:").pack(side='left', padx=5)
        self.job_combobox = ttk.Combobox(top_frame, state="readonly", width=30)
        self.job_combobox.pack(side='left', padx=5)
        btn_query = tk.Button(top_frame, text="查询", command=self.refresh_config_details)
        btn_query.pack(side='left', padx=5)
        self.tree_config = self.create_treeview(self.tab_config, self.col_names["config"])

        self.create_buttons(self.tab_skills, self.tree_skills, "skills")
        self.create_buttons(self.tab_techs, self.tree_techs, "techs")
        self.create_buttons(self.tab_skilllvs, self.tree_skilllvs, "skilllvs")
        self.create_buttons(self.tab_jobs, self.tree_jobs, "jobs")

    def create_treeview(self, parent, col_names):
        tree = ttk.Treeview(parent, columns=col_names, show="headings")
        tree.pack(fill='both', expand=True, side='left')
        for col in col_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        return tree

    def create_buttons(self, parent, tree, data_type):
        frame = tk.Frame(parent)
        frame.pack(side='bottom', fill='x')
        btn_add = tk.Button(frame, text="添加", command=lambda: self.add_record(data_type))
        btn_edit = tk.Button(frame, text="编辑", command=lambda: self.edit_record(tree, data_type))
        btn_delete = tk.Button(frame, text="删除", command=lambda: self.delete_record(tree, data_type))
        btn_refresh = tk.Button(frame, text="刷新", command=lambda: self.refresh_tree(data_type))
        btn_add.pack(side='left', padx=5, pady=5)
        btn_edit.pack(side='left', padx=5, pady=5)
        btn_delete.pack(side='left', padx=5, pady=5)
        btn_refresh.pack(side='left', padx=5, pady=5)

    def auto_load_default_files(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        skill_path = os.path.join(cur_dir, "skill.txt")
        tech_path = os.path.join(cur_dir, "tech.txt")
        skilllv_path = os.path.join(cur_dir, "skilllv.txt")
        jobs_path = os.path.join(cur_dir, "jobs.txt")
        if os.path.exists(jobs_path):
            self.data_manager.load_jobs(jobs_path)
            self.job_file = jobs_path
            self.refresh_tree("jobs")
            self.update_job_combobox()
        if os.path.exists(skill_path):
            self.data_manager.load_skills(skill_path)
            self.skill_file = skill_path
            self.refresh_tree("skills")
        if os.path.exists(tech_path):
            self.data_manager.load_techs(tech_path)
            self.tech_file = tech_path
            self.refresh_tree("techs")
        if os.path.exists(skilllv_path):
            self.data_manager.load_skilllvs(skilllv_path)
            self.skilllv_file = skilllv_path
            self.refresh_tree("skilllvs")
        else:
            print("jobs.txt not found")

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
        elif data_type == "techs":
            tree = self.tree_techs
            data = self.data_manager.techs
            cols = self.col_names["techs"]
        elif data_type == "skilllvs":
            tree = self.tree_skilllvs
            data = self.data_manager.skilllvs
            cols = self.col_names["skilllvs"]
            for i, row in enumerate(data):
                if len(row) > 2:
                    data[i][2] = self.data_manager.transform_jobid(row[2])
            for i, row in enumerate(data):
                if len(row) > 1:
                    skill_id = row[1]
                    tech = next((t for t in self.data_manager.techs if len(t) > 6 and t[5] == skill_id and t[6] == "1"), None)
                    if tech:
                        data[i][1] = tech[0]
        elif data_type == "jobs":
            tree = self.tree_jobs
            data = self.data_manager.jobs
            cols = self.col_names["jobs"]
        elif data_type == "config":
            tree = self.tree_config
            data = self.data_manager.join_all()
            cols = self.col_names["config"]
        else:
            return

        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            row_extended = row + [""] * (len(cols) - len(row))
            tree.insert("", "end", values=row_extended)

    def update_job_combobox(self):
        job_list = []
        for job in self.data_manager.jobs:
            if len(job) >= 2:
                job_list.append(f"{job[1]}: {job[0]}")
        self.job_combobox['values'] = job_list
        if job_list:
            self.job_combobox.current(0)

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
        new_record = [""] * len(cols)
        def callback(rec):
            data.append(rec)
            self.refresh_tree(data_type)
        RecordEditor(self, new_record, cols, callback)

    def edit_record(self, tree, data_type):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("编辑", "请选择一行")
            return
        index = tree.index(selected[0])
        item = tree.item(selected[0])
        values = list(item['values'])
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
