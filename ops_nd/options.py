#coding=utf8

"""
every opt of used should bu define first


this options is based on tornado.options
"""

from tornado.options import define, parse_command_line,\
        parse_config_file, options

common_opts = [
        {
            "name": 'debug',
            "default": False,
            "help": 'if logged debug info',
            "type": bool,
        },
        {
            "name": 'verbose',
            "default": False,
            "help": 'if log detail',
            "type": bool,
        },
        {
            "name": 'config',
            "default": '/etc/nomad/ops_nd.conf',
            "help": 'path of config file',
            "type": str,
            "callback": lambda path: parse_config_file(path, final=False)
        },
        {
            "name": 'sql_connection',
            "default": '"mysql+pymysql://neutron:ok2dFyiyeKh8WIa7s9xYvHAZpcCmDrTb6giLCe4o@172.16.68.165:3306/neutron"',
            "help": 'The SQLAlchemy connection string used to connect to \
                    the database',
            "type": str,
        },
        {
            "name": 'db_driver',
            "default": 'ops_nd.db.api',
            "help": 'default db driver',
            "type": str,
        },
        {
            "name": 'lock_path',
            "default": '/var/lock',
            "help": 'path of config file',
            "type": str,
        },
        {
            "name": 'api_port',
            "default": 8915,
            "help": 'listen port of api',
            "type": int,
        },
        {
            "name": 'listen',
            "default": '127.0.0.1',
            "help": 'listen address',
            "type": str,
        },
        {
            "name": 'keystone_endpoint',
            # "default": 'http://172.16.68.106:35357/v2.0',
            "default": 'http://10.200.100.8:35357/v3',
            "help": 'the keystone endpoint url',
            "type": str,
        },
        {
            "name": 'username',
            "default": 'admin',
            "help": 'username of auth',
            "type": str,
        },
        {
            "name": 'password',
            "default": 'MCmRMoLslUW9UeHtDTOuoMc36TMbkHu8zqr9O70e',
            "help": 'password of auth',
            "type": str,
        },
        {
            "name": 'extra_opts',
            "default": '',
            "help": "all opts of app's",
            "type": str,
        },

        {
            "name": 'neutron_endpoint',
            # "default": 'http://172.16.68.102:9696/v2.0',
            "default": 'http://10.200.100.8:9696/v2.0',
            "help": 'the neutron endpoint url',
            "type": str,
        },

        {
            "name": 'tenant',
            "default": 'admin',
            "help": 'the neutron endpoint url',
            "type": str,
        },

        {
            "name": 'keystone_admin_endpoint',
            # "default": 'http://172.16.68.102:5000/v2.0',
            "default": 'http://10.200.100.8:5000/v2.0',
            "help": 'the keystone admin endpoint url',
            "type": str
        },

        {
            "name": 'overlay_ip',
            # "default": 'http://172.16.68.102:5000/v2.0',
            "default": '',
            "help": 'the sdn switch vtep endpoint url',
            "type": str,
        },

        {
            "name": 'cmdb_ep',
            # "default": 'http://172.16.68.102:5000/v2.0',
            "default": '',
            "help": 'cmdb end point',
            "type": str,
        },
        ]


def register_opt(opt, group=None):
    """Register an option schema
    opt = {
            "name": 'config',
            "default": 'ops_nd.conf',
            "help": 'path of config file',
            "tyle": str,
            "callback": lambda path: parse_config_file(path, final=False)
        }
    """
    if opt.get('name', ''):
        optname = opt.pop('name')
        if optname in options._options.keys():
            options._options.pop(optname)
        define(optname, **opt)


def register_opts(opts, group=None):
    """Register multiple option schemas at once."""
    for opt in opts:
        register_opt(opt, group)
    return options


def get_options(opts=None, group=None):
    if opts:
        register_opts(opts, group)
    options = register_opts(common_opts, 'common')
    if options.as_dict().get('extra_opts', ''):
        try:
            extra_opts = __import__(options.extra_opts)
            options = register_opts(extra_opts.config.opts, 'extra')
        except:
            print "get config error"
    parse_config_file(options.config, final=False)
    parse_command_line()
    return options

if __name__ == "__main__":
    print get_options().as_dict()
    options = get_options()
    print options.get('sql_connection', None)
