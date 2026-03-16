class Solution {
public:
    int calculate(string s) {
        stack<int> st;
        int len=s.size();
        if(len==0) return 0;
        long long operand=0,res=0,sign=1; // sign 1=positive and -1=negative
        for(int i=0;i<len;i++) {
            if(isdigit(s[i])) {
                operand=operand*10+(s[i]-'0');
            } else if(s[i]=='+') {
                res+=sign*operand;
                sign=1;
                operand=0;
            } else if(s[i]=='-') {
                res+=sign*operand;
                sign=-1;
                operand=0;
            } else if(s[i]=='(') {
                st.push(res);
                st.push(sign);
                // reset sign and res
                sign=1;
                res=0;
            } else if(s[i]==')') {
                res+=sign*operand;
                res*=st.top();
                st.pop(); 
                res+=st.top();
                st.pop();
                operand=0;
            }
        }
        return res+(sign*operand);
    }
};