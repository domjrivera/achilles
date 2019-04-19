# ================[Hyperparameters]=================
TEST_SIZE = 0.1
MAX_WORDS = 1000
MAX_LEN = 150
EPOCHS = 10
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.2
MIN_DELTA = 0.0001
DROPOUT_RATE = 0.5
LOSS_FUNCT = 'binary_crossentropy'
ACTIVATION_FUNCT = 'relu'

# =================[Achilles Info]==================
__version__ = "Beta 0.2.0"
version_info = "\x1b[33mProject Achilles ....................... " \
               + __version__ + "\n" \
                               " The Towson University Software Engineering Department\n" \
                               " Nicholas Saccente | View more at github.com/strickolas\x1b[m"