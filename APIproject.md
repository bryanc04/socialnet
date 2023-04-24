---
marp: true
theme: gaia
class: invert

---
 <style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

<br></br><br></br>

# Social Media Network 

Bryan Chung

---
# 1. Objective
- To model one's instagram followings/followers up to a certain depth as a directed graph and later represent it as an image
-  To extensively figure out the extent of one's connections. For example, over how many connections do I "know" Elon Musk (although he does not have instagram)? 
- To determine who is actually popular (this is fun)

---

# 2. Limitations
- Practically impossible to reach beyond the first two "depths," as the it would take exponential time
- No Instagram's official API support
- Lack of my knowledge in graph theory

---

# 3. APIs and Data Structures
- InstaLoader API: Resorted to this unofficial API on GitHub for retreiving followers.
- Sessions and Cookies: As Instagram would always block me when I try to log in through the unofficial API, I decided to use firefox (which I know how to obtain session files and cookies from thru Python) and then "steal" cookies to access my information using the firefox cookies. 
*This was perhaps the most difficult part of the project, but because it is irrelevant I will not discuss much about the actual algorithm.

---
- JSON: Used to save a dictionary contianing user followers as a local file. Useful because reduces wasted operations. 
- Graph: Used to model the Instagram network

---

# 3.1 What is a Graph?



![width:650px](graph.webp)

---

# 4. Algorithms
- DFS/BFS: Two very simple and easy graph traversal algorithms. For some reason DFS would keep getting me blocked, so had to resort to BFS for both implementations (which I will discuss later).
- Pagerank: A really fun and surprisingly simple (at least on the surface level) algorithm used by Google's search engine to rank pages. 
- Dijkstra's: In this case, it is simply BFS as there are no weights to the graph. Still wanted to mention it, as, if the edges were weighted, BFS would not find the shortest path, so we must have used dijkstra's.

---

# 4.1 Depth First Search and Breadth First Search

![width:800px height:400px](dfsvsbfs.jpeg)

---

# 4.2 Pagerank

---

# 5. Code Implementation
```
import instaloader
import os.path
import networkx as nx
import json
from collections import deque
import concurrent.futures
import time
import pathlib
import chardet
import requests
import matplotlib.pyplot as plt
```

...Too long, so just go to tiny.cc/BryanGithub


---

# 6. Outcomes

*Note: I will not demo the code because it simply takes too long to re-retrieve all the followers, and there is no point simply reading off the json file. I also don't want to get banned on instagram again--they have the worst tech support known to humanity. So, just see pictures. 

---

