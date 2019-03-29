package javalang.brewtab.com;
class Test {

    final int PI = 2;
    private int val;

    static void main(String[] args) {
        int x = 23;
        if (x == 2) {
            System.out.println("Hello World!");
        }
        else {
            hi(2);
        }
    }



    public static void hi(int j) {
        System.out.println("HI");
        byte b = 0010;
    }

    private static int guy() {
        return 1;
    }

    public void bad() throws Throwable {
        String data;
        if (true) {
            data = ""; {
                Properties properties = new Properties();
                FileInputStream streamFileInput = null;
                try {
                    streamFileInput = new FileInputStream("../common/config.properties");
                    properties.load(streamFileInput);
                    data = properties.getProperty("data");
                }

                catch (IOException exceptIO) {
                    IO.logger.log(Level.WARNING, "Error with stream reading", exceptIO);
                }

                finally {
                    try {
                        if (streamFileInput != null) {
                            streamFileInput.close();
                        }

                    }

                    catch (IOException exceptIO) {
                        IO.logger.log(Level.WARNING, "Error closing FileInputStream", exceptIO);
                    }

                }

            }

        }

        else {
            data = null;
        }

        if (true) {
            int numberOfLoops;
            try {
                numberOfLoops = Integer.parseInt(data);
            }

            catch (NumberFormatException exceptNumberFormat) {
                IO.writeLine("Invalid response. Numeric input expected. Assuming 1.");
                numberOfLoops = 1;
            }

            for (int i=0; i < numberOfLoops; i++) {
                IO.writeLine("hello world");
            }

        }
    }
}