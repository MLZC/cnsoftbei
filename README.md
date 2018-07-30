### 程序说明

#### 环境说明

- **系统环境**:Ubuntu 1604 x64
- **Python环境**:Anaconda3-5.1.0


#### 程序结构说明

- 程序包括原始数据处理,查找两个部分，对应的源代码为**data_deal.py,search.py**,相应的运行程序为**run_deal.py,run_search.py**.

- **run.py**为执行两个步骤。

#### 程序运行说明：

##### 数据处理

1. 解压程序
2. 进入程序根目录
3. 将原始数据base_vector.fea放入./data路径下(确保名称无误)
4. 进入程序根目录,在终端中执行以下命令
    >python run_deal.py
5. 程序运行结束,将输出10个文件到./data下
6. 执行查询过程

##### 数据查询

1. 解压程序
2. 进入程序根目录
3. 将评测所用数据verify_vector.fea放入./data路径下(替换,确保名称无误)
4. 进入程序根目录,在终端中执行以下命令
    >python run_search.py
5. 程序运行结束,结果保存在outcomes_index.txt
6. 程序各个阶段耗时,直接输出到终端

以上步骤可以合并：
- 在./data路径中删除.pkl文件，将base_vector.fea和base_vector.fea放入./data下
- 进入程序根目录,在终端中执行以下命令
    >python run.py