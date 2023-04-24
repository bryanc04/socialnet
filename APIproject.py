import instaloader
import os.path
import networkx as nx
import json
from collections import deque
import concurrent.futures
import time
import requests
import matplotlib.pyplot as plt
import random


USERNAME = 'bryan.chung.0504'

L = instaloader.Instaloader()
L.load_session_from_file("bryan.chung.0504")

data_file = {}

#Load data from data.json file
with open("data.json") as file:
    data = json.load(file)
    data_file = data


#Function to get a target_user's followers and return it as a list.
def getFollowers(target_user, data):
    if target_user in data:
        return data[target_user]

    user = instaloader.Profile.from_username(L.context, target_user)
    followers = [follower.username for follower in user.get_followers()]

    data[target_user] = followers
    return followers

#Use dfs, but doesnt work
# def makeGraph(username, max_depth):
#     DisplayG = nx.DiGraph()
#     AllG = nx.DiGraph()
#     visited = set()
    
#     def dfs(current_user, depth):
#         if depth > max_depth:
#             return

#         print(f"Processing user: {current_user}, Depth: {depth}")

#         if current_user not in visited:
#             visited.add(current_user)

#             if current_user in data_file.keys():
#                 print("Already visited previously. ")
#                 followers = data[current_user]
#                 time.sleep(5)
#             else:
#                 print("Loading...")
#                 followers_future = executor.submit(getFollowers, current_user, data)
#                 followers = followers_future.result()
#                 data_file[current_user] = followers

#             numFollowers = len(followers)
#             print(f"Number of followers: {numFollowers}")

#             if numFollowers > 2000:
#                 for follower in followers:
#                     AllG.add_edge(current_user, follower)
#                     dfs(follower, depth + 1)
#             else:
#                 for follower in followers:
#                     AllG.add_edge(current_user, follower)
#                     DisplayG.add_edge(current_user, follower)
#                     dfs(follower, depth + 1)

#     try:
#         with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#             dfs(username, 0)

#     except KeyboardInterrupt:
#         with open("data.json", 'w') as outfile:
#             json.dump(data_file, outfile)
#         pos = nx.random_layout(DisplayG) 
#         plt.figure(figsize=(20,20))
#         nx.draw(DisplayG, pos, with_labels=True, node_color='skyblue', node_size=0.2, edge_color='red', font_size=0.1, arrowsize=0.0000000000001)
#         plt.savefig("graph.png", dpi=1200)

#         # Show the graph using Matplotlib
#         plt.show()

#     # Save updated data to JSON file
#     with open(data_file, 'w') as outfile:
#         json.dump(data_file, outfile)

#     return DisplayG

#Working BFS Solution
def makeGraph(username, max_depth):

    #DisplayG to display in matplotlib (for simplication purposes), AllG with everyone
    DisplayG = nx.DiGraph()
    AllG = nx.DiGraph()

    queue = deque([(username, 0)]) #[username,depth]
    visited = set()
    cnt = 0

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while queue:
                current_user, depth = queue.popleft()

                if depth > max_depth:
                    break

                print(f"Processing user: {current_user}, Depth: {depth}")

                if current_user not in visited:
                    visited.add(current_user)
                    if current_user in data.keys(): #Check if followrs > 0 because in previous runs followers might have been recorded as 0 after error
                        print(f"Getting user: {current_user}, Depth: {depth}")
                        followers = data_file[current_user]
                    else:
                        # with open("data.json", 'w') as outfile:
                        #         json.dump(data_file, outfile)
                        # pos = nx.random_layout(DisplayG) 
                        # plt.figure(figsize=(20,20))
                        # nx.draw(DisplayG, pos, with_labels=True, node_color='skyblue', node_size=0.2, edge_color='red', font_size=0.1, arrowsize=0.00000000000000000001)
                        # plt.savefig("graph.png", dpi=1200)
                        return AllG
                        # time.sleep(5)
                        print(f"Processing user: {current_user}, Depth: {depth}")

                        followers_future = executor.submit(getFollowers, current_user, data)
                        followers = followers_future.result()
                        cnt += 1
                        if cnt % 10 == 0:
                            print("dumped")#Dump file every 10 iteration to save
                            with open("data.json", 'w') as outfile:
                                json.dump(data_file, outfile)
                    numFollowers = len(followers)
                    print(f"Number of followers: {numFollowers}")

                    if numFollowers < 2000:
                        for follower in followers:
                            AllG.add_edge(current_user, follower)
                            queue.append((follower, depth + 1))
                    else:
                        for follower in followers:
                            AllG.add_edge(current_user, follower)
                            DisplayG.add_edge(current_user, follower)
                            queue.append((follower, depth + 1))
                    if cnt == 50:#My trick that may or may not work to bypass instagram security(apparently doesnt work)
                        print("sleeping...")
                        time.sleep(300)
                        print("awake...")
                    

    except KeyboardInterrupt:
        with open("data.json", 'w') as outfile:
            json.dump(data_file, outfile)
        pos = nx.random_layout(DisplayG) 
        plt.figure(figsize=(10,10))
        nx.draw(DisplayG, pos, with_labels=True, node_color='skyblue', node_size=0.2, edge_color='red', font_size=0.1, arrowsize=0.0000000000001)
        plt.savefig("graph.png", dpi=1200)

# Show the graph using Matplotlib
        plt.show()

    # Save updated data to JSON file
    with open("data.json", 'w') as outfile:
        json.dump(data_file, outfile)

    return AllG

#BFS shortest path algorithm, couldnt check if it works but theoretically should work?
def bfsShort(graph, start, end):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            return path

        for adj in graph.neighbors(node):
            if adj not in visited:
                new_path = path + [adj]
                queue.append(new_path)
                visited.add(adj)

#Random surfer implementation that doesnt work for some reason, it has many problems now. 
def randomSurferPagerank(G, alpha=0.85, num_iter=10000, tolerance=1e-6):
    print("Pageranking...")
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    ranks = {node: 1/num_nodes for node in nodes}
    old_ranks = ranks.copy()

    current_node = random.choice(nodes)
    for i in range(num_iter):
        neighbors = list(G.neighbors(current_node))

        if not neighbors or random.random() < 1 - alpha:
            next_node = random.choice(nodes)
            teleport = True
        else:
            next_node = random.choice(neighbors)
            teleport = False

        transferred_rank = ranks[current_node] * (1 - alpha) if teleport else ranks[current_node] * alpha / len(neighbors)

        if teleport:
            for node in nodes:
                ranks[node] += transferred_rank / num_nodes
        else:
            for node in neighbors:
                ranks[node] += transferred_rank

        ranks[current_node] -= transferred_rank
        current_node = next_node

        if i % num_nodes == 0:
            max_diff = max(abs(ranks[node] - old_ranks[node]) for node in nodes)#very lazt way
            if max_diff < tolerance:
                break
            old_ranks = ranks.copy()

    return ranks






if __name__ == "__main__":
    graph = makeGraph(USERNAME, 2)
    print(f'Nodes: {len(graph.nodes())}, Edges: {len(graph.edges())}')
    # print(bfsShort(graph, "bryan.chung.0504", "nilannandish"))
    pageranks = randomSurferPagerank(graph)
    # pageranks = nx.pagerank(graph)
    sorted_usernames = sorted(pageranks.keys(), key=lambda x: pageranks[x], reverse=True)
    print("Sorted Usernames:", sorted_usernames[:3])



# from argparse import ArgumentParser
# from glob import glob
# from os.path import expanduser
# from platform import system
# from sqlite3 import OperationalError, connect

# try:
#     from instaloader import ConnectionException, Instaloader
# except ModuleNotFoundError:
#     raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


# def get_cookiefile():
#     default_cookiefile = {
#         "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
#         "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
#     }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
#     cookiefiles = glob(expanduser(default_cookiefile))
#     if not cookiefiles:
#         raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
#     return cookiefiles[0]


# def import_session(cookiefile, sessionfile):
#     print("Using cookies from {}.".format(cookiefile))
#     conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
#     try:
#         cookie_data = conn.execute(
#             "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
#         )
#     except OperationalError:
#         cookie_data = conn.execute(
#             "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
#         )
#     instaloader = Instaloader(max_connection_attempts=1)
#     instaloader.context._session.cookies.update(cookie_data)
#     username = instaloader.test_login()
#     if not username:
#         raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
#     print("Imported session cookie for {}.".format(username))
#     instaloader.context.username = username
#     instaloader.save_session_to_file(sessionfile)


# if __name__ == "__main__":
#     p = ArgumentParser()
#     p.add_argument("-c", "--cookiefile")
#     p.add_argument("-f", "--sessionfile")
#     args = p.parse_args()
#     try:
#         import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
#     except (ConnectionException, OperationalError) as e:
#         raise SystemExit("Cookie import failed: {}".format(e))