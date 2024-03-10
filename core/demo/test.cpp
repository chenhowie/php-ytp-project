#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define pll pair<ll,ll>
#define pii pair<int,int>
#define fs first
#define sc second
#define tlll tuple<ll,ll,ll>



int main(int argc,char* argv[]){
	ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
	string s;
	if(argc>1)s = string(argv[1]);
	ofstream f1((s+".csv").c_str());
	ofstream f2((s+"_ans.csv").c_str());
	srand(time(NULL));
	for(int i = 0;i<5;i++)f1<<(i?",":"")<<"F"<<i;f1<<endl;
	f2<<"A0"<<endl;
	for(int i = 0;i<100000;i++){
		int arr[5];
		int s = 0;
		for(int j = 0;j<5;j++)s += (arr[j] = rand()%10)*pow(10,j),f1<<(j?",":"")<<arr[j];
		f1<<endl;
		f2<<(argc>2?1.0*s+rand()%10*0.1:1.0*s)<<endl;
	}
	return 0;
}
