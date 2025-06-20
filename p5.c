#include <stdio.h>
#define maxn 500
#define inf 1000000000000000000
typedef long long ll;

ll p[maxn], a[maxn];
ll sum(int i, int j) {
	return p[j-1] - ((i>=1)?p[i-1]:0);
}

ll dp[maxn][maxn];
ll split[maxn][maxn];

ll min(ll a, ll b) {
	if (a > b) return b;
	return a;
}

ll f(int i, int j) {
	if (dp[i][j] != inf) return dp[i][j];
	if (j-i == 1) {
		return dp[i][j] = 0;
	}
	ll ret = inf;
	ll bestK = i+1;
	for (int k = i+1; k < j; k++) {
		ll val = f(i, k)+f(k, j)+sum(i, j);
		if (val < ret) {
			ret = val;
			bestK = k;
		}
	}
	dp[i][j] = ret;
	split[i][j] = bestK;
	return ret;
}

 void print(int i, int j) {
	if (j - i <= 1) return;
	int k = split[i][j];
	print(i, k);
	print(k, j);
	printf("Merging %d and %d\n", sum(i, k), sum(k, j));
} 

int main() {
	int n;
	scanf("%d", &n);
	for (int i = 0; i < n; i++) scanf("%d", a+i);
	p[0] = a[0];
	for (int i = 1; i < n; i++) p[i] = p[i-1] + a[i];
	for (int i = 0; i < n; i++) {
		for (int j = i; j <= n; j++) dp[i][j] = inf;
	}
	printf("%lld\n", f(0, n));
	print(0, n);
}

