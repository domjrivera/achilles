package javalang.brewtab.com;

class Test {

    final int PI = 2;
    private int val;

    public static void main(String[] args) {
        int x = 23;
        if (x == 2) {
            System.out.println("Hello World!");
        } else {
            hi(2);
        }
    }

    private void goodB2G() throws Throwable {
        String data;
        data = "";
        {
            Connection connection = null;
            PreparedStatement preparedStatement = null;
            ResultSet resultSet = null;
            try {
                connection = IO.getDBConnection();
                preparedStatement = connection.prepareStatement("select name from users where id=0");
                resultSet = preparedStatement.executeQuery();
                data = resultSet.getString(1);
            } catch (SQLException exceptSql) {
                IO.logger.log(Level.WARNING, "Error with SQL statement", exceptSql);
            } finally {
                try {
                    if (resultSet != null) {
                        resultSet.close();
                    }

                } catch (SQLException exceptSql) {
                    IO.logger.log(Level.WARNING, "Error closing ResultSet", exceptSql);
                }

                try {
                    if (preparedStatement != null) {
                        preparedStatement.close();
                    }

                } catch (SQLException exceptSql) {
                    IO.logger.log(Level.WARNING, "Error closing PreparedStatement", exceptSql);
                }

                try {
                    if (connection != null) {
                        connection.close();
                    }

                } catch (SQLException exceptSql) {
                    IO.logger.log(Level.WARNING, "Error closing Connection", exceptSql);
                }

            }

        }

        String[] dataArray = new String[5];
        dataArray[2] = data;
        (new CWE89_SQL_Injection__database_prepareStatement_66b()).goodB2GSink(dataArray);
    }

    public void bad() throws Throwable {
        int count;
        count = Integer.MIN_VALUE;
        {
            Properties properties = new Properties();
            FileInputStream streamFileInput = null;
            try {
                streamFileInput = new FileInputStream("../common/config.properties");
                properties.load(streamFileInput);
                String stringNumber = properties.getProperty("data");
                if (stringNumber != null) // avoid NPD incidental warnings {
                    try {
                        count = Integer.parseInt(stringNumber.trim());
                    } catch (NumberFormatException exceptNumberFormat) {
                        IO.logger.log(Level.WARNING, "Number format exception parsing count from string", exceptNumberFormat);
                    }

            }

        }

            catch(IOException exceptIO){
            IO.logger.log(Level.WARNING, "Error with stream reading", exceptIO);
        }

            finally{
            try {
                if (streamFileInput != null) {
                    streamFileInput.close();
                }

            } catch (IOException exceptIO) {
                IO.logger.log(Level.WARNING, "Error closing FileInputStream", exceptIO);
            }

        }

    }

    ByteArrayOutputStream streamByteArrayOutput = null;
    ObjectOutput outputObject = null;
        try

    {
        streamByteArrayOutput = new ByteArrayOutputStream();
        outputObject = new ObjectOutputStream(streamByteArrayOutput);
        outputObject.writeObject(count);
        byte[] countSerialized = streamByteArrayOutput.toByteArray();
        (new CWE400_Resource_Exhaustion__PropertiesFile_for_loop_75b()).badSink(countSerialized);
    }

        catch(
    IOException exceptIO)

    {
        IO.logger.log(Level.WARNING, "IOException in serialization", exceptIO);
    }

        finally

    {
        try {
            if (outputObject != null) {
                outputObject.close();
            }

        } catch (IOException exceptIO) {
            IO.logger.log(Level.WARNING, "Error closing ObjectOutputStream", exceptIO);
        }

        try {
            if (streamByteArrayOutput != null) {
                streamByteArrayOutput.close();
            }

        } catch (IOException exceptIO) {
            IO.logger.log(Level.WARNING, "Error closing ByteArrayOutputStream", exceptIO);
        }

    }
}