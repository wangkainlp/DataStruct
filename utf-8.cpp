#include <iostream>
#include <string>
#include <vector>
#include <cstring>
using namespace std;

void toBinary(uint32_t ch, int len = 8) {
    for (int i = len - 1; i >= 0; --i ) {
        printf("%d", (ch >> i) & 1);
        if (i % 8 == 0) {
            printf(" ");
        }
    }
    printf("\n");
}


void unicode_to_utf8(uint32_t ch, char* ss) {

    int len = strlen(ss);
    for (int i = 0; i < len; ++i) {
        ss[i] = '\0';
    }

    int size = 0;
    
    if (0x00000000 <= ch && ch <= 0x0000007F) {
        size = 1;
    } else if (0x00000080 <= ch && ch <= 0x000007FF) {
        size = 2;
    } else if (0x00000800 <= ch && ch <= 0x0000FFFF) {
        size = 3;
    } else if (0x00010000 <= ch && ch <= 0x001FFFFF) {
        size = 4;
    } else if (0x00200000 <= ch && ch <= 0x03FFFFFF) {
        size = 5;
    } else if (0x04000000 <= ch && ch <= 0x7FFFFFFF) {
        size = 6;
    }

    if (size == 1) {
        ss[0] = uint8_t(ch);
        ss[size] = '\0';
        return;
    }

    uint8_t prefix = uint8_t(0xFE << (8 - size - 1));
    uint8_t mask = uint8_t(0xFF << (8 - size - 1));
    uint8_t inner_mask = uint8_t(0xFF << 6);
    uint8_t inner_prefix = uint8_t(0xFE << 6);

    for (int i = 0; i < size; ++i) {
        if (i == 0) {
            ss[i] = prefix | (uint8_t(~mask) & (ch >> (6 * (size - i - 1))));
        } else {
            ss[i] = inner_prefix | (uint8_t(~inner_mask) & (ch >> (6 * (size - i - 1))));
        }
        toBinary(ss[i], 8);
    }
    ss[size] = '\0';
}

uint32_t utf8_to_unicode(char* ch_utf8) {
    int len = strlen(ch_utf8);
    for (int i = 0; i < len; ++i) {
        toBinary(ch_utf8[i]);
    }

    if (len == 1) {
        if (ch_utf8[0] & uint8_t(0x01 << 7)) {
            return 0x80000000;
        } else {
            return uint32_t(ch_utf8[0]);
        }
    }

    uint8_t prefix = uint8_t(0xFE << (8 - len - 1));
    uint8_t mask = uint8_t(0xFF << (8 - len - 1));
    toBinary(mask, 8);
    toBinary(prefix, 8);

    uint8_t inner_mask = uint8_t(0xFF << 6);
    uint8_t inner_prefix = uint8_t(0xFE << 6);
    toBinary(inner_mask, 8);
    toBinary(inner_prefix, 8);

    uint32_t ch_u_ = 0x00;
    for (int i = 0; i < len; ++i) {
        if (i == 0) {
            if ((ch_utf8[i] & mask) == prefix) {
                ch_u_ |= (ch_utf8[i] & uint8_t(~mask)) << (6 * (len - i - 1));
            } else {
                cout << "prefix" << endl;
                toBinary(prefix, 8);
                toBinary(ch_utf8[i] & mask, 8);
                return 0x80000000;
            }
        } else {
            if ((ch_utf8[i] & inner_mask) == inner_prefix) {
                ch_u_ |= (ch_utf8[i] & uint8_t(~inner_mask)) << (6 * (len - i - 1));
            } else {
                return 0x80000000;
            }
        }
        toBinary(ch_u_, 32);
    }
    cout << "end:" << endl;
    toBinary(ch_u_, 32);
    return ch_u_;
}

int get(const char* s, int pos, int len, string& str) {
    uint8_t prefix = uint8_t(0xFE << (8 - len - 1));
    uint8_t mask = uint8_t(0xFF << (8 - len - 1));
    uint8_t inner_mask = uint8_t(0xFF << 6);
    uint8_t inner_prefix = uint8_t(0xFE << 6);

    char tmp[len + 1];
    for (int i = 0; i < len; ++i) {
        if (i == 0) {
            if ((s[i + pos] & mask) == prefix) {
                tmp[i] = s[i + pos];
            } else {
                return 1;
            }
        } else {
            if ((s[i + pos] & inner_mask) == inner_prefix) {
                tmp[i] = s[i + pos];
            } else {
                return 1;
            }
        }
    }
    tmp[len] = 0x0;
    str = string(tmp);
    return 0;
}

int segment_utf8(const char* str, vector<string>& segs) {
    segs.clear();

    int len = strlen(str);
    int inner = 0;
    cout << str << ":" << len << endl;

    for (int i = 0; i < len; ) {
        toBinary(str[i]);
        int _size = -1;
        for (int j = 0; j <= 6; ++j) {
            uint8_t prefix = uint8_t(0xFE << (8 - j - 1));
            uint8_t mask = uint8_t(0xFF << (8 - j - 1));
            if ((str[i] & mask) == prefix) {
                _size = j;
                break;
            }
        }
        cout << i << ":" <<  _size << endl;
        toBinary(str[i]);

        if (_size == 0) {
            char t[2] = {str[i], 0};
            segs.push_back(string(t));
            ++i;
        } else if (_size == 1) {
            return _size;
        } else if (_size >= 2) {
            string tmp;
            int ret = get(str, i, _size, tmp);
            if (ret == 0) {
                segs.push_back(tmp);
                i += _size;
            } else {
                return _size;
            }
            // cout << ret << "->" << tmp.c_str() << endl;
        } else {
            return _size;
        }
        // cout << i << endl;
    }
    return 0;
}

int main() {

    char s[] = "你";
    cout << s << endl;
    cout << strlen(s) << endl;

    uint32_t ch_u = utf8_to_unicode(s);
    cout << ch_u << endl;

    char ss[10];

    unicode_to_utf8(ch_u, ss);
    cout << ss << endl;

    cout << "-----------------------" << endl;
    char sent[] = "注: Unicode编码目前规划的总空间是17个平面，。";

    vector<string> segs;
    segment_utf8(sent, segs);

    for (int i = 0; i < segs.size(); ++i) {
        cout << segs[i] << endl;
    }

    return 0;
}
