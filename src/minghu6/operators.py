def get(coll, key, default=None):
     try:
         value = coll[key]
     except (LookupError, TypeError):
         return default
     else:
         return value
