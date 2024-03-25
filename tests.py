import Modules
import cProfile
import logging

def test_format():
    pass

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        filename='app.log', 
        filemode='a', 
        format='%(asctime)s [%(process)d %(name)s] %(levelname)s: %(message)s'
    )
    logging.info("starting profiling")
    pr = cProfile.Profile()
    pr.enable()

    # tests here

    pr.disable()
    # pr.print_stats()
    pr.dump_stats('prof_data.prof')
    logging.info("end profiling")