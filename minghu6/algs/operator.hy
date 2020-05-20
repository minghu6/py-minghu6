(defn getone [coll key [default None]]
  (try
    (get coll key)
    (except [_ [IndexError KeyError TypeError]]
      default
    )
  )
)


(defn c-not [var]
  (cond [(none? var) 0])
  (cond [(numeric? var)
         (cond [(zero? var) 0]
               [1])]))

(setv builtin-first first)
(defn first [arg]
  "
  (first []) => None
  "
  (builtin-first arg))


(setv builtin-last last)
(defn last [arg]
  "
  (last []) => None
  "
  (try
    (builtin-last arg)
    (except [IndexError] None)
  )
)

(defmain [&rest _]
  (print (getitem [0 [1 2] 3] 1 2 :default 0)))

(defn head [coll] (first coll))
