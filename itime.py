#!/usr/bin/env python

import sys, time, operator, datetime

""""
    $ pip2 install pytz tzlocal
"""

try:
    import pytz
    timezones = pytz.all_timezones
except:
    print("ERROR: `pytz` package not exists!")
    sys.exit(0)

try:
    import tzlocal
    default_timezone = tzlocal.get_localzone().zone
except:
    print("WARN: `tzlocal` package not exists! ")
    default_timezone = "Asia/Shanghai"


class Datetime:
    _datetime = None
    def __init__(self, *args, **kwargs):
        if "_datetime" in kwargs and isinstance(kwargs["_datetime"], datetime.datetime):
            if isinstance(kwargs["_datetime"].tzinfo, datetime.tzinfo):
                self._datetime = kwargs["_datetime"]
            else:
                raise ValueError("tzinfo error.")
        elif len(args) > 0 and isinstance(args[0], datetime.datetime):
            if isinstance(args[0].tzinfo, datetime.tzinfo):
                self._datetime = args[0]
            else:
                raise ValueError("tzinfo error.")
        else:
            _datetime = datetime.datetime(*args)
            if not isinstance(_datetime.tzinfo, datetime.tzinfo):
                if "timezone" in kwargs and kwargs["timezone"] in timezones:
                    timezone = kwargs["timezone"]
                else:
                    timezone = default_timezone
                tz = pytz.timezone(timezone)
                _datetime = tz.localize(_datetime)
            self._datetime = _datetime

    @classmethod
    def now(cls, timezone=None, *args, **kwargs):
        return cls.from_timestamp(time.time(), timezone=timezone)

    def tzinfo(self):
        return self._datetime.tzinfo
    
    def utcoffset(self):
        return self._datetime.utcoffset().total_seconds()

    @classmethod
    def from_datetime(cls, _datetime, timezone=None, *args, **kwargs):
        assert( isinstance(_datetime, datetime.datetime) )
        if not isinstance(_datetime.tzinfo, datetime.tzinfo):
            if timezone not in timezones:
                timezone = default_timezone
            tz = pytz.timezone(timezone)
            _datetime = tz.localize(_datetime)
        return Datetime(_datetime=_datetime)

    def to_datetime(self):
        return self._datetime

    @classmethod
    def from_timestamp(cls, timestamp, timezone=None, *args, **kwargs):
        if timezone not in timezones:
            timezone = default_timezone
        tz = pytz.timezone(timezone)
        _datetime = datetime.datetime.fromtimestamp(timestamp, tz)
        return Datetime(_datetime=_datetime)

    def to_timestamp(self):
        return float(self.to_string("%s.%f"))
    
    def to_utc_timestamp(self):
        return self.to_timestamp() + self.utcoffset()

    @classmethod
    def from_timestruct(cls, time_struct, timezone=None):
        # time_struct = time.localtime()
        # time_tuple  = (time_struct.tm_year, time_struct.tm_mon, time_struct.tm_mday, 
        #     time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec, 
        #     time_struct.tm_wday, time_struct.tm_yday, time_struct.tm_isdst)
        return cls.from_timestamp(time.mktime(time_struct), timezone=timezone)

    def to_timestruct(self):
        return self._datetime.timetuple()

    def to_isoformat(self):
        return self._datetime.isoformat()

    @classmethod
    def from_string(cls, fmt, date_str, timezone=None):
        d = datetime.datetime.strptime(fmt, date_str)
        return cls.from_datetime(d, timezone=timezone)

    def to_string(self, *args, **kwargs):
        if len(args) > 0:
            return self._datetime.strftime(args[0])
        else:
            return self.to_isoformat()

    def __lt__(self, other):
        return operator.lt(self.to_timestamp(), other.to_timestamp())
    def __le__(self, other):
        return operator.le(self.to_timestamp(), other.to_timestamp())
    def __eq__(self, other):
        return operator.eq(self.to_timestamp(), other.to_timestamp())
    def __ne__(self, other):
        return operator.ne(self.to_timestamp(), other.to_timestamp())
    def __ge__(self, other):
        return operator.ge(self.to_timestamp(), other.to_timestamp())
    def __gt__(self, other):
        return operator.gt(self.to_timestamp(), other.to_timestamp())

    def __add__(self, other):
        return operator.add(self.to_timestamp(), other.to_timestamp())
    def __sub__(self, other):
        # "%.15f" % float_num
        return operator.sub(self.to_timestamp(), other.to_timestamp())
    def __mul__(self, other):
        return operator.mul(self.to_timestamp(), other.to_timestamp())
    def __floordiv__(self, other):
        return operator.floordiv(self.to_timestamp(), other.to_timestamp())
    def __div__(self, other):
        return operator.div(self.to_timestamp(), other.to_timestamp())
    def __truediv__(self, other):
        return operator.truediv(self.to_timestamp(), other.to_timestamp())
    def __mod__(self, other):
        return operator.mod(self.to_timestamp(), other.to_timestamp())
    def __divmod___(self, other):
        return divmod(self.to_timestamp(), other.to_timestamp())
    def __pow__(self, other):
        return operator.pow(self.to_timestamp(), other.to_timestamp())
    def __and__(self, other):
        return operator.and_(self.to_timestamp(), other.to_timestamp())
    def __or__(self, other):
        return operator.or_(self.to_timestamp(), other.to_timestamp())

    def __str__(self):
        return self.to_string()
    def __repr__(self):
        return "<Datetime datetime=%s sec=%f>" % (self.to_string(), self.to_timestamp())

class Duration:
    btime  = None
    def __init__(self, btime=None, *args, **kwargs):
        if isinstance(btime, Datetime):
            self.btime = btime
        else:
            self.btime = Datetime.now()

    def elapsed(self, *args, **kwargs):
        etime = Datetime.now()
        return etime - self.btime


def now(timezone=None, *args, **kwargs):
    return Datetime.now(timezone=timezone)

def strftime(fmt, _datetime, timezone=None):
    if isinstance(_datetime, Datetime):
        return _datetime.to_string(fmt)
    elif isinstance(_datetime, datetime.datetime):
        dt = Datetime.from_datetime(_datetime, timezone=timezone)
        return dt.to_string(fmt)
    else:
        raise ValueError("Ooops ...")

def strptime(fmt, _date_str, timezone=None):
    return Datetime.from_string(fmt, _date_str, timezone=timezone)


def test_datetime_now():
    b = Datetime.now()
    time.sleep(1)
    e = Datetime.now()
    print( repr(b) )
    print( repr(e) )
    print(e-b)

def test_init_datetime():
    dt0 = datetime.datetime(2016, 11, 13, 0, 0, 0, 0)
    print(dt0)
    
    dt  = Datetime(2016, 11, 13, timezone="Asia/Shanghai")
    dt1 = Datetime(2016, 11, 13, timezone="Asia/Tokyo")
    dt2 = Datetime(2016, 11, 13, 0, 0, 0, 0 timezone="UTC")
    dt3 = Datetime(2016, 11, 13, 0, 0, 0, 0 timezone="US/Hawaii")
    dt4 = Datetime(2016, 11, 13, 0, 0, 0, 0 timezone="America/Los_Angeles")
    print(dt)
    print(dt1)
    print(dt2)
    print(dt3)
    print(dt4)

def test():
    test_init_datetime()
    test_datetime_now()

def main():
    test()

if __name__ == '__main__':
    main()
