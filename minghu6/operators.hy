(defn getone [coll key [default None]]
  (try
    (get coll key)
    (except [_ [IndexError KeyError TypeError]]
      default
    )
  )
)

; def getone(coll, key, default=None):
;     try:
;         value = coll[key]
;     except [IndexError, KeyError, TypeError]:
;         return default;
;     else:
;         return value;

(defn none? [a]
    (is a None))

(defn numeric? [a]
      (isinstance a #(int float complex)))

(defn zero? [a]
    (= a 0))

(defn c-not [var]
  (cond 
    (none? var) 
        0
    (numeric? var)
         (if (zero? var) 0 1)))
