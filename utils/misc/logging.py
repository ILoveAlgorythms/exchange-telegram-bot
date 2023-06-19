import logging

logging.basicConfig(
    filename='logs/error.log',
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.WARNING
)
