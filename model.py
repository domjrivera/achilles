from javalect import JavaJulietSuite


def collect_data(data_path):
    suite = JavaJulietSuite(data_path)
    suite.write_good()
    suite.write_bad()


collect_data("/Volumes/CoreBlue/Programming/Projects/achilles/juliet_java_data/CWE15_External_Control_of_System_or_Configuration_Setting")