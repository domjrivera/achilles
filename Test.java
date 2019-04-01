package javalang.brewtab.com;

class Test {

    final int PI = 2;
    private int val;

    public static void main(String[] args) {
        int x = 23;
        if (x == 2) {
            x = x + good(2, 3);
        } else {
            bad();
        }
    }

    private void good() throws Throwable {
        byte data;
        if (privateFive == 4) {
            data = 3;
        }
        if (privateFive == 5) {
            if (data < 0) {
                byte result = (byte) (data * 2);
                IO.writeLine("result: " + result);
            }
        }
    }

    public void bad(HttpServletRequest request, HttpServletResponse response) throws Throwable {
        String data;
        data = "";
        {
            StringTokenizer tokenizer = new StringTokenizer(request.getQueryString(), "&");
            while (tokenizer.hasMoreTokens()) {
                String token = tokenizer.nextToken();
                if (token.startsWith("id=")) {
                    data = token.substring(3);
                    break;
                }
            }
        }
        (new CWE81_XSS_Error_Message__Servlet_getQueryString_Servlet_53b()).badSink(data, request, response);
    }
}
