import networkx as nx
from TuGraphClient import TuGraphClient
import json
import sys

# 1. 连接配置
HOST = "101.37.195.98:7070"   # 如果报错，改成 101.37.195.98:9090
USER = "admin"
PASSWORD = "!6BJ7BaD1de0p8Ije"

print("正在连接 TuGraph...")
try:
    client = TuGraphClient(HOST, USER, PASSWORD)
    client.call_cypher("MATCH (n) RETURN count(n) LIMIT 1")
    print("连接成功！")
except Exception as e:
    print(f"连接失败，报错：{e}")
    sys.exit()

# 2. 拉取边数据
print("正在拉取边数据...")
cypher_edges = "MATCH (a:developer)-[r:follows]->(b:developer) RETURN a.id AS src, b.id AS dst"
res_edges = client.call_cypher(cypher_edges)

# === 核心修复：自动兼容各种返回格式 ===
if isinstance(res_edges, str):
    try:
        res_edges = json.loads(res_edges)
    except:
        pass

edges_list = []
# 如果结果是字典列表 [{"src": 1, "dst": 2}, ...]
if isinstance(res_edges, list) and len(res_edges) > 0 and isinstance(res_edges[0], dict):
    for record in res_edges:
        edges_list.append((record.get("src"), record.get("dst")))
# 如果结果是二维列表/元组 [[1, 2], [3, 4], ...]
elif isinstance(res_edges, list) and len(res_edges) > 0 and isinstance(res_edges[0], (list, tuple)):
    for record in res_edges:
        edges_list.append((record[0], record[1]))
# 如果结果是包含 header 和 result 的大字典
elif isinstance(res_edges, dict) and "result" in res_edges:
    for record in res_edges["result"]:
         edges_list.append((record[0], record[1]))
# ===================================

if not edges_list:
    print("解析失败，返回的数据格式为：", type(res_edges), str(res_edges)[:200])
    sys.exit()

print(f"成功拉取 {len(edges_list)} 条边。")

# 3. 执行 PageRank 算法
print("\n" + "="*40)
print("开始执行 PageRank 算法...")

G = nx.DiGraph() # 有向图
G.add_edges_from(edges_list)
pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=100)

# 排序并打印前10名
sorted_pr = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:10]

print("✅ PageRank 计算完成！影响力排名前 10 的节点：")
for rank, (node_id, score) in enumerate(sorted_pr, 1):
    print(f"  第 {rank} 名 - 节点 ID: {node_id}, 得分: {score:.6f}")

print("="*40)
print("请截图以上结果。")
