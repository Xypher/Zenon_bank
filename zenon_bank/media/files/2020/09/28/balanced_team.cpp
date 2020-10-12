#include <iostream> 
#include <algorithm>
#include <cmath>


using namespace std; 

const int N = int(2e5) + 10;
int n, seq[N]; 

int main(){
 

    cin >> n;
    for(int i = 0; i < n; ++i)
        cin >> seq[i];

    sort(seq, seq + n);

    int l = 0, r = 0;

    int res = -1;
    while(r < n){

        while(l + 1 <= r && seq[r] - seq[l] > 5)
            l++;

        res = max(r - l + 1,  res);
        r++;
    }

    cout << res;


  
 
}