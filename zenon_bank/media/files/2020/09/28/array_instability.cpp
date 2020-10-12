#include <iostream>
#include <algorithm>

using namespace std;

const int N = int(2e5) + 10;
int n, arr[N];

int main()
{

    cin >> n;
    for (int i = 0; i < n; ++i)
        cin >> arr[i];

    sort(arr, arr + n);

  
    cout << min(arr[n - 1] - arr[1], arr[n - 2] - arr[0]);
}