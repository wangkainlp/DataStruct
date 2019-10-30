#include<iostream>
#include<vector>

using namespace std;

#define MIN(a, b, c) (std::min(a, std::min(b, c)))


int edit_distance(const string& str1, const string& str2) {
    int s1_len = str1.size();
    int s2_len = str2.size();

    if (s1_len == 0) {
        return s2_len;
    }
    if (s2_len == 0) {
        return s1_len;
    }

    int m = s1_len + 1;
    int n = s2_len + 1;

    int matrix[m][n];
    matrix[0][0] = 0;

    for (int i = 1; i < m; ++i) {
        matrix[i][0] = matrix[i-1][0] + 1;
    }

    for (int i = 1; i < n; ++i) {
        matrix[0][i] = matrix[0][i-1] + 1;
    }

    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            int cost = str1[i - 1] == str2[j - 1] ? 0 : 1;
            matrix[i][j] = MIN(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + cost);
        }
    }

    int distance = matrix[m - 1][n - 1];

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
    return distance;
}

int main() {

    string s1 = "abc";
    string s2 = "aaaaaa";
    int dist = edit_distance(s1, s2);
    cout << dist << " " << 1 - 1.0 * dist / std::max(s1.size(), s2.size()) << endl;

    return 0;
}
