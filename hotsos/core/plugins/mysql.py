import glob
import os

from hotsos.core.config import HotSOSConfig
from hotsos.core.host_helpers import (
    APTPackageHelper,
    PebbleHelper,
    SystemdHelper,
)
from hotsos.core import (
    host_helpers,
    plugintools,
)

SVC_VALID_SUFFIX = r'[0-9a-zA-Z-_]*'
MYSQL_SVC_EXPRS = [rf'mysql{SVC_VALID_SUFFIX}']
CORE_APT = ['mysql']


class MySQLChecks(plugintools.PluginPartBase):
    """ MySQL checks. """
    plugin_name = 'mysql'
    plugin_root_index = 3

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.apt = APTPackageHelper(core_pkgs=CORE_APT)
        self.pebble = PebbleHelper(service_exprs=MYSQL_SVC_EXPRS)
        self.systemd = SystemdHelper(service_exprs=MYSQL_SVC_EXPRS)

    @property
    def plugin_runnable(self):
        return self.apt.core is not None


class MySQLConfig(host_helpers.IniConfigBase):
    """ MySQL config interface. """
    def __init__(self, *args, **kwargs):
        path = os.path.join(HotSOSConfig.data_root,
                            'etc/mysql/mysql.conf.d/mysqld.cnf')
        super().__init__(*args, path=path, **kwargs)


class MySQLRouterConfig(host_helpers.IniConfigBase):
    """ MySQL Router config interface. """
    def __init__(self, *args, **kwargs):
        path = os.path.join(HotSOSConfig.data_root,
                            'var/lib/mysql/*mysql-router/mysqlrouter.conf')
        # expect only one
        for f in glob.glob(path):
            path = f

        super().__init__(*args, path=path, **kwargs)
