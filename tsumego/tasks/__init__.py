from django_rq import job

from .tsumego_result import TsumegoResultParser


@job
def parse_current_tsumego():
    parser = TsumegoResultParser('1L6neXQIj39wW_9pkTz2iWcJ0fEDQy8hdoUXPKPpD_Dc')
    parser.run_current()
