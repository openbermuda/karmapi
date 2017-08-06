"""

Python 3.6.0+ (default, Mar  2 2017, 14:39:40) 
[GCC 6.2.0 20161005] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from karmapi import pigfarm
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jng/devel/karmapi/karmapi/pigfarm.py", line 18, in <module>
    from karmapi import hush
  File "/home/jng/devel/karmapi/karmapi/hush.py", line 37, in <module>
    from karmapi import sonogram
  File "/home/jng/devel/karmapi/karmapi/sonogram.py", line 23, in <module>
    class SonoGram(pigfarm.MagicCarpet):
AttributeError: module 'karmapi.pigfarm' has no attribute 'MagicCarpet'
>>> 
>>> 
>>> from karmapi import hush
>>> from karmapi import pigfarm
>>> pigfarm.MagicCarpet
<class 'karmapi.pigfarm.MagicCarpet'>
>>> 

"""
