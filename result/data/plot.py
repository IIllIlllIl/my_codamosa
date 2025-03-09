import math

import matplotlib.pyplot as plt
import numpy as np


# Energy data of a basic unit
class DataUnit:
    def __init__(self, input_vector):
        self.cpu_energy = float(input_vector[0])
        self.ram_energy = float(input_vector[1])
        self.gpu_energy = float(input_vector[2])
        self.total_energy = self.cpu_energy + self.ram_energy + self.gpu_energy
        self.run_time = float(input_vector[3])

    def display(self):
        print(str(self.cpu_energy) + " & " + str(self.ram_energy) + " & "
              + str(self.gpu_energy) + " & " + str(self.total_energy))


# Energy data of a module under test
class TestModule:
    def __init__(self, name, cov):
        self.module_name = name
        self.coverage = float(cov)
        self.mosa = DataUnit([0, 0, 0, 0])
        self.llm_15b = DataUnit([0, 0, 0, 0])
        self.llm_3b = DataUnit([0, 0, 0, 0])
        self.llm_7b = DataUnit([0, 0, 0, 0])

    def display(self):
        print(self.module_name)
        print(self.coverage)
        self.mosa.display()
        self.llm_15b.display()
        self.llm_3b.display()
        self.llm_7b.display()


# Energy data of all test generation process
class Data:
    def __init__(self):
        self.module_list = []

    def read_data(self, path):
        file = open(path, 'r')
        temp_module = TestModule("module", 0)
        try:
            line_cnt = 0
            while True:
                line = file.readline()
                if line:
                    line_data = line[:-1].split(",")
                    # print(line_data)
                    # module name, coverage
                    if line_cnt == 0:
                        temp_module.module_name = line_data[0]
                        temp_module.coverage = line_data[1]
                    # mosa
                    elif line_cnt == 1:
                        temp_module.mosa = DataUnit(line_data)
                    # llm 1.5b
                    elif line_cnt == 2:
                        temp_module.llm_15b = DataUnit(line_data)
                    # llm 3b
                    elif line_cnt == 3:
                        temp_module.llm_3b = DataUnit(line_data)
                    # llm 7b
                    elif line_cnt == 4:
                        temp_module.llm_7b = DataUnit(line_data)
                        self.module_list.append(temp_module)
                        temp_module = TestModule("module", 0)
                    else:
                        pass
                    line_cnt += 1
                    line_cnt %= 6
                else:
                    break
        finally:
            pass

    def display(self):
        for m in self.module_list:
            m.display()

    def extract(self, option):
        if option == 0:
            return self.extract_cpu()
        elif option == 1:
            return self.extract_ram()
        elif option == 2:
            return self.extract_gpu()
        else:
            return self.extract_total()

    def extract_cpu(self):
        mosa = []
        llm_15b = []
        llm_3b = []
        llm_7b = []
        for m in self.module_list:
            mosa.append(m.mosa.cpu_energy)
            llm_15b.append(m.llm_15b.cpu_energy)
            llm_3b.append(m.llm_3b.cpu_energy)
            llm_7b.append(m.llm_7b.cpu_energy)
        return [np.array(mosa), np.array(llm_15b),
                np.array(llm_3b), np.array(llm_7b)]

    def extract_ram(self):
        mosa = []
        llm_15b = []
        llm_3b = []
        llm_7b = []
        for m in self.module_list:
            mosa.append(m.mosa.ram_energy)
            llm_15b.append(m.llm_15b.ram_energy)
            llm_3b.append(m.llm_3b.ram_energy)
            llm_7b.append(m.llm_7b.ram_energy)
        return [np.array(mosa), np.array(llm_15b),
                np.array(llm_3b), np.array(llm_7b)]

    def extract_gpu(self):
        mosa = []
        llm_15b = []
        llm_3b = []
        llm_7b = []
        for m in self.module_list:
            mosa.append(m.mosa.gpu_energy)
            llm_15b.append(m.llm_15b.gpu_energy)
            llm_3b.append(m.llm_3b.gpu_energy)
            llm_7b.append(m.llm_7b.gpu_energy)
        return [np.array(mosa), np.array(llm_15b),
                np.array(llm_3b), np.array(llm_7b)]

    def extract_total(self):
        mosa = []
        llm_15b = []
        llm_3b = []
        llm_7b = []
        for m in self.module_list:
            mosa.append(m.mosa.total_energy)
            llm_15b.append(m.llm_15b.total_energy)
            llm_3b.append(m.llm_3b.total_energy)
            llm_7b.append(m.llm_7b.total_energy)
        return [np.array(mosa), np.array(llm_15b),
                np.array(llm_3b), np.array(llm_7b)]


# Run time of a test case
class TimeUnit:
    def __init__(self, input_vector):
        self.coverage = float(input_vector[0])
        self.time_list = []
        for t in input_vector[1:]:
            self.time_list.append(float(t))

    def get_total_time(self):
        return sum(self.time_list)

    def get_total_time_per_coverage(self):
        if self.coverage == 0:
            return math.inf
        else:
            return sum(self.time_list) / self.coverage

    def get_average_time(self):
        return sum(self.time_list) / len(self.time_list)

    def get_related_time(self, threshold=1e6):
        related_list = []
        for t in self.time_list:
            if t < threshold:
                related_list.append(t)
        return related_list

    def display(self):
        time_temp = ""
        for t in self.time_list:
            time_temp += str(t) + ", "
        if len(time_temp) > 2:
            time_temp = time_temp[:-2]
        print(str(self.coverage) + " & " + time_temp)


# Run time of a module under test
class TimeModule:
    def __init__(self, path, name):
        self.dir = path
        self.name = name
        self.mosa = TimeUnit([1, 0])
        self.llm_15b = TimeUnit([1, 0])
        self.llm_3b = TimeUnit([1, 0])
        self.llm_7b = TimeUnit([1, 0])

    def display(self):
        print(self.dir + ", " + self.name)
        self.mosa.display()
        self.llm_15b.display()
        self.llm_3b.display()
        self.llm_7b.display()

    # total time per coverage
    def get_time(self):
        mosa_time = self.mosa.get_total_time_per_coverage()
        llm_15b_time = self.llm_15b.get_total_time_per_coverage()
        llm_3b_time = self.llm_3b.get_total_time_per_coverage()
        llm_7b_time = self.llm_7b.get_total_time_per_coverage()
        return [mosa_time, llm_15b_time, llm_3b_time, llm_7b_time]

    def get_average_time(self):
        mosa_time = self.mosa.get_average_time()
        llm_15b_time = self.llm_15b.get_average_time()
        llm_3b_time = self.llm_3b.get_average_time()
        llm_7b_time = self.llm_7b.get_average_time()
        return [mosa_time, llm_15b_time, llm_3b_time, llm_7b_time]

    def get_normalized_time(self):
        mosa_time = self.mosa.get_total_time_per_coverage()
        llm_15b_time = self.llm_15b.get_total_time_per_coverage()
        llm_3b_time = self.llm_3b.get_total_time_per_coverage()
        llm_7b_time = self.llm_7b.get_total_time_per_coverage()
        if mosa_time == 0:
            return [1, math.inf, math.inf, math.inf]
        else:
            return [1, llm_15b_time / mosa_time,
                    llm_3b_time / mosa_time, llm_7b_time / mosa_time]


# Run time of all test cases
class Time:
    def __init__(self):
        self.time_list = []

    def read_data(self, path):
        file = open(path, 'r')
        temp_module = TimeModule("dir", "name")
        try:
            line_cnt = 0
            while True:
                line = file.readline()
                if line:
                    line_data = line[:-1].split(",")
                    # print(line_data)
                    # module name, coverage
                    if line_cnt == 0:
                        temp_module.dir = line_data[0]
                        temp_module.name = line_data[1]
                    # mosa
                    elif line_cnt == 1:
                        temp_module.mosa = TimeUnit(line_data)
                    # llm 1.5b
                    elif line_cnt == 2:
                        temp_module.llm_15b = TimeUnit(line_data)
                    # llm 3b
                    elif line_cnt == 3:
                        temp_module.llm_3b = TimeUnit(line_data)
                    # llm 7b
                    elif line_cnt == 4:
                        temp_module.llm_7b = TimeUnit(line_data)
                        self.time_list.append(temp_module)
                        temp_module = TimeModule("dir", "name")
                    else:
                        pass
                    line_cnt += 1
                    line_cnt %= 6
                else:
                    break
        finally:
            pass

    def display(self):
        for t in self.time_list:
            t.display()

    def get_total_time(self):
        mosa_list = []
        llm_15b_list = []
        llm_3b_list = []
        llm_7b_list = []
        for t in self.time_list:
            time_temp = t.get_time()
            mosa_list.append(time_temp[0])
            llm_15b_list.append(time_temp[1])
            llm_3b_list.append(time_temp[2])
            llm_7b_list.append(time_temp[3])
        return [np.array(mosa_list), np.array(llm_15b_list),
                np.array(llm_3b_list), np.array(llm_7b_list)]

    def get_normalized_time(self):
        mosa_list = []
        llm_15b_list = []
        llm_3b_list = []
        llm_7b_list = []
        for t in self.time_list:
            time_temp = t.get_normalized_time()
            mosa_list.append(time_temp[0])
            llm_15b_list.append(time_temp[1])
            llm_3b_list.append(time_temp[2])
            llm_7b_list.append(time_temp[3])
        return [np.array(mosa_list), np.array(llm_15b_list),
                np.array(llm_3b_list), np.array(llm_7b_list)]

    def get_case_time(self):
        mosa_list = []
        llm_15b_list = []
        llm_3b_list = []
        llm_7b_list = []
        for t in self.time_list:
            mosa_list += t.mosa.time_list
            llm_15b_list += t.llm_15b.time_list
            llm_3b_list += t.llm_3b.time_list
            llm_7b_list += t.llm_7b.time_list
        return [np.array(mosa_list), np.array(llm_15b_list),
                np.array(llm_3b_list), np.array(llm_7b_list)]

    def get_average_time(self):
        mosa_list = []
        llm_15b_list = []
        llm_3b_list = []
        llm_7b_list = []
        for t in self.time_list:
            time_temp = t.get_average_time()
            mosa_list.append(time_temp[0])
            llm_15b_list.append(time_temp[1])
            llm_3b_list.append(time_temp[2])
            llm_7b_list.append(time_temp[3])
        return [np.array(mosa_list), np.array(llm_15b_list),
                np.array(llm_3b_list), np.array(llm_7b_list)]

    def get_related_case_time(self, threshold=1e6):
        mosa_list = []
        llm_15b_list = []
        llm_3b_list = []
        llm_7b_list = []
        for t in self.time_list:
            mosa_list += t.mosa.get_related_time(threshold)
            llm_15b_list += t.llm_15b.get_related_time(threshold)
            llm_3b_list += t.llm_3b.get_related_time(threshold)
            llm_7b_list += t.llm_7b.get_related_time(threshold)
        return [np.array(mosa_list), np.array(llm_15b_list),
                np.array(llm_3b_list), np.array(llm_7b_list)]


# Draw figure
class DataPlot:
    def __init__(self, data_list, title, labels):
        self.data = data_list
        self.y_label = labels
        self.title = title
        self.labels = ["Mosa", "DeepSeek-R1-Distill-Qwen-1.5B", "stablelm-3b-4e1t", "Mistral-7B-Instruct-v0.3-GPTQ"]

    def draw(self):
        plt.figure(figsize=(14, 8))  # 设置图像大小
        plt.boxplot(
            self.data,
            labels=self.labels,  # 设置分组标签
            vert=True,  # 垂直方向（False为水平）
            patch_artist=True,  # 填充箱体颜色
            showmeans=True,  # 显示均值线
            meanline=True  # 均值以线而非点显示
        )

        plt.title(self.title)  # 标题
        plt.xlabel("Algorithm")  # X轴标签
        plt.ylabel(self.y_label)  # Y轴标签
        plt.grid(linestyle="--", alpha=0.4)  # 网格线
        plt.show()


# Run all tests
class AnalysisRunner:
    def __init__(self, path1="all/rq1.txt", path2="all/rq2.txt", path3="all/rq3.txt"):
        self.time_data = Time()
        self.case_time = Time()
        self.energy_data = Data()
        self.energy_data.read_data(path1)
        self.time_data.read_data(path2)
        self.case_time.read_data(path3)

    def display_energy(self):
        self.energy_data.display()

    def display_time(self):
        self.time_data.display()

    # rq1 Package energy consumption of test generation
    def rq1_cpu(self, lang="zh"):
        if lang == "en":
            plot = DataPlot(self.energy_data.extract(0),
                            "Package energy consumption of test generation", "Package energy consumption")
        else:
            plot = DataPlot(self.energy_data.extract(0), "测试用例生成的包能耗", "包能耗")
        plot.draw()

    # rq1 RAM energy consumption of test generation
    def rq1_ram(self, lang="en"):
        if lang == "en":
            plot = DataPlot(self.energy_data.extract(1),
                            "RAM energy consumption of test generation", "RAM energy consumption")
        else:
            plot = DataPlot(self.energy_data.extract(1), "测试用例生成的主存能耗", "主存能耗")
        plot.draw()

    # rq1 GPU energy consumption of test generation
    def rq1_gpu(self, lang="en"):
        if lang == "en":
            plot = DataPlot(self.energy_data.extract(2),
                            "GPU energy consumption of test generation", "GPU energy consumption")
        else:
            plot = DataPlot(self.energy_data.extract(2), "测试用例生成的主存能耗", "主存能耗")
        plot.draw()

    # rq1 Total energy consumption of test generation
    def rq1_total(self, lang="en"):
        if lang == "en":
            plot = DataPlot(self.energy_data.extract(3),
                            "Total energy consumption of test generation", "Total energy consumption")
        else:
            plot = DataPlot(self.energy_data.extract(3), "测试用例生成的显卡能耗", "显卡能耗")
        plot.draw()

    # rq2 Total run time per coverage
    def rq2_total(self, lang="en"):
        if lang == "en":
            plot = DataPlot(self.time_data.get_normalized_time(), "Total run time per coverage", "Run time")
        else:
            plot = DataPlot(self.time_data.get_normalized_time(), "单位覆盖率下的测试用例运行时间", "运行时间")
        plot.draw()

    # rq2 Run time of each test cases
    def rq2_cases(self, lang="en", threshold=350000):
        if lang == "en":
            plot = DataPlot(self.time_data.get_related_case_time(threshold), "Run time of each test cases", "Run time")
        else:
            plot = DataPlot(self.time_data.get_related_case_time(threshold), "单个测试用例运行时间", "运行时间")
        plot.draw()

    def rq3_total_pearson(self, op):
        energy = self.energy_data.extract(op)
        time = self.case_time.get_total_time()
        cor = []
        for i in range(4):
            if op == 2 and i == 0:
                cor.append(-3)
                continue
            eng = energy[i]
            tim = time[i]
            if len(eng) != len(tim):
                cor.append(-2)
                continue
            else:
                corr_matrix = np.corrcoef(eng, tim)
                cor.append(round(corr_matrix[0, 1], 3))
        return cor

    def rq3_case_pearson(self, op):
        energy = self.energy_data.extract(op)
        time = self.case_time.get_average_time()
        cor = []
        for i in range(4):
            if op == 2 and i == 0:
                cor.append(-3)
                continue
            eng = energy[i]
            tim = time[i]
            if len(eng) != len(tim):
                cor.append(-2)
                continue
            else:
                corr_matrix = np.corrcoef(eng, tim)
                cor.append(round(corr_matrix[0, 1], 3))
        return cor

    # rq3 correlation between generation energy and total cases energy per coverage
    def rq3_total_table(self):
        print(" - & Mosa & DeepSeek-R1-Distill-Qwen-1.5B & stablelm-3b-4e1t & Mistral-7B-Instruct-v0.3-GPTQ")
        label = ["pkg", "ram", "gpu", "total"]
        for i in range(4):
            output = label[i]
            for cor in self.rq3_total_pearson(i):
                if cor < -1:
                    output += " &  -"
                else:
                    output += " & " + str(cor)
            print(output)

    # rq3 correlation between generation energy and average cases energy
    def rq3_average_table(self):
        print(" - & Mosa & DeepSeek-R1-Distill-Qwen-1.5B & stablelm-3b-4e1t & Mistral-7B-Instruct-v0.3-GPTQ")
        label = ["pkg", "ram", "gpu", "total"]
        for i in range(4):
            output = label[i]
            for cor in self.rq3_case_pearson(i):
                if cor < -1:
                    output += " &  -"
                else:
                    output += " & " + str(cor)
            print(output)

    def run_all(self, lang="en", threshold=350000):
        self.rq1_cpu(lang)
        self.rq1_ram(lang)
        self.rq1_gpu(lang)
        self.rq1_total(lang)
        self.rq2_total(lang)
        self.rq2_cases(lang, threshold)
        self.rq3_total_table()
        self.rq3_average_table()


# choose dir
options = ["all", "origin", "mutation"]
index = 0

# create AnalysisRunner
paths = []
for i in range(3):
    paths.append(options[index] + "/rq" + str(i + 1) + ".txt")
ar = AnalysisRunner(paths[0], paths[1], paths[2])

# output result
ar.run_all()

