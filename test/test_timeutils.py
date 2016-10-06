from pyutils import localfstr, strflocal

#spec = '9/27/2015 9:45 +60m'
#tm = localfstr(spec)

spec = 'heute vor 1h'
tm = localfstr(spec)

print(spec)
print(strflocal(tm))

