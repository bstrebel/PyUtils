import os, sys, logging, logging.config, pyutils
from pyutils import Options, LogAdapter, get_logger, log_level

def main():

    from ConfigParser import ConfigParser
    from argparse import ArgumentParser

    options = {
        'option': 'OPTION',
        'secrets': {'token': 'secret'},
        'loglevel': 'INFO'
    }

# region Command line arguments

    parser = ArgumentParser(description='PySnc Engine Rev. 0.1 (c) Bernd Strebel')
    parser.add_argument('-c', '--config', type=str, help='use alternate configuration file')

    parser.add_argument('-l', '--loglevel', type=str,
                        choices=['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL',
                                 'debug', 'info', 'warn', 'warning', 'error', 'critical'],
                        help='debug log level')

    args = parser.parse_args()
    opts = Options(options, args, config=True)

#    _logger = get_logger('root',log_level(opts.loglevel))
#    logger = LogAdapter(_logger, {'package': 'init'})
#    logger.info("Console logger initilized")

# endregion

# region (I) Basic configuration and logger settings from config file

    # if opts.config_file:
    #     if os.path.isfile(opts.config_file):
    #         logging.config.fileConfig(opts.config_file)
    #         config = ConfigParser(options)
    #         config.read(opts.config_file)
    #     else:
    #         logger.critical('Configuration file %s not found!' % (opts.config_file))
    #         exit(1)
    # else:
    #     logger.critical("Missing configuration file!")
    #     exit(1)
    #
    # _logger = logging.getLogger()
    # _logger.setLevel(log_level(opts.loglevel))
    #
    # logger = LogAdapter(_logger, {'package': 'main'})

# endregion

# region (II) Basic configuration and logger settings from config parser

    config = opts.config_parser
    logger = LogAdapter(opts.logger, {'package': 'main'})

# endregion

    logger.info('Default logger configured from %s' % (opts.config_file))
    print opts.option

    s = opts.get('string_option', False)
    t = opts['secrets']['token']
    pass
    #f = Options.get_bool_value(opt)

# region __Main__

if __name__ == '__main__':

    main()
    exit(0)

# endregion
