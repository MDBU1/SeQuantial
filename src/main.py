from sequantial.logfile import func_setup_logger
from attributes.commands import func_return_commands
from attributes.parameters import Order, ClassParameterRandomizer

import logging
import datetime as dt

def func_run():
    clss_cmds = func_return_commands()
    func_setup_logger("/home/phe.gov.uk/michael.d.brown/Projects/misc/sequantial", clss_cmds)
    test = Order(
        id = 1,
        item_name = "test",
        quantity = 3,
        created_at = dt.datetime.now(),
        delivered_to = dt.datetime.now() + dt.timedelta(days=1)
    )
    print(test)

    print(clss_cmds.int_no_synthetic)
    test = ClassParameterRandomizer(
        str_ref_dna = "abx",
        int_ref_dna_length = 3,
        int_number_synthetic = clss_cmds.int_no_synthetic,
    )
    logging.info(f'randomizer running input parameters:\n{test}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    func_run()

