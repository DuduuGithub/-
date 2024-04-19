#include <iostream>
#include <list>
#include<map>
#include<algorithm>
#include<iterator>
using namespace std;
typedef map<int, list<int>> id_map;

int main() {
	int n;
	cin >> n;
	id_map map;
	list<id_map> lst;
	while (n--) {
		string op;
		cin >> op;
		if (op == "new") {
			int newId;
			cin >> newId;
			map.insert(make_pair(newId, list<int>()));
		}
		else if (op == "add") {
			int id, n;
			cin >> id >> n;
			id_map::iterator it = map.find(id);
			it->second.push_back(n);
		}
		else if (op == "merge") {
			int id1, id2;
			cin >> id1 >> id2;
			id_map::iterator it1 = map.find(id1);
			id_map::iterator it2 = map.find(id2);
			if (id1 != id2) it1->second.merge(it2->second);
		}
		else if (op == "unique") {
			int id;
			cin >> id;
			id_map::iterator it = map.find(id);
			it->second.sort();
			it->second.unique();
		}
		else if (op == "out") {
			int id;
			cin >> id;
			id_map::iterator it = map.find(id);
			it->second.sort();
			ostream_iterator<int> oit(cout, " ");
			copy(it->second.begin(), it->second.end(), oit);
			cout << endl;
		}
	}
}