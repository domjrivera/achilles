from javalect import JavaJulietSuite


def collect_data(data_path):
    suite = JavaJulietSuite(data_path)
    suite.write_good()
    suite.write_bad()


collect_data("/Users/Strickolas/Downloads/Java")
