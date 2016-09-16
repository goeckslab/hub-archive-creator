# Internal dependencies
import Datatype

class Psl(Datatype):
    def __init__(self, input_psl_path, data_psl):
        super(Psl, self).__init__()

        self.track = None

        self.input_psl_path = input_psl_path
        self.name_psl = data_psl["name"]
        self.priority = data_psl["order_index"]

        # psl to BigPsl processing
        trackName = "".join((self.name_psl, ".bb"))

        # Get the bed12+12 with pslToBigPsl

        # Get the binary indexed bigPsl with bedToBigBed

        # self.createTrack()

        print("- BigPsl %s created" % self.name_psl)