from sst.actions import *
from dateutil.relativedelta import relativedelta

go_to('http://github.com')
assert_title_contains('GitHub')
