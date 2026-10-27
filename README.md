本实验选用的数据集是来自UCI机器学习仓库的GitHub MUSAE数据集（DOI: 10.24432/C5Z02B），该数据集由研究者于2019年6月通过GitHub公开API采集构建，旨在反映开发者之间的社交网络结构及属性特征。
在结构上，该网络包含37,700个节点（均为至少给10个仓库点过星标的开发者）和289,003条无向边（代表开发者之间的相互关注关系），每个节点还附带了基于开发者地理位置、星标仓库、雇主和邮箱地址提取的4,006维二进制指示符特征。
该数据集的核心功能是用于图机器学习中的二分类节点分类任务，即利用开发者的社交网络连接和特征向量，预测其职位属性属于Web开发方向还是机器学习方向，是评估图嵌入算法和节点分类模型的典型基准数据集。
<img width="1376" height="847" alt="image" src="https://github.com/user-attachments/assets/04c8766c-5e8c-4e61-bd2c-ff486ccda246" />
用PageRank算法输出影响力排名前 10 的开发者节点及其 PageRank 得分：
<img width="612" height="592" alt="image" src="https://github.com/user-attachments/assets/9d30531a-7db2-4c5b-9b4d-bfacf7555ba0" />
基于Node2Vec算法成功将图节点转化为64维嵌入向量，计算了分类准确率：
<img width="600" height="285" alt="image" src="https://github.com/user-attachments/assets/1a0b24af-a8db-481b-942c-baf260195eea" />
