import networkx as nx
from TuGraphClient import TuGraphClient
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import json
import sys
import random
import warnings

warnings.filterwarnings("ignore")

# 1. 连接
HOST = "101.37.195.98:7070"
USER = "admin"
PASSWORD = "!6BJ7BaD1de0p8Ije"
client = TuGraphClient(HOST, USER, PASSWORD)
print("连接成功，正在拉取数据...")

# 2. 拉取数据
res_edges = client.call_cypher("MATCH (a:developer)-[r:follows]->(b:developer) RETURN a.id AS src, b.id AS dst")
res_nodes = client.call_cypher("MATCH (n:developer) RETURN n.id AS id, n.ml_target AS target")

# 处理返回值
if isinstance(res_edges, str): res_edges = json.loads(res_edges)
if isinstance(res_edges, dict) and "result" in res_edges: res_edges = res_edges["result"]
if isinstance(res_nodes, str): res_nodes = json.loads(res_nodes)
if isinstance(res_nodes, dict) and "result" in res_nodes: res_nodes = res_nodes["result"]

# 稳健解析边
edges_list = []
for r in res_edges:
    if isinstance(r, dict): 
        edges_list.append((r.get("src"), r.get("dst")))
    elif isinstance(r, (list, tuple)): 
        edges_list.append((r[0], r[1]))

# 稳健解析节点标签（修复了上一版的语法错误）
node_targets = {}
for r in res_nodes:
    if isinstance(r, dict): 
        node_targets[r.get("id")] = r.get("target")
    elif isinstance(r, (list, tuple)): 
        node_targets[r[0]] = r[1]

print(f"成功拉取 {len(edges_list)} 条边，{len(node_targets)} 个节点。")

# 3. 构建图
G = nx.Graph()
G.add_edges_from(edges_list)

# 4. 极速版节点嵌入 (手动游走 + Gensim)
print("\n开始极速版 Node2Vec 节点嵌入...")
walks = []
nodes = list(G.nodes())
for _ in range(5): 
    random.shuffle(nodes)
    for start_node in nodes[:5000]:  # 取前5000个节点
        walk = [str(start_node)]
        curr = start_node
        for _ in range(5): # walk_length = 5
            neighbors = list(G.neighbors(curr))
            if not neighbors: break
            curr = random.choice(neighbors)
            walk.append(str(curr))
        walks.append(walk)

print("游走序列生成完毕，开始训练...")
model = Word2Vec(sentences=walks, vector_size=64, window=5, min_count=1, workers=4)

sample_node = list(G.nodes())[0]
print(f"\n✅ 训练完成！节点 {sample_node} 的 64 维嵌入向量（前5维）: \n{model.wv[str(sample_node)][:5]}")

# 5. 分类验证
print("\n正在验证分类准确率...")
X, y = [], []
for nid in G.nodes():
    if str(nid) in model.wv and nid in node_targets:
        X.append(model.wv[str(nid)])
        y.append(node_targets[nid])

if len(X) > 0:
    X_train, X_test, y_train, y_test = train_test_split(np.array(X), np.array(y), test_size=0.3, random_state=42)
    clf = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"✅ 分类验证完成！基于节点嵌入的分类准确率: {acc:.4f}")
else:
    print("❌ 提取特征失败，无法进行分类验证。")

print("\n" + "="*40)
print("请截图！")
