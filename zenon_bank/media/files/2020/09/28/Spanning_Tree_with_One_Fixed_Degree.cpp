#include <iostream> 
#include <utility>
#include <algorithm>
#include <vector>
#include <map>
#include <set> 
#include <queue>

using namespace std; 

const int N = int(2e5) + 10; 

int n, m, k, degree, comps;
vector<int> graph[N];
bool visited[N], vis[N];
vector<pair<int, int> > sol;
int comp[N];

void traverse(int prnt, int id){

    visited[prnt] = true;
    comp[prnt] = id;

    for(auto child: graph[prnt]){

        if(!visited[child])
            traverse(child, id);
    }
}


int dfs(){

    int cnt = 0;
    visited[1] = true;
    for(auto child: graph[1]){

        if(!visited[child]){

            cnt++;
            traverse(child, cnt);
        }

    }

    return cnt;

}




void bfs(){


    map<int, vector<int>> mp;

    for(auto child: graph[1])
        mp[comp[child]].push_back(child);

    
    set<int> st;
    for(auto m: mp)
        st.insert(m.second.back());


    int gv = 0;
    while(gv < graph[1].size() && st.size() < k){

        st.insert(graph[1][gv]);
        gv++;
    }

    graph[1].clear();
    for(auto x: st)
        graph[1].push_back(x);

    queue<int> que;
    que.push(1);
    vis[1] = 1; 


    int prnt;
    while(!que.empty()){

        prnt = que.front(); que.pop();

        for(auto child: graph[prnt]){

            if(!vis[child]){

                vis[child] = true;
                que.push(child);
                sol.push_back({prnt, child});
            }
        }
    }
}



int main(){
 

    ios_base::sync_with_stdio(0); cin.tie(0);

    degree = 0;

    cin >> n >> m >> k;
    
    int u, v;
    while(m--){

        cin >> u >> v;
        degree += (u == 1);
        degree += (v == 1);

        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    if(degree < k){

        cout << "NO" << '\n';
        return 0;
    }


    comps = dfs();

    if(k < comps){

        cout << "NO" << '\n';
        return 0;
    }

    bfs();

    cout << "YES\n";

    for(auto e: sol)
        cout << e.first << ' ' << e.second << '\n';
 
}